---
layout: default
title: "[Design Pattern]Decorator Pattern"
date: 2021-08-09 10:23:45 +0900
categories: [Design Pattern]
slug: post-105-design-patterndecorator-pattern
image: /images/105/img.png
---
{% raw %}

참조:<https://coding-factory.tistory.com/713?category=974095>

### 데코레이터 패턴이란?

데코레이터 패턴은 주어진 상황 및 용도에 따라 어떤 객체에 책임(기능)을 동적으로 추가하는 패턴을 말한다.

데코레이터 말 그대로 장식이라고 생각하면 된다.

기본 기능을 가지고 있는 클래스를 하나 만들어주고 추가할 수 있는 기능들을 추가하기 편하도록 설계하는 방식이다.

![](/images/105/img.png)

Component:실질적인 인스턴스를 컨트롤하는 역할

ConcreteComponent:Component의 실절적인 인스턴스의 부분으로 책임의 주체의 역할

Decorator:Component와 ConcreteDecorator를 동일시 하도록 해주는 역할

### 데코레이터 패턴의 장단점

#### 장점

1. 기존 코드를 수정하지 않고도 데코레이터 패턴을 통해 행동을 확장시킬 수 있다.
2. 구성과 위임을 통해서 실행중에 새로운 행동을 추가할 수 있다.

#### 단점

1. 의미없는 객체들이 너무 많이 추가될 수 있다.
2. 데코레이터를 너무 많이 사용하면 코드가 필요이상으로 복잡해질 수 있다.

### 데코레이터 패턴을 이럴때 사용하면 좋다!

1. 클래스의 요소들을 계속해서 수정을 하면서 사용하는 구조가 필요한 경우
2. 여러 요소들을 조합해서 사용하는 클래스 구조인 경우

위와 같은 상황일때가 언제일까?예를들어 커피를 제조하는 방법에 대해 설명하겠다.

커피는 종류마다 아메리카노는 에스프레소에 물을 섞고 카페라떼는 에스프레소에 스팀우유나 휘핑크림을 얹기도 하는 등 커피를 만들때 다양한 재료들의 구성으로 하나의 커피가 완성된다.

이 재료들을 모두 클래스로 구현해 준다면 굉장히 많은 클래스들을 구현해줘야 할 것이다.

또 이 구조는 상당히 비효율적이다.그이유는 새로운 커피를 개발할 때마다 그 커피에 들어가는 재료의 객체를 만들고

기능을 추가해주어야 하기 때문이다.커피의 종류가 많으면 많이질수록 코드가 비효율적일 것이다.

또한 커피를 만들때마다 매번 해당하는 클래스들의 객체를 생성해주어야 하는 문제도 있다.

이를 해결하기 위해 기본 커피의 재료인 에스프레소라는 틀을 추상적으로 가지고 커피를 만들때 들어가는 재료들을 장식하는 방식을 사용하는 것이다.

### 테코레이터 패턴 사용 예제

```java
public interface Component {
    String add(); //재료 추가
}
```
```java
public class BaseComponent implements Component {

    @Override
    public String add() {
        // TODO Auto-generated method stub
        return "에스프레소";
    }
}
```
```java
abstract public class Decorator implements Component {
    private Component coffeeComponent;
    
    public Decorator(Component coffeeComponent) {
        this.coffeeComponent = coffeeComponent;
    }
    
    public String add() {
        return coffeeComponent.add();
    }
}
```
```java
abstract public class Decorator implements Component {
    private Component coffeeComponent;
    
    public Decorator(Component coffeeComponent) {
        this.coffeeComponent = coffeeComponent;
    }
    
    public String add() {
        return coffeeComponent.add();
    }
}
```
```java
//우유를 추가해주는 클래스
public class MilkDecorator extends Decorator {
    public MilkDecorator(Component coffeeComponent) {
        super(coffeeComponent);
    }
    
    @Override
    public String add() {
        // TODO Auto-generated method stub
        return super.add() + " + 우유";
    }
}
```
```java
public class Main {

    public static void main(String[] args) {
        Component espresso = new BaseComponent();
        System.out.println("에스프레소 : " + espresso.add());
        
        Component americano = new WaterDecorator(new BaseComponent());
        System.out.println("아메리카노 : " + americano.add());
        
        Component latte = new MilkDecorator(new WaterDecorator(new BaseComponent()));
        System.out.println("라떼 : " + latte.add());
    }
}
```

#### 출력

```html
에스프레소 : 에스프레소
아메리카노 : 에스프레소 + 물
라떼 : 에스프레소 + 물 + 우유
```
{% endraw %}