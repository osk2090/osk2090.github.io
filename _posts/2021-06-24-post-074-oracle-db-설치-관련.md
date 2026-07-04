---
layout: default
title: "Oracle DB 유저 생성 기법 및 테이블스페이스(TABLESPACE)와 임시(TEMPORARY) 개념 분석"
date: 2021-06-24 18:59:32 +0900
categories: [Database]
slug: post-074-oracle-db-설치-관련
---
{% raw %}

오라클(Oracle) 데이터베이스는 다른 보편적인 오픈소스 관계형 데이터베이스(예: MySQL, MariaDB)와 대비되는 구조적인 차이를 지니고 있습니다. 그중 대표적인 개념이 바로 **테이블스페이스(Tablespace)**입니다. 이번 포스팅에서는 오라클 데이터베이스 설치 직후 개발용 신규 사용자를 생성하는 SQL 명령어 구조와 함께, `DEFAULT TABLESPACE`와 `TEMPORARY TABLESPACE`의 물리적 정의 및 실무적 의미에 대해 분석해 보겠습니다.

---

## 1. Oracle DB 사용자 계정 생성 SQL

오라클 데이터베이스에 관리자 권한(`SYS`, `SYSTEM`)으로 접속한 후, 실제 프로젝트 개발을 위해 신규 계정을 구성할 때는 보통 아래와 같은 SQL 구문을 수행합니다.

```sql
-- 신규 사용자 생성 및 패스워드 설정, 저장 공간 지정
CREATE USER book_ex IDENTIFIED BY book_ex
DEFAULT TABLESPACE USERS
TEMPORARY TABLESPACE TEMP;
```

### 1) `DEFAULT TABLESPACE USERS`
* **의미**: 사용자가 향후 테이블이나 인덱스 등의 실제 데이터베이스 객체(Segment)를 생성할 때, 별도의 테이블스페이스명을 명시하지 않으면 자동으로 데이터를 채워 넣을 **기본 물리 저장 공간(USERS)**을 지정합니다.

### 2) `TEMPORARY TABLESPACE TEMP`
* **의미**: 사용자 쿼리 처리 과정에서 연산 속도 향상을 위해 메모리 외에 보조적으로 임시 데이터를 저장하는 **임시 테이블스페이스(TEMP)**를 지정합니다.

---

## 2. 테이블스페이스(Tablespace)란?

오라클에서 테이블스페이스는 **데이터베이스의 논리적인 저장 구조이며, 물리적인 데이터 파일(.dbf)들과 1대N 관계로 매핑**됩니다.

```
[Oracle Database]
   └─ Tablespace (논리적 공간: SYSTEM, USERS, TEMP 등)
         └─ Data Files (물리적 파일: system01.dbf, users01.dbf, temp01.dbf 등)
```

즉, 테이블 자체는 물리적 디스크 파일에 직접 생성되는 것이 아니라 논리적 저장소인 테이블스페이스에 속하게 되며, 테이블스페이스에 바인딩된 실제 물리 데이터 파일에 데이터가 안전하게 기록되는 유연한 저장 구조를 제공합니다.

---

## 3. 임시 테이블스페이스(TEMPORARY TABLESPACE)의 진정한 역할

기본적인 데이터 조작(INSERT, UPDATE 등)은 모두 `DEFAULT TABLESPACE`에 기록됩니다. 그렇다면 `TEMPORARY TABLESPACE TEMP`는 무엇을 위해 필요할까요?

데이터베이스 엔진이 쿼리를 실행하다 보면 서버의 메모리(SGA 내의 SQL Work Area) 한계를 넘어서는 **엄청난 크기의 데이터 처리 작업**을 수행해야 할 때가 있습니다.
1. **대량의 데이터 정렬 (`ORDER BY`, `GROUP BY`)**: 메모리 내에서 다 소화하지 못하는 대용량 정렬 작업이 발생하면, 오라클은 데이터를 쪼개어 임시 테이블스페이스(TEMP)에 임시 보관한 뒤 정렬 병합(Merge Sort)을 수행합니다.
2. **해시 조인 (`HASH JOIN`)**: 조인 테이블 크기가 커서 해시 테이블을 메모리에 다 적재하지 못할 때 디스크(TEMP) 영역을 빌려 연산합니다.
3. **대규모 인덱스 생성 (`CREATE INDEX`)**: 인덱스를 빌드할 때 발생하는 내부 정렬 작업에 사용됩니다.

이처럼 임시 테이블스페이스는 데이터의 영구 저장이 아닌 **"정렬 및 고속 처리를 위한 디스크 작업용 임시 공간"** 역할을 담당합니다.

---

## 4. 계정 생성 후 필수 단계: 권한 부여 (GRANT)

오라클에서는 계정을 생성하는 것만으로는 접속할 수 없습니다. 시스템 접근 및 테이블 생성을 위해 명시적으로 시스템 권한을 위임받아야 합니다.

```sql
-- 접속(CONNECT) 권한 및 객체 생성(RESOURCE) 권한 부여
GRANT CONNECT, RESOURCE TO book_ex;

-- 테이블스페이스 할당량(Quota) 설정 (USERS 공간에 무제한 쓰기 허용)
ALTER USER book_ex QUOTA UNLIMITED ON USERS;
```

* **`CONNECT`**: 세션 생성(로그인) 등 기본 접속 권한이 포함된 롤(Role)입니다.
* **`RESOURCE`**: 테이블, 시퀀스, 트리거 등 실제 개발에 필요한 리소스 생성 권한이 포함된 롤입니다.

MySQL만 접하던 백엔드 개발자에게 오라클의 물리/논리 분리 사상인 테이블스페이스 구조는 다소 까다롭게 느껴질 수 있습니다. 하지만 시스템 규모가 커지고 저장 공간 튜닝이 절실한 실무 아키텍처 환경에서는 저장 파일 분배 및 정렬 성능 최적화를 위한 핵심 장치임을 인지해야 합니다.

* [Oracle 19c XE Prior Releases Download](https://www.oracle.com/database/technologies/xe-prior-releases.html)
* [Oracle SQL Developer Download](https://www.oracle.com/tools/downloads/sqldev-downloads.html)
{% endraw %}