---
layout: default
title: "Spring-Batch 의 처리 방법"
date: 2021-08-26 17:17:53 +0900
categories: [Spring Batch]
slug: post-118-spring-batch-의-처리-방법
---

배치를 처리할 수 있는 방법은 크게 2가지가 된다.

### Tasklet을 사용한 Task기반 처리

- 배치 처리 과정이 비교적 쉬운 경우 쉽게 사용
- 대량 처리를 하는 경우 더욱 복잡
- 하나의 큰 덩어리를 여러 덩어리로 나누어 처리하기 부적합

```java
@Bean
    public Step shareStep2() {
        return stepBuilderFactory.get("shareStep2")
                .tasklet((contribution, chunkContext) -> {
                    StepExecution stepExecution = contribution.getStepExecution();
                    ExecutionContext stepExecutionContext = stepExecution.getExecutionContext();

                    JobExecution jobExecution = stepExecution.getJobExecution();
                    ExecutionContext jobExecutionContext = jobExecution.getExecutionContext();

                    log.info("jobKey : {}, stepKey : {}",
                            jobExecutionContext.getString("jobKey", "emptyJobKey"),
                            stepExecutionContext.getString("stepKey", "emptyStepKey"));
                    return RepeatStatus.FINISHED;
                })
                .build();
    }
```

### Chunk를 사용한 chunk(덩어리) 기반 처리

- ItemReader,ItemProcessor,ItemWriter의 관계 이해 필요
- 대량 처리를 하는 경우 Tasklst 보다 비교적 쉽게 구현
- 예를 들면 10000개의 데이터 중 1000개씩 10개의 덩어리로 수행
- 이를 Tasklet으로 처리하면 10000를 한번에 처리하거나 수동으로 1000개씩 분할한다.

```java
@Bean
    public Step chunkBaseStep() {
        return stepBuilderFactory.get("chunkBaseStep")
                .<String, String>chunk(10)
                .reader(itemReader())
                .processor(itemProcessor())
                .writer(itemWriter())
                .build();
    }
```