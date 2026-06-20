---
layout: default
title: "[Java] hashCode()"
date: 2022-12-06 13:13:20 +0900
categories: [Java]
slug: post-132-java-hashcode
render_with_liquid: false
---

우선 클래스-인스턴스에서의 hashCode()는 인스턴스 주소값을 정수로 바꾼다.

```bash
Person person1 = new Person("osk");
Person person2 = person1;
Person person3 = new Person("osk");
System.out.println(person1.hashCode()); //918221580
System.out.println(person2.hashCode()); //918221580
System.out.println(person3.hashCode()); //2055281021
```

person1과 2번은 같은 인스턴스를 바라보기 때문에 정수값이 같다.

하지만 person3은 새로운 인스턴스를 생성했기때문에 정수값이 다르다.

문자열에서의 hashCode()는 문자열을 정수로 바꾼것이기 때문에 객체가 달라도 정수값은 같다.

```bash
String name1 = "osk";
String name2 = "osk";
System.out.println(name1.hashCode()); //110343
System.out.println(name2.hashCode()); //110343
```