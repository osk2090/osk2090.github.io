---
layout: default
title: "[MyBatis/SQL] 입력 파라미터를 결과로 다시 반환(Echoing)하는 쿼리 및 활용법"
date: 2021-08-05 17:28:45 +0900
categories: [Database]
slug: post-099-sql파라미터를-다시-리턴-하는-query
---

데이터베이스에서 조회 쿼리(SELECT)를 실행할 때, 테이블에 저장된 실제 데이터를 가져오는 것뿐만 아니라 **쿼리의 입력 파라미터로 전달된 값을 SELECT 결과 컬럼에 그대로 포함하여 다시 반환(Echoing)**해야 할 때가 있습니다. 이번 포스팅에서는 이러한 파라미터 리턴 쿼리의 SQL 문법과 실무적인 필요성 및 자바 코드 측면에서의 활용 예제를 정리해 보겠습니다.

---

## 1. 쿼리 파라미터를 다시 리턴한다는 것의 의미

일반적으로 SELECT 쿼리는 테이블의 물리적 컬럼값을 읽어옵니다. 하지만 SQL 표준에서는 고정된 리터럴이나 입력 바인딩 파라미터 자체를 조회 결과의 열(Column)로 출력할 수 있도록 지원합니다.

### SQL 예시
```sql
-- 파라미터 바인딩(? 혹은 #{keyword})을 결과 컬럼으로 반환
SELECT ? AS search_keyword, info, amount
FROM trade_history
WHERE trade_accnt = ?;
```
위 쿼리를 실행하면 데이터베이스는 매칭된 행들의 `info`와 `amount` 컬럼을 조회함과 동시에, 입력했던 첫 번째 파라미터를 `search_keyword`라는 별칭(Alias) 컬럼으로 결과 행마다 똑같이 복사하여 응답 결과 셋(ResultSet)에 실어 보내 줍니다.

MyBatis 프레임워크 예시로는 다음과 같이 표현할 수 있습니다.
```xml
<select id="findByTradeAccntAndAmount" resultType="TradeResultDto">
    SELECT 
        #{keyword} AS keyword,
        info,
        amount
    FROM trade_history
    WHERE trade_accnt = #{accnt}
</select>
```
`#{keyword}`로 전달된 값이 데이터베이스 단에서 해석되어 조회 데이터 결과의 `keyword` 필드에 동적으로 세팅되어 자바의 DTO로 그대로 바인딩됩니다.

---

## 2. 실무에서 이 기법이 필요한 이유

단순한 데이터 조회의 경우 자바 애플리케이션 단에 이미 파라미터 값이 존재하므로 필요성이 낮아 보일 수 있지만, 다음과 같은 상황에서 매우 높은 효율성을 보입니다.

### 1) 다량의 파라미터 리스트 루프 매핑
애플리케이션에서 다수의 파라미터 세트 목록을 순회하며 개별 조회를 수행하는 상황을 가정해 보겠습니다.
```java
public void printTradeAccntAndAmount() {
    List<InfoRequest> requests = getRequestList();
    for (InfoRequest req : requests) {
        // 개별 요청 정보(req)를 전달해 쿼리를 실행합니다.
        TradeResultDto result = tradeDao.findByTradeAccntAndAmount(req);
        
        // 반환받은 데이터와 원래 요청값(파라미터)을 결합해 로깅하거나 비즈니스 로직을 처리합니다.
        System.out.println("요청계좌: " + result.getKeyword() + " -> 결과액수: " + result.getAmount());
    }
}
```
데이터베이스 조회 결과가 비어 있거나 다중 행이 리턴될 때, 반환된 각 행(DTO)들이 원래 어떤 파라미터 요청(예: 검색 키워드, 특정 타겟 식별자 등)에 대한 결과물인지 DTO 내부 정보만으로 직관적으로 판별하고 매핑할 수 있게 되어 코드가 매우 깔끔해집니다.

### 2) UNION ALL을 이용한 다중 조회 일괄 처리
여러 쿼리를 `UNION ALL`로 묶어 한 번에 실행하면서 결과 셋이 각각 어떤 검색 조건군에 속하는 결과 데이터인지 구분자를 쿼리 레벨에서 파라미터값으로 꽂아 반환받을 때 유용합니다.

---

## 3. MyBatis 구현 시 주의할 점

MyBatis 환경에서 파라미터값을 결과 셋으로 다시 매핑할 때 아래 사항들을 인지해 두어야 오류를 방지할 수 있습니다.

1. **별칭(Alias) 지정 필수**: 반드시 `as keyword` 혹은 `as main`과 같이 DTO 클래스의 필드명과 일치하는 컬럼 별칭을 선언해 주어야 자바 빈즈 규약에 의해 자동 바인딩이 수행됩니다.
2. **DBMS 별 바인딩 타스킹 타입 체크**: 일부 DBMS(예: PostgreSQL)는 고정 리터럴이나 바인딩 값을 SELECT 절에 타입 캐스팅 없이 올리면 SQL 파서 에러가 날 수 있으므로 필요시 명시적 타입 변환(`CAST(#{keyword} AS VARCHAR)`)을 적용해 주어야 합니다.

자주 쓰이지 않는 기능처럼 보일 수 있지만, 복잡한 통계 계산 쿼리나 조회 조건을 결과 리스트와 묶어서 단일 리스폰스 DTO로 화면 단에 바로 내려주어야 할 때 매우 가독성 높은 설계를 도와주는 유용한 쿼리 기법입니다.