---
layout: default
title: "try-with-resources에 대해..."
date: 2023-10-07 01:47:59 +0900
categories: [Java]
slug: post-137-try-with-resources에-대해
render_with_liquid: false
image: /images/137/img.png
---

```java
package org.example;

import java.lang.ref.Cleaner;

public class Room implements AutoCloseable { // 자동 자원 회수를 위한 인터페이스 구현
    private static final Cleaner cleaner = Cleaner.create();

    private static class State implements Runnable { // static 선언을 한 이유는 static 선언을 하지 않으면 중첩 클래스는 외부 클래스를 자동으로 참조하기때문에 외부 클래스가 GC에 의해 자원회수가 되면 중첩 클래스의 동작에 대한 보장을 받을수 없기때문에 외부 클래스 참조를 갖지않기 위해 static으로 정적 선언을 함.
        int numJunkPiles;

        State(int numJunkPiles) {
            this.numJunkPiles = numJunkPiles;
        }

        @Override
        public void run() {
            System.out.println("현재 방청소 상태값:" + numJunkPiles);
            System.out.println("방 청소!");
            numJunkPiles = 0;
        }
    }

    private final State state;

    private final Cleaner.Cleanable cleanable;

    public Room(int numJunkPiles) {
        state = new State(numJunkPiles);
        cleanable = cleaner.register(this, state);
    }

    @Override
    public void close() throws Exception {
        cleanable.clean(); // 자동 자원회수시 동작
    }
}
```

![](/images/137/img.png)

'이펙티브 자바-finalizer와 cleaner 사용을 피해라' 에 대한 내용을 정리하였다.

1. 자동 자원 회수를 위해 AutoCloseable 인터페이스의 close 메소드 구현
2. Room 클래스의 생성자를 통해 State 중첩 클래스(Runnable 인터페이스의 run 메소드 구현)는 static으로 외부 클래스(Room 클래스)로 부터 인스턴스 참조 분리 -> GC로 부터 독립
3. try-with-resources 를 통해 close 메소드를 자동 호출하여 자원 회수에 용이하도록 구현
4. 만약 new Room()으로 익명 인스턴스를 참조하면 중첩 클래스는 변수로 할당되지 않아 run 메소드 동작에 대한 보장을 받을수 없음

---

Cleaner 인터페이스와 Runnalbe 인터페이스의 연관관계를 확인하고자 Cleaner 인터페이스 문서를 찾아본바로는,

```java
The cleaning action is a Runnable to be invoked at most once 
when the object has become phantom reachable unless it has already been explicitly cleaned.
```

공식문서를 번역하자면 Runnalbe 인터페이스를 구현한 클래스의 인스턴스 객체가 **phantom reachable 상태(객체 참조가 없어져서 접근할수 없지만 메모리에 남아있는 상태)** 로 되면 정리작업 호출시(clean 메서드 호출) Runnable 인터페이스의 run 메서드가 호출된다.

따라서 try-with-resource 구현시 자동으로 AutoClosealbe 인터페이스의 close 메서드를 자동으로 동작시키며 해당 메서드 안의 clean 메서드를 호출함으로써 Runnalbe의 run 메서드를 호출하게 된다.