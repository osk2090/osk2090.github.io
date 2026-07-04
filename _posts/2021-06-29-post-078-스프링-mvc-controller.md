---
layout: default
title: "스프링 MVC Controller"
date: 2021-06-29 18:50:16 +0900
categories: [Spring]
slug: post-078-스프링-mvc-controller
image: /images/78/img.png
---
{% raw %}

스프링 MVC를 이용하는 경우 작성되는 컨트롤러에는 특징이 있다.

- HttpServletRequest/HttpServletResponse를 거의 사용할 필요 없이 필요한 기능 구현
- 다양한 타입의 파라미터 처리,다양한 타입의 리턴 타입 사용 가능
- GET 방식,POST 방식등 전송 방식에 대한 처리를 어노테이션으로 처리 가능
- 상속/인터페이스 방식 대신에 어노테이션만드로도 필요한 설정 가능

이렇듯 어노테이션을 중심으로 구성되기 때문에 각 어노테이션의 의미를 주의하며 작성해야 한다.

#### 예제

클래스 선언부에 @Controller 어노테이션을 선언하는데 이렇게 되면 자동으로 빈이 생성된다.

이에 대한 증거로는 servlet-context.xml 또는 ServletConfig.class이다.

```java
@EnableWebMvc
@ComponentScan(basePackages = {"com.osk2090.controller"})//해당 패키지를 스캔하도록 되어 있다.
public class ServletConfig implements WebMvcConfigurer {
...생략
}
```

그래서 해당 클래스를 스프링에서 관리하면 사진처럼 뜬다.

![](/images/78/img.png)

클래스 선언부에는 @Controller와 함께 @RequestMapping을 많이 사용한다.

@RequestMapping은 현재 클래스의 모든 메서드들의 기본적인 URL 경로가 된다.

예를 들어 SampleController 클래스를 다음과 같이 "/sample/\*"이라는 경로로 지정했다면

다음과 같이 URL은 모두 SampleController에서 처리된다.

- /sample/aaa
- /sample/bbb

@RequestMapping 어노케이션은 클래스의 선언과 메서드 선언데 사용할 수 있다.

그래서 구동을 해보고 콘솔창을 확인해보면 정보를 확인할 수 있다.

```java
INFO : org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping - 
Mapped "{[/],methods=[GET]}" onto public java.lang.String com.osk2090.controller.
HomeController.home(java.util.Locale,org.springframework.ui.Model)

INFO : org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping - 
Mapped "{[/sample/*]}" onto public void com.osk2090.controller.SampleController.basic()
```

현재 프로젝트의 경우'/'와 'sample/\*'는 호출이 가능한 경로라는 것을 확인 할 수 있다.
{% endraw %}