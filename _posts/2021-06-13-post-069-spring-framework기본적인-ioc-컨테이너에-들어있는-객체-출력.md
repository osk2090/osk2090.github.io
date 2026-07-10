---
layout: default
title: "[Spring Framework]기본적인 IoC 컨테이너에 들어있는 객체 출력"
date: 2021-06-13 02:54:13 +0900
categories: [Spring]
slug: post-069-spring-framework기본적인-ioc-컨테이너에-들어있는-객체-출력
published: false
---
{% raw %}

%[https://gist.github.com/osk2090/aa540b05131757e25177930c4ef05f1e]

해당 코드를 출력해보면

```html
==============================================
빈의 개수: 5
org.springframework.context.annotation.internalConfigurationAnnotationProcessor = org.springframework.context.annotation.ConfigurationClassPostProcessor
org.springframework.context.annotation.internalAutowiredAnnotationProcessor = org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor
org.springframework.context.annotation.internalCommonAnnotationProcessor = org.springframework.context.annotation.CommonAnnotationBeanPostProcessor
org.springframework.context.event.internalEventListenerProcessor = org.springframework.context.event.EventListenerMethodProcessor
org.springframework.context.event.internalEventListenerFactory = org.springframework.context.event.DefaultEventListenerFactory
==============================================
```

총 5개의 객체(빈)이 자동으로 생성되는것을 볼 수 있다.

- ConfigurationClassPostProcessor : @Configuration에 대한 설정 처리를 한다.

- AutowiredAnnotationBeanPostProcessor : @Autowired에 대한 의존 주입 처리를 한다.

- CommonAnnotationBeanPostProcessor : JSR-250(@PostConstruct 등)에 대한 라이프사이클 처리를 한다.

(@postConstruct

- 객체의 초기화 부분  
- 객체가 생성된 후 별도의 초기화 작업을 위해 실행하는 메소드를 선언한다.  
- @PostConstruct 어노테이션을 설정해놓은 init 메소드는 WAS가 띄워질 때 실행된다.)

- EventListenerMethodProcessor:([원문](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/event/EventListenerMethodProcessor.html))Registers [EventListener](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/event/EventListener.html) methods as individual [ApplicationListener](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/ApplicationListener.html) instances

이벤트리스너 메서드를 개별적으로 애플리케이션 인스턴스로 등록한다.

(해당 코드에 이벤트리스너를 심어놓으면 설정한 코드대로 출력을 해주거나 동작한다.)

- DefaultEventListenerFactory:([원문](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/context/event/DefaultEventListenerFactory.html))Used as "catch-all" implementation by default. 말그대로 범용적으로 이벤트 리스너를 적용한다는 것.

출처: <https://goddaehee.tistory.com/46> [갓대희의 작은공간]

https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=javaking75&logNo=220728817382
{% endraw %}