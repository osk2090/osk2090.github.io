---
layout: default
title: "Spring-Batch:@Scope"
date: 2021-08-27 09:48:13 +0900
categories: [Spring Batch]
slug: post-119-spring-batchscope
---

@Scope는 어떤 시점에 bean을 생성/소멸 시킬 지 bean의 lifecycle을 설정

@JobScope는 job 실행 시점에 생성/소멸

- Step 선언

@StepScope는 step 실행 시점에 생성/소멸

- Tasklet,Chunk(ItemReader,ItemProcessor,ItemWriter)에 선언

Spring의 @Scope과 같은 것

- @Scope("job") == @JobScope
- @Scope("step") == @StepScope

Job과 Step 라이프사이클에 의해 생성되기 때문에 Thread safe하게 작동

@Value("#{jobParameters[key]}")를 사용하기 위해 @JobScope와 @StepScope 필수