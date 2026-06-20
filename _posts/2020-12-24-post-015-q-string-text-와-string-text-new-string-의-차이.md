---
layout: default
title: "[Q] String text = ''; 와 String text = new String(); 의 차이"
date: 2020-12-24 13:55:09 +0900
categories: [Etc]
slug: post-015-q-string-text-와-string-text-new-string-의-차이
render_with_liquid: false
---

먼저 “ ”는 문자열을 나타내며 new연산자로 인해 heap 메모리에 인스턴스된 text는 엄연히 다르다.

### **new String()의 경우,**

new 연산자는 heap 메모리내의 일반적인 객체를 생성한뒤 그 주소를 갖는다.

### **" "의 경우,**

“”는 일반적인 문자열로 heap 메모리내의 **String constant pool**에 저장한다

그러나 이미 존재하는 문자열이라면 그 저장된 배열의 인덱스 번호를 가르친다.

그래서 text == text1 에 대한 결과는 false가 나오게 되는것 이다 같은 객체를 참조하는 것이 아니기 때문이다

하지만 text.equals(text1)은 문자열 자체를 비교하여 결과를 돌려받기 때문에 true가 나온다

[(참조)](https://hashcode.co.kr/questions/857/%EC%9E%90%EB%B0%94%EC%97%90%EC%84%9C-string%EA%B0%9D%EC%B2%B4%EC%99%80-%EB%AC%B8%EC%9E%90%EC%97%B4-string%EC%9D%98-%EC%B0%A8%EC%9D%B4%EA%B0%80-%EB%AD%94%EA%B0%80%EC%9A%94)