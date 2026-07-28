---
layout: default
title: "PostgreSQL 힙 페이지 내부 구조와 라인 포인터(Line Pointer)의 역할 분석"
date: 2024-12-18 13:54:51 +0900
categories: [Database]
slug: postgresql-line-pointer-heap-page-architecture
image: /images/147/img.png
---
{% raw %}

![](/images/147/img.png)

PostgreSQL은 데이터를 8KB 크기의 **힙 페이지(Heap Page 또는 Block)** 단위로 관리합니다. 디스크 I/O와 메모리(Shared Buffers) 적재의 최소 단위인 이 페이지 내부에서 각 행(Tuple) 데이터는 무작위로 위치하는 것이 아니라, **페이지 헤더와 라인 포인터(Line Pointer)**라는 가상 간접 주소 체계를 통해 정밀하게 관리됩니다.

이번 포스팅에서는 PostgreSQL 힙 페이지의 내부 아키텍처와 라인 포인터(Line Pointer)의 핵심 역할, 그리고 MVCC 및 HOT(Heap Only Tuple) 최적화와의 관계를 깊이 있게 알아보겠습니다.

---

## 1. PostgreSQL 힙 페이지 구조

PostgreSQL의 8KB 페이지는 다음과 같이 위(Header)와 아래(Special/Tuple) 양방향에서 가운데로 데이터가 채워지는 역방향 성장 구조를 가집니다.

```
+-------------------------------------------------------+
| PageHeaderData (24 bytes)                             |  <-- 페이지 헤더
+-------------------------------------------------------+
| Line Pointer 1 (itemIdData, 4 bytes)                  |  <-- pd_lower 방향으로
| Line Pointer 2 (itemIdData, 4 bytes)                  |      아래로 증가
| Line Pointer 3 (itemIdData, 4 bytes)                  |
| ...                                                   |
+-------------------------------------------------------+
|                  <--- Free Space --->                 |  <-- 여유 공간 (pd_lower ~ pd_upper)
+-------------------------------------------------------+
| ...                                                   |
| HeapTupleHeader & Data (Tuple 3)                      |  <-- pd_upper 방향으로
| HeapTupleHeader & Data (Tuple 2)                      |      위로 쌓임
| HeapTupleHeader & Data (Tuple 1)                      |
+-------------------------------------------------------+
| Special Space (Index 전용 영역 등)                      |
+-------------------------------------------------------+
```

- **PageHeaderData (24 bytes)**: 페이지 전체 메타데이터 (LSN, pd_lower, pd_upper, pd_special 등)
- **Line Pointer Array (itemIdData)**: 4바이트 크기의 배열. 페이지 상단에서 아래로(`pd_lower` 방향) 추가됩니다.
- **Heap Tuples**: 실제 튜플 데이터(Header + User Data). 페이지 최하단에서 위로(`pd_upper` 방향) 적재됩니다.
- **Free Space**: `pd_lower`와 `pd_upper` 사이의 미사용 빈 공간입니다.

---

## 2. 라인 포인터(Line Pointer, ItemIdData)란?

라인 포인터는 페이지 상단의 4바이트짜리 포인터 항목으로, **해당 페이지 내에서 튜플의 실제 바이트 오프셋(Offset)과 상태**를 기록하는 일종의 "페이지 내부 인덱스" 역할을 수행합니다.

### ItemIdData의 4바이트 비트 구조
1. **lp_off (15 bits)**: 페이지 시작점으로부터 튜플 시작 지점까지의 바이트 오프셋
2. **lp_flags (2 bits)**: 라인 포인터의 상태
   - `00 (LP_UNUSED)`: 사용되지 않는 빈 라인 포인터
   - `01 (LP_USED)`: 튜플 데이터를 유효하게 가리키고 있음
   - `10 (LP_REDIRECT)`: HOT(Heap-Only Tuple) 체인에 의해 다른 라인 포인터로 리다이렉트됨
   - `11 (LP_DEAD)`: 튜플은 수거되었으나 라인 포인터 배열 자리는 보존 중
3. **lp_len (15 bits)**: 해당 튜플의 바이트 길이

---

## 3. 라인 포인터가 필요한 이유: 간접 주소 지정 방식 (Indirection)

PostgreSQL의 ROW ID 역할을 하는 **ctid**는 `(BlockNumber, Offnum)` 형태입니다. 여기서 `Offnum`은 튜플의 실제 디스크 바이트 오프셋이 아닌 **"라인 포인터의 번호(1-indexed)"**를 의미합니다.

### 왜 직접 바이트 오프셋 대신 라인 포인터를 거칠까?

1. **인덱스 수정 없는 튜플 이동 (Page Defragmentation & Compaction)**:
   페이지 내에서 데드 튜플(Dead Tuple)이 VACUUM되어 정리되면 튜플 위치를 당겨서 여유 공간(Free Space)을 병합합니다. 이때 라인 포인터의 `lp_off` 오프셋 값만 수정하면 되므로, **테이블 인덱스(B-Tree)가 갖고 있는 ctid 주소를 수정할 필요가 없습니다.**

2. **HOT (Heap Only Tuple) 최적화**:
   UPDATE로 인해 동일 페이지 내에 새로운 버전의 튜플이 생성되었을 때, 인덱스를 새로 추가하지 않고 기존 라인 포인터를 `LP_REDIRECT`로 지정하여 새 라인 포인터를 가리키게 함으로써 **인덱스 팽창(Index Bloat)을 방지**합니다.

---

## 4. DELETE 및 VACUUM 시 라인 포인터의 변화 Lifecycle

1. **DELETE 실행 시**: 튜플 데이터에 DELETE 트랜잭션 XMAX가 기록되며, 라인 포인터는 여전히 `LP_USED` 상태를 유지합니다 (MVCC 가시성 보장).
2. **VACUUM 실행 시**: 어떤 트랜잭션도 참조할 수 없는 Dead 상태가 되면 튜플 데이터 공간이 `Free Space`로 환원되고 라인 포인터는 `LP_DEAD` 또는 `LP_UNUSED`로 변경됩니다.
3. **재사용**: 신규 INSERT 발생 시 기존 `LP_UNUSED` 라인 포인터 번호를 우선 재사용합니다.

---

## 💡 요약

- 라인 포인터는 **8KB 힙 페이지 상단에 위치한 4바이트 오프셋 포인터**로, 튜플의 물리적 위치 변경으로부터 외부 인덱스와 ctid 주소를 보호하는 **간접 주소(Indirection Layer)** 역할을 담당합니다.
- 이를 통해 PostgreSQL은 인덱스 재작성 없이 페이지 공간 압축(Compaction)과 HOT 최적화를 효율적으로 실행할 수 있습니다.
{% endraw %}