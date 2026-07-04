---
layout: default
title: "[Design Pattern]Adapter Pattern"
date: 2021-08-08 20:17:09 +0900
categories: [Design Pattern]
slug: post-103-design-patternadapter-pattern
image: /images/103/img.gif
---
{% raw %}

참조:<https://lee1535.tistory.com/72?category=819409>

[Lee's Grow Up

lee1535.tistory.com](https://lee1535.tistory.com/72?category=819409)

### 어뎁터 패턴이란?

한 클래스의 인터페이스를 사용하고자 하는 다른 인터페이스로 변환할 때 주로 사용하며

이를 이용하면 인터페이스 호환성이 맞지 않아 같이 쓸 수 없는 클래스를 연관 관계로 연결해서 사용할 수 있게 해주는 패턴이다.

### 어뎁터 패턴의 등장 인물

Target(대상)의 역할

1. 지금 필요한 메소드를 결정한다.

Client(의뢰자)의 역할

1. Target 역할의 메소드를 사용해서 로직을 처리한다.

Adaptee(개조되는 쪽)의 역할

1. 이미 준비되어 있는 메소드를 가지고 있는 역할이다.
2. Adaptee역의 메소드가 Target 역할의 메소드와 일치하면 다음 Adapter의 역할은 필요 없다.

Adapter의 역할

Adaptee 역할의 메소드를 사용해서 Target 역할을 만족시키기 위한 역할이다.

class에 의한 Adapter 패턴의 경우 상속을 사용한 Adaptee의 역할을 이용한다.

instance에 의한 Adapter 패턴의 경우 위임을 사용한 Adaptee의 역할을 이용한다.

### 어뎁터 패턴의 클래스 다이어그램

![](/images/103/img.gif)

### 예제(상속을 사용한 Adapter 패턴)

![](/images/103/img.png)

#### Banner 클래스

변환을 하게 해주는 Adaptee에 해당한다.

```java
public class Banner {
    private String string;

    public Banner(String string) {
        this.string = string;
    }

    public void printBanner() {
        System.out.println("(" + string + ")");
    }
}
```

#### Print 클래스

Adapter가 구현해야할 인터페이스이다.즉 Adapter 패턴 클래스 다이어그램의 Target Interface에 해당한다.

```java
public interface Print {
    public abstract void printWeak();
    public abstract void printStrong();
}
```

#### PrintBanner 클래스

Adapter이다.즉 Adapter 패턴 클래스 다이어그램의 Adapter에 해당한다.

Banner 클래스를 상속 받았기 때문에 인스턴스 없이 printBanner() 메소드를 사용할 수 있다.

```java
public class PrintBanner extends Banner implements Print {
    public PrintBanner(String string) {
        super(string);
    }

    @Override
    public void printStrong() {
        // TODO Auto-generated method stub
        System.out.println("********************");
        printBanner();
        System.out.println("********************");
    }

    @Override
    public void printWeak() {
        // TODO Auto-generated method stub
        printBanner();
    }
}
```

#### Main 클래스

Adapter 패턴 클래스 다이어그램의 Client에 해당한다.

```java
public class Main {
    public static void main(String[] args) {
        Print p = new PrintBanner("Lee's Grow Up 디자인 패턴 공부입니다.");
        System.out.println("=== Weak배너 ===");
        p.printWeak();
        System.out.println("=== Strong배너 ===");
        p.printStrong();
    }
}
```

### 

### 예제(위임을 사용한 Adapter 패턴)

위 코드에서 상속이 아닌 인스턴스를 사용한 방식을 설명한다.

```java
public class PrintBanner implements Print {
    Banner banner ;
    public PrintBanner(String string) {
        banner = new Banner(string);
    }

    @Override
    public void printStrong() {
        // TODO Auto-generated method stub
        System.out.println("********************");
        banner.printBanner();
        System.out.println("********************");
    }

    @Override
    public void printWeak() {
        // TODO Auto-generated method stub
        banner.printBanner();
    }
}
```

위 방식처럼 상속이 아닌 인스턴스를 통해 메소드에 접근하는 방식이 차이점이다.

#### 이렇게 사용된 이유는 무엇일까?

1. 이처럼 Adapter 패턴은 이미 존재하는 클래스,특히 그 클래스가 충분한 테스트를 받아서 버그가 적으며              실제로 지금까지 사용된 실적이 있다면 그 클래스를 새로 정의하는 행위보다 해당 클래스를 부품으로써 재이용하기 위함이다.
2. Adapter 패턴은 기존 클래스를 개조해서 필요한 클래스를 만들기 때문에 필요한 메소드를 빠르게 구현가능하고   디버그도 새로 정의한 Adapter 클래스를 기준으로 하면 되기 때문에 비교적 복잡한 로직 클래스에 새로운 기능을 추가해도 검사가 상당히 쉬어진다는 장점이 있다.
{% endraw %}