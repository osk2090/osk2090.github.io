---
layout: default
title: "Java-Spring 면접준비"
date: 2022-12-08 17:29:29 +0900
categories: [Spring]
slug: post-133-java-spring-면접준비
---

#### JVM

자바 가상 머신은 자바 프로그램 실행환경을 만들어 주는 소프트웨어이다.

자바 코드를 컴파일하여 .class 바이트 코드로 만들면 이 코드가 자바 가상 머신환경에서 실행된다.

JVM은 자바 실행 환경 JRE에 포함되어 있다.

자바의 경우에는 JVM이 운영체제에 맞는 실행 파일로 바꿔주기 때문에 플랫폼에 맞게끔 컴파일을 따로 해줘야 할 필요가 없다.

#### 제네릭

제네릭 타입을 사용함으로써 잘못된 타입이 사용될 수 있는 문제를 컴파일 과정에서 제거할 수 있기 때문이다.

자바 컴파일러는 코드에서 잘못 사용된 타입 때문에 발생하는 문제점을 제거하기 위해 제네릭 코드에 대해 강한 타입 체크를 한다.

실행시 타입 에러가 나는것보다는 컴파일 시에 미리 타입을 강하게 체크해서 에러를 사전에 방지하는 것이 좋다. 또 제네릭 코드를 사용하면 타입을 국한하기 때문에 요소를 찾아올 때 타입 변환을 할 필요가 없어 프로그램 성능이 향상되는 효과를 얻을 수 있다.

#### final keyword

- 클래스: 다른 클래스에서 상속하지 못한다.
- 메서드: 다른 메서드에서 오버라이딩하지 못한다.
- 상수: 변하지 않는 상수값이 되어 새로 할당할 수 없는 변수가 된다.

#### finally

try-catch 구문을 사용할 때 정상적으로 작업 처리하거나 에러가 발생했을 경우 반드시 마무리 작업을 해줘야하는 경우 해당 블록에 작업을 추가한다.

#### Overriding VS Overloading

- 오버라이딩: 상속받은 기존의 메서드를 재정의
- 오버로딩: 새로운 메서드를 정의

```bash
public class Parent {
    public void display() {
        System.out.println("부모 클래스의 display() 매소드");
    }
}

public class Child extends Parent {
    public void display() {
        System.out.println("자식 클래스의 display() 메소드");
    }

    public void display(String str) {
        System.out.println(str);
    }
}

public class Main {
    public static void main(String[] args) {
        Child c = new Child();
        c.display();//자식 클래스의 display() 메소드
        c.display("오버로딩된 메서드");//오버로딩된 메서드
    }
}
```

#### Spring 주요설명

IOC(aka. Inversion Of Control): 제어의 역전이라고 부른다. 한마디로 프레임워크의 라이프사이클을 관리한다.

기존에 자바 기반으로 어플리케이션을 개발할 때 자바 객체를 생성하고 서로간의 의존 관계를 연결시키는 작업에 대한 제어권은 보통 개발되는 어플리케이션에 있었는데 IOC컨테이너는 객체의 생성,초기화,서비스 소멸에 관한 모든 권한을 가지면서 객체의 생명주기를 관리한다.

이것을 제어권을 역전되었다해서 IOC 라고 부른다.

AOP(aka. Aspect Oriented Programming): 관점지향프로그램이라 칭한다.

개발을 하다보면 반복되는 작업들이 있다. 이것들의 공통 작업되는 것들을 모아서 필요한 적절한 시기에 적용하는 개념이다.

따로 해당 코드 밖에서 개발을 해두고 프록시 개념으로 메서드가 실행되기전,실행된 직후, 실행시점에 따라 따로 기능을 적용시키는 것을 말한다.

DI(aka. Dependency Injection): 의존성 주입, 객체 자체가 아니라 Framework에 의해 객체의 의존성을 주입되는 설계 패턴인데 IOC와 연결되는 개념이다.

IOC의 제어권이 프레임워크에게 가게 되는것은 IOC 컨테이너는 DI를 통해 주입시키는데 주입하는 방법은 생성자,메소드의 setter,멤버변수에 @Inject,@Autowired를 통해 주입한다.

#### JPA

일반적으로는 어플리케이션 class와 RDB의 테이블을 매핑(연결)한다는 의미이며 큰 특징으로는 개발자가 직접 SQL을 작성하지 않아도 된다는 점이다. 기술적으로는 객체를 RDB 테이블에 자동으로 영속화 해주는데 여기서 영속화는 DB에 저장하여 영원한다는 의미이다.