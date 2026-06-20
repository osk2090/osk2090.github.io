---
layout: default
title: "Spring Security-Exception 처리에 관해"
date: 2022-12-28 00:12:22 +0900
categories: [Spring]
slug: post-134-spring-security-exception-처리에-관해
image: /images/134/img.png
---
{% raw %}

![](/images/134/img.png)

사진과 같이 전역예외처리는 Filter단에서 일어난 예외를 별도로 처리할 수 없다.

그래서 Filter단에서 예외를 던져줘야 한다.

- security config

![](/images/134/img_1.png)

- jwt filter

![](/images/134/img_2.png)

- exception 리턴

![](/images/134/img_3.png)

출처: <https://jhkimmm.tistory.com/29>

[[Spring Security] Filter 에서 발생한 예외 핸들링하기

Spring Security에서 JWT를 사용한 인증에서 발생할 수 있는 ExpiredJwtException, JwtException, IllegalArgumentException과 같이 Filter에서 발생하는 Exception을 핸들링하는 방식에 대해 알아보겠습니다. @ControllerAdvice

jhkimmm.tistory.com](https://jhkimmm.tistory.com/29)

<https://w97ww.tistory.com/74>

[[Spring Boot] GlobalExceptionHandler

TIL 40일차 개인프로젝트 globalExceptionhandler를 만들어보려고 한다. Controller를 작성할 때 예외상황을 고려하며 처리해야 하는 작업이 늘어남에 따라, 스프링 MVC에서는 @ExceptionHandler와 @ControllerAdvice

w97ww.tistory.com](https://w97ww.tistory.com/74)
{% endraw %}