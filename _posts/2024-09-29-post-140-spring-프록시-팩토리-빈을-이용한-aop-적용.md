---
layout: default
title: "Spring 프록시 팩토리 빈을 이용한 AOP 적용"
date: 2024-09-29 16:06:19 +0900
categories: [Spring]
slug: post-140-spring-프록시-팩토리-빈을-이용한-aop-적용
render_with_liquid: false
image: /images/140/img.png
---

먼저 예시코드를 보고 진행해보자.

```bash
void proxyFactoryBean() {
        ProxyFactoryBean pfBean = new ProxyFactoryBean(); // 프록시 객체를 만들수 있도록 함
        pfBean.setTarget(new HelloTarget()); // 타겟을 정함 즉 어떤 객체를 프록시 객체로 만드는지
        pfBean.addAdvice(new UpperCaseAdvice()); // 위에서 정한 타겟에 어떤 어드바이스를 적용시킬지

        Hello proxiedHello = (Hello) pfBean.getObject(); // 해당 메서드로 호출하면 위에서 정한 타겟의 프록시 객체를 던진다.
        assertThat(proxiedHello.sayHello("Osk")).isEqualTo("HELLO OSK");
        assertThat(proxiedHello.sayHi("Osk")).isEqualTo("HI OSK");
        assertThat(proxiedHello.sayThankYou("Osk")).isEqualTo("THANK YOU OSK");
    }
```

위 코드의 주석처럼 타겟을 정할 객체와 해당 객체에 적용시킬 즉 프록시 객체에 적용시킬 코드가 있는 클래스를 넣어준다.

나는 해당 코드를 아래와 같이 선언했다.

```bash
static class UpperCaseAdvice implements MethodInterceptor {

        @Override
        public Object invoke(MethodInvocation invocation) throws Throwable {
            String ret = (String) invocation.proceed();
            return ret.toUpperCase();
        }
    }
```

특별한 기능은 없고 프록시 객체는 원본 객체에서 반환된 문자열을 대문자로 바꿔서 프록시가 리턴받도록 한다.

![](/images/140/img.png)

클로드 참조

하지만 메서드가 포인트컷과 불일치 하면 프록시 객체는 원본 객체에서 반환받은 값을 어드바이저에서 처리하지 않고 바로 클라이언트에게 반환하도록 한다.

여기서 포인트컷과 메서드가 다른지 확인하는 많은 기준이 있지만 기본적으로 호출하는 메서드명이 일치하는 것인다.

만약 메서드명과 포인트컷이 다르면 어떻게 되는지 확인해보자.

```bash
void proxyFactoryBeanDifferentMethodName() {
        ProxyFactoryBean pfBean = new ProxyFactoryBean();
        pfBean.setTarget(new HelloTarget());

        // 포인트컷을 "sayThankYou" 메서드에만 적용하도록 변경
        NameMatchMethodPointcut pointcut = new NameMatchMethodPointcut();
        pointcut.setMappedName("sayThankYou");

        pfBean.addAdvisor(new DefaultPointcutAdvisor(pointcut, new UpperCaseAdvice()));

        Hello proxiedHello = (Hello) pfBean.getObject();

        // 테스트
        assertThat(proxiedHello.sayHello("Osk")).isEqualTo("HELLO OSK");
        assertThat(proxiedHello.sayHi("Osk")).isEqualTo("HI OSK");
        assertThat(proxiedHello.sayThankYou("Osk")).isEqualTo("THANK YOU OSK");
    }
```

위의 코드를 돌려보면 sayThankYou 메서드에만 포인트컷을 적용시켰기때문에 첫번째 테스트는 변환되지 않았기 때문에 실패를 하게 된다.