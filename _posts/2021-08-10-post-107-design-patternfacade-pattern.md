---
layout: default
title: "[Design Pattern]Facade Pattern"
date: 2021-08-10 09:07:05 +0900
categories: [Design Pattern]
slug: post-107-design-patternfacade-pattern
image: /images/107/img.png
---

### 파사드패턴이란?

건물의 정면을 의미하는 단어로 어떤 소프트웨어의 다른 커다란 코드 부분에 대하여 간략화된 인터페이스를 제공해주는 디자인 패턴을 의미한다.

파사드 객체는 복잡한 소프트웨어 바깥쪽의 코드가 라이브러리의 안쪽 코드에 의존하는 일을 감소시켜 주고

복잡한 소프트웨어를 사용할 수 있게 간단한 인터페이스를 제공해준다.

쉽게 단계를 설명하자면

음료를 준비한다->티비를 킨다->영화를 검색한다->영화를 결제한다->영화를 재생한다

사용자 입장에서는 영화를 보기 위해서는 복잡한 코드를 사용하여 영화를 봐야만 한다.

여기서 퍼사드 객체가 등장하게 되는데 퍼사드는 이런 사용자와 영화를 보기위해 사용하는 서브 클래스들 사이의 간단한 통합 인터페이스를 제공해주는 역할을 하게 된다.

![](/images/107/img.png)

Client 입장에서는 Facade 객체에서 제공하는 doSomething() 메서드를 호출함으로써 복잡한 서브 클래스의 사용을 도와주고 있다.

### 예제

```java
public class Remote_Control {
    
    public void Turn_On() {
        System.out.println("TV를 켜다");
    }

    public void Turn_Off() {
        System.out.println("TV를 끄다");
    }
}
```

리모컨을 조작하는 클래스이다.복잡한 서브 클래스들 중 하나이다.

```java
public class Movie {
    private String name = "";

    public Movie(String name) {
        this.name = name;
    }

    public void Search_Movie() {
        System.out.println(name + " 영화를 찾다");
    }

    public void Charge_Movie() {
        System.out.println("영화를 결제하다");
    }

    public void play_Movie() {
        System.out.println("영화 재생");
    }
}
```

영화 재생과 관련된 클래스이다.마찬가지로 복잡한 서브 클래스들 중 하나이다.

```java
public class Beverage {
    private String name = "";

    public Beverage(String name) {
        this.name = name;
    }

    public void Prepare() {
        System.out.println(name + " 음료 준비 완료 ");
    }
}
```

음료를 제공하는 클래스이다.복잡한 서브 클래스들 중 하나이다.

```java
public class Facade {
    private String Beverage_Name = "";
    private String Movie_Name = "";

    public Facade(String beverage_Name, String movie_Name) {
        Beverage_Name = beverage_Name;
        Movie_Name = movie_Name;
    }

    public void view_Movie() {
        Beverage beverage = new Beverage(Beverage_Name);
        Remote_Control remote = new Remote_Control();
        Movie movie = new Movie(Movie_Name);

        beverage.Prepare();
        remote.Turn_On();
        movie.Search_Movie();
        movie.Charge_Movie();
        movie.play_Movie();
    }
}
```

여기서 가장 중요한 Facade 클래스이다.복잡한 서브 클래스들에 대한 인스턴스를 가지며 복잡한 호출 방식에 대하여 view\_Movie() 메서드 내에서 구현하도록 하였다.

```java
public class Viewer {
    public Viewer() {
        Facade facade = new Facade("콜라", "어벤져스");
        facade.view_Movie();
    }
}
```

사용자 입장에서는 이제 서브 클래스에 대해서 알 필요가 없다

단지 Facade 객체의 view\_Movie() 메서드를 호출하면서 서브 클래스들의 복잡한 기능을 수행할 수 있기 때문이다.