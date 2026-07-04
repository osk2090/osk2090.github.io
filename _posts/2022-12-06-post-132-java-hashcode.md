---
layout: default
title: "자바의 hashCode()와 equals() 규약, 그리고 함께 오버라이딩해야 하는 이유"
date: 2022-12-06 13:13:20 +0900
categories: [Java]
slug: post-132-java-hashcode
---

자바에서 객체의 논리적 동등성을 비교하기 위해 반드시 이해해야 하는 두 메서드가 바로 `equals()`와 `hashCode()`입니다. 자바 기본 라이브러리인 Object 클래스에 정의되어 있으며 모든 자바 객체가 상속받습니다. 이번 포스팅에서는 `hashCode()`의 기본적인 특성과 함께, 왜 이 두 메서드를 오버라이딩할 때 세트로 반드시 함께 구현해야 하는지 그 중요성과 원리에 대해 자세히 다뤄보겠습니다.

---

## 1. hashCode()의 기본 개념

Object 클래스 수준에서 정의된 기본 `hashCode()`는 객체의 **메모리 주소값**을 기반으로 고유한 정수 해시값을 생성하여 반환합니다.

### 인스턴스 주소 기반 해시값 비교 예제
```java
Person person1 = new Person("osk");
Person person2 = person1;
Person person3 = new Person("osk");

System.out.println(person1.hashCode()); // 918221580
System.out.println(person2.hashCode()); // 918221580 (같은 주소)
System.out.println(person3.hashCode()); // 2055281021 (새로 할당된 다른 주소)
```
* `person1`과 `person2`는 동일한 힙 메모리상의 인스턴스를 가리키므로 해시값 정수가 일치합니다.
* `person3`은 속성(`name="osk"`) 값은 동일할지언정, `new` 키워드로 힙 영역의 다른 위치에 개별적으로 할당된 인스턴스이므로 다른 정수값이 출력됩니다.

### 문자열(String) 객체의 hashCode()
이와 다르게 자바의 `String` 클래스는 이미 내부적으로 `hashCode()`를 문자열의 리터럴 내용 기반으로 작동하도록 오버라이딩해 두었습니다.
```java
String name1 = "osk";
String name2 = "osk";
System.out.println(name1.hashCode()); // 110343
System.out.println(name2.hashCode()); // 110343
```
문자열은 메모리 위치가 다르더라도 문자열 내 문자 배열(char array) 구성이 똑같다면 동일한 정수값을 반환하여 데이터 동등성을 보장해 줍니다.

---

## 2. 동일성(Identity) vs 동등성(Equality)

자바에서 두 객체를 비교할 때 이 두 개념의 분리가 매우 중요합니다.

* **동일성 (`==` 연산자)**: 두 참조 변수가 물리적으로 **동일한 메모리 주소(인스턴스)**를 가리키고 있는지 비교합니다.
* **동등성 (`equals()` 메서드)**: 두 객체가 가리키는 주소는 다를지라도, 내포하고 있는 정보나 **논리적 데이터 내용**이 같은지 비교합니다.

우리가 커스텀 클래스(예: `Person`)를 만들 때 두 객체의 내부 필드 값이 같으면 논리적으로 동등한 객체로 판단하고 싶다면, `equals()` 메서드를 적절히 재정의해야 합니다.

---

## 3. equals()와 hashCode()의 공식 규약 (Java API)

자바의 대원칙 중 하나는 다음과 같은 API 규약입니다.

> **"equals(Object) 연산 결과가 true인 두 객체는 반드시 동일한 hashCode() 값을 가져야 한다."**

만약 `equals()`는 필드 값을 비교해 `true`를 반환하도록 재정의해 두고 `hashCode()`는 그대로 내버려 두면, 주소가 다른 두 객체는 서로 다른 해시코드를 가지게 되어 이 규약을 위반하게 됩니다.

---

## 4. 규약을 위반할 때 발생하는 컬렉션(Collection) 버그

규약 위반이 서비스에 미치는 영향은 `HashMap`이나 `HashSet`처럼 **해시 알고리즘을 사용하는 자료구조**에 객체를 저장할 때 치명적인 버그로 나타납니다.

### 문제 상황 재현
`equals()`만 재정의하고 `hashCode()`를 재정의하지 않은 `Person` 객체를 사용해 봅니다.
```java
Map<Person, String> map = new HashMap<>();
Person p1 = new Person("osk");
map.put(p1, "개발자 버즈");

// p1과 논리적으로 완벽하게 똑같은 정보를 가진 p2를 생성합니다.
Person p2 = new Person("osk");
String value = map.get(p2); 

System.out.println(value); // null이 출력됩니다!
```

### 왜 찾지 못할까? (HashMap의 검색 매커니즘)
`HashMap`에서 `get(key)`을 시도할 때 내부는 다음 순서로 탐색을 수행합니다.
1. **해시 버킷 위치 찾기**: 전달받은 `key`의 `hashCode()`를 먼저 호출해 배열 버킷 번호를 찾습니다.
2. **논리적 동등성 검사**: 같은 버킷 번호 내에 등록된 노드들을 순회하며 `equals()`를 수행해 결과가 `true`인 것을 골라냅니다.

위 코드에서 `p1.hashCode()`와 `p2.hashCode()`는 다른 주소값을 쓰기 때문에 서로 완전히 다른 해시 정수가 리턴됩니다. 결국 `HashMap`은 `p2`를 엉뚱한 해시 버킷에서 열심히 찾다가 데이터가 존재하지 않는다는 결론을 내리고 `null`을 반환하게 되는 것입니다.

---

## 5. 결론 및 올바른 오버라이딩

이러한 문제를 예방하기 위해, IDE에서 제공하는 자동 완성(Generator) 기능이나 롬복의 `@EqualsAndHashCode`, 혹은 자바 7부터 지원하는 `Objects.hash()`를 이용하여 두 메서드를 일관되게 쌍으로 오버라이딩해 주어야 합니다.

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    Person person = (Person) o;
    return Objects.equals(name, person.name);
}

@Override
public int hashCode() {
    return Objects.hash(name);
}
```

안정적인 자바/스프링 시스템 구축을 원하신다면 커스텀 객체를 컬렉션에 활용할 때 항상 `equals()`와 `hashCode()`의 관계를 상기하며 설계하시길 바랍니다.