---
layout: default
title: "스프링 MVC Controller-3"
date: 2021-07-01 21:36:35 +0900
categories: [Spring]
slug: post-081-스프링-mvc-controller-3
render_with_liquid: false
image: /images/81/img.png
---

### Controller의 리턴 타입

스프링 MVC의 구조가 기존의 상속과 인터페이스에서 어노테이션을 사용하는 방식으로 변한 이후에

가장 큰 변환 중 하나는 리턴 타입이 자유로워 졌다는 점이다.

Controller의 메서드가 사용할 수 있는 리턴 타입은 주로 다음과 같다.

1. String:jsp를 이용하는 경우에는 jsp 파일의 경로와 파일이름을 나타내기 위해서 사용한다.
2. void:호출하는 URL과 동일한 이름의 jsp를 의미한다.
3. VO,DTO 타입:주로 JSON타입의 데이터를 만들어서 반환하는 용도로 사용한다.
4. ResponseEntity 타입:response 할 때 Http 헤더 정보와 내용을 가공하는 용도로 사용한다.
5. Model,ModelAndView:Model로 데이터를 반환하거나 화면까지 같이 지정하는 경우에 사용한다.(비추천)
6. HttpHeaders:응답에 내용 없이 http 헤더 메시지만 전달하는 용도로 사용한다.

### void 타입

메서드의 리턴 타입을 void로 지정하는 경우 일반적인 경우에는

해당 URL의 경로를 그대로 jsp 파일의 이름으로 사용하게 된다.

SampleController.class

```java
@GetMapping("/ex05")
    public void ex05() {
        log.info("/ex05................");
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex05
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - /ex05................
```

![](/images/81/img.png)

에러 메시지를 보면 에러 메시지의 원인이

"/WEB-INF/views/sample/ex05.jsp"가 존재하지 않아서 생기는 문제라는 것을 볼 수 있다.

이것은 ServletConfig.class의 아래 설정과 같이 맞물려 URL경로를 View로 처리하기 때문에 생기는 결과이다.

```java
@Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        InternalResourceViewResolver bean = new InternalResourceViewResolver();
        bean.setViewClass(JstlView.class);
        bean.setPrefix("/WEB-INF/views/");
        bean.setSuffix(".jsp");
        registry.viewResolver(bean);
    }
```

### String 타입

void 타입과 더불어서 가장 많이 사용하는 것은 String 타입이다.

String 타입은 상황에 따라 다른 화면을 보여줄 필요가 있을 경우에 유용하게 사용한다.

(if~else와 같은 처리가 필요한 상황)

일반적으로 String 타입은 현재 프로젝트의 경우 JSP 파일의 이름을 의미한다.

프로젝트 생성 시 기본으로 만들어진 HomeController의 코드를 보면 String을 반환 타입으로 사용하는 것을 볼 수 있다.

HomeController.class

```java
@RequestMapping(value = "/", method = RequestMethod.GET)
	public String home(Locale locale, Model model) {
		logger.info("Welcome home! The client locale is {}.", locale);
		
		Date date = new Date();
		DateFormat dateFormat = DateFormat.getDateTimeInstance(DateFormat.LONG, DateFormat.LONG, locale);
		
		String formattedDate = dateFormat.format(date);
		
		model.addAttribute("serverTime", formattedDate );
		
		return "home";
	}
```

home() 메서드는 "home"이라는 문자열을 리턴했기 때문에 경로는 "/WEB-INF/views/home.jsp"경로가 된다.

String 타입에는 다음과 같은 특별한 키워드를 붙여서 사용할 수 있다.

1. redirect:리다이렉트 방식으로 처리하는 경우
2. forward:포워드 방식으로 처리하는 경우

### 객체 타입

Controller의 메서드 리턴 타입을 VO(Value Object)나 DTO(Data Transfer Object)타입 등

복합적인 데이터가 들어각 객체 타입으로 지정할 수 있는데,

이 경우는 주로 JSON 데이터를 만들어 내는 용도로 사용한다.

pom.xml 추가

```html
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.9.4</version>
</dependency>
```

SampleController.class

```java
@GetMapping("/ex06")
    public @ResponseBody
    SampleDTO ex06() {
        log.info("ex06.....................");
        SampleDTO dto = new SampleDTO();
        dto.setAge(29);
        dto.setName("osk");
        return dto;
    }
```

URL

```html
http://localhost:8080/controller_war_exploded/sample/ex06
```

Browser

```java
{"name":"osk","age":29}
```

개발자 도구를 통해서 살펴보면 서버에서 전공하는 MINE 타입이 "application/json"으로 처리되는 것을 볼 수 있다.

만일 Jackson-databind 라이브러리가 포함되지 않았다면 에러가 뜬다.

스프링 MVC 리턴 타입에 맞게 데이터를 변환해주는 역할을 지정할 수 있는데 기본적으로 JSON은 처리가 되므로

별도의 설정이 필요하지 않는다.

### ResponseEntity 타입

Web을 다루다 보면 HTTP 프로트콜의 헤더를 다루는 경우도 종종 있다.

스프링 MVC의 사상은 HttpServletRequest나 HttpServlerResponse를 직접 핸들링하지 않아도

이런 작업이 가능하도록 작성되었기 때문에 이러한 처리를 위해 ResponseEntity를 통해서

원하는 헤더 정보나 데이터를 전달할 수 있다.

SampeController.class

```java
@GetMapping("/ex07")
    public ResponseEntity<String> ex07() {
        log.info("/ex07............");
        String msg = "{\"name\":\"osk\"}";
        HttpHeaders header = new HttpHeaders();
        header.add("Content-Type", "application/json;charset=UTF-8");
        return new ResponseEntity<>(msg, header, HttpStatus.OK);
    }
```

ResponseEntity는 HttpHeaders 객체를 같이 전달할 수 있고,

이를 통해서 원하는 HTTP 헤더 메시지를 가공하는 것이 가능하다.

ex07()의 경우 브라우저에는 JSON타입이라는 헤더 메시지와 200OK라는 상태 코드를 전송한다.

![](/images/81/img_1.png)

### 파일 업로드 처리

Controller의 많은 작업은 스프링 MVC를 통해서 처리하기 때문에 개발자는

자신이 해야 하는 역할에만 집중해서 코드를 작성 할 수 있지만,

조금 신경써야 하는 부분이 있다면 파일을 업로드하는 부분에 대한 처리일 것이다.

파일 업로드를 하기 위해서는 전달되는 파일 데이터를 분석해야 하는데,

이를 위해서 Servlet 3.0 전까지는 commons의 파일 업로드를 이용하거나 cos.jar 등을 이용해서 처리를 해왔다.

여기서는 commons-fileupload를 이용하도록 하겠다.

pom.xml

```java
<dependency>
    <groupId>commons-fileupload</groupId>
    <artifactId>commons-fileupload</artifactId>
    <version>1.3.3</version>
</dependency>
```

그리고 필자는 E:\git\upload/tmp 경로로 폴더를 만들어 줬다.

servlet-context,xml 설정

servlet-context.xml은 스프링 MVC의 특정한 객체(빈)를 설정해서 파일을 처리한다.

다른 객체(Bean)를 설정하는 것과 달리 파일 업로드의 경우에는

반드시 id 속성의 값을 "multipartResolver"로 정확하게 지정해야 하므로 주의가 필요하다.

ServletConfig.class

```html
@Bean(name = "multipartResolver")
    public CommonsMultipartResolver getResolver()throws Exception {
        CommonsMultipartResolver resolver = new CommonsMultipartResolver();
        //10MB
        resolver.setMaxUploadSize(1024 * 1024 * 10);
        //2MB
        resolver.setMaxUploadSizePerFile(1024 * 1024 * 2);
        //1MB
        resolver.setMaxInMemorySize(1024 * 1024);

        //저장위치
        resolver.setUploadTempDir(new FileSystemResource("E:\\git\\upload\\tmp"));
        resolver.setDefaultEncoding("UTF-8");
        return resolver;
    }
```

maxUploadSize는 한 번의 Request로 전달될 수 있는 최대의 크래를 위미하고

maxUploadSizePerFile은 하나의 파일 최대 크기,maxInMemorySize는 메모리상에서 유지하는 최대의 크기를 의미한다.

만일 이 크기 이상의 데이터는 uploadTempfir에 임시 파일의 형태로 보관한다.

uploadTempDir에서 절대 경로를 이용하려면 URI 형태로 제공해야 하기 때문에 "file:/"로 시작하도록 한다.

defaultEncoding은 업로드하는 파일의 이름이 한글일 경우 깨지는 문제를 처리한다.

SampleController.class

```java
@GetMapping("/exUpload")
    public void exUpload() {
        log.info("/exUpload.............");
    }

    @PostMapping("/exUploadPost")
    public void exUploadPost(ArrayList<MultipartFile> files) {
        files.forEach(file->{
            log.info("-------------------------------------");
            log.info("name" + file.getOriginalFilename());
            log.info("size" + file.getSize());
        });
    }
```

exUpload.jsp

```java
<form action="exUploadPost" method="post" enctype="multipart/form-data">
    <div><input type="file" name="files"></div>
    <div><input type="file" name="files"></div>
    <div><input type="file" name="files"></div>
    <div><input type="file" name="files"></div>
    <div><input type="file" name="files"></div>
    <div><input type="submit"></div>
</form>
```

콘솔창

```html
INFO : com.osk2090.controller.SampleController - /exUpload.............
INFO : com.osk2090.controller.SampleController - -------------------------------------
INFO : com.osk2090.controller.SampleController - name다운로드.jpg
INFO : com.osk2090.controller.SampleController - size881
INFO : com.osk2090.controller.SampleController - -------------------------------------
INFO : com.osk2090.controller.SampleController - name꼬깔콘.jpg
INFO : com.osk2090.controller.SampleController - size32152
INFO : com.osk2090.controller.SampleController - -------------------------------------
INFO : com.osk2090.controller.SampleController - name버질.jpg
INFO : com.osk2090.controller.SampleController - size57865
INFO : com.osk2090.controller.SampleController - -------------------------------------
INFO : com.osk2090.controller.SampleController - name이지.jpg
INFO : com.osk2090.controller.SampleController - size76491
INFO : com.osk2090.controller.SampleController - -------------------------------------
INFO : com.osk2090.controller.SampleController - namex.jpg
INFO : com.osk2090.controller.SampleController - size24777
```

위의 콘솔창 로그를 보면 업로드 정보가 올바르게 처리되는 것을 보여주고 있다.

최종 업로드를 하려면 byte[]를 처리해야 하는데 이 예제는 아직 처리하지 않고 있다.