---
layout: default
title: "postgresql-wal-4-record"
date: 2026-10-09 14:24:21 +0900
categories: [Database]
slug: postgresql-wal-4-record
---
{% raw %}

> 💡 **PostgreSQL WAL(Write Ahead Log) 시리즈**
> - **1편: [PostgreSQL WAL (1) 동작 원리와 세그먼트·레코드 내부 구조](/database/2026/08/15/postgresql-wal-1-architecture.html)**
> - **2편: [PostgreSQL WAL (2) LSN 구조와 WAL 추적 함수 분석](/database/2026/09/05/postgresql-wal-2-lsn.html)**
> - **3편: [PostgreSQL WAL (3) 체크포인트 메커니즘과 세그먼트 관리 및 아카이빙](/database/2026/10/03/postgresql-wal-3-checkpoint.html)**
> - **4편: PostgreSQL WAL (4) WAL 레코드 내부 구조 분석** (현재 글)

---

## 1. WAL 레코드란?

쉽게 말하면 <u>어느 테이블의 파일의 몇번째 페이지를 어떻게 바꿨다</u> 라고 이해하면 된다.

예를들면 insert 1개가 발생하면 이 페이지에 이 튜플 추가 했다는 의미의 레코드 1개를 추가했다고 이걸 한개의 WAL 레코드라고 보면 되겠다.

WAL 레코드에는 트랜잭션 id(xid), 페이지 id, 오프셋, 길이, 이전 데이터, 현재 데이터 등을 담고있다.

CRUD가 발생하면 먼저 WAL 버퍼에 기록된다. 변경된 내용은 즉시 디스크에 반영하지 않고 공유 메모리 영역인 WAL 버퍼에 임시 저장한다. 근데 갑자기 여기서 WAL 버퍼 영역을 이야기해서 당황하였다.
그래서 WAL 영역에 대해서 클로드한테 물어보았다.

> WAL버퍼는 WAL 레코드를 디스크 즉, WAL 파일에 반영하기 전에 잠깐 모아두는 공유 메모리 영역이다.

라고 설명해준다. 결국 WAL 레코드도 디스크에 바로바로 반영하면 병목현상이 발생할 것이다. 이 점을 해결하기 위해서 메모리에 올려놓고 주기적으로 디스크에 반영한다고 보면 되겠다.

근데 앞에서 공부한 shared buffer 영역과 비슷한 역할을 하는데 뭐가 다른건지 궁금하였다.

간단하게 비교하면 shared buffer 영역은 일반 데이터들을 관리하는것이고, WAL buffer는 WAL 레코드들을 관리하는것이라고 보면 된다.

다시 WAL 버퍼로 돌아오면 결국 여기에 적재된 데이터들은 언젠가는 flush되어야된다. 그 조건은 아래와 같다.

1. 수행 중인 트랜잭션이 커밋/취소가 수행될 때
2. WAL 버퍼가 많은 레코드로 채워질 때
3. WAL Writer 프로세스에 의해 주기적으로 기록될 때

---

### 💡 INSERT → COMMIT → 체크포인트 단계별 시뮬레이션

아래 인터랙티브 시뮬레이션을 통해 트랜잭션 수행부터 커밋, 체크포인트까지 WAL 버퍼와 디스크의 변화 과정을 단계별로 직접 확인해보실 수 있습니다.

<iframe src="/assets/html/insert-commit-checkpoint-simulation.html" width="100%" height="820px" style="border: 1px solid #cfd9de; border-radius: 12px; margin: 20px 0; background: #fff;" loading="lazy"></iframe>

> 🔗 화면이 작거나 잘 보이지 않는다면 [새 탭에서 전체 화면으로 보기](/assets/html/insert-commit-checkpoint-simulation.html){:target="_blank"}를 클릭해 주세요.

{% endraw %}

