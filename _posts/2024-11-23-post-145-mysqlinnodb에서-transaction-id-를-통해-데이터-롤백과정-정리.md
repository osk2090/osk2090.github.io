---
layout: default
title: "Mysql(InnoDB)에서 Transaction ID 를 통해 데이터 롤백과정 정리"
date: 2024-11-23 16:40:34 +0900
categories: [Database]
slug: post-145-mysqlinnodb에서-transaction-id-를-통해-데이터-롤백과정-정리
render_with_liquid: false
---

1. 트랜잭션과 함께 데이터 변경이 발생하면 해당 데이터 로우의 trx\_id는 최신 트랜잭션 id를 저장
2. 롤백 세그먼트 영역이 별도로 존재하는데 거기에는 undo 세그먼트가 그 하위에 undo 로그로 변경 전의 데이터를 저장
3. roll\_ptr은 해당 데이터 로우에 존재하며 해당 영역에는 undo 로그의 위치를 저장
4. 아직 커밋이 안된상태에서 select 쿼리가 오면 roll\_ptr를 통해 undo 로그에 저장된 변경전의 데이터를 반환
   1. 커밋이 되면 해당 undo 로그는 필요하지 않으므로 가비지 콜랙터에 들어가게되어 삭제
   2. 롤백이 되면 해당 데이터 로우의 roll\_ptr의 undo 로그에 있는 변경전 데이터를 다시 입력하여 데이터 원복

- 동작 시각화(생성: GPT)

```bash
CREATE TABLE test_table (
    id INT PRIMARY KEY,
    value VARCHAR(50)
);

INSERT INTO test_table (id, value) VALUES (1, 'one');

-- 트랜잭션 1: 데이터 변경
START TRANSACTION;
UPDATE test_table SET value = 'two' WHERE id = 1;

-- 데이터 상태 확인 (트랜잭션 중)
SELECT id, value, trx_id, roll_ptr FROM information_schema.innodb_trx;

-- 결과 (예제):
-- id   | value | trx_id | roll_ptr
-- -----|-------|--------|----------
-- 1    | two   | 1001   | 0x12345678 (Undo 로그 위치)

-- 트랜잭션 롤백
ROLLBACK;

-- 데이터 상태 확인
SELECT * FROM test_table;

-- 결과:
-- id   | value
-- -----|-------
-- 1    | one   -- 변경 전 상태로 복원

-- 트랜잭션 Commit
COMMIT;

-- Undo 로그는 일정 시간이 지나면 정리됨
```