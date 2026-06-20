---
layout: default
title: "[Design Pattern]Observer Pattern"
date: 2021-08-09 11:52:30 +0900
categories: [Design Pattern]
slug: post-106-design-patternobserver-pattern
image: /images/106/img.jpg
---

```java
public class User1 extends Observer{
	
    public User1(String msg){
        this.msg = msg;
    }
}
```

참조:<https://coding-factory.tistory.com/710>

[[Design Pattern] 옵저버 패턴(Observer Pattern)에 대하여

옵저버 패턴(Observer Pattern)이란? 옵저버패턴이란 객체의 상태 변화를 관찰하는 관찰자들, 즉 옵저버들의 목록을 객체에 등록하여 상태 변화가 있을 때마다 메서드 등을 통해 객체가 직접 목록의

coding-factory.tistory.com](https://coding-factory.tistory.com/710)

### 옵저버 패턴이란?

옵저버 패턴이란 객체의 상태 변화를 관찰하는 관찰자들, 즉 옵저버들의 목록을 객체에 등록하여 상태 변화가 있을때 마다 메서드 등을 통해 객체가 직접 목록의 각 옵저버에게 통지하도록 하는 디자인 패턴이다.

어떤 객체의 변경 사항이 발생하였을때 이와 연관된 객체들에게 알려주는 디자인 패턴이라고 생각하면 된다.

![](/images/106/img.jpg)

옵저버 패턴에는 주체 객체와 상태의 변경을 알아야 하는 관찰 객체가 존재하며 이들의 관계는 1:1이 될 수도 있고 1:N이 될 수도 있다.

### 옵저버 패턴의 장단점

#### 장점

1. 실시간으로 한 객체의 변경사항을 다른 객체에 전파할 수 있다.
2. 느슨한 결합으로 시스템이 유연하고 객체간의 의존성을 제거할 수 있다.

#### 단점

1. 너무 많이 사용하게 되면 상태 관리가 힘들 수 있다.
2. 데이터 배분에 문제가 생기면 자칫 큰 문제로 이어질 수 있다.

### 옵저버 패턴 사용 예제

공지사항을 알릴때를 예제로 공지사항을 전파할 때(상태변화) 옵저버와 관련된 객체들(유저들)에게 통지하도록 하는 간단한 예제를 옵저버 패턴으로 만들어보겠다.

```java
public class Observer {
    public String msg;

    public void receive(String msg){
        System.out.println(this.msg + "에서 메시지를 받음 : " + msg);
    }
}
```
```java
public class User1 extends Observer{
	
    public User1(String msg){
        this.msg = msg;
    }
}
```
```java
public class User2 extends Observer{
	
    public User2(String msg) {
        this.msg = msg;
    }
}
```
```java
public class Notice {
    private List<Observer> observers = new ArrayList<Observer>();

    // 옵저버에 추가
    public void attach(Observer observer){
        observers.add(observer);
    }

    // 옵저버에서 제거
    public void detach(Observer observer){
        observers.remove(observer);
    }

    // 옵저버들에게 알림
    public void notifyObservers(String msg){
        for (Observer o:observers) {
            o.receive(msg);
        }
    }
}
```
```java
public class Main {
    public static void main(String[] args) {
        Notice notice = new Notice();
        User1 user1 = new User1("유저1");
        User2 user2 = new User2("유저2");
        
        notice.attach(user1);
        notice.attach(user2);
       
        String msg = "공지사항입니다~!";
        notice.notifyObservers(msg);

        notice.detach(user1); // user1 공지사항 받는 대상에서 제거
        msg = "안녕하세요~";
        notice.notifyObservers(msg);
    }
}
```

#### 출력

```html
유저1에서 메시지를 받음 : 공지사항입니다~!
유저2에서 메시지를 받음 : 공지사항입니다~!
유저2에서 메시지를 받음 : 안녕하세요~
```