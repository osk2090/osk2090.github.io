---
layout: default
title: "ChainMethod 기법"
date: 2021-08-04 12:27:13 +0900
categories: [Etc]
slug: post-097-chainmethod-기법
render_with_liquid: false
---

```java
package com.demo.domain;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor // 모든 생성자
@NoArgsConstructor // 빈 생성자
@Data // getter, setter, ToString
public class AccntInfo {

    String cstmrCode;
    String accnt;
    String createdAt;
    long blce;

    public AccntInfo cSetCstmrCode(String cstmrCode) {
        this.cstmrCode = cstmrCode;
        return this;
    }

    public AccntInfo cSetAccnt(String accnt) {
        this.accnt = accnt;
        return this;
    }

    public AccntInfo cSetCreatedAt(String createdAt) {
        this.createdAt = createdAt;
        return this;
    }

    public AccntInfo cSetBlce(long blce) {
        this.blce = blce;
        return this;
    }
}
```
```java
package com.demo;

import com.demo.domain.AccntInfo;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);

		new AccntInfo().cSetAccnt("asdasd").cSetBlce(1234L);
	}
}
```

이렇게 쓰면 한줄로 체인처럼 메서드를 호출할 수 있기에 가독성을 높인다.