---
layout: default
title: "Spring Batch의 @JobScope와 @StepScope 동작 원리 및 늦은 바인딩(Late Binding) 분석"
date: 2021-08-27 09:48:13 +0900
categories: [Spring Batch]
slug: post-119-spring-batchscope
---
{% raw %}

스프링 배치(Spring Batch)를 사용하다 보면 일반적인 스프링 빈(Bean)의 싱글톤(Singleton) 컨텍스트와는 다른 독특한 스코프 어노테이션인 `@JobScope`와 `@StepScope`를 접하게 됩니다. 이번 포스팅에서는 이 배치 전용 스코프들의 역할과 설정 시 내부에서 일어나는 프록시(Proxy) 기반 동작 방식, 그리고 이를 통해 얻을 수 있는 장점에 대해 깊이 있게 알아보겠습니다.

---

## 1. @JobScope & @StepScope란?

스프링 배치의 기본 빈 생성 주기는 싱글톤(Application 구동 시점 생성)이지만, 배치 컴포넌트에 배치 스코프를 선언하면 빈의 생명주기(Lifecycle)가 각각 **Job 실행 시점** 또는 **Step 실행 시점**으로 늦춰지게 됩니다.

### 1) @JobScope
* **대상**: Step 선언문에 설정할 수 있습니다.
* **주기**: 배치의 `Job`이 실행되고 끝날 때까지 빈의 생명이 유지됩니다.
* **표현식**: `@Scope("job")`과 동일합니다.

### 2) @StepScope
* **대상**: Step 안의 Tasklet이나 Chunk 지향 컴포넌트(`ItemReader`, `ItemProcessor`, `ItemWriter`)에 설정할 수 있습니다.
* **주기**: 배치의 `Step`이 시작되는 시점에 생성되고, 해당 Step이 종료되면 소멸합니다.
* **표현식**: `@Scope("step")`과 동일합니다.

---

## 2. 늦은 바인딩(Late Binding)과 활용

배치 스코프를 사용하는 가장 대표적인 이유는 **늦은 바인딩(Late Binding / 지연 바인딩)**입니다. 애플리케이션 실행 시점이 아니라, 실제 Job이나 Step이 실행되는 시점에 매개변수를 주입받아 빈을 동적으로 구성할 수 있습니다.

### 예시 코드: JobParameter 동적 주입
```java
@Bean
@StepScope
public FlatFileItemReader<Person> reader(
        @Value("#{jobParameters['requestDate']}") String requestDate) {
    
    // 애플리케이션 구동 시점이 아닌, Job 실행 중 파라미터가 들어왔을 때 실행됩니다.
    System.out.println("======> Reader 생성! requestDate: " + requestDate);
    
    return new FlatFileItemReaderBuilder<Person>()
            .name("personReader")
            .resource(new ClassPathResource("people-" + requestDate + ".csv"))
            // ... 생략 ...
            .build();
}
```

만약 `@StepScope`가 없다면 애플리케이션 구동 시점에 스프링 컨테이너가 `reader` 빈을 싱글톤으로 미리 만들기 때문에, 아직 존재하지도 않는 `jobParameters`의 값을 해석할 수 없어 구동 시 에러가 발생하거나 엉뚱한 값을 가지게 됩니다.

---

## 3. 내부 동작 원리: 프록시 패턴 (Proxy Pattern)

그렇다면 어떻게 스프링은 애플리케이션 실행 시점에 파라미터가 없는데도 에러를 내지 않고 컴포넌트 빈을 주입받아 등록할 수 있을까요? 바로 **프록시(Proxy)** 기술 덕분입니다.

```text
[애플리케이션 구동 시점]
Spring Container ──> Proxy 객체 등록 (실제 Reader는 생성되지 않음)

[Job/Step 실행 시점]
배치 실행 ──> Proxy 객체의 메소드 호출 ──> 내부적으로 StepContext에서 실제 빈 인스턴스 생성 ──> 실제 빈 호출
```

1. **가짜 객체(프록시)의 주입**: 애플리케이션이 시작될 때 스프링 컨테이너는 주입될 빈의 실제 인스턴스 대신 CGLIB 등을 이용해 생성한 **가짜 프록시 빈**을 먼저 등록해 둡니다.
2. **실제 인스턴스 위임**: 런타임에 이 가짜 프록시 빈의 메소드가 최초로 호출되면, 프록시 내부에서 스프링 배치의 `StepContext` 혹은 `JobContext`에 접근하여 실제 배치 매개변수를 담은 **진짜 빈 인스턴스를 동적으로 생성**한 뒤 호출을 위임합니다.
3. **생명주기 관리**: Step이 끝나는 즉시, 생성되었던 진짜 빈 인스턴스는 가비지 컬렉터(GC)의 수거 대상이 되며 프록시 내부 저장소에서도 제거됩니다.

---

## 4. Thread-Safe 보장 및 이점

### 1) 병렬 처리(Multi-thread) 환경에서의 동시성 보장
여러 개의 스레드가 동시에 배치를 수행하거나 여러 Step이 같은 `ItemReader` 빈의 설정을 사용할 때, 각 스레드는 각자의 `StepContext`에 매핑된 독립적인 Reader 인스턴스를 지연 생성하여 사용하므로 상태값이 뒤엉키지 않는 **Thread-safe**한 동작을 완벽히 보장받습니다.

### 2) 동일 컴포넌트의 병렬 실행(Parallel Steps)
동일한 빈 정의를 사용하더라도 파라미터가 다르면 각 배치 흐름별로 다른 목적을 지닌 컴포넌트로 개별 분기 처리가 가능해집니다.

결론적으로, 스프링 배치 개발 시 **JobParameter를 동적으로 다루어야 하거나 병렬 배치 가동 시 동시성 이슈를 예방**하고 싶다면 컴포넌트 빈 선언부에 `@JobScope` 또는 `@StepScope`를 적극 선언하여 사용하시길 권장합니다.
{% endraw %}