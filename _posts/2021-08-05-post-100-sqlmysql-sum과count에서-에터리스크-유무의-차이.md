---
layout: default
title: "[SQL]MySQL SUM()과COUNT()에서 *(에터리스크) 유무의 차이"
date: 2021-08-05 18:16:29 +0900
categories: [Database]
slug: post-100-sqlmysql-sum과count에서-에터리스크-유무의-차이
render_with_liquid: false
---

SUM()과 COUNT() 둘다 자주 쓰는 SQL명령어 인데

왜 SUM에서는 컬럼명(데이터는 문자열)은 가능하고 \*는 불가하고

COUNT()에서는 컬럼명 또는 \*(에터리스크) 둘다 가능한 것을 볼 수 있다.

결론은

SUM(\*)을 사용하면 문자열도 다 연산하라는 의미가 되므로 에러가 뜨는 것이다.

그래서 \*는 COUNT(\*)에서만 사용할 수 있다.