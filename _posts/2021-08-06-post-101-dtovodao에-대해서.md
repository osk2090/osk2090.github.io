---
layout: default
title: "DTO,VO.DAO에 대해서"
date: 2021-08-06 14:48:31 +0900
categories: [Etc]
slug: post-101-dtovodao에-대해서
render_with_liquid: false
---

### DAO(Data Access Object)

데이터베이스의 data에 접근하기 위한 객체이며

데이터베이스 접근을 하기 위한 로직과 비즈니스 로직을 분리하기 위해서 사용한다.

사용자는 자신이 필요한 interface를 DAO에게 던지고

이 interface를 구현한 객체를 사용자에게 편리하게 사용할 수 있도록 반환한다.

DAO는 데이터베이스와 연결할 Connection까지 설정되어 있는 경우가 많다.

그래서 현재 쓰이는 MyBatis 등을 사용할 경우 커넥션풀까지 제공되고 있기 때문에 DAO를 별도로 만드는 경우는 드물다.

```java
public interface ClubDao {

    int insert(Club club) throws Exception;

    Club findByNo(int no) throws Exception;

    int update(Club club) throws Exception;

    int delete(int cno) throws Exception;
.
.
.
```

### DTO(Data Transfer Object)

VO라고도 표현하며 계층 간 데이터 교환을 위한 자바 빈즈(Java Beans)이다.

데이터베이스 레코드의 데이터를 매핑하기 위한 데이터 객체를 말한다.DTO는 보통 로직을 가지고 있지 않고 data와 그 data에 접근을 위한 getter/setter만 가지고 있다.

정리하면 DTO는 Database에서 Data를 얻어 Service나 Controller 등으로 보낼 때 사용하는 객체를 말한다.

```java
@Data
public class Club {
    private int no;//클럽번호

    private Member writer;
    private List<Member> members;

    private String arrive;//도착지
    private String theme;//테마
    private String title;//제목
    private String content;//내용
    private Date startDate;//가는날
    private Date endDate;//오는날
    private int total;//인원수
    private int nowTotal;//현재참여 인원수
    private List<Object> photos;//사진
    .
    .
    .
```

위의 클래스를 보면 롬복을 이용하여 getter/setter가 생성된다.

여기서 중요한 것은 Property(프로퍼티) 개념인데 자바는 Property가 문법적으로 제공되지 않는다.

자바에서 Property라는 개념을 사용하기 위해 지켜야 할 약속이 있다.

setter/getter에서 set과 get 이후에 나오는 단어가 Property라고 약속하는 것이다.

그래서 위 클래스에서 프로퍼티는 name과 age이다.

중요한 것은 프로퍼티가 멤버 변수 name,age로 결정되는 것이 아닌 getter/setter로 프로퍼티(데이터)를 표현한다는 것이다.

자바는 다양한 프레임워크에서 데이터 자동화 처리를 위해 리플렉션 기법을 사용하는데

데이터 자동화 처리에서 제일 중요한 것은 표준 규격이다.예를 들어 위 클래스 DTO에서 프로퍼티가 name,age라면

name,age의 키값으로 들어온 데이터는 리플렉션 기법으로 setter를 실행시켜 데이터를 넣을 수 있다.

중요한 것은 우리가 setter를 요청하는 것이 아닌 프레임워크 내부에서 setter가 실행된다는 점이다.

그래서 layer간(특히 서버=>뷰로 이동 등)에 데이터를 넘길 때 DTO를 쓰면 편하다는 것이 이런 이유 때문이다.

뷰에 있는 form에서 name 필드 값을 프로퍼티에 맞춰 넘겼을 때 받아야 하는 곳에서 일일이 처리하는 것이 아니라

name 속성의 이름과 매칭되는 프로퍼티에 자동적으로 DTO가 인스턴스화되어 PersonDTO를 자료형으로 값을 받을 수 있다.

### VO(Value Object)

VO는 DTO와 혼용해서 쓰이긴 하지만 미묘한 차이가 있다.

VO는 값 오브젝트로써 값을 위해 쓰인다.자바는 값 타입을 표현하기 위해 불변 클래스를 만들어 사용하는데

불변이라는 것은 read only 특징을 가진다.

DTO와 VO의 공통적음 넣어진 데이터를 getter를 통해 사용하므로 주 목적은 같으나 DAO는 가변적인 성격을 가진 클래스이며(setter 활용) 그에 비해 VO는 불변의 성격을 가졌기에 차이점이 있다.