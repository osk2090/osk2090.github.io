---
layout: default
title: "[Design Pattern]Singleton Pattern"
date: 2021-08-08 17:43:33 +0900
categories: [Design Pattern]
slug: post-102-design-patternsingleton-pattern
---

참조:<https://elfinlas.github.io/2019/09/23/java-singleton/>

[Java에서 싱글톤(Singleton) 패턴을 사용하는 이유와 주의할 점

Java에서 Singleton 패턴이란?Singleton(이하 싱글톤) 패턴은 자바에서 많이 사용한다.먼저 싱글톤이란 어떤 클래스가 최초 한번만 메모리를 할당하고(Static) 그 메모리에 객체를 만들어 사용하는 디자

elfinlas.github.io](https://elfinlas.github.io/2019/09/23/java-singleton/)

싱글톤 패턴은 자바에서 많이 사용한다.

먼저 싱글톤이란 어떤 클래스가 최최 한번만 메모리를 할당하고(static) 그 메모리에 객체를 만들어 사용하는 디자인 패턴을 말한다.

즉 생성자의 호출이 반복적으로 이루어져도 실제로 생성되는 객체는 최초 생성된 객체를 반환해주는 것이다.

```java
package com.company.design.singleton;

public class SocketClient {

    private static SocketClient socketClient = null;

    //default생성자를 막아준다.
    private SocketClient() {

    }

    //외부에서 new로 생성자를 만들 수 없게 만들어준다.
    public static SocketClient getInstance() {
        if (socketClient == null) {
            socketClient = new SocketClient();
        }
        return socketClient;
    }

    public void connect() {
        System.out.println("connect");
    }
}
```

코드를 보면 socketClient라는 전역 변수를 선언하는데

static을 줌으로써 인스턴스화 하지 않고 사용할 수 있게 하지만

접근제한자가 private로 되어 있어 직접적인 접근은 불가능하다.

또한 생성자도 private으로 되어 있어 new 를 통한 객체 생성도 불가능하다.

결국 getInstance 메서드를 통해서 해당 인스턴스를 얻을 수 있게 된다.

```java
public class AClazz {
    private SocketClient socketClient;

    public AClazz() {
        this.socketClient = SocketClient.getInstance();
    }

    public SocketClient getSocketClient() {
        return this.socketClient;
    }
}
```
```java
public class Main {

    public static void main(String[] args) {

        AClazz aClazz = new AClazz();
        BClazz bClazz = new BClazz();

        SocketClient aClient = aClazz.getSocketClient();
        SocketClient bClient = bClazz.getSocketClient();

        System.out.println("두개의 객체가 동일한가?");
        System.out.println(aClient.equals(bClient));

    }
}
```

### 

### 그렇다면 싱글톤 패턴을 사용하는 이유는?

위에서도 언급된 바와 같이 한번의 객체 생성으로 재사용이 가능하기 때문에 메모리 낭비를 방지할 수 있다.

또한 싱글톤으로 생성된 객체는 무조건 한번 생성으로 전역성을 띄기에 다른 객체와 공유가 용이하다.

하지만 문제점도 존재한다.

### 싱글톤의 문제점

싱글톤으로 만든 객체의 역할이 간단한 것이 아닌 역할이 복잡한 경우라면 해당 싱글톤 객체를 사용하는 다른 객체간의 결함도가 높아져서 객체 지향 설계 원칙에 어긋나게 된다(개방-폐쇄)

또한 해당 싱글톤 객체를 수정할 경우 싱글톤 객체를 사용하는 곳에서 사이드 이팩트 발생 확률이 생기게 되며

멀티쓰래드 환경에서 동기화 처리 문제등이 생기게 된다.

### 다양한 싱글톤의 구현

#### static block

```java
public class ExampleClass {
    //Instance
    private static ExampleClass instance;

    //private construct
    private ExampleClass() {}

    static {
        try { instance = new ExampleClass();}
        catch(Exception e) { throw new RuntimeException("Create instace fail. error msg = " + e.getMessage() ); }
    }

    public static ExampleClass getInstance() {
        return instance;
    }
}
```

위와 같이 static 블럭을 사용할 경우 클래스가 로딩될 때 한번만 실행을 하게 되는 특성을 사용한다.

하지만 인스턴스가 사용되는 시점이 아닌 클래스 로딩 시점에 실행이 된다.

#### lazy init

위 static 방법에서 개선하여 클래스 로딩 시점이 아닌 인스턴스가 필요하여 요청할 때 생성되는 형태로 작성하였다.

```java
public class ExampleClass {
    //Instance
    private static ExampleClass instance;

    //private construct
    private ExampleClass() {}

    public static ExampleClass getInstance() {
        if (instance == null) { instance = new ExampleClass();}
        return instance;
    }
}
```

하지만 위 형태로 구성할 경우 멀티 쓰레드 환경에서 취약한다.

특정 쓰레드가 동시에 getInstance() 메서드를 호출하게 되면 인스턴스가 두번 생성되는 문제가 발생한다.

#### Tread Safe + Lazy

```java
public class ExampleClass {
    //Instance
    private static ExampleClass instance;

    //private construct
    private ExampleClass() {}

    public static synchronized ExampleClass getInstance() {
        if (instance == null) { instance = new ExampleClass();}
        return instance;
    }
}
```

Lazy에서 보였던 getInstance() 메서드에 synchronized(동기화) 키워드를 붙임으로써 쓰레드에서 동시 접근에 대한 문제를 해결하였다.하지만 synchronized 키워드는 성능 저하를 발생시킨다.

#### Holder

```java
public class ExampleClass {

    //private construct
    private ExampleClass() {}

    private static class InnerInstanceClazz() {
        private static final ExampleClass instance = new ExampleClass();
    }

    public static ExampleClass getInstance() {
        return InnerInstanceClazz.instance;
    }
}
```

JVM의 클래스 로더 메커니즘과 클래스의 로드 시점을 이용하여 내부 클래스를 통해 생성 시킴으로써

쓰레드 간의 동기화 문제를 해결한다.

위 방법은 현재 java에서 싱글통 생성에서 사용하는 대표적인 방법이다.

### 마지막

싱글톤 패턴은 Spring framework에서도 많이 사용되며

어떤식으로 구현하는지 알아두면 도움이 된다.

자바와 Spring에서의 싱글톤 차이점이라면 싱글톤 객체의 생명주기가 다르다.

또한 자바에서 공유 범위는 Class loader 기준이지만 Spring에서는 ApplicatiinContext가 기준이 된다.