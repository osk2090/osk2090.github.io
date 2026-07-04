---
layout: default
title: "Quartz Job Scheduler의 아키텍처 및 Spring Boot 클러스터링(Clustering) 적용 가이드"
date: 2021-08-23 16:32:11 +0900
categories: [Etc]
slug: post-115-quartz-job-scheduler
---
{% raw %}

배치 처리나 주기적인 백그라운드 작업이 필요한 대규모 엔터프라이즈 시스템에서 신뢰성 높은 작업 예약을 위해 필수적으로 고려되는 자바 오픈소스 라이브러리가 있습니다. 바로 **Quartz Job Scheduler**입니다. 스프링 기본 스케줄러(`@Scheduled`)가 단일 JVM 내에서 단순 실행을 지원하는 데 비해, Quartz는 다중 서버(Clustering) 환경에서의 트랜잭션 관리와 Fail-over 기능을 네이티브하게 제공합니다.

이번 포스팅에서는 Quartz의 핵심 아키텍처와 구성요소를 분석하고, 실무 다중화 인프라 환경에서 안정적으로 스케줄러를 가동하기 위한 JDBCJobStore 기반 클러스터링 설정에 대해 알아보겠습니다.

---

## 1. Quartz의 3대 핵심 구성 요소

Quartz 아키텍처를 이해하려면 다음 세 가지 객체의 관계와 역할을 정립해야 합니다.

```
                  ┌──────────────────────┐
                  │      Scheduler       │
                  └──────────┬───────────┘
                             │ (스케줄링 등록 및 제어)
             ┌───────────────┴───────────────┐
             ▼                               ▼
    ┌────────────────┐              ┌────────────────┐
    │   JobDetail    │              │    Trigger     │
    │ (실행할 작업 정의)  │              │ (언제 실행할지 지정)  │
    └────────────────┘              └────────────────┘
```

### 1) Job & JobDetail
* **Job**: 실제로 실행되어야 하는 비즈니스 로직을 구현하는 인터페이스입니다. 단 하나의 `execute(JobExecutionContext context)` 메서드를 가집니다.
* **JobDetail**: Job의 상세 정의를 담고 있는 인스턴스입니다. Job의 이름, 그룹, 그리고 실행 시 필요한 매개변수 정보(`JobDataMap`)를 담고 있습니다. Quartz는 성능 향상을 위해 Job의 실행 시점마다 새로운 Job 인스턴스를 동적으로 생성하여 호출하기 때문에, 상태 정보는 JobDetail에 등록하여 보관합니다.

### 2) Trigger
* Job을 **언제, 어떤 주기로** 실행할 것인지 정의하는 스케줄링 옵션입니다.
* **SimpleTrigger**: 특정 시간대 시작, 단순 반복 간격(초, 분 등) 및 횟수 지정 시 사용합니다.
* **CronTrigger**: Unix 크론 표현식(예: `0 0 12 ? * WED` - 매주 수요일 낮 12시)을 지원하여 매우 세밀하고 복잡한 주기적 스케줄을 처리할 수 있습니다.

### 3) Scheduler
* `JobDetail`과 `Trigger`의 정보를 바탕으로 실제 백그라운드 스레드 풀을 제어하여 작업을 트리거하고 모니터링하는 컨트롤 타워입니다.

---

## 2. Spring Boot와 Quartz 연동 예시 코드

Spring Boot 환경에서는 `spring-boot-starter-quartz` 의존성을 추가하면 간편하게 빈으로 등록하여 연동할 수 있습니다.

### Job 구현체
```java
public class HelloWorldJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobDataMap dataMap = context.getJobDetail().getJobDataMap();
        String message = dataMap.getString("message");
        System.out.println("======> Quartz Job 실행! 메시지: " + message);
    }
}
```

### Configuration 설정
```java
@Configuration
public class QuartzConfig {

    @Bean
    public JobDetail helloWorldJobDetail() {
        return JobBuilder.newJob(HelloWorldJob.class)
                .withIdentity("helloWorldJob", "group1")
                .usingJobData("message", "안녕하세요, Quartz입니다.")
                .storeDurably() // 트리거가 없이도 스케줄러에 저장 유지
                .build();
    }

    @Bean
    public Trigger helloWorldJobTrigger(JobDetail helloWorldJobDetail) {
        return TriggerBuilder.newTrigger()
                .forJob(helloWorldJobDetail)
                .withIdentity("helloWorldTrigger", "group1")
                .withSchedule(CronScheduleBuilder.cronSchedule("0/10 * * * * ?")) // 10초마다 실행
                .build();
    }
}
```

---

## 3. 다중 서버 환경에서의 클러스터링: JDBCJobStore

서버가 2대 이상 실행되는 이중화 환경에서 내장 메모리(`RAMJobStore`)를 사용하여 스케줄러를 돌릴 경우, 각 서버마다 동일한 시간이 되어 스케줄을 똑같이 가동해 중복 데이터 생성이나 리소스 낭비가 초래되는 심각한 문제가 발생합니다.

이를 해결하기 위해 Quartz는 데이터베이스 테이블을 공유하여 동시성 제어를 수행하는 **JDBCJobStore 클러스터링**을 제공합니다.

### 1) 동작 메커니즘
* 모든 서버 인스턴스는 동일한 RDBMS 스키마(Quartz 테이블들: `QRTZ_LOCKS`, `QRTZ_TRIGGERS` 등)를 공유합니다.
* 특정 서버가 스케줄을 획득할 때, 데이터베이스의 행 잠금(Row Lock) 기법(`QRTZ_LOCKS` 행에 트랜잭션 락 획득)을 사용하여 **하나의 서버 인스턴스만 특정 Job을 가져가 실행**하도록 강제합니다.
* 실행 중인 서버 한 대가 강제 종료(Fail)되더라도, 다른 노드가 데이터베이스의 트리거 상태를 주기적으로 감지하여 중단된 스케줄을 이어받는 **Fail-over** 기능이 보장됩니다.

### 2) 설정 파일 (`application.yml`)
```yaml
spring:
  quartz:
    job-store-type: jdbc # 데이터베이스 기반으로 스토어 설정
    jdbc:
      initialize-schema: always # 최초 기동 시 DB 스키마 자동 생성
    properties:
      org:
        quartz:
          scheduler:
            instanceId: AUTO # 서버별 고유 인스턴스 ID 부여
          jobStore:
            isClustered: true # 클러스터 활성화
            clusterCheckinInterval: 20000 # 클러스터 노드 감지 주기 (20초)
```

스프링 배치가 대량의 일괄 데이터 처리를 주 목적으로 삼는다면, Quartz는 비즈니스 이벤트 시점의 **정밀한 실행 예약 및 조작 제어**를 담당합니다. 다중화 인프라 하에서 견고하게 구동될 스케줄러 시스템 설계를 목표로 하신다면, 락 분할 제어 성능을 고려한 JDBC JobStore 스키마 설정을 적극 검토해야 합니다.

* 참조:<https://advenoh.tistory.com/51>
{% endraw %}