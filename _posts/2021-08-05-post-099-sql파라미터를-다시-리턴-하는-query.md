---
layout: default
title: "[SQL]파라미터를 다시 리턴 하는 Query"
date: 2021-08-05 17:28:45 +0900
categories: [Database]
slug: post-099-sql파라미터를-다시-리턴-하는-query
---

```java
public void printTradeAccntAndAmount() {
        for (info i : a()) {
            System.out.println(findByTradeAccntAndAmount(i));
        }
    }
```

리턴값을 바로 파라미터로 넣는 코드

```sql
SELECT #{방출하는부분} as keyword,info,amount
```

#{accnt} as main 부분은 파라미터로 들어온 값을 다시 리턴해주는 query 이다.