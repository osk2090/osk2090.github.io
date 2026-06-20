---
layout: default
title: "[내용 추가 예정]Quartz Job Scheduler"
date: 2021-08-23 16:32:11 +0900
categories: [Etc]
slug: post-115-내용-추가-예정quartz-job-scheduler
render_with_liquid: false
---

참조:<https://advenoh.tistory.com/51>

[Quartz Job Scheduler란?

Gatsby로 블로그 마이그레이션을 하여 이 링크를 클릭하면 해당 포스팅으로 갑니다. 감사합니다. http://blog.advenoh.pe.kr 1. 들어가며 Quartz Job Scheduler에 대한 내용은 여러 시리즈 형식으로 작성을 하

advenoh.tistory.com](https://advenoh.tistory.com/51)

### Quartz란?

Job Scheduling 라이브러리로 완전히 자바로 개발되어 자바 프로그램에서도 쉽게 통합해서 개발할 수 있다.

Quartz는 수십에서 수천 개의 작업도 실행 가능하며 간단한 interval 형식이나 Cron 표현식으로 복잡한 스케줄링도 지원한다.예를 들면 매주 금요일 새벽 1시 30분에 매주 실행하는 작업이나 매월 마지막 날에 실행하는 작업도 지정할 수 있다.

#### 장점

- DB기반으로 스케줄러 간의 Clustering 기능을 지원한다.
- 시스템 fail-over와 Random 방식의 로드 분산처리를 지원한다.
- in-memory Job Scheduler도 제공한다.
- 여러 기본 플러그인을 제공한다.
- ShutdownHookPlugin-JVM 종료 이벤트를 캐치해서 스케줄러에게 종료를 알린다.
- LoggingJobHistoryPlugin-Job 실행에 대한 로그를 남겨 디버깅할 때 유용하게 사용할 수 있다.

#### 단점

- Clustering 기능을 제공하지만 단순한 random 방식이라서 완벽한 Cluster 간의 로드 분산은 안된다.
- 어드민 UI를 제공하지 않는다.
- 스케줄링 실행에 대한 History는 보관하지 않는다.
- Fixed Delay 타입을 보장하지 않으므로 추가 작업이 필요하다.

### Quartz 아키텍처와 구성요소

#### Job

Quartz API에서 단 하나의 메서드를 가진 execute(JobExecutionContext context) Job 인터페이스를 제공한다.

Quartz를 사용하는 개발자는 수행해야 하는 실제 작업을 이 메서드에서 구현하면 된다.

Job의 Trigger가 발생하면 스케줄러는 JobExecutionContext 객체를 넘겨주고 execute 메서드를 호출한다.