---
layout: default
title: "REST 방식과 Ajax를 이용하는 댓글 처리"
date: 2021-07-31 15:14:04 +0900
categories: [Etc]
slug: post-095-rest-방식과-ajax를-이용하는-댓글-처리
image: /images/95/img.png
---

REST는 Representational State Transfer의 약어로 하나의 URI는 하나의 고유한 리소르를 대표하도록 설계된다는 개념에 전송방식을 결합해서 원하는 작업을 지정한다.예를 들어 /boards/123은 게시물 중에서 123번이라는 고유한 의미를 가지도록 설계하고 이에 대한 처리는 GET,POST 방식과 같이 추가적인 정보를 통해서 결정한다.따라서 REST 방식은 다음과 같이 구성된다고 생각할 수 있다.

![](/images/95/img.png)

스프링은 @ReqeustMapping이나 @ResponseBody와 같이 REST 방식의 데이터 처리를 위한 여러 종류의 어노테이션과 기능이 있다.REST와 관련해서 알아 두어야 하는 어노테이션들은 다음과 같다.

|  |  |
| --- | --- |
| 어노테이션` | 기능 |
| @RestController | Controller가 REST 방식을 처리하기 위한 것임을 명시 |
| @ResponseBody | 일반적인 JSP와 같은 뷰로 전달되는 게 아니라 데이터 자체를 전달하기 위한 용도 |
| @PathVariable | URL 경로에 있는 값을 파라미터로 추출하려고 할 때 사용 |
| @CrossOrigin | Ajax의 크로스 도메인 문제를 해결해주는 어노테이션 |
| @RequestBody | JSON 데이터를 원하는 타입으로 바인딩 처리 |

### @RestController

REST 방식에서 가장 먼저 기억해야 하는 점은 서버에서 전송하는 것이 순수한 데이터라는 점이다.

기존의 Controller에서 Model에 데이터를 담아서 JSP 등과 같은 뷰로 전달하는 방식이 아니므로 기존의 Controller와는 조금 다르게 동작한다.

스프링4에서부터는 @Controller외에 @RestController라는 어노테이션을 추가해서 해당 Controller의 모든 메서드의 리턴 타입을 기존과 다르게 처리한다는 것을 명시한다.@RestController 이전에는 @Controller와 메서드 선언부에 @ResponseBody를 이용해서 동일한 결과를 만들 수 있다.@RestController는 메서드의 리턴 타입으로 사용자가 정의한 클래스 타입을 사용할 수 있고 이를 JSON이나 XML로 자동으로 처리할 수 있다.

#### 프로젝트 준비

Spring Legavy Project를 이용해서 ex03 프로젝트를 생성한다.

생성하는 프로젝트의 기본 패키지는 com.osk2090.controller를 지정한다.

pom.xml의 스프링 버전은 5.0.7버전으로 수정한다.

이전 예제와 같이 Java 버전이나 Maven Compile 버전 등은 1.8버전으로 수정하고 프로젝트를 업데이트 한다.

```java
<properties>
		<java-version>11</java-version>
		<org.springframework-version>5.0.7.RELEASE</org.springframework-version>
		<org.aspectj-version>1.6.10</org.aspectj-version>
		<org.slf4j-version>1.6.6</org.slf4j-version>
	</properties>
    ...
    
<plugins>
            <plugin>
                <artifactId>maven-eclipse-plugin</artifactId>
                <version>2.9</version>
                <configuration>
                    <additionalProjectnatures>
                        <projectnature>org.springframework.ide.eclipse.core.springnature</projectnature>
                    </additionalProjectnatures>
                    <additionalBuildcommands>
                        <buildcommand>org.springframework.ide.eclipse.core.springbuilder</buildcommand>
                    </additionalBuildcommands>
                    <downloadSources>true</downloadSources>
                    <downloadJavadocs>true</downloadJavadocs>
                </configuration>
            </plugin>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>2.5.1</version>
                <configuration>
                    <source>11</source>
                    <target>11</target>
                    <compilerArgument>-Xlint:all</compilerArgument>
                    <showWarnings>true</showWarnings>
                    <showDeprecation>true</showDeprecation>
                </configuration>
            </plugin>
```

작성된 프로젝트에는 우선적으로 JSON 데이터를 처리하기 위한 jackson-databind라는 라이브러리를 pom.xml에 추가한다.jackson-databind 라이브러리는 나중에 브라우저에 객체를 JSON이라는 포멧의 문자열로 변환시켜 전송할 때 필요하다.

---

JSON은 JavaScript Object Notation의 약어로 구조가 있는 데이터를 {}로 묶고 키와 같으로 구성하는 경량의 데이터 포맷이다.프로그래밍 언에서 말하는 개체들의 구조는 {}를 이용해서 다음과 같이 표현할 수 있다.

```java
 {
    "이름": "홍길동",
    "나이": 25,
    "성별": "여",
    "주소": "서울특별시 양천구 목동",
    "특기": ["농구", "도술"],
    "가족관계": {"#": 2, "아버지": "홍판서", "어머니": "춘섬"},
    "회사": "경기 수원시 팔달구 우만동"
 }
```

구조를 표현한 문자열은 프로그래밍 언어에 관계없이 사용할 수 있기 때문에 XML과 더불어 가장 많이 사용되는 데이터의 표현 방식이다.

---

브라우저를 이용해서 Maven jackson-databind 등을 검색하면 메이븐 관련 저장소를 찾을 수 있다.

XML의 처리는 jackson-databind-xml 라이브러리를 이용한다.

```java
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.13.0-rc1</version>
</dependency>

<dependency>
    <groupId>com.fasterxml.jackson.dataformat</groupId>
    <artifactId>jackson-dataformat-xml</artifactId>
    <version>2.13.0-rc1</version>
</dependency>
```

테스트할 때는 직접 Java 인스턴스를 JSON 타입의 문자열로 변환해야 하는 일들도 있으므로 gson 라이브러리도 추가한다.

pom.xml

```java
<dependency>
  <groupId>com.google.code.gson</groupId>
  <artifactId>gson</artifactId>
  <version>2.8.7</version>
</dependency>
```

작성된 프로젝트의 서블릿 버전을 수정하고 Lombok 관련 설정을 추가한다.

```java
<dependency>
  <groupId>javax.servlet</groupId>
  <artifactId>javax.servlet-api</artifactId>
  <version>3.1.0</version>
  <scope>provided</scope>
</dependency>
....
<dependency>
  <groupId>org.projectlombok</groupId>
  <artifactId>lombok</artifactId>
  <version>1.18.20</version>
</dependency>
```

테스트를 위해서 JUnit 버전을 변경하고 spring-test 관련 모듈을 추가한다.

```java
<!-- Test -->
<dependency>
    <groupId>junit</groupId>
    <artifactId>junit</artifactId>
    <version>4.7</version>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-test</artifactId>
    <version>${org.springframework-version}</version>
</dependency>
```

### @RestController의 반환 타입

스프링의 @RestController는 특별히 기존의 @Controller와 다른 점은 없다.

com.osk2090.controller 패키지에 SampleController를 생성한다.

SampleController.class

```java
package com.osk2090.controller;

import lombok.extern.log4j.Log4j;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/sample")
@Log4j
public class SampleController {

}
```

#### 단순 문자열 반환

@RestController는 JSP와 달리 순수한 데이터를 반환하는 형태이므로 다양한 포맷의 데이터를 전송할 수 있다.

주로 많이 사용하는 형태는 일반 문자열이나 JSON,XML 등을 사용한다.

SampleController에 문자열을 반환하려면 다음과 같은 형태로 작성한다.

SampleController.class

```java
package com.osk2090.controller;

import lombok.extern.log4j.Log4j;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/sample")
@Log4j
public class SampleController {

    @GetMapping(value = "/getText", produces = "text/plain; charset=UTF-8")
    public String getText() {
        log.info("MIME TYPE: " + MediaType.TEXT_PLAIN_VALUE);
        return "안녕하세요";
    }
}
```

기존의 @Controller는 문자열을 반환하는 경우에는 JSP 파일의 이름으로 처리하지만

@RestController의 경우에는 순수한 데이터가 된다.@GetMapping에 사용된 produces 속성은 해당 메서드가 생산하는 MIME 타입을 의미한다.예제와 같이 문자열로 직접 지정할 수도 있고 메서드 내의 MediaType이라는 클래슬 이용할 수도 있다.

![](/images/95/img_1.png)

프로젝트의 실행은 이전 예제들과 같이 /경로로 실행되도록 하고 브라우저를 통해서 /sample/getText 를 호출한다.

브라우저에 전송된 실제 데이터는 브라우저의 개발자 도구를 이용해서 확인할 수 있다.

![](/images/95/img_2.png)

결과를 보면 produces의 속성값으로 지정된 text/plain 결과가 나오는 것을 확인할 수 있다.

#### 객체의 반환

객체를 반환하는 작업은 JSON이나 XML을 이용한다.전달된 객체를 생성하기 위해서 com.osk2090.domain 패키지를 생성하고 SampleVO 클래스를 작성한다.

SampleVO.class

```java
package com.osk2090.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SampleVO {
    private Integer mno;
    private String firstName;
    private String lastName;
}
```

SampleVO 클래스는 비어 있는 생성자를 만들기 위한 @MoArgsConstructor와 모든 속성을 사용하는 생성자를 위한 @AllArgsConsructor 어노테이션을 이용한다.어노테이션을 통해서 생성된 결과를 보면 생성자가 여러 개 생성되는 것을 볼 수 있다.

![](/images/95/img_3.png)

SampleController에서는SampleVO를 리턴하는 메서드를 아래와 같이 설계한다.

SampleVO.class

```java
@GetMapping(value = "/getSample",
produces = {MediaType.APPLICATION_JSON_UTF8_VALUE,
MediaType.APPLICATION_XML_VALUE})
public SampleVO getSample() {
	return new SampleVO(112, "스타", "로또");
}
```

getSample()은 XML과 JSON 방식의 데이터를 생성할 수 있도록 작성되었는데

브라우저에서 /sample/getSample.json 을 호출하면 JSON 타입의 데이터가 전달되는 것을 확인할 수 있다.

![](/images/95/img_4.png)

@GetMapping이나 @RequestMapping의 produces 속성은 반드시 지정해야 하는 것은 아니므로 생략하는 것도 가능하다.

SampleController.class

```java
@GetMapping(value = "/getSample2")
public SampleVO getSample2() {
	return new SampleVO(113, "로켓", "라쿤");
}
```

#### 컬렉션 타입의 객체 반환

경우에 따라서는 여러 데이터를 한 번에 전송하기 위해서 배열이나 리스트,맵 타입의 객체들을 전송하는 경우도 발생한다.

SampleController.class

```java
@GetMapping(value = "/getList")
public List<SampleVO> getList() {
    return IntStream.range(1,10).mapToObj(i->new SampleVO(i,i+"First",i+"Last")).
    collect(Collectors.toList());
}
```

getList()는 내부적으로 1부터 10미만까지의 루프를 처리하면서 SampleVO 객체를 만들어서 List<SampleVO>를 만들어 낸다.

브라우저를 통해서 /sample/getList 를 호출하면 기본적으로는 XML 데이터를 전송하는 것을 볼 수 있다.

뒤에 확장자를 .json으로 처리하면 []로 싸여진 JSON 형태의 배열 데이터를 볼 수 있다.

![](/images/95/img_5.png)

맵의 경우에는 키 와 값을 가지는 하나의 객체로 간주된다.

SampleController.class

```java
  @GetMapping(value = "/getMap")
  public Map<String, SampleVO> getMap() {
      Map<String, SampleVO> map = new HashMap<>();
      map.put("First", new SampleVO(111, "그루트", "주니어"));
      return map;
  }
```

브라우저에서 /sample/getMap을 호출하면 아래와 같은 결과를 확인할 수 있다.

![](/images/95/img_6.png)

Map을 이용하는 경우에는 키가 속하는 데이터는 XML로 변환되는 경우에 태그의 이름이 되기 때문에 문자열을 지정한다.

#### ResponseEntity 타입

REST 방식으로 호출되는 경우는 화면 자체가 아니라 데이터 자체를 전송하는 방식으로 처리되기 때문에 데이터를 요청한 쪽에서는 정상적인 데이터인지 비정상적인 데이터인지를 구분할 수 있는 확실한 방법을 제공해야만 한다.

ResponseEntity는 데이터와 함께 HTTP 헤더의 상태 메시지 등을 같이 전달하는 용도로 사용한다.

HTTP의 상태 코드와 에러 메시지 등을 함께 데이터를 전달할 수 있기 때문에 받는 입장에서는 확실하게 결과를 알 수 있다.

SampleController.class

```java
@GetMapping(value = "/check", params = {"height", "weight"})
public ResponseEntity<SampleVO> check(Double height, Double weight) {
    SampleVO vo = new SampleVO(0, "" + height, "" + weight);
    ResponseEntity<SampleVO> result = null;
    if (height < 150) {
    	result = ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(vo);
    } else {
    	result = ResponseEntity.status(HttpStatus.OK).body(vo);
    }
    return result;
}
```

check()은 반드시 height와 weight를 파라미터로 전달받는다.이때 만일 height 값이 150보다 작다면 502(bad gateway) 상태 코드와 데이터를 전송하고 그렇지 않다면 200(ok) 코드와 데이터를 전송한다.

/sample/check.json?height=140&weight=60 과 같이 JSON 타입의 데이터를 요구하고

height 값을 150보다 작게 하는 경우에는 502메시지와 데이터가 전달된다.

![](/images/95/img_7.png)

![](/images/95/img_8.png)

502 에러

### 

### @RestController에서 파라미터

@RestController는 기존의 @Controller에서 사용하던 일반적인 타입이나 사용자가 정의한 타입(클래스)을 사용한다.

여기에 추가로 몇 가지 어노테이션을 이용하는 경우가 있다.

- PathVariable:일반 컨트롤러에서도 사용이 가능하지만 REST 방식에서 자주 사용한다.URL 경로의 일부를 파라미터로 사용할 때 이용
- RequestBody:JSON데이터를 원하는 타입의 객체로 변환해야 하는 경우에 주로 사용

#### PathVariable

REST 방식에서는 URL 내에 최대한 많은 정보를 담으려고 노력한다.

예전에는 ? 뒤에 추가되는 쿼리 스트링(query string)이라는 형태로 파라미터를 이용해서 전달되던 데이터들이

REST방식에서는 경로의 일부로 차용되는 경우가 많다.

스프링 MVC에서는 @PathVariable 어노테이션을 이용해서 URL 상에 경로의 일부를 파라미터로 사용할 수 있다.

|  |
| --- |
| http://localhost:8080/sample/{sno} |
| http://localhost:8080/sample/{sno}/page/{pno} |

위의 URL에서 {}로 처리된 부분은 컨트롤러의 메서드에서 변수로 처리가 가능하다.

@Pathvariable은 {}의 이름을 처리할 때 사용한다.

REST 방식에서는 URL 자체에 데이터를 식별할 수 있는 정보들을 표현하는 경우가 많으므로 다양한 방식으로 @PathVariable이 사용된다.

SampleController.class

```java
@GetMapping("/product/{cat}/{pid}")
public String[] getPath(
@PathVariable("cat") String cat,
@PathVariable("pid") Integer pid
) {
	return new String[]{"category: " + cat, "productid: " + pid};
}
```

@PathVariable을 적용하고 싶은 경우에는 {}를 이용해서 변수명을 지정하고

@PathVariable을 이용해서 지정된 이름의 변숫값을 얻을 수 있다.값을 얻을 때에는 int,double과 같은 기본 자료형은 사용할 수 없다.

브라우저에서 /sample/product/bags/1234 로 호출하면 cat과 pid 변수의 값으로 처리되는 것을 확인할 수 있다.

#### @RequestBody

@RequestBody는 전달된 요청(request)의 내용(body)을 이용해서 해당 파라미터의 타입으로 변환을 요구한다.

내부적으로 HttpMessageConverter 타입의 객체들을 이용해서 다양한 포맷의 입력 데이터를 변환할 수 있다.

대부분의 경우에는 JSON 데이터를 서버에 보내서 원하는 타입의 객체로 변환하는 용도로 사용되지만

경우에 따라서는 원하는 포맷의 데이터를 보내고 이를 해석해서 원하는 타입으로 사용하기도 한다.

변환을 위한 예제를 위해서 com.osk2090.domain 패키지에 Ticket 클래슬 정의한다.

Ticket.class

```java
package com.osk2090.domain;

import lombok.Data;

@Data
public class Ticket {
    private int tno;
    private String owner;
    private String grade;

}
```

Ticket 클래스는 번호(tno)와 소유주(owner),등급(grade)을 지정한다.

Ticket을 사용하는 예제는 SampleController에 추가한다.

SampleController.class

```java
@PostMapping("/ticket")
public Ticket convert(@RequestBody Ticket ticket) {
    log.info("convert........ticekt" + ticket);
    return ticket;
}
```

SampleController의 다른 메서드와 달리 @PostMapping이 적용된 것을 볼 수 있는데

이것은 @RequestBody가 말 그대로 요청(request)한 내용(body)을 처리하기 때문에 일반적인 파라미터 전달방식을 사용할 수 없기 때문이다.(테스트는 추후 진행)

### REST 방식의 테스트

위와 같이 GET 방식이 아니고 POST 등의 방식으로 지정되어 있으면서 JSON 형태의 데이터를 처리하는 것을 브라우저에서 개발하려면 많은 시간과 노력이 들어간다.

@RestController를 쉽게 테스트할 수 있는 방법은 주로 REST 방식의 데이터를 전송하는 툴을 이용하거나

JUnit과 spring-text 를 이용해서 테스트하는 방식을 고려할 수 있다.

#### JUnit 기반의 테스트

src/test/java 폴더 아래 SampleControllerTests 추가한다.

SampleControllerTests.class

```java
package com.osk2090.controller;

import com.google.gson.Gson;
import com.osk2090.domain.Ticket;
import lombok.Setter;
import lombok.extern.log4j.Log4j;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;

@RunWith(SpringJUnit4ClassRunner.class)
@WebAppConfiguration
@ContextConfiguration({"file:src/main/webapp/WEB-INF/spring/root-context.xml",
        "file:src/main/webapp/WEB-INF/spring/appServlet/servlet-context.xml"})
@Log4j
public class SampleControllerTests {

    @Setter(onMethod_ = {@Autowired})
    private WebApplicationContext ctx;

    private MockMvc mockMvc;

    @Before
    public void setup() {
        this.mockMvc = MockMvcBuilders.webAppContextSetup(ctx).build();
    }

    @Test
    public void testConvert()throws Exception {
        Ticket ticket = new Ticket();
        ticket.setTno(123);
        ticket.setOwner("Admin");
        ticket.setGrade("AAA");

        String jsonStr = new Gson().toJson(ticket);

        log.info(jsonStr);

        mockMvc.perform(post("../sample/ticket")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonStr))
                .andExpect(status().is(200));
    }

}
```

testConvert()는 SampleController에 작성해 둔 convert() 메서드를 테스트하기 위해서 작성했다.

SampleController의 convert()는 JSON으로 전달되는 데이터를 받아서 Ticket 타입으로 변환한다.

이를 위해서는 해당 데이터가 JSON이라는 것을 명시해 줄 필요가 있다.

MockMvc는 contentType()을 이용해서 전달하는 데이터가 무엇인지를 알려줄 수 있다.

코드 내의 Gson 라이브러리는 Java의 객체를 JSON 문자열로 변환하기 위해서 사용한다.

위의 코드를 실행하면 다음과 같이 전달되는 JSON 문자열이 Ticket 타입의 객체를 변환된 것을 볼 수 있다.

```java
INFO : org.springframework.test.web.servlet.TestDispatcherServlet - FrameworkServlet '': initialization completed in 11 ms
INFO : com.osk2090.controller.SampleControllerTests - {"tno":123,"owner":"Admin","grade":"AAA"}
```

JUnit을 이용하는 방식의 테스트 장점은 역시 Tomcat을 구동하지 않고도 컨트롤러를 구동해 볼 수 있다는 점이다.

#### 기타도구

JUnit을 이용하는 방식 외에도 Tomcat을 구동한다면 REST 방식을 테스트할 수 있는 여러 가지 도구들이 존재한다.

만일 Mac이나 리눅스 등을 이용한다면 간단히 curl 같은 도구를 이용할 수도 있고

Java나 각종 언어로 개발된 라이브러리들을 사용할 수 있다.

브라우저에서 직접 REST 방식을 테스트할 수 있는데 크롬에서 REST client로 검색해서 사용할 수 있다.

여러 확장 프로그램 중에서 yet another rest client 등을 이용해서 테스트를 진행한다.

![](/images/95/img_9.png)

Tomcat을 실행하였다면 Restlet Client 에서는 GET/POST/... 등의 방식으로 접근이 가능하다.

요청의 내용(body) 역시 오른쪽의 화면처럼 원하는 내용을 전달할 수 있다.

### 다양한 전송방식

REST 방식의 데이터 교환에서 가장 특이한 점은 기존의 GET/POST 외에 다양한 방식으로 데이터를 전달한다는 점이다.

HTTP의 전송방식은 아래와 같은 형태로 사용된다.

|  |  |
| --- | --- |
| 작업 | 전송방식 |
| Create | POST |
| Read | GET |
| Update | PUT |
| Delete | DELETE |

REST방식은 URI와 같이 결합하므로 회원(member)이라는 자원을 대상으로 전송방식을 결합하면 다음과 같은 형태가 된다.

|  |  |  |
| --- | --- | --- |
| 작업 | 전송방식 | URI |
| 등록 | POST | /members/new |
| 조회 | GET | /members/{id} |
| 수정 | PUT | /members/{id}+body(json 데이터) |
| 삭제 | DELETE | /members/{id} |

POST 방식도 그렇지만 PUT,DELETE 방식은 브라우저에서 테스트하기가 쉽지 않기 때문에 개발 시 JUnit이나 Restlst Client 등과 같은 도구를 이용해서 테스트하고 개발해야만 한다.