---
layout: default
title: "[Design Pattern] 전략 패턴(Strategy Pattern)의 이해와 Spring DI 활용"
date: 2021-08-11 09:07:37 +0900
categories: [Design Pattern]
slug: post-108-design-patternstrategy-pattern
---

소프트웨어 디자인 패턴 중 가장 빈번하게 사용되고 객체지향 설계의 꽃이라 불리는 패턴이 있습니다. 바로 **전략 패턴(Strategy Pattern)**입니다. 전략 패턴을 적용하면 알고리즘(실제 비즈니스 로직)을 사용하는 클라이언트 코드의 수정 없이도, 런타임에 동적으로 로직을 자유롭게 갈아끼울 수 있는 유연성을 확보할 수 있습니다.

이번 포스팅에서는 전략 패턴의 개념과 왜 이 패턴이 객체지향 원칙을 충족하는지, 그리고 스프링(Spring) 의존성 주입(DI)과의 연관성에 대해 자바 코드 예제와 함께 자세히 알아보겠습니다.

---

## 1. 전략 패턴이란?

> **"동일한 계열의 알고리즘들을 개별적으로 캡슐화하여 런타임에 동적으로 상호교환이 가능하게 만드는 패턴"**

간단히 말해, 무엇인가 실행하는 방식을 **인터페이스(Interface)**로 추상화하고, 이를 구현하는 구체적인 방식(전략)들을 클래스로 구현하여 클라이언트 상황에 맞게 유연하게 공급하는 기법입니다.

---

## 2. 자바 코드 예제: 자동차 이동 전략

예를 들어, 어떤 자동차(Car)가 앞으로 움직이려 할 때, '임의의 수(Random)를 기반으로 갈지 말지 정하는 전략'과 '무조건 앞으로 가는 전략'이 있다고 가정해 보겠습니다.

### [1단계] 전략 인터페이스 선언
움직이는 행위를 캡슐화한 인터페이스를 작성합니다.
```java
public interface MoveStrategy {
    int moveValue();
}
```

### [2단계] 구체적인 전략 구현체 작성
상황별 알고리즘을 독립된 클래스로 분리합니다.
```java
// 1) 랜덤 조건 이동 전략
public class RandomMove implements MoveStrategy {
    private static final int MIN_NUMBER = 0;
    private static final int MAX_NUMBER = 9;

    @Override
    public int moveValue() {
        return RandomUtils.nextInt(MIN_NUMBER, MAX_NUMBER);
    }
}

// 2) 무조건적인 이동 전략
public class UnconditionalMove implements MoveStrategy {
    private static final int MOVE_STANDARD = 4;

    @Override
    public int moveValue() {
        return MOVE_STANDARD;
    }
}
```

### [3단계] 컨텍스트(Context - 전략을 사용하는 객체) 구현
자동차 클래스는 구체적인 전략 클래스(RandomMove 등)에 직접 의존하지 않고, 추상화된 인터페이스(`MoveStrategy`)에만 의존합니다.
```java
public class Car {
    private static final int MOVING_BASELINE = 4;
    private int position;

    public void move(MoveStrategy moveStrategy) {
        // 인터페이스에 의존해 실제 동작을 실행합니다. (다형성)
        if (moveStrategy.moveValue() >= MOVING_BASELINE) {
            this.position++;
        }
    }
}
```

### [4단계] 클라이언트 사용
런타임에 필요한 전략 인스턴스를 주입해 주면 자동차의 이동 동작을 동적으로 바꿀 수 있습니다.
```java
public class Application {
    public static void main(String[] args) {
        Car car = new Car();
        
        // 상황에 맞게 전략을 유연하게 갈아끼우며 호출합니다.
        car.move(new RandomMove());
        car.move(new UnconditionalMove());
    }
}
```

---

## 3. 객체지향 설계 원칙(SOLID)과의 연계성

전략 패턴은 객체지향 5대 원칙(SOLID) 중 특히 아래 두 원칙을 충실하게 지원합니다.

### 1) 개방-폐쇄 원칙 (OCP, Open-Closed Principle)
* **의미**: 확장에 열려 있고 변경에 닫혀 있어야 합니다.
* **적용**: 새로운 이동 전략(예: `BackwardsMove`)이 추가되어야 할 때, 기존 `Car` 클래스의 코드나 기존 전략들의 코드는 단 한 줄도 수정할 필요가 없습니다. 오직 `MoveStrategy` 인터페이스를 상속받은 새 클래스만 구현하여 주입하면 확장이 끝납니다.

### 2) 의존역전 원칙 (DIP, Dependency Inversion Principle)
* **의미**: 구체적인 구현 클래스에 의존하지 말고 추상화(인터페이스)에 의존해야 합니다.
* **적용**: `Car` 클래스는 구체 클래스인 `RandomMove`가 아닌 상위 인터페이스인 `MoveStrategy`에 의존하고 있어 결합도가 크게 낮아집니다.

---

## 4. Spring DI(Dependency Inversion)와의 궁극적 연관성

자바 진영에서 스프링 프레임워크가 탄생한 철학적 기반 역시 전략 패턴에 맞닿아 있습니다.
스프링 컨테이너가 제공하는 **의존성 주입(DI, Dependency Injection)**은 바로 이 전략 패턴을 프레임워크 수준에서 대규모로 자동화해 둔 매커니즘입니다.

개발자는 생성자 주입 등을 통해 상위 인터페이스 타입으로 의존성을 정의해 두고, 실제 빈 컨텍스트 설정에 구체 클래스 빈을 지정하는 행위 자체가 스프링이라는 컨텍스트 하에 구현 전략을 결정해 주는 세련된 전략 패턴의 형태인 것입니다.

디자인 패턴 학습 시 클래스 간 결합도를 낮추고 유지보수성을 극대화하기 위해 이 전략 패턴의 사상을 기본 뼈대로 늘 염두에 두시길 추천합니다.

* 참조:<https://velog.io/@max9106/Java-%EC%A0%84%EB%9E%B5%ED%8C%A8%ED%84%B4strategy-pattern>