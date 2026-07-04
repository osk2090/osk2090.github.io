---
layout: default
title: "[Spring Framework]Log4j의 역할"
date: 2021-06-24 08:40:08 +0900
categories: [Spring]
slug: post-071-spring-frameworklog4j의-역할
---
{% raw %}

log4j는 프로그램을 작성하는 도중에 로그를 남기는 자바 기반의 우틸리티이다

총 6개의 단계를 표시해주며 개발자가 단계를 지정할 수 있다

- FATAL:어플리케이션 작동이 불가능
- ERROR:요청을 처리할 수 없는 상태
- WARN:처리 가능하지만 위험성을 안고 있는 상태
- INFO:정보성 메세지 확인
- DEBUG:개발시 디버그 위함
- TRACE:DEBUG 레벨의 상세화 단계

### 사용법

pom.xml

```html
<dependency>
    <groupId>log4j</groupId>
    <artifactId>log4j</artifactId>
    <version>1.2.17</version>
</dependency>
```

log4j.xml

```html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE log4j:configuration PUBLIC "-//APACHE//DTD LOG4J 1.2//EN" "log4j.dtd">
<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
    <!-- Appenders -->
    <appender name="console" class="org.apache.log4j.ConsoleAppender">
        <param name="Target" value="System.out" />
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="%-5p: %c - %m%n" />
        </layout>
    </appender>
    <!-- Application Loggers -->
    <logger name="com.mycompany.sd">
        <level value="info" />
    </logger>
    <!-- 3rdparty Loggers -->
    <logger name="org.springframework.core">
        <level value="info" />
    </logger>
    <logger name="org.springframework.beans">
        <level value="info" />
    </logger>
    <logger name="org.springframework.context">
        <level value="info" />
    </logger>
    <logger name="org.springframework.web">
        <level value="info" />
    </logger>
    <!-- Root Logger -->
    <root>
        <priority value="warn" />
        <appender-ref ref="console" />
    </root>
</log4j:configuration>
```

출처:위키백과,<https://cloudstudying.kr/lectures/346>
{% endraw %}