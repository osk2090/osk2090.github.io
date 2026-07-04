---
layout: default
title: "PostgreSQL 대해"
date: 2026-02-17 16:56:11 +0900
categories: [Database]
slug: post-152-postgresql-대해
---
{% raw %}

1. PostgreSQL은 시스템 메모리가 1GB 이상일 경우 전체 메모리의 약 25%를 shared\_buffers로 설정하는 것이 일반적이다.
2. PostgreSQL은 DB 내부 버퍼(shared\_buffers)와 OS의 페이지 캐시를 함께 활용하는 구조이기 때문에, shared buffer를 과도하게 크게 설정하지 않는다.
3. 데이터 조회 시 ① shared buffer → ② OS page cache → ③ 디스크 순으로 접근하여 최대한 디스크 I/O를 줄인다.
4. 반면 Oracle은 DB 내부 메모리를 크게 사용하는 구조이며, PostgreSQL은 OS 캐시와 협력하는 방식으로 전체 시스템 메모리 효율을 높이는 전략을 사용한다.

공유 메모리

shared buffer: 일반적인 데이터베이스의 버퍼영역과 동일하며 디스크 IO를 줄여주는 역할. 128KB를 기본값

WAL(write ahead log): 변경사항들을 바로 디스크에 반영하지않고 메모리에 기록해두는 영역이며 일정시간 혹은 조건을 만족하면 디스크에 반영을 하는데 이때 WAL 세그먼트에 반영

Clog(comiit log): 트랜잭션별로 결과를 저장하는 영역이며 트랜잭션이 진행중이면 in-progress, 정상적인 commit이되면 "commited", rollback되면 "aborted" 결과를 반환한다.

```sql
SELECT txid_current();
-- 751
SELECT txid_status(751);
```

락 스페이스: 데이터베이스에서 락을 관리하는 장부이며 누가(PID), 무엇을(table/row), 어떤 종류의 락(exclusive/shared)을 점유하고 있는지 알수 있음.

로컬 메모리

backend 프로세스가 관리하는 영역이며 쿼리를 실행후 결과를 전송

세션/트랜잭션별로 단위 메모리를 설정 가능
{% endraw %}