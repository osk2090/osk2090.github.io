---
layout: default
title: "@Transaction 어노테이션 readOnly=true 옵션에 관해"
date: 2024-10-04 16:32:18 +0900
categories: [Database]
slug: post-142-transaction-어노테이션-readonlytrue-옵션에-관해
render_with_liquid: false
---

나도 그냥 구글링해서 찾아본 바로는 단순히 데이터를 가져오는 메서드에 @Transaction(readOnly=true) 옵션을 주면

최적화가 된다고 들었다. 근데 왜 최적화가 되는지 그리고 어떻게 최적화가 되는지 궁금해서 찾아봤다.

먼저 단계별로 장점들이 있다.

1. 데이터베이스 레이어
   1. 일부 데이터베이스에서는 읽기전용 트랜잭션이 가벼운 잠금을 하기때문에 데이터베이스에 부하가 가지 않는다.
2. JDBC 레이어
   1. 가져온 데이터들을 내부적으로 캐싱하기 때문에 추후 중복된 데이터를 가져올때 데이터베이스에 중복된 쿼리를 날리는 것을 방지할수 있다.
3. ORM 레이어
   1. 가져온 데이터에 변경이 일어나는지에 대한 변경체크(dirty checking)을 하는데 이건 아무래도 스프링 내부에서 계속 주시해야되기 때문에 readOnly=true 상태라면 해당 기능을 off하기때문에 좋을것이다.
4. 스프링 레이어
   1. 트랜잭션 시작시 불필요한 리소스 할당을 줄임.

@Transactional(readOnly = true) 최적화

스프링 레이어: 불필요한 리소스 할당 감소

ORM 레이어: 변경 감지(Dirty Checking) 비활성화

JDBC 레이어: 결과 캐싱, 네트워크 최적화

데이터베이스 레이어: 가벼운 잠금 사용