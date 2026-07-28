---
layout: default
title: "Oracle DB의 ITL, UBA 및 Undo Segment를 활용한 데이터 롤백(Rollback)과 읽기 일관성(Consistent Read) 메커니즘"
date: 2024-11-23 15:40:01 +0900
categories: [Database]
slug: oracle-itl-uba-undo-rollback-mechanism
---
{% raw %}

Oracle Database는 멀티버전 동시성 제어(MVCC) 및 트랜잭션 롤백(Rollback)을 실현하기 위해 데이터 블록 헤더 내 **ITL(Interested Transaction List)**과 **Undo Segment** 구조를 정교하게 활용합니다.

이 포스팅에서는 트랜잭션 수행 시 Oracle 데이터 블록 헤더에 기록되는 메타데이터와 **UBA(Undo Block Address)**를 통해 데이터 복구 및 Consistent Read(읽기 일관성)가 어떤 메커니즘으로 동작하는지 상세 분석해보겠습니다.

---

## 1. Oracle 데이터 블록과 ITL(Interested Transaction List)

Oracle의 데이터 블록(Data Block) 헤더에는 블록 내 튜플 변경 권한을 다투는 트랜잭션 슬롯 배열인 **ITL(Interested Transaction List)** 영역이 존재합니다 (`INITRANS` 매개변수로 초기 슬롯 개수 설정).

```
+-------------------------------------------------------+
| Data Block Header                                     |
|   - ITL Slot 1: Transaction ID (XID), UBA, Flag, Lock |
|   - ITL Slot 2: Transaction ID (XID), UBA, Flag, Lock |
+-------------------------------------------------------+
| Row Directory & Row Data                              |
|   - Row 1 (Header: ITL Slot 1을 가리키는 Lock Byte)    |
|   - Row 2                                             |
+-------------------------------------------------------+
```

1. **트랜잭션 시작 및 ITL 슬롯 확보**:
   DML(UPDATE/DELETE)이 실행되면 트랜잭션은 타겟 데이터 블록 헤더의 비어있는 ITL 슬롯 하나를 점유하고, 자신의 **Transaction ID (XID)**와 **Undo Block Address (UBA)** 정보를 기록합니다.
2. **Row Level Lock**:
   수정 대상 행의 헤더(Row Header) 내 Lock Byte에 해당 ITL 슬롯 번호를 기록하여 Row-Level Lock을 표시합니다.

---

## 2. Undo Segment와 UBA (Undo Block Address)

**UBA(Undo Block Address)**는 언두 테이블스페이스 내에 저장된 변경 전 이전 데이터(Old Version / Before Image)의 정확한 물리적 위치(File, Block, Slot 번호)를 가리키는 포인터입니다.

```
+-----------------------------------------+
| 데이터 블록 (User Data Block Header)       |
|-----------------------------------------|
| ITL Slot 1:                             |
|   - TXID = 10023                        |
|   - UBA  = Undo File 2, Block 405, Slot 2 |
|-----------------------------------------|
| Row Data                                |
|   - Value = "Updated Data" (New Version) |
+-----------------------------------------+
                    │
                    ▼ (UBA 포인터 참조)
+-----------------------------------------+
| Undo 블록 (Undo Tablespace)             |
|-----------------------------------------|
| File 2, Block 405, Slot 2               |
|   - Before Image: Value = "Original"    |
|   - TXID = 10023                        |
+-----------------------------------------+
```

---

## 3. ROLLBACK(롤백) 및 읽기 일관성(Consistent Read) 동작 흐름

### 1) ROLLBACK 실행 과정
1. 세션에서 `ROLLBACK`을 요청하면 Oracle은 데이터 블록 ITL 슬롯의 **UBA 포인터**를 추적합니다.
2. **Undo Segment**에 저장된 이전 버전 데이터(Before Image)를 읽어와 데이터 블록의 로우 값을 원본("Original") 상태로 되돌립니다.
3. 해당 ITL 슬롯의 트랜잭션 상태를 해제하고 커밋 SCN을 정리합니다.

### 2) SELECT 질의와 CR(Consistent Read) 캐시 복제본 생성
- 다른 세션에서 데이터를 조회할 때 해당 데이터 블록의 ITL 슬롯이 커밋되지 않은 상태(`Active`)라면, Oracle은 **락(Lock) 대기를 하지 않고** 즉시 메모리(Buffer Cache) 상에 **CR(Consistent Read) 복제 블록**을 하나 만듭니다.
- CR 복제 블록에 UBA의 Undo 데이터를 덮어씌워 쿼리 시작 시점의 SCN 기준 "과거 버전 데이터"를 손쉽게 재구성하여 리턴합니다.
- 이 메커니즘 덕분에 Oracle에서는 **"읽는 작업은 쓰는 작업을 막지 않고, 쓰는 작업은 읽는 작업을 막지 않는다"**는 완벽한 동시성이 보장됩니다.

---

## 💡 요약

- Oracle은 데이터 블록 헤더의 **ITL**에 **UBA(Undo Block Address)**를 저장하여 Undo 테이블스페이스의 이전 버전 데이터(Before Image) 위치를 관리합니다.
- **ROLLBACK** 시 UBA를 역추적하여 원본을 복원하며, **SELECT** 시 락 대기 없이 CR 복제본을 생성하여 뛰어난 읽기 일관성을 제공합니다.
{% endraw %}