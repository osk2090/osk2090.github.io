---
layout: default
title: "Oracle, Postgresql, Mysql(InnoDB)"
date: 2024-11-30 16:00:33 +0900
categories: [Database]
slug: post-146-oracle-postgresql-mysqlinnodb
image: /images/146/img.png
---

### Oracle

1. 오라클에서 트랜잭션이 커밋되면 트랜잭션 테이블의 undo 세그먼트 헤더의 state 값을 10(active) -> 9(committed) 처리
2. scn(system change number)에는 현재 커밋시점의 scn으로 업데이트
3. 그 외 ITL(interested transcation list)의 항목들중 일부 컬럼들을 commit시점의 데이터로 정리하는데 이를 블록 클린 아웃
4. 만약 클린아웃할 항목들이 많으면 일단 메모리에 있는 일부만 우선 클린아웃을 하고 나머지들은 해당 데이터를 select할때 동작한다. 이를 dealay block cleanout이라고 한다. 해당 기능은 디비에 과부하를 줄이기 위해 동작한다.

### Postgresql

1. 레코드마다 튜플헤더가 존재하는데 이중에 infomask컬럼의 첫번째 byte(하위 4bits)로 해당 레코드의 트랜잭션 상태값을 표현
2. postgresql은 delete 커맨드가 들어오면 이전 데이터는 delete, 새로운 데이터 insert 처리하여 update하여 insert된 데이터와 새로 insert된 byte는 다름

직접 로컬에서 확인해본결과 일단 postgresql에 확장프로그램을 깔아서 t\_infomask를 볼수 있도록 한다.

```sql
-- 익스텐션 설치
CREATE EXTENSION pageinspect;
-- infomask 식별할수 있는 테이블생성
CREATE TABLE infomask_flags (
                                flag_name text,
                                flag_bits bit(16)
);
-- infomask컬럼의 데이터를 보고 상태값을 볼수 있는 데이터 입력
INSERT INTO infomask_flags VALUES
                               ('HEAP_HASNULL',        B'0000000000000001'),
                               ('HEAP_HASVARWIDTH',    B'0000000000000010'),
                               ('HEAP_HASEXTERNAL',    B'0000000000000100'),
                               ('HEAP_HASOID',         B'0000000000001000'),
                               ('HEAP_XMAX_KEYSHR_LOCK', B'0000000000010000'),
                               ('HEAP_COMBOCID',       B'0000000000100000'),
                               ('HEAP_XMAX_EXCL_LOCK', B'0000000001000000'),
                               ('HEAP_XMAX_LOCK_ONLY', B'0000000010000000'),
                               ('HEAP_XMIN_COMMITTED', B'0000000100000000'),
                               ('HEAP_XMIN_INVALID',   B'0000001000000000'),
                               ('HEAP_XMAX_COMMITTED', B'0000010000000000'),
                               ('HEAP_XMAX_INVALID',   B'0000100000000000'),
                               ('HEAP_XMAX_IS_MULTI',  B'0001000000000000'),
                               ('HEAP_UPDATED',        B'0010000000000000'),
                               ('HEAP_MOVED_OFF',      B'0100000000000000'),
                               ('HEAP_MOVED_IN',       B'1000000000000000');
-- 데이터 출력
SELECT
    hpi.t_ctid,
    hpi.t_xmin,
    hpi.t_xmax,
    hpi.t_infomask,
    string_agg(ifl.flag_name, ', ') AS set_flags
FROM
    heap_page_items(get_raw_page('test_table', 0)) AS hpi
        JOIN infomask_flags AS ifl
             ON (hpi.t_infomask::bit(16) & ifl.flag_bits)::integer::boolean
GROUP BY
    hpi.t_ctid, hpi.t_xmin, hpi.t_xmax, hpi.t_infomask;
```

위의 커맨드를 동작시키고 일단 데이터 한개를 insert 했을때이다.

![](/images/146/img.png)

xmin 컬럼에 값이 있고 xmax에 값이 없는것을 보니 이건 insert된 데이터인것을 확인할수 있다.

그리고 set-flag를 보면 hasvarwidth는 해당 레코드에 가변 길이 데이터(예: VARCHAR)가 포함되어 있다는 것을 알수 있다.

그리고 xmin-committed는 해당 데이터는 insert하여 comit이 된 데이터라는 점

xmax-invalid인것은 아직 해당 레코드가 update or delete 된 것이 아니라는 점을 알수가 있다.

이제 데이터를 업데이트 해보자

![](/images/146/img_1.png)

ctid가 같은 값인걸 보니 한 트랜잭션이라는 것을 알수 있다.

xmin=837인 레코드가 새로 입력된 데이터이고 그 이전의 값은 이전 레코드라는 것이다.

두 레코드의 set-flag를 보면 이전의 데이터와 달라진 점을 알수 있다.

이전 레코드는 xmin-committed만 남았고 새로운 레코드는 xmax-invalid, updated 되었다는 것을 알수 있다.

정리하면 두개의 레코드로 알수 있는 점은 수정전의 데이터와 업데이트된 데이터는 존재하고 수정전의 데이터는 xmax값이 있기때문에 vaccum을 동작시키면 타겟팅이 되어 해당 로우는 물리적으로도 삭제되는 데이터라는 점이다.

mysql(InnoDB)

1. 트랜잭션이 커밋되면 해당 커밋시점의 max-trx-id를 언두 블록의 trx-no 컬럼에 저장
2. 롤백 세그먼트 히스토리 리스트에 커밋된 언두 블록을 등록
3. trx-sys에 active-trx 리스트중에 커밋된 trx-sturcture를 제외시켜 갱신