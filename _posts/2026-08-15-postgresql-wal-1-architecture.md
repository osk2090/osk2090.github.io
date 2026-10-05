---
layout: default
title: "PostgreSQL WAL (1) 동작 원리와 세그먼트·레코드 내부 구조"
date: 2026-08-15 11:14:49 +0900
categories: [Database]
slug: postgresql-wal-1-architecture
---

{% raw %}

> 💡 **PostgreSQL WAL(Write Ahead Log) 시리즈**
> - **1편: PostgreSQL WAL (1) 동작 원리와 세그먼트·레코드 내부 구조** (현재 글)
> - **2편: [PostgreSQL WAL (2) LSN 구조와 WAL 추적 함수 분석](/database/2026/09/05/postgresql-wal-2-lsn.html)**
> - **3편: [PostgreSQL WAL (3) 체크포인트 메커니즘과 세그먼트 관리 및 아카이빙](/database/2026/10/03/postgresql-wal-3-checkpoint.html)**

---

## 1. 데이터 무결성과 WAL(Write Ahead Log)

데이터 무결성은 데이터에 대한 **정확성, 일관성, 유효성**을 의미한다.

- **정확성**: 데이터 중복이 발생하거나 누락되지 않은 상태
- **일관성**: 원인과 결과가 연속적으로 보장되어 변하지 않은 상태

데이터베이스 서버에 예기치 못한 장애(서버 다운, 정전 등)가 발생하면 RAM(메모리)에 있던 휘발성 데이터는 모두 손실된다. 데이터의 무결성을 영구히 보장하려면 데이터 변경 사항을 비휘발성 저장 장치인 디스크에 안전하게 저장해야 한다.

PostgreSQL에서는 클라이언트가 요청한 데이터 변경이 먼저 메모리 버퍼(Shared Buffer)에 반영된 후, 디스크 파일에 일괄적으로 기록된다. 하지만 변경된 모든 메모리 페이지가 트랜잭션 종료 시마다 즉시 디스크에 기록되는 것은 아니다(디스크 랜덤 I/O 비용이 매우 크기 때문). 따라서 메모리에만 변경 사항이 남아있는 상태에서 시스템이 다운되면 데이터 일관성이 깨질 위험이 존재한다.

이러한 문제를 해결하고 데이터 무결성을 보장하기 위해 도입된 기법이 바로 **WAL(Write Ahead Log)**이다. 문자의미 그대로 **"데이터 파일에 쓰기 전에 로그에 먼저 기록한다"**는 원칙이다.

---

## 2. WAL 동작 순서

트랜잭션에서 데이터 변경이 일어날 때의 순차적인 흐름을 정리하면 다음과 같다.

1. **데이터 변경 발생**: 클라이언트가 INSERT, UPDATE, DELETE 쿼리 실행
2. **Shared Buffer 변경**: 메모리 영역인 Shared Buffer의 데이터 페이지를 수정 (이 시점의 페이지를 Dirty Page라 함)
3. **WAL Buffer 기록**: 동시에 메모리의 WAL Buffer 영역에 데이터 변경 내용에 대한 로그(**WAL Record**)를 기록
4. **Shared Buffer 변경 완료**: 메모리상 변경 작업 마무리
5. **WAL 디스크 기록 및 flush**: 트랜잭션 커밋 시, WAL Buffer의 WAL Record들을 디스크의 **WAL Segment 파일에 순차(append) 기록하고 fsync(flush)**
6. **데이터 파일 최종 저장**: 실제 테이블 데이터 파일(`base/` 디렉토리)에는 나중에 체크포인트나 백그라운드 라이터를 통해 일괄 반영

WAL 로그는 디스크의 끝부분에 순차적으로 이어 쓰는 **Append-only 방식**으로 기록되므로, 무작위 데이터 블록을 쓰는 랜덤 I/O에 비해 디스크 오버헤드가 매우 적고 빠르다. 

만약 실제 데이터 파일에 변경 사항이 아직 반영되지 못한 상태에서 장애가 발생하더라도, 디스크에 안전하게 플러시된 WAL 세그먼트 파일을 읽어 순차적으로 재실행(Redo)하면 데이터를 최신 상태로 완벽하게 복구할 수 있다.

---

## 3. [실습] 트랜잭션에 따른 WAL 동작 확인

이해를 돕기 위해 테스트 테이블을 생성하고 트랜잭션 전후의 WAL 위치 변화를 직접 확인해 보자.

### 1) 테스트 테이블 생성 및 데이터 주입

```sql
CREATE TABLE wal_test (
    id int PRIMARY KEY,
    name text
);

INSERT INTO wal_test VALUES (1, 'before');
```

### 2) 현재 WAL 위치 확인

```sql
SELECT
    pg_current_wal_insert_lsn() AS wal_insert,
    pg_current_wal_flush_lsn() AS wal_flush;
```

**실행 결과:**

![](/images/postgresql-wal-mechanism/img_1.png)

### 3) 트랜잭션 시작 및 데이터 수정 (커밋 전)

```sql
BEGIN;

UPDATE wal_test
SET name = 'after'
WHERE id = 1;
```

### 4) 커밋하지 않은 상태에서 WAL 위치 확인

```sql
SELECT
    pg_current_wal_insert_lsn() AS wal_insert,
    pg_current_wal_flush_lsn() AS wal_flush;
```

**실행 결과:**

![](/images/postgresql-wal-mechanism/img_2.png)

첫 번째 조회 결과와 비교했을 때, 아직 `COMMIT`을 하지 않았음에도 불구하고 `UPDATE` 쿼리가 실행되면서 WAL 버퍼/세그먼트에 레코드가 생성되어 WAL 위치(LSN)가 증가했음을 확인할 수 있다.

### 5) 커밋 수행

```sql
COMMIT;
```

### 6) 커밋 후 WAL 위치 확인

```sql
SELECT
    pg_current_wal_insert_lsn() AS wal_insert,
    pg_current_wal_flush_lsn() AS wal_flush;
```

커밋 시점에 WAL 레코드가 디스크로 확실히 flush되며, 장애 복구의 기준이 된다.

---

## 4. pg_wal 디렉토리와 세그먼트 파일 명명 규칙

PostgreSQL의 데이터 디렉토리 내 `pg_wal` 폴더를 확인하면 여러 개의 WAL 세그먼트 파일들이 존재한다. 이 파일들은 다음과 같은 24자리 16진수 파일명 형식을 갖는다.

```
00000001 00000000 0000000B
──────── ──────── ────────
Timeline Log ID   Segment ID
```

### 1) 앞자리 8자리: 타임라인 ID (Timeline ID)
- 예시의 `00000001`은 타임라인 ID를 의미한다.
- 데이터베이스의 복구 분기(PITR, Point-In-Time-Recovery)나 복제 전환(Failover) 시 시점을 식별하기 위한 부호 없는 4바이트 정수다.

### 2) 중간 8자리: 논리적 로그 ID (Log ID)
- 예시의 `00000000`은 **Log ID**로, WAL 내부의 큰 논리적 구간을 구분하기 위한 값이다.
- 수많은 WAL 세그먼트가 연속해서 생성되므로, 큰 묶음 단위로 구간을 나누는 식별자 역할을 한다.

```
[ Log ID 0 ] <----- 중간 8자리
  ├─ Segment 0
  ├─ Segment 1
  ├─ ...
  └─ Segment FF
[ Log ID 1 ]
  ├─ Segment 0
  ├─ Segment 1
  └─ ...
```

### 3) 마지막 8자리: 세그먼트 ID (Segment ID)
- 예시의 `0000000B`는 현재 Log ID 내에서의 물리적인 세그먼트 번호다.

### 세그먼트 파일명 회전 규칙
- 16진수 한 자리는 `0 ~ F`까지 사용된다.
- `F` 다음은 `10`으로 증가한다 (`0F` → `10`, `1F` → `20`).
- `FF`는 16진수로 255를 뜻한다.
- PostgreSQL 기본 WAL 세그먼트 크기가 16MB일 때, Segment ID는 일반적으로 `00000000`부터 `000000FF`(총 256개, 약 4GB)까지 사용된다.
- `FF` 세그먼트까지 모두 사용되면 Log ID가 1 증가하고, Segment ID는 다시 `00000000`부터 시작한다.

```
...00000000000000FE
...00000000000000FF
...0000000100000000  <-- Log ID가 1 증가하고 Segment ID가 00으로 리셋
```

현재 데이터베이스에서 사용 중인 WAL 세그먼트 목록은 아래 쿼리로 확인할 수 있다.

```sql
SELECT * FROM pg_ls_waldir() ORDER BY modification DESC LIMIT 5;
```

---

## 5. WAL 세그먼트 내부 계층 구조

WAL 세그먼트 파일 내부는 **세그먼트(Segment) → 페이지(Page) → 레코드(Record)**의 계층 구조로 체계화되어 있다.

```
WAL 세그먼트 파일 (기본 16MB)
 ├─ Page (기본 8KB)
 │   ├─ WAL Record
 │   ├─ WAL Record
 │   └─ WAL Record
 ├─ Page (기본 8KB)
 │   ├─ WAL Record
 │   └─ WAL Record
 └─ ...
```

### 1) WAL Record의 구조

각각의 WAL Record는 변경 작업의 메타데이터와 실제 데이터로 나뉜다.

```
WAL Record
 ├─ Header
 │   ├─ LSN
 │   ├─ 레코드 크기
 │   ├─ 트랜잭션 ID
 │   └─ 기타 메타정보
 │
 └─ Data
     ├─ 실제 변경 내용
     ├─ 어떤 테이블/페이지를 변경했는지
     └─ 어떤 작업(INSERT/UPDATE/DELETE 등)을 했는지
```

예를 들어 다음과 같은 SQL이 실행되었다고 가정해 보자.

```sql
UPDATE account
SET name = 'kim'
WHERE id = 1;
```

PostgreSQL은 이 작업에 대해 대략 다음과 같은 정보가 담긴 WAL Record를 생성한다.

```
Header
 ├─ LSN: 이 WAL 레코드의 위치 (예: LSN 100)
 ├─ Transaction ID: 트랜잭션 식별자
 └─ 크기 등의 메타 정보

Data
 ├─ account 테이블의 특정 페이지 번호
 ├─ 페이지 내 특정 레코드(튜플) 오프셋
 └─ name 값이 'kim'으로 변경됨
```

---

## 6. WAL 페이지 및 레코드 구성 요소 상세

### 1) WAL 페이지 구성 요소 (Page Header & Body)

- **Page Header**: 각 8KB WAL 페이지의 메타데이터를 저장한다.
- **Magic Number**: WAL 파일 형식을 식별하는 매직 넘버.
- **Page Size 및 Version**: 페이지의 크기 및 PostgreSQL 버전 정보.
- **Log Sequence Number(LSN)**: 이 페이지의 시작 위치를 나타내는 LSN.
- **Page Number**: 세그먼트 파일 내에서 몇 번째 페이지인지 나타냄.
- **Previous Page Pointer**: 이전 페이지의 번호를 가리키는 포인터.
- **Timeline ID**: 페이지가 속한 타임라인.
- **CRC32 Checksum**: 페이지 데이터의 무결성을 검증하기 위한 체크섬.
- **XLog Record**: 실제 트랜잭션 변경 로그 레코드들이 기록되는 공간.
- **Page Trailer**: 페이지의 마지막 부분 정보.

### 2) WAL 레코드 구성 요소 (Record Header & Data)

- **Record Header**: 각 트랜잭션 레코드의 메타데이터를 저장한다.
- **XLogRecPtr**: 레코드의 시작 위치를 가리키는 고유 LSN.
- **XLog Record Type**: 레코드 유형(INSERT, UPDATE, DELETE, COMMIT, CHECKPOINT 등).
- **XLog Record Length**: 레코드의 전체 길이(레코드 경계 식별용).
- **Checkpoint Information**: 레코드의 복구 시점 관련 정보.
- **Previous LSN**: 바로 직전 레코드의 시작 위치 LSN (역방향 탐색용 체이닝).
- **Record Version**: 레코드 구조의 버전 정보.
- **XLog Data**: 실제 변경된 트랜잭션 페이로드 데이터.
- **CRC Checksum**: 레코드 훼손 여부를 감지하는 체크섬 정보.

---

> ➡️ **다음 편 예고:**
> WAL 레코드마다 붙는 **LSN(Log Sequence Number)**의 64비트 주소 체계와 구조, 그리고 PostgreSQL의 다양한 WAL 추적 내장 함수 실습은 **[2편: PostgreSQL WAL (2) LSN 구조와 WAL 추적 함수 분석](/database/2026/09/05/postgresql-wal-2-lsn.html)**에서 자세히 다룹니다.

{% endraw %}
