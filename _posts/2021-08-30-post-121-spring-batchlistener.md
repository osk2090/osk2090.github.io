---
layout: default
title: "Spring-Batch:Listener"
date: 2021-08-30 09:36:03 +0900
categories: [Spring Batch]
slug: post-121-spring-batchlistener
image: /images/121/img.png
---

참조:<https://oingdaddy.tistory.com/180>

[[Spring Batch] Listener Example (Springboot based)

지난 글에서 다뤘던 Springboot Batch Chunk Example에서 소스들을 살펴 볼때 Listener도 살짝 나왔다. 우리가 정의한 Job이나 Step 실행 전 후로 필요한 공통 작업을 기술하기 위해 주로 사용되며 사용된다.

oingdaddy.tistory.com](https://oingdaddy.tistory.com/180)

실제로 스프링 배치에서는 거의 모든 측면에서 생명주기가 잘 정의되있다.

이를 바탕으로 스프링 배치는 생명 주기의 여러 시점에 로직을 추가할 수 있는 기능을 제공한다.

잡 실행과 관련이 있다면 JobExecutionListener를 사용할 수 있다.

이 인터페이스는 beforeJob과 afterJob의 두 메서드를 제공한다.

말그대로 잡주기에서 가장 먼저 실행되거나 가장 나중에 실행되는것을 말한다.

![](/images/121/img.png)

```java
@Slf4j
public class SavePersonListener {

	//어노테이션을 이용한 리스너(Step)
    public static class SavePersonStepExecutionListener {
        @BeforeStep
        public void beforeStep(StepExecution stepExecution) {
            log.info("beforeStep");
        }

        @AfterStep
        public ExitStatus afterStep(StepExecution stepExecution) {
            log.info("afterStep : {}", stepExecution.getWriteCount());
            if (stepExecution.getWriteCount() == 0) {
                return ExitStatus.FAILED;
            }
            return stepExecution.getExitStatus();
        }
    }

	//JobExecutionListener 구현체를 이용한 리스너(Job)
    public static class SavePersonJobExecutionListener implements JobExecutionListener {

        @Override
        public void beforeJob(JobExecution jobExecution) {
            log.info("beforeJob");
        }

        @Override
        public void afterJob(JobExecution jobExecution) {
            int sum = jobExecution.getStepExecutions().stream().mapToInt(StepExecution::getWriteCount).sum();
            log.info("afterJob : {}", sum);
        }
    }

	//어노테이션을 이용한 리스너(Job)
    public static class SavePersonAnnotationJobExecutionListener {

        @BeforeJob
        public void beforeJob(JobExecution jobExecution) {
            log.info("annotationBeforeJob");
        }

        @AfterJob
        public void afterJob(JobExecution jobExecution) {
            int sum = jobExecution.getStepExecutions().stream().mapToInt(StepExecution::getWriteCount).sum();
            log.info("annotationAfterJob : {}", sum);
        }
    }

}
```
```java
    @Bean
    public Job savePersonJob() throws Exception {
        return this.jobBuilderFactory.get("savePersonJob")
                .incrementer(new RunIdIncrementer())
                .start(this.savePersonStep(null))
                //리스너 사용(Job)
                .listener(new SavePersonListener.SavePersonJobExecutionListener())
                .listener(new SavePersonListener.SavePersonAnnotationJobExecutionListener())
                .build();
    }

    @Bean
    @JobScope
    public Step savePersonStep(@Value("#{jobParameters[allow_duplicate]}") String allowDuplicate) throws Exception {
        return this.stepBuilderFactory.get("savePersonStep")
                .<Person, Person>chunk(10)
                .reader(itemReader())
                .processor(new DuplicateValidationProcessor<>(Person::getName, Boolean.parseBoolean(allowDuplicate)))
                .writer(itemWriter())
                //리스너 사용(Step)
                .listener(new SavePersonListener.SavePersonStepExecutionListener())
                .build();
    }
```