---
layout: default
title: "MySQL InnoDB B+Tree 페이지 분할(Page Split)과 .ibd 파일 구조 분석"
date: 2024-12-26 14:47:14 +0900
categories: [Database]
slug: innodb-btree-page-split-ibd-structure
image: /images/148/img.png
---
{% raw %}

![](/images/148/img.png)

MySQL InnoDB 스토리지 엔진은 모든 테이블 데이터를 **B+Tree 구조의 클러스터드 인덱스(Clustered Index)** 형태로 저장하며, 실제 디스크 상의 데이터는 16KB 단위의 **페이지(Page)**로 구분되어 `.ibd` 단일 테이블스페이스 파일에 기록됩니다.

이 글에서는 테이블 데이터와 세컨더리 인덱스(Secondary Index)가 증가함에 따라 발생되는 **InnoDB 페이지 분할(Page Split)** 메커니즘과 `.ibd` 파일 내부 구조의 물리적 변화를 상세히 분석합니다.

---

## 1. 테이블 최초 생성 및 인덱스 초기 할당

InnoDB 테이블을 생성하면 해당 테이블의 `.ibd` 파일 내부에는 클러스터드 인덱스를 위한 **루트 페이지(Root Page, Page No. 3)**가 최초로 할당됩니다.

```sql
CREATE TABLE tb_demo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    created_at DATETIME
) ENGINE=InnoDB;
```

![](/images/148/img_1.png)

- **클러스터드 인덱스 (Clustered Index)**: 초기에는 Root Page 1개만 존재하며, 데이터 개수가 적을 때는 Root Page가 곧 Leaf Page 역할(Data Record 저장)까지 겸합니다.
- **세컨더리 인덱스 (Secondary Index)**: `CREATE INDEX` 명령으로 보조 인덱스를 추가하면, 해당 인덱스만을 위한 별도의 B+Tree Root Page가 `.ibd` 파일 내에 추가 할당됩니다.

---

## 2. 데이터 증가와 페이지 분할 (Page Split)

16KB 크기의 1개 InnoDB 페이지는 데이터 크기 및 가변길이 컬럼 구조에 따라 약 수백 개~수천 개의 레코드를 수용할 수 있습니다. 

![](/images/148/img_2.png)

### 327개 로우 추가 시 발생하는 B+Tree 분할 과정

1. **페이지 포화 (Page Full)**: 단일 Root Page에 더 이상 레코드를 추가할 수 없는 상태에 도달합니다.
2. **새 Leaf Page 할당**: InnoDB는 새로운 16KB Leaf Page 2개를 신규 할당합니다 (예: Page No. 4, Page No. 5).
3. **데이터 이관 및 Root 승격**: 기존 Root Page에 있던 데이터의 50%(또는 순차 저장 시 15/16)를 신규 Leaf Page로 할당/이동(Split)하고, 기존 Root Page는 Leaf Page들의 키 범위와 주소를 가리키는 **Non-Leaf(Internal) Node**로 변환됩니다.

```
                  ┌──────────────────────┐
                  │    Root Page (No.3)  │  <-- Key range pointer
                  └──────────┬───────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
 ┌─────────────────────┐           ┌─────────────────────┐
 │ Leaf Page A (No.4)  │ <───────> │ Leaf Page B (No.5)  │  <-- Double Linked List
 └─────────────────────┘           └─────────────────────┘
```

---

## 3. 순차 키(Sequential Key) vs 무작위 키(Random Key) 삽입 시 페이지 분할 차이

![](/images/148/img_3.png)

![](/images/148/img_4.png)

1. **AUTO_INCREMENT (순차 키 삽입)**:
   - 레코드가 항상 페이지 오른쪽 끝에 추가되므로, 페이지가 가득 찼을 때 50:50이 아닌 **15:16 비율(Page Fill Factor ~93.75%)**로 효율적인 분할이 일어납니다.
   - 단방향 분할을 통해 빈 공간 낭비 없이 메모리와 디스크 효율을 극대화합니다.

2. **UUID / Random Hash Key (무작위 키 삽입)**:
   - 무작위 위치에 데이터가 삽입되므로 기존 페이지 중간에 빈 공간을 만들기 위해 **50:50 분할**이 번번이 일어납니다.
   - 이로 인해 **페이지 단편화(Fragmentation)**가 발생하고 `.ibd` 파일 크기가 불필요하게 커지며(B-Tree Bloat), 이중 연결 리스트(Doubly Linked List) 재정렬 및 디스크 I/O 부하가 급증합니다.

---

## 💡 요약 및 실무 팁

- InnoDB의 모든 테이블과 세컨더리 인덱스는 **16KB B+Tree 페이지** 단위로 저장되며, 레코드가 찰 때마다 **Page Split**을 거쳐 계층적 나무 구조를 형성합니다.
- 대량 데이터 Write 성능을 최적화하고 `.ibd` 파일 용량 팽창을 막으려면 Primary Key로 **AUTO_INCREMENT나 순차적 시간 기반 ID(TSID, ULID)**를 채택하는 것이 가장 효과적입니다.
{% endraw %}