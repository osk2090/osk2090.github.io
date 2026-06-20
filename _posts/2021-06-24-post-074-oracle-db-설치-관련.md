---
layout: default
title: "Oracle DB 설치 관련"
date: 2021-06-24 18:59:32 +0900
categories: [Database]
slug: post-074-oracle-db-설치-관련
render_with_liquid: false
---

Oracle DB 설치

<https://www.oracle.com/database/technologies/xe-prior-releases.html>

SQL Developer 설치

<https://www.oracle.com/tools/downloads/sqldev-downloads.html>

명령문

```html
CREATE USER book_ex IDENTIFIED BY book_ex ---> 계정이름과 계정비밀번호 선언
DEFAULT TABLESPACE USERS ---> 기본 테이블 스페이스 선언
TEMPORARY TABLESPACE TEMP; ---> 임시 테이블 스페이스 선언
```

필자는 원래 MySQL을 사용하여 처음보는 임시테이블인데 오라클에서는 따로 선언해주는 부분이 있다.

(트랜잭션을 이유로 선언하는 것 같다.)