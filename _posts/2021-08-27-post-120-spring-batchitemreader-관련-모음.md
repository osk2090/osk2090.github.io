---
layout: default
title: "Spring-Batch:ItemReader 관련 모음"
date: 2021-08-27 10:35:52 +0900
categories: [Spring Batch]
slug: post-120-spring-batchitemreader-관련-모음
render_with_liquid: false
---

### ItemReader Interface

배치 대상 데이터를 읽기 위한 설정

- 파일,DB,네트워크, 등에서 읽기 위함

Step에 ItemReader는 필수

기본 제공되는 ItemReader 구현체

- file,jdbc,jpa,hibernate,kafka,etc...

ItemReader 구현체가 없으면 직접 개발

ItemStreamd은 ExecutionContext로 read,write 정보를 저장

---

### FlatFileItemReader

DB가 아닌 파일 형식으로 된 데이터를 읽어올 수 있도록 구현된 구현체이다.

한번 read 할 때 지정된 resource의 한 라인씩 읽어들인다.

---

### JDBC 데이터 읽기

#### Cursor 기반 조회

배치 처리가 완료될 때까지 DB Connection이 연결

DB Connection 빈도가 낮아 성능이 좋은 반면, 긴 Connection 유지 시간 필요

하나의 Connection에서 처리되기 때문에 Thread Safe하지 않는다

모든 결과를 메모리에 할당하기 때문에 더 많은 메모리를 사용한다.

#### Paging 기반 조회

페이징 단위로 DB Connection을 연결

DB Connection 반도가 높아 비교적 성능이 낮은 반면 짧은 Connection 유지 시간 필요하다.

매번 Connection을 하기 때문에 Thread safe

페이징 단위의 결과만 메모리에 할당하기 때문에 비교적 더 적

은 메모리를 사용한다.

\*Thread safe: 멀티 스레드 프로그래밍에서 일반적으로 어떤 함수나 변수, 혹은 객체가 여러 스레드로부터 동시에 접근이 이루어져도 프로그램의 실행에 문제가 없음을 뜻한다.