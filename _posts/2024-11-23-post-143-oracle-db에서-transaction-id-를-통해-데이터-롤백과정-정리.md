---
layout: default
title: "Oracle DB에서 Transaction ID 를 통해 데이터 롤백과정 정리"
date: 2024-11-23 15:40:01 +0900
categories: [Database]
slug: post-143-oracle-db에서-transaction-id-를-통해-데이터-롤백과정-정리
---
{% raw %}

1. 트랜잭션이 시작되면서 데이터 변경이 발생, 변경이 발생한 데이터의 로우의 헤더
영역에 ITL(interested trasaction list) 에 해당 트랜잭션 id와 UBA(undo block address) 에는 undo block에 대한 주소값을 저장
2. undo block에는 old version(이전 데이터)를 저장
3. 만약 이 시점에 select 쿼리가 날라오면 consistent read(일관성 읽기)로 인해 old version의 데이터를 CR 캐시에 저장되고 해당 데이터를 리턴(트랜잭션이 끝나더라도 CR 캐시는 데이터가 변경되더라도 일정시간 저장)
   1. 만약 커밋이 되면 데이터 변경 완료
   2. 만약 롤백이 되면 해당 데이터 로우에 저장된 ITL영역의 UBA를 이용해서 old version 데이터를 가져와서 원복시킨다.

- 동작 시각화(생성: GPT)

```bash
+-----------------------------------------+
| 데이터 블록 (User Data Block)            |
|-----------------------------------------|
| Header Area                             |
|   - ITL (Interested Transaction List):  |
|      TXID = 123                         |
|      UBA  = File 1, Block 10, Slot 3    |
|-----------------------------------------|
| Row Data                                |
|   - 변경된 데이터: Value = "Updated"    |
+-----------------------------------------+

            ↓ (UBA를 통해 Undo 블록 참조)

+-----------------------------------------+
| Undo 블록 (Undo Tablespace)             |
|-----------------------------------------|
| File 1, Block 10, Slot 3                |
|   - Old Version: Value = "Original"     |
|   - TXID = 123                          |
|-----------------------------------------+
```
{% endraw %}