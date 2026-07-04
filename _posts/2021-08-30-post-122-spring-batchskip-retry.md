---
layout: default
title: "Spring-Batch:Skip/Retry"
date: 2021-08-30 12:57:59 +0900
categories: [Spring Batch]
slug: post-122-spring-batchskip-retry
---
{% raw %}

참조:<https://oingdaddy.tistory.com/183>

[[Spring Batch] Skip/Retry Simple Example (Springboot based)

Spring Batch의 기본적인 기능들을 지난 포스팅들을 통해 알아보았다. 이번에 알아볼 Skip/Retry도 Spring Batch에서는 기본적으로 제공을 하는 기능이다. 간단한 예제를 통해서 알아보자. us-500.csv (웹에

oingdaddy.tistory.com](https://oingdaddy.tistory.com/183)

### Skip

```java
@Bean
    @JobScope
    public Step savePersonStep(@Value("#{jobParameters[allow_duplicate]}") String allowDuplicate) throws Exception {
        return this.stepBuilderFactory.get("savePersonStep")
                .<Person, Person>chunk(10)
                .reader(itemReader())
//                .processor(new DuplicateValidationProcessor<>(Person::getName, Boolean.parseBoolean(allowDuplicate)))
                .processor(itemProcessor(allowDuplicate))
                .writer(itemWriter())
                .listener(new SavePersonListener.SavePersonStepExecutionListener())
                .faultTolerant()
                .skip(NotFoundNameException.class)
                .skipLimit(2)//에러발생시 스킵할 횟수
                .build();
    }
```

skip/retry을 사용하기 위해서 먼저 faultToLerant() 라는 메서드를 사용해야 한다.

- skipLimit()-skip 허용 횟수지정,허용 횟수를 넘어가면 job은 실패한다.skip()과 반드시 같이 써야 한다.
- skip()-해당 exception이 발생했을때 skip하지 않겠다는 것이다.
- noSkip()-해당 exception이 발생하면 skip을 하지 않고 오류를 내겠다는 것이다.
- skipPolicy()-사용자의 정의로 skip에 대한 policy를 만들어서 적용하고 싶을때 사용한다.

위의 코드를 보면 skipLimit은 2로 되어있다는 것은 배치 수행중에 에러가 발생하면

2번까지는 skip하고 그 뒤로는 오류를 발생시킨다는 것이다.

### Retry

```java
@Slf4j
public class PersonValidationRetryProcessor implements ItemProcessor<Person, Person> {

    private final RetryTemplate retryTemplate;

    public PersonValidationRetryProcessor() {
        this.retryTemplate = new RetryTemplateBuilder()
                .maxAttempts(3)//reptyrLimit과 비슷
                .retryOn(NotFoundNameException.class)//retry 메서드와 비슷
                .withListener(new SavePersonRetryListener())
                .build();

    }

    @Override
    public Person process(Person item) throws Exception {
        return this.retryTemplate.execute(context -> {
                    //maxAttempts(3)
                    //3번 만큼 돈다.
                    //RetryCallback
                    //호출되면 처음 시작되는 지점
                    if (item.isNoEmptyName()) {
                        //이름이 있다면 그 아이템을 리턴한다.
                        return item;
                    }
                    throw new NotFoundNameException();
        }, context -> {
            //RecoveryCallback
            //위에서 3번만큼 돌면(3번 돌아도 에러가 발생한다면) 이쪽으로 넘어온다.
            return item.unknownName();//이름을 강제로 부여후 item을 리턴
                }
        );
    }

    public static class SavePersonRetryListener implements RetryListener {
        @Override
        public <T, E extends Throwable> boolean open(RetryContext context, RetryCallback<T, E> callback) {
            return true;//true라고 설정해줘야 retry가 실핸된다.
        }

        @Override
        //종료후 호출
        public <T, E extends Throwable> void close(RetryContext context, RetryCallback<T, E> callback, Throwable throwable) {
            log.info("close");
        }

        @Override
        //에러발생
        public <T, E extends Throwable> void onError(RetryContext context, RetryCallback<T, E> callback, Throwable throwable) {
            log.info("onError");
        }
    }
}
```

- retryLimit()-재시도 횟수,정한 값을 넘어가면 더이상 재시도를 하지 않고 실패처리한다.
- retry()-해당 exception이 발생했을 때 retry 하겠다는 것이다.
- noRetry()-해당 exception이 발생했을 때 retry하지 않겠다는 것이다.
- retryPolicy()-사용자의 정의로 retry에 대한 policy를 만들어서 적용하고 싶을때 사용한다.
{% endraw %}