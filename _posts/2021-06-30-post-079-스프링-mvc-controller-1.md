---
layout: default
title: "스프링 MVC Controller-1"
date: 2021-06-30 20:19:10 +0900
categories: [Spring]
slug: post-079-스프링-mvc-controller-1
image: /images/79/img.png
---
{% raw %}

### @RequestMapping의 변화

@Controller 어노테이션은 추가적인 속성을 지정할 수 없지만,

@RequestMapping의 경우 몇 가지의 속성을 추가할 수 있다.

이 중에서도 가장 많이 사용하는 method 속성이다.그중에서 GET방식과 POST방식을 구분해서 사용할 때 이용한다.

스프링 4.3버전 부터는 이러한 @requestMapping을 줄여서 사용할 수 있는

@GestMapping @PostMapping으로 축약형의 표현이다.

### Controller의 파라미터 수집

Controller를 작성할 때 가장 편리한 기능은 파라미터가 자동으로 수집되는 기능이다.

이 기능을 이용하면 매번 request.getParameter()를 이용하는 불편함을 없앨수 있다.

#### @Data

Lombok의 어노테이션중 하나인데 이것을 이용하게 되면

getter/setter,equals(), toString() 등의 메서드를 자동 생성하게 해준다.

#### 예제

SampleDTO.class

```java
@Data//getter/setter,equals(), toString() 자동 생성
public class SampleDTO {
    private String name;
    private int age;
}
```

SampleController.class

```java
@Controller
@RequestMapping("/sample/*")
@Log4j
public class SampleController {

...생략...

    @GetMapping("/ex01")
    public String ex01(SampleDTO dto) {
        log.info("" + dto);
        return "ex01";
    }
}
```

URL

![](/images/79/img.png)

콘솔창

```html
INFO : com.osk2090.controller.SampleController - SampleDTO(name=AAA, age=10)
```

실행된 결과를 보면 SampleDTO 객체 안에서 name과 age 속성이 제대로 수집된 것을 볼 수 있다.

주목할 점은 자동으로 타입을 변환해서 처리한다는 점이다.

#### 파라미터 수집과 변환

Controller가 파라미터를 수집하는 방식은 파라미터 타입에 따라 자동으로 변환하는 방식을 이용한다.

예를 들어 SampleDTO()에는 int 타입으로 선언된 age가 자동으로 숫자로 변환되는 것을 알 수 있다.

만일 기본 자료형이나 문자열 등을 이용한다면 파라미터의 타입만을 맞게 선언해주는 방식을 사용 할 수 있다.

예제

```java
@Controller
@RequestMapping("/sample/*")
@Log4j
public class SampleController {

...생략...

    @GetMapping("/ex02")
    public String ex02(@RequestParam("name") String name
            , @RequestParam("age") int age) {
        log.info("name:" + name);
        log.info("age: " + age);
        return "ex02";
    }
}
```

ex02() 메서드는 파라미터에 @RequestParams 어노테이션을 사용해서 작성되었는데

@RequestParams은 파라미터로 사용된 변수의 이름과 전달되는 파라미터의 이름이 다른 경우에 유용하게 사용된다.

예)

```java
@GetMapping("/ex02")
    public String ex02(@RequestParam("n") String name
            , @RequestParam("a") int age) {
        log.info("name:" + name);
        log.info("age: " + age);
        return "ex02";
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex02?n=AAA&a=10
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - name:AAA
INFO : com.osk2090.controller.SampleController - age: 10
```

여기서 return "들어갈 주소"는 기본적으로 해당  view(JSP)를 호출하는 것이다.결국엔 화면에 어떤걸 뿌릴지 지정해주는것이다.

하지만 들어갈 주소에 'redirect:/들어갈 주소' 는 오른쪽 주소로 다시 URL을 요청하는 것이다.

### 리스트,배열 처리

동일한 이름의 파라미터가 여러 개 전달되는 경우에는 ArrayList<> 등을 이용해 처리가 가능하다.

```java
@GetMapping("/ex02List")
    public String ex02List(@RequestParam("ids") ArrayList<String> ids) {
        log.info("ids: " + ids);
        return "ex02List";
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex02List?ids=1&ids=2&ids=3&ids=4&ids=5&ids=6
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - ids: [1, 2, 3, 4, 5, 6]
```

#### 다른방법

```java
@GetMapping("/ex02Array")
    public String ex02Array(@RequestParam("ids") String[] ids) {
        log.info("array ids: " + Arrays.toString(ids));
        return "ex02Array";
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex02Array?ids=a&ids=b&ids=c&ids=d&ids=e&ids=f
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - array ids: [a, b, c, d, e, f]
```

### 객체리스트

전달하려는 데이터가 객체타입이고 여러개를 처리해야 한다면 약간의 작업을 통해 한 번에 처리할 수 있다.

SampleDTOList.class

```java
@Data
public class SampleDTOList {
    private List<SampleDTO> list;

    public SampleDTOList() {
        list = new ArrayList<>();
    }
}
```

SampleController.class

```java
@GetMapping("/ex02Bean")
    public String ex02Bean(SampleDTOList list) {
        log.info("list dto: " + list);
        return "ex02Bean";
    }
```

URL([]은 특수문자로 허용되지 않아 에러가 뜬다.그래서 %5B"인덱스번호 삽입"%5D 으로 진행한다.)

```html
http://localhost:8080/controller_war_exploded/sample/ex02Bean?list%5B0%5D.name=osk&list%5B0%5D.age=29
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - list dto: SampleDTOList(list=[SampleDTO(name=osk, age=29)])
```

### @InitBinder

파라미터의 수집을 다른 용어로는 binding(바인딩)이라고 한다.

변환이 가능한 데이터는 자동으로 변환되지만 경우에 따라서 파라미터를 변환해서 처리해야 하는 경우도 있다.

예를들어 2020-01-01과 같이 문자열로 전달된 데이터를 java.util.Date 타입으로 변환하는 작업이 있다.

스프링 Controller에서는 파라미터를 바인딩할때 자동으로 호출되는 @InitBinder를 이용해서 이러한 변환을 처리할 수 있다.

TodoDTO.class

```java
@Data
public class TodoDTO {
    private String title;
    private Date dueDate;
}
```

SampleController.class

```java
 @GetMapping("/ex03")
    public String ex03(TodoDTO todo) {
        log.info("todo: " + todo);
        return "ex03";
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex03?title=test&dueDate=2020-01-01
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - todo: TodoDTO(title=test, dueDate=Wed Jan 01 00:00:00 KST 2020)
```

반면에 @InitBinder 처리가 되지 않는다면 브라우저에서는 300에러가 발생하는 것을 볼 수 있다.

(400 에러는 요청 구문(syntax)이 잘못되었다는 의미이다.)

날짜가 정상적으로 처리되어도 아직 jsp 페이지는 없으므로 다음과 같이 출력된다.

![](/images/79/img_1.png)

### 

### @DateTimeFormat

@InitBinder를 이용해서 날짜를 변환할 수 있지만,파라미터로 사용되는 인스턴스 변수에 @DateTimeFormat을 적용해도

변환이 가능하다.

참고로 @DateTimeFormat을 이용하는 경우에는 @InitBinder는 필요하지 않다.)

TodoDTO.class

```java
@Data
public class TodoDTO {
    private String title;

    @DateTimeFormat(pattern = "yyyy/MM/dd")
    private Date dueDate;
}
```

SampleController.class

```java
@GetMapping("/ex03")
    public String ex03(TodoDTO todo) {
        log.info("todo: " + todo);
        return "ex03";
    }
```

URL

```java
http://localhost:8080/controller_war_exploded/sample/ex03?title=date&dueDate=2020/01/01
```

콘솔창

```java
INFO : com.osk2090.controller.SampleController - todo: TodoDTO(title=date, dueDate=Wed Jan 01 00:00:00 KST 2020)
```
{% endraw %}