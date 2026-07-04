---
layout: default
title: "[기초3일]switch문/while문"
date: 2020-12-17 01:03:37 +0900
categories: [Etc]
slug: post-010-기초3일switch문-while문
---
{% raw %}

### **후위 연산자**

맨 마지막에 실행되는 특징이 있으며

형식으로는 **변수++ 변수-- 변수\*\*** 등등 사칙연산을 넣을 수 있다

### **전위 연산자**

가장 먼저 실행되는 특징이며

형식으로는 후위연산자의 사칙연산자를 앞으로 옮기면 된다

**++변수 --변수 \*\*변수**

### **숏컷(short cut)**

먼저 or연산자를 들여다 보면

하나라도 참이면-참

만약 거짓을 발견하면-연결시키는 뒤의 조건을 확인해야한다

그러나 먼저 참을 발견하면-이미 참이므로 뒤를 안본다

and연산자의 특징으로는

하나라도 거짓이 있으면-거짓

만약 참을 발견하면-뒤의 조건을 확인해야한다

그러나 먼저 거짓을 발견하면-이미 거짓으로 뒤를 안본다

**결론:**

**or연산자 경우,상대적으로 잘 걸리는 녀석을 전면에 배치한다**

**and연산자 경우,상대적으로 잘 안걸리는 녀석을 전면에 배치한다**

### switch문

if문의 경우 조건 케이스가 여러개 나오는 경우 복잡해진다

이러한 복잡함을 단순화하기 위해 나온것이 switch문이다(가독성을 높이기 위해)

작성법

1.switch(특정 변수)를 적는다

2.case 특정변수의 결과: 형식으로 작성한다

3.각 case상황에 동작할 코드를 작성한다

4.break를 통해서 제어가 끝났음을 알린다

5.특정 상황이 아닌 다른 상황을 처리할 수 있도록 default: 케이스를 작성한다

입력된 값을 출력하는 조건문

```java
Scanner scan = new Scanner(System.in);

        System.out.println("정수를 입력하세요");
        int num = scan.nextInt();

        switch (num) {
            case 1:
                System.out.println("1");
                break;
            case 2:
                System.out.println("2");
                break;
            case 3:
                System.out.println("3");
                break;
            default:
                System.out.println("그외의 값들");
                break;
        }
```

성적을 확인하는 조건문

```java
Scanner scan = new Scanner(System.in);

        System.out.println("성적을 입력하세요[0~100]");
        int score = scan.nextInt();

        int subScore = score / 10;//앞에자리만 추출하는 로직

        switch (subScore) {
            case 10:
            case 9:
                System.out.println("A");
                break;
            case 8:
                System.out.println("B");
                break;
            case 7:
                System.out.println("C");
                break;
            case 6:
                System.out.println("D");
                break;
            case 5:
            case 4:
            case 3:
            case 2:
            case 1:
            case 0:
                System.out.println("F");
            default:
                System.out.println("범위를 벗어난 점수입니다.확인해주세요");
                break;
        }
```

위에 switch문을 if문으로 바꾸기

```java
Scanner scan = new Scanner(System.in);

        System.out.println("성적을 입력하세요[0~100]");
        int score = scan.nextInt();

        if (score >= 90 && score <= 100) {
            System.out.println("A");
        } else if (score >= 80 && score <= 89) {
            System.out.println("B");
        } else if (score >= 70 && score <= 79) {
            System.out.println("C");
        } else if (score >= 60 && score <= 69) {
            System.out.println("D");
        } else if (score < 0 || score > 100) {
            System.out.println("범위를 벗어난 점수입니다.확인해주세요");
        } else {
            System.out.println("F");
        }
```

if문은 switch문과 다르게 우선순위를 잘 고려햐줘야만 올바른 결과를 얻을수 있다

if~else if 복합문 작성시 유의할 점으로는

가장 범위가 큰것부터 작은 것 순으로 내려 작성한다

내림차순으로 작성한다

### while문

사전적 의미로는 ~동안

~이 결국엔 조건을 의미하며

해당 조건을 마족하는 동안으로 해석할 수 있을 것이다

그렇기 때문에 반복문이 되는 것이다

while문 작성법

1.while을 적고 소괄호를 열고 닫으며 중괄호를 열고 닫늗다

2.소괄호 내부에 조건을 작성한다

3.중괄호 내부에는 반복시킬 작업을 작성한다

연습 문제 1.   
5 ~ 15 까지 출력해보기

```java
int n = 5;
        while (n < 16) {
            System.out.print(n + "\t");
            n++;
        }
```

연습 문제 2.   
0 ~ -19 까지 출력하기

```java
int n = 0;
        while (n > -20) {
            System.out.print(n + "\t");
            n--;
        }
```

연습 문제 3.   
1 ~ 30 까지 숫자중에서   
짝수만 골라서 출력해보자!

```java
int n = 1;
        while (n < 31) {
            if (n % 2 == 0) {
                System.out.print(n + "\t");
            }
            n++;
        }
```

연습 문제 4.   
1 ~ 100 까지의 숫자중에서   
짝수의 합과 홀수의 합을 모두 출력해보자!

```java
int n = 1;
        int a = 0;//짝수의 합
        int b = 0;//홀수의 합

        while (n < 101) {
            if (n % 2 == 0) {
                a += n;
            } else if (n % 2 == 1) {
                b += n;
            }
            n++;
        }
        System.out.printf("짝수의 합=%d , 홀수의 합=%d", a, b);
```

숙제 1.   
2 ~ 77 까지 3의 배수만 출력해보자!

```java
int n = 2;
        while (n < 78) {
            if (n % 3 == 0) {
                System.out.print(n + "\t");
            }
            n++;
        }
```

숙제 2.   
1 ~ 100까지 모든 수의 합을 구해보자!

```java
int n = 1;
        int a = 0;//값을 축적하는 변수
        while (n < 101) {
            a += n;
            n++;
        }
        System.out.println("1~100까지 수의 합은 " + a);
```

숙제 3.   
1 ~ 100까지 짝수는 2의 배수는 더하고   
3의 배수는 빼보자!   
전체 합을 계산하시오.   
(6과 같이 2와 3이 되는 케이스는 더하고 뺀다 즉 0)

```java
int n = 1;
        int a = 0;
        while (n < 101) {
            if (n % 2 == 0) {
                a += n;
            } if (n % 3 == 0) {
                a -= n;
            }
            n++;
        }
        System.out.println(a);
```
{% endraw %}