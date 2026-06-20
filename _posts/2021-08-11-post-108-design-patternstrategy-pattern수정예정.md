---
layout: default
title: "[Design Pattern]Strategy Pattern(수정예정)"
date: 2021-08-11 09:07:37 +0900
categories: [Design Pattern]
slug: post-108-design-patternstrategy-pattern수정예정
---
{% raw %}

참조:<https://velog.io/@max9106/Java-%EC%A0%84%EB%9E%B5%ED%8C%A8%ED%84%B4strategy-pattern>

[[Java] 전략패턴(strategy pattern)

디자인 패턴의 꽃이라고 불릴만큼 많이, 다양하게 사용하는 패턴이다.알고리즘을 사용하는 클라이언트와 독립적으로 알고리즘을 변경할 수 있다. 즉 기존 코드의 변경 없이도 실제 로직을 바꿀

velog.io](https://velog.io/@max9106/Java-%EC%A0%84%EB%9E%B5%ED%8C%A8%ED%84%B4strategy-pattern)

본 패턴은 가장 많이 사용하는 패턴 중에 하나이다.

### 전략 패턴이란?

디자인 패턴의 꽃이라고 불릴만큼 많이,다양하게 사용하는 패턴이다

알고리즘을 사용하는 클라이언트와 독립적으로 알고리즘을 변경할 수 있다.

즉 기존 코드의 변경 없이도 실제 로직을 바꿀 수 있게 해주는 패턴이다.

```java
public interface MoveStrategy {
    int moveValue();
}
```
```java
public class RandomMove implements MoveStrategy {
    private static final int MIN_NUMBER = 0;
    private static final int MAX_NUMBER = 9;

    @Override
    public int moveValue() {
        return RandomUtils.nextInt(MIN_NUMBER, MAX_NUMBER);
    }
}
```
```java
public class UnconditionalMove implements MoveStrategy {
    private static final int MOVE_STANDARD = 4;

    @Override
    public int moveValue() {
        return MOVE_STANDARD;
    }
}
```
```java
public class Car {
    private static final int MOVING_BASELINE = 4;
    private int position;
    
    /*...*/
    
    public void move(MoveStrategy moveStrategy) {
    	if (moveStrategy.moveValue() >= MOVING_BASELINE) {
            this.position++;
        }
    }
}
```
```java
public class Application {
    public static void main(String[] args) {
		Car car = new Car();
        
        car.move(new RandomMove());
        car.move(new UnconditionalMove());
    }
}
```
{% endraw %}