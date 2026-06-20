---
layout: default
title: "Postgresql에서 Transaction ID 를 통해 데이터 롤백과정 정리"
date: 2024-11-23 16:13:58 +0900
categories: [Database]
slug: post-144-postgresql에서-transaction-id-를-통해-데이터-롤백과정-정리
render_with_liquid: false
---

1. 예시의 데이터로 tmin=1, value="one"데이터가 트랜잭션으로 수정이 발생하면
2. 물리적으로 새 로우가 생성되고 tmin=2, tmax=null, value="two" 상태로 생성
3. 변경전의 로우에는 tmax=2로 변경이 된다.(현재 value="one"인 데이터의 tmin=1, tmax=2)
4. 이때 만약 select 쿼리가 오면 해당 시점의 데이터는 아직 반영이 안되어서 value="one"을 리턴하게 된다.
   1. 여기서 커밋이 되면 two가 반영이 되고 vaccum이 동작하면 tmax에 값이 있는 로우를 dead tuple로 판단하여 물리적 삭제
   2. 여기서 롤백이 되면 물리적으로 새로 생성된 로우는 삭제되고 이전데이터의 tmax=null 처리되어 유효한 데이터로 판단

- 동작 시각화(생성: GPT)

```bash
-- 1. 테이블 생성
CREATE TABLE test_table (
    id SERIAL PRIMARY KEY,
    value TEXT
);

-- 2. 초기 데이터 삽입
INSERT INTO test_table (value) VALUES ('one');

-- 데이터 상태 확인 (트랜잭션 전)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과:
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 | NULL | one

-- 3. 트랜잭션 시작 및 데이터 수정
BEGIN;
UPDATE test_table SET value = 'two' WHERE id = 1;

-- 데이터 상태 확인 (트랜잭션 중)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과:
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 |    2 | one     -- 기존 행 무효화(tmax 설정됨)
-- (0, 2)  |    2 | NULL | two     -- 새 행 삽입(tmin 설정됨)

-- Commit
COMMIT;

-- 데이터 상태 확인 (Commit 후)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과:
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 |    2 | one     -- 기존 행 (Dead Tuple)
-- (0, 2)  |    2 | NULL | two     -- 새 행 (유효 데이터)

-- 4. 트랜잭션 시작 및 데이터 수정
BEGIN;
UPDATE test_table SET value = 'three' WHERE id = 1;

-- 데이터 상태 확인 (트랜잭션 중)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과:
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 |    3 | one     -- 기존 행 무효화(tmax 설정됨)
-- (0, 3)  |    3 | NULL | three   -- 새 행 삽입(tmin 설정됨)

-- Rollback
ROLLBACK;

-- 데이터 상태 확인 (Rollback 후)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과:
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 | NULL | one     -- 기존 행 복구(tmax 값 제거)
-- (0, 3)  |    3 | NULL | three   -- 새 행 (Dead Tuple)

-- 5. Rollback 또는 Commit 후 Dead Tuple 정리
VACUUM test_table;

-- 데이터 상태 확인 (VACUUM 후)
SELECT ctid, xmin, xmax, value FROM test_table;

-- 예상 결과 (Dead Tuple 제거):
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 1)  |    1 | NULL | one     -- Rollback 후 복구된 데이터
-- 또는
-- ctid    | xmin | xmax | value
-- --------|------|------|-------
-- (0, 2)  |    2 | NULL | two     -- Commit 후 유효 데이터만 남음

-- 6. 트랜잭션 상태에 따른 SELECT 동작 확인
BEGIN;
UPDATE test_table SET value = 'four' WHERE id = 1;

-- 데이터 상태 확인 (트랜잭션 중)
SELECT value FROM test_table;

-- 예상 결과:
-- "one" (트랜잭션이 완료되지 않아 변경 전 데이터 반환)

-- Commit 후 데이터 확인
COMMIT;
SELECT value FROM test_table;

-- 예상 결과:
-- "four" (트랜잭션 완료 후 변경 데이터 반환)
```