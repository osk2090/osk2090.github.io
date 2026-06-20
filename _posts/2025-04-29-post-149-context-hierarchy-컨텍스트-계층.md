---
layout: default
title: "Context Hierarchy-컨텍스트 계층"
date: 2025-04-29 00:03:19 +0900
categories: [Etc]
slug: post-149-context-hierarchy-컨텍스트-계층
render_with_liquid: false
---

스프링 컨텍스트 계층은 크게 나누면 자식 컨텍스트인 Servlet-WebApplicationContext가 있고 그의 부모인 Root-WebApplicationContext가 있다.

Servlet-WebApplicationContext엔 주로 웹과 관련된 컨트롤러-뷰-헨들러가 있으며

Root-WebApplicationContext엔 비즈니스 계층, DB 커넥터와 같은 공통적으로 사용하는 리소스에 대한 빈을 관리한다.

그래서 빈을 조회하면 먼저 자식 컨텍스트에서 조회를 하고 자식에게 빈이 없으면 부모 컨텍스트에서 조회를 하고 빈을 찾으면 자식 컨텍스트에게 주입하여 사용한다.

http 요청시 동작방식(GPT 참고)

1. **HTTP 요청 → DispatcherServlet**
2. 클라이언트가 /foo 같은 URL로 요청을 보내면, DispatcherServlet(서블릿 컨텍스트)에서 받음.
3. **웹 전용 빈 조회**이때 필요한 인터셉터나 뷰 리졸버 등 웹계층 전용 빈들은 **자식(Web) 컨텍스트**에서 바로 조회
4. HandlerMapping → @Controller 빈 → 해당 컨트롤러의 메서드 실행
5. **비즈니스 로직 호출**  
   - 먼저 **자식 컨텍스트**에 MyService 빈이 있는지 찾고,
   - 없으면 **부모(Root) 컨텍스트**로 올라가서 MyService 빈을 찾아 주입·실행
6. 컨트롤러 내부에서 @Autowired 된 MyService 같은 **서비스 빈**을 호출하면,
7. **DB 접근 등 인프라 빈**모두 부모 컨텍스트에서 조회되어 사용
8. MyService 안에서 @Autowired 된 DataSource·TransactionManager·MyRepository 같은 빈들도 모두 부모 컨텍스트에서 조회되어 사용

이런 구조를 통해

- 웹·비즈니스 로직을 깔끔히 분리할 수 있고,
- 여러 서블릿이 하나의 공통 서비스·리포지토리를 재사용할 수 있다.