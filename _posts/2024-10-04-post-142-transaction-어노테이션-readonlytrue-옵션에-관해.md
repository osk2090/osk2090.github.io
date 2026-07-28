---
layout: default
title: "Spring @Transactional(readOnly = true)의 성능 최적화 동작 원리 분석"
date: 2024-10-04 16:32:18 +0900
categories: [Database]
slug: spring-transactional-readonly-optimization
---
{% raw %}

스프링 프레임워크 기반 백엔드 애플리케이션 개발 시 조회 전용 서비스 메서드에 `@Transactional(readOnly = true)` 옵션을 부여하는 것은 보편적인 관례(Best Practice)입니다.

단순히 "조회 성능이 좋아진다"를 넘어, 계층별(스프링, JPA/Hibernate, JDBC, DB)로 어떤 메커니즘을 통해 최적화가 이루어지는지 계층 구조별로 정밀 분석해보겠습니다.

---

## 1. ORM (JPA / Hibernate) 레이어 최적화

JPA를 사용하는 경우 `@Transactional(readOnly = true)`의 가장 큰 이점은 **엔티티 스냅샷 미생성과 변경 감지(Dirty Checking) 비활성화**입니다.

### 1) FlushMode.MANUAL 설정
- 일반적인 `@Transactional` 메서드에서는 트랜잭션 종료 시점(또는 JPQL 실행 직전) 영속성 컨텍스트(Persistence Context)가 `flush()`를 호출하여 엔티티 변경 사항을 DB에 반영합니다.
- `readOnly = true`가 적용되면 하이버네이트는 **`FlushMode`를 `MANUAL`로 변경**합니다.
- 따라서 명시적으로 `flush()`를 호출하지 않는 한 트랜잭션 커밋 시 플러시가 자동으로 일어나지 않아, 디스크 I/O 발생이 원천 차단됩니다.

### 2) 메모리 절약 (Snapshot 미저장)
- 영속성 컨텍스트는 조회한 엔티티의 초기 상태를 1차 캐시에 **스냅샷(Snapshot)** 형태로 보관하여 추후 비즈니스 로직에 따른 변경 여부를 비교합니다.
- `readOnly = true` 상태에서는 하이버네이트가 스냅샷 작성을 생략(또는 1차 캐시 최적화)하므로 **메모리 사용량이 대폭 줄어듭니다.**

---

## 2. Spring Framework & Transaction Manager 레이어

### 1) 트랜잭션 동기화 및 롤백 유무 판별 절차 간소화
- Spring의 `PlatformTransactionManager`는 트랜잭션 생성 시 `TransactionDefinition` 객체의 `isReadOnly()` 값을 확인합니다.
- 읽기 전용 상태일 경우 예외 발생 시의 롤백 전파(Rollback Propagation) 메커니즘을 가볍게 처리하고, 불필요한 트랜잭션 동기화 메타데이터 생성을 최소화합니다.

### 2) Master-Replica 데이터베이스 동적 라우팅
- `@Transactional(readOnly = true)`는 **DB Master/Replica (Replication) 분기 처리**의 기준 태그가 됩니다.
- `AbstractRoutingDataSource`를 확장하여 구현된 라우팅 레이어는 `readOnly` 여부를 감지하여 CUD 쿼리는 Master DB로, 단순 SELECT 쿼리는 읽기 전용 Slave(Replica) DB로 자동 분산 전달합니다.

---

## 3. JDBC Driver & Database 레이어 최적화

### 1) Connection.setReadOnly(true) 힌트 전송
- JDBC 드라이버 수준에서 `connection.setReadOnly(true)` 힌트가 데이터베이스 세션으로 전달됩니다.

### 2) DB 엔진 레벨의 락(Lock) 및 트랜잭션 ID 최소화
- **MySQL (InnoDB)**:
  - Read-Only 트랜잭션으로 지정되면 InnoDB는 해당 트랜잭션에 **트랜잭션 ID(trx_id)를 부여하지 않고** 가벼운 Read-Only Transaction 목록(`trx_sys->ro_trx_list`)으로 관리합니다.
  - 이로 인해 Undo Log 할당과 트랜잭션 테이블 락(Lock) 오버헤드가 완전히 제거됩니다.
- **PostgreSQL**:
  - PostgreSQL 엔진 차원에서 읽기 전용 트랜잭션 내에서 `INSERT/UPDATE/DELETE` 수행 시 즉시 SQL 예외를 발생시켜 데이터 오염을 방지하고, MVCC Snapshot 획득 및 락 경합을 줄입니다.

---

## 💡 결론 및 정리 표

| 계층 | 주요 최적화 메커니즘 | 성과 |
| :--- | :--- | :--- |
| **ORM (JPA)** | `FlushMode.MANUAL` 전환, Snapshot 미생성 | Dirty Checking 차단, GC 부하 감소 |
| **Spring** | `AbstractRoutingDataSource` 연동 | Replica DB로 읽기 쿼리 자동 분산 |
| **JDBC** | `Connection.setReadOnly(true)` 전달 | 드라이버 및 DB 커넥션 힌트 제공 |
| **Database** | Read-Only Transaction 지정 (trx_id 미발급) | Undo Log 할당 및 락 오버헤드 제거 |
{% endraw %}