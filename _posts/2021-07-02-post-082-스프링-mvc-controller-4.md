---
layout: default
title: "스프링 MVC Controller-4"
date: 2021-07-02 16:55:59 +0900
categories: [Spring]
slug: post-082-스프링-mvc-controller-4
render_with_liquid: false
image: /images/82/img.png
---

### Controller의 Exception 처리

Controller를 작성할 때 예외 상황을 고려하면 처리해야 하는 작업이 엄청나게 늘어날 수 밖에 없다.

스프링 MVC에서는 이러한 작업을 다음과 같은 방식으로 처리할 수 있다.

- @ExceptionHandler와 @ControllerAdvice를 이용한 처리
- @ResponseEntity를 이용하는 예외 메시지 구성

#### @ControllerAdvice

@ControllerAdvice는 뒤에서 배우게되는 AOP(Aspect-Oriented-Programming)를 이용하는 방식이다.

AOP는 간단히 말하면 핵심적인 로직은 아니지만 프로그램에서 필요한 '공통적인 관심사는 분리' 하자는 개념이다.

Controller를 작설할 때는 메서드의 모든 예외사항을 전부 핸들링해야 한다면

중복적이고 많은 양의 코드를 작성해야 하지만 AOP방식을 이용한다면

공통적인 예외사항에 대해서는 별도로 @ControllerAdvice를 이용해서 분리하는 방식이다.

CommonExceptionAdvice.class

```java
@ControllerAdvice
@Log4j
public class CommonExceptionAdvice {
    @ExceptionHandler(Exception.class)
    public String except(Exception ex, Model model) {
        log.error("Exception...." + ex.getMessage());
        model.addAttribute("exception", ex);
        log.error(model);
        return "error_page";
    }
}
```

CommonExceptionAdvice 클래스에는

@ControllerAdvice라는 어노테이션과 @ExceptionHandler라는 어노테이션을 사용하고 있다.

@ControllerAdvice는 해당 객체가 스프링의 컨트롤러에서

발생하는 예외를 처리하는 존재임을 명시하는 용도로 사용하고

@ExceptionHandler는 해당 메서드가 () 들어가는 예외 타입을 처리한다는 것을 의미한다.  
@ExceptionHandler 어노테이션의 속성으로 Exception 클래스 타입을 지정할 수 있다.

위와 같은 경우 Exception.class를 지정하였으므로 모든 예외에 대한 처리가 except()만을 이용해서 처리할 수 있다.

만일 특정한 타입의 예외를 다루고 싶다면 Exception.class 대신에 구체적인 예외의 클래스를 지정해야 한다.

JSP화면에서도 구체적인 메시지를 보고 싶다면 Model을 이용해서 전달하는 것이 좋다.

com.osk2090.exception 패키지는 servlet-context.xml에서 인식하지 않기 때문에 <component-scan>을 이용해서 해당 패키지의 내용을 조사하도록 해야 한다.

필자는 현재 ServletConfig.class를 사용하고 있으므로

```java
@ComponentScan(basePackages = {"com.osk2090.controller", "com.osk2090.exception"})
```

위와 같이 기재하였다.

CommonExceptionAdvice의 except()의 리턴값은 문자열이므로 JSP 파일의경로가 된다.

JSP는 error\_page.jsp이므로 /WEB-INF/views 폴더 내에 작성해야 한다.

이제 여기서 고의로 에러를 발생시켜보자

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex04?name=osk&age=o&page=11
```

age를 보면 int가 아닌 문자열이 들어간것을 볼 수 있다.

그래서 실행해 보면 에러가 출력된다.

![](/images/82/img.png)

### 404 에러 페이지

WAS의 구동 중 가장 흔한 에러와 관련된 HTTP 상태 코드는 404와 500에러 코드이다.

500 메시지는 Internal Server Error이므로

@ExceptionHandler를 이용해서 처리하지만 잘못된 URL을 호출할 때 보이는 404에러 메시지의 경우는

조금 다르게 처리하는 것이 좋다.

서블릿이나 JSP를 이용했던 개발 시에는 web.xml을 이용해서 별도의 에러 페이지를 지정 할 수 있다.

에러 발생 시 추가적인 작업을 하기에는 어렵기 때문에 스프링을 이용해서 404와 같이

WAS내부에서 발생하는 에러를 처리하는 방식을 알아두는 것이 좋다.

스프링 MVC의 모든 요청은 DispatcherServlet을 이용해서 처리되므로

404 에러도 같이 처리할 수 있도록 web.xml을 수정한다.

WebConfig.class

```java
public class WebConfig extends
        AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class[]{
                RootConfig.class
        };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class[]{ServletConfig.class};
    }

    @Override
    protected String[] getServletMappings() {
        return new String[]{"/"};//스프링 MVC의 기본 경로 /로 수정
    }

	@Override//디스패쳐서블릿 추가설정을 위한 메서드중 하나
    protected void customizeRegistration(
            ServletRegistration.Dynamic registration
            //애플리케이션의 리로딩없이 프로그램 내부에서 동적으로 웹객체를 추가
            ) {
        registration.setInitParameter("throwExceptionIfNoHandlerFound", "true");
        //CommonExceptionAdvice.class가 동작한다면 즉 에러404가 뜬다면
        //custom404.jsp가 출력되게 한다.
    }
}
```

CommonExceptionAdvice.class

```java
@ControllerAdvice
@Log4j
public class CommonExceptionAdvice {
    @ExceptionHandler(NoHandlerFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String handle404(NoHandlerFoundException ex) {
        return "custom404";
    }
}
```

cutom404.jsp

```java
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<h1>해당 URL은 존재하지 않습니다.</h1>
</body>
</html>
```

URL

```java
http://localhost:8080/controller_war_exploded/e
```

존재하지 않는 URL로 테스트를 해보면

![](/images/82/img_1.png)

jsp에서 작성한 내용이 출력되는 것을 알 수 있다.