---
layout: default
title: "Spring-Mapper파일 mapUnderscoreToCamelCase에 관해"
date: 2021-08-04 19:04:20 +0900
categories: [Spring]
slug: post-098-spring-mapper파일-mapunderscoretocamelcase에-관해
---

```java
<resultMap id="memberMap" type="member">
    <id column="mno" property="no"/>
    <result column="mname" property="name"/>
    <result column="mphoto" property="photo"/>
    <result column="mtel" property="tel"/>
    <result column="mgender" property="gender"/>
    <result column="mstatus" property="status"/>
    <result column="mpow" property="power"/>
    <result column="mcnt" property="count"/>
  </resultMap>
```

DB와 도메인의 프로퍼티가 다르다면 코드처럼 연관이 있다고 선언해줘야 한다.

결국엔 귀찮아진다...

해결 방법은

mybatis-config.xml

```java
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN" "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <settings>
        <setting name="mapUnderscoreToCamelCase" value="true"/>//이 부분이 중요!
        <setting name="callSettersOnNulls" value="true"/>
        <setting name="jdbcTypeForNull" value="NULL"/>
    </settings>
</configuration>
```

이렇게 설정해주면 DB의 컬럼명과 VO 또는 도메인에서 camelcase로 자동으로 변환하여 매핑해준다.

참조:<https://solbel.tistory.com/1520>