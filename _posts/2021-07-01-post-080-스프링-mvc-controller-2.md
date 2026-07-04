---
layout: default
title: "스프링 MVC Controller-2"
date: 2021-07-01 02:58:35 +0900
categories: [Spring]
slug: post-080-스프링-mvc-controller-2
image: /images/80/img.png
---
{% raw %}

### Model이라는 데이터 전달자

Controller의 메서드를 작성할 때는 특별하게 Model이라는 타입을 파라미터로 지정할 수 있다.

Model 객체는 JSP에 컨트롤러에서 생성된 데이터를 담아서 전달하는 역할을 하는 존재이다.

이를 이용해서 JSP와 같은 뷰(view)로 전달해야 하는 데이터를 담아서 보낼 수 있다.

메서드의 파라미터에 Model 타입이 지정된 경우에는

스프링은 특별하게 Model 타입의 객체를 만들어서 메서드에 주입한다.

메서드의 파라미터를 Model 타입으로 선언하게 되면 자동으로 스프링 MVC에서 Model 타입의 객체를

만들어 주기 때문에 개발자의 입장에서는 필요한 데이터를 담아 주는 작업만으로 모든 작업이 완료된다.

Model을 사용해야 하는 경우 주로 Controller에 전달된 데이터를 이용해서 추가적인 데이터를 가져와야 하는 상황이다.

예를 들어 다음과 긑은 경우들을 생각해 볼 수 있다.

1. 리스트 페이지 번호를 파라미터로 전달받고,실제 데이터를 view로 전달해야 하는 경우
2. 파라미터들에 대한 처리 후 결과를 전달해야 하는 경우

### @ModelArrtibute 어노테이션

웹페이지의 구조는 Request에 전달된 데이터를 가지고 필요하다면 추가적인 데이터를 생성해서 화면으로 전달하는 방식으로 동작한다.

Model의 경우는 파라미터로 전달된 데이터는 존재하지 않지만 화면에서 필요한 데이터를 전달하기 위해서 사용한다.

예를 들어 페이지 번호는 파라미터로 전달되지만,결과 데이터를 전달하려면 Model에 담아서 전달한다.

스프링 MVC의 Controller는 기본적으로 [Java Beans](https://pjh3749.tistory.com/75) 규칙에 맞는 객체는 다시 화면으로 객체를 전달한다.

좁은 의미에서 Java Beans의 규칙은 단순히 생성자가 없거나 빈 생성자를 가져야 하며,

getter/setter를 가진 클래스의 객체들을 의미한다.

앞의 예제에서 파라미터로 사용된 SampleDTO의 경우는 Java Bean의 규칙에 맞기 때문에 자동으로 다시 화면까지 전달된다.전달될 때에는 클래스명의 앞글자는 소문자로 처리된다.

반면에 기본 자료형의 경우는 파라미터로 선언하더라도 기본적으로 화면까지 전달되지는 않는다.

SampleController.class

```java
@GetMapping("/ex04")
    public String ex04(SampleDTO dto, int page) {
        log.info("dto: " + dto);
        log.info("page: " + page);
        return "/sample/ex04";
    }
```

SampleDTO 타입과 int 타입의 데이터를 파라미터로 사용한다.

결과를 확인하기 위해서 "/WEB-INF/views"폴터 아래 sample 폴더를 생성하고

리턴값에서 사용한 "ex04"에 해당하는 ex04.jsp를 작성한다.

![](/images/80/img.png)

jsp 위치

ex04.jsp

```java
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Title</title>
</head>
<body>
<h2>SAMPLEDTO ${sampleDTO }</h2>

<h2>PAGE ${page }</h2>

</body>
</html>
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex04?name=osk&age=29&page=11
```

View

![](/images/80/img_1.png)

view

콘솔창

```html
INFO : com.osk2090.controller.SampleController - dto: SampleDTO(name=osk, age=29)
INFO : com.osk2090.controller.SampleController - page: 11
```

view를 보면 page의 int값이 안보이는 것을 볼 수 있다.

그래서 보완을 하자면

@ModelAttribute는 강제로 전달받은 파라미터를 Model에 담아서 전달하도록 할 때 필요한 어노테이션이다.

@ModelAttribute가 걸린 파라미터는 타입에 관계없이 무조건 Model에 담아서 전달되므로

파라미터로 전달된 데이터를 다시 화면에서 사용해야 할 경우 유용하게 사용된다.

SampleController.class

```java
@GetMapping("/ex04")
    public String ex04(SampleDTO dto, @ModelAttribute("page") int page) {
        log.info("dto: " + dto);
        log.info("page: " + page);
        return "/sample/ex04";
    }
```

View

![](/images/80/img_2.png)

page에 11이 들어간 것을 확인한거 처럼 기본 자료형에는

@ModelAttribute를 적용할 경우에는 반드시 @ModelAttribute("page")와 같이 값을 지정해야한다.

### @RedirectAttributes

Model 타입과 더불어서 스프링 MVC가 자동으로 전달해 주는 타입 중에는 RedirectAttribute 타입이 존재한다.

RedirectAttribute는 조금 특별하게도 일회성으로 데이터를 전달하는 용도로 사용된다.

RedirectAttribute는 기존에 Servlet에서는 response,sendRedirect()를 사용할 때와 동일한 용도로 사용된다.

Servlet에서 redirect방식

```java
response.sendRedirect("/home?name=aaa&age=10");
```

스프링 MVC를 이용하는 redirect 처리

```java
rttr.addFlashAttribute("name","AAA");
	rttr.addFlashAttribute("age",10);
	return "redirect:/";
```

RedirectAttribute는 Model과 같이 파라미터로 선언해서 사용하고

addFlashAttribute(이름,값) 메서드를 이용해서 화면에 한 번만 사용하고

다음에는 사용되지 않는 데이터를 전달하기 위해서 사용한다.
{% endraw %}