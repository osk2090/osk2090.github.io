---
layout: default
title: "PostgreSQL WAL (2) LSN 구조와 WAL 추적 함수 분석"
date: 2026-09-05 12:00:00 +0900
categories: [Database]
slug: postgresql-wal-2-lsn
---

{% raw %}

> 💡 **PostgreSQL WAL(Write Ahead Log) 시리즈**
> - **1편: [PostgreSQL WAL (1) 동작 원리와 세그먼트·레코드 내부 구조](/database/2026/08/15/postgresql-wal-1-architecture.html)**
> - **2편: PostgreSQL WAL (2) LSN 구조와 WAL 추적 함수 분석** (현재 글)
> - **3편: [PostgreSQL WAL (3) 체크포인트 메커니즘과 세그먼트 관리 및 아카이빙](/database/2026/10/03/postgresql-wal-3-checkpoint.html)**

---

## 1. LSN(Log Sequence Number)이란?

**LSN(Log Sequence Number)**은 WAL 세그먼트 파일에 기록된 각 트랜잭션 레코드의 고유한 위치(바이트 단위 오프셋)를 식별하기 위한 64비트 정수 주소다. 

데이터베이스가 장애 후 복구 작업을 수행하거나, 복제 서버(Replica)가 원본 서버(Primary)의 변경 사항을 어디까지 따라잡았는지 추적할 때 모두 이 LSN을 기준으로 비교한다.

```
WAL 스트림
───────────────────────────────────────────>
 레코드 A         레코드 B         레코드 C
 LSN 100          LSN 200          LSN 300
```

---

## 2. LSN의 64비트 내부 구조 분석

PostgreSQL에서 LSN을 조회해 보면 보통 `0/16B3748`과 같이 슬래시(`/`)로 구분된 16진수 형태로 출력된다. 

![image-20260905120234748](/images/postgresql-wal-mechanism/img_3.png)

LSN은 전체 64비트(unsigned 8-byte integer)로 구성되어 있는데, 사람이 직관적으로 읽기 어렵기 때문에 상위 32비트와 하위 32비트를 반으로 잘라 슬래시로 표기한다. 

(예를 들어 초 단위의 `3,725초`라는 값을 사람이 보기 편하게 `1시간 2분 5초(1:02:05)` 형태로 나누어 표시하는 것과 같은 원리다.)

LSN의 구조를 자세히 분석하면 다음과 같다.

```
AAAAAAAA / BB CCCCCC
└──┬───┘   ┬  └──┬──┘
 로그 ID   │   세그먼트 파일 안에서의 바이트 오프셋
           │   (6자리 16진수 = 최대 16MB)
           │
      세그먼트 번호
      (2자리 16진수 = 0~255, 즉 256개)
```

- **상위 32비트 (`AAAAAAAA`)**: **Log ID**를 의미한다. 논리적 구간의 고유 식별자이자 순서를 유지하기 위한 값이다.
- **하위 32비트 (`BBCCCCCC`)**: 해당 Log ID 내부에서의 위치를 나타낸다.
  - **앞 2자리 (`BB`)**: 세그먼트 번호. 이 로그 파일 구간에서 몇 번째 세그먼트(0~255)인지를 나타낸다.
  - **뒤 6자리 (`CCCCCC`)**: 해당 16MB 세그먼트 파일 안에서 몇 바이트째(오프셋) 위치인지를 나타낸다. (16진수 6자리는 최대 `FFFFFF` = 16,777,215 바이트 ≈ 16MB)

---

## 3. 도서관 비유로 쉽게 이해하기

LSN 주소 체계가 직관적으로 와닿지 않는다면, 도서관 서가 체계에 비유해 볼 수 있다.

만약 LSN 값이 `0/C0000B70`이라면:

- `0 /` : **도서관 0층**(Log ID 0)으로 이동한다.
- `0C` : 서가에서 **12번째 책**(세그먼트 번호 0C, 파일명 `...0000000C`)을 꺼낸다.
- `000B70` : 책을 펼쳐 처음부터 읽으면서 **2,928번째 글자 위치**(오프셋 `000B70`을 10진수로 변환하면 2928)를 찾는다.

> **"도서관 0층(Log ID 0)에 있는 12번 책(세그먼트 0C)의 2928번째 글자(오프셋 B70)"**

---

## 4. [실습] LSN 기반 실제 WAL 세그먼트 파일 추적

실제 데이터베이스에서 LSN 주소가 가리키는 WAL 세그먼트 파일을 추적해 보자.

![image-20260912114056564](/images/postgresql-wal-mechanism/img_4.png)

위 실습 결과에서:
1. 최신 LSN을 기준으로 함수를 실행하면, 해당 LSN이 저장된 세그먼트 파일명(`pg_walfile_name`)과 파일 내 오프셋(`pg_walfile_name_offset`)을 추출할 수 있다.
2. 실제로 `$PGDATA/pg_wal` 디렉토리를 확인해 보면 쿼리 결과에 출력된 파일명이 그대로 디렉토리에 존재함을 확인할 수 있다.

---

## 5. 핵심 WAL 모니터링 & 조작 함수

### 1) pg_current_wal_lsn() vs pg_current_wal_insert_lsn()

```sql
SELECT 
    pg_current_wal_lsn(),
    pg_current_wal_insert_lsn();
```

- **`pg_current_wal_lsn()`**: 디스크(WAL 세그먼트 파일)에 완전히 기록된 마지막 LSN 위치.
- **`pg_current_wal_insert_lsn()`**: 아직 디스크에 flush되지 않았더라도 메모리(WAL 버퍼)에 삽입된 최신 논리적 LSN 위치.

![image-20260925141200512](/images/postgresql-wal-mechanism/img_5.png)

동시 쓰기 작업이 없는 한가한 상태에서는 WAL 파일에 기록된 LSN과 버퍼에 입력된 LSN이 동일하게 나타난다.

출력된 LSN이 `0/C0000B70`일 때:
- Log ID: `0`
- WAL 세그먼트 파일 번호: `0C`
- LSN 바이트 오프셋: `000B70`

### 2) pg_walfile_name() & pg_walfile_name_offset()

```sql
SELECT 
    pg_walfile_name(pg_current_wal_lsn()),
    pg_walfile_name_offset(pg_current_wal_lsn());
```

![image-20260925144422836](/images/postgresql-wal-mechanism/img_6.png)

조회 결과, 현재 LSN이 속한 실제 WAL 파일명은 `00000001000000000000000C`이며, 파일 내 오프셋은 `2928` 바이트로 분해되어 반환된다.

> **타임라인 1(00000001)의 Log ID 0(00000000), 12번째 세그먼트(0000000C) 파일의 2,928번째 바이트**

### 3) pg_switch_wal()

```sql
SELECT pg_switch_wal();
```

현재 작성 중인 WAL 세그먼트 파일을 즉시 종료하고 다음 번호의 새로운 WAL 세그먼트 파일로 강제 전환한다.

- 주로 베이스 백업을 수행하기 직전/직후나, 복구 시점을 명확하게 구분하고 싶을 때 수동으로 세그먼트를 닫고 새 파일을 열기 위해 사용된다.

### 4) pg_wal_lsn_diff() 와 복제(Replication) 모니터링

`pg_wal_lsn_diff(lsn1, lsn2)`는 두 LSN 간의 바이트(Byte) 차이를 계산해 주는 함수다.

```sql
SELECT pg_wal_lsn_diff('0/C0001000', '0/C0000B70');
```

복제 환경에서는 원본 서버의 현재 LSN(`pg_current_wal_lsn()`)과 복제 서버가 재생(Replay)한 LSN(`pg_last_wal_replay_lsn()`) 사이의 차이를 구하여 **복제 지연(Replication Lag)** 바이트 수를 측정할 때 필수적으로 쓰인다.

#### 주의: Primary 서버에서의 동작
Primary(원본) 서버에서 복제 모니터링 함수인 `pg_last_wal_replay_lsn()`을 호출하면 `NULL`이 반환된다.

현재 서버가 복구/복제 상태인지 확인하려면 다음 함수를 사용할 수 있다.

```sql
SELECT pg_is_in_recovery();
```

- 결과가 `false`: 현재 서버가 원본 서버(Primary)라는 의미이다.
- 결과가 `true`: 현재 서버가 대기 서버(Standby / Replica)이며 WAL을 재생 중이라는 의미이다.

Primary 서버는 WAL을 직접 생성하는 주체이므로 '재생'하지 않아 `pg_last_wal_replay_lsn()`이 `NULL`이 되는 것이다.

직접 두 LSN 값을 대입해 차이를 계산해 보면:

![image-20260925172304821](/images/postgresql-wal-mechanism/img_7.png)

첫 번째 인자(나중에 생성된 LSN)에서 두 번째 인자(이전에 생성된 LSN)를 차감한 바이트 크기가 양수로 정상 계산됨을 확인할 수 있다.

---

> ➡️ **다음 편 예고:**
> 이렇게 쌓인 WAL 세그먼트는 영원히 쌓아둘 수 없습니다. 메모리의 변경 사항을 디스크에 동기화하고 WAL을 정리하는 핵심 메커니즘인 **체크포인트(Checkpoint)**와 세그먼트 파일 수명주기, 아카이빙은 **[3편: PostgreSQL WAL (3) 체크포인트 메커니즘과 세그먼트 관리 및 아카이빙](/database/2026/10/03/postgresql-wal-3-checkpoint.html)**에서 살펴봅니다.

{% endraw %}
