---
layout: default
title: "pg_prewarm 사용하기"
date: 2026-07-17 12:40:01 +0900
categories: [Database]
slug: pg_prewarm-사용하기
image: /images/pg_prewarm/img_1.png
---

{% raw %}

데이터베이스가 재시작되면 버퍼에 유지되고 있던 데이터들은 모두 제거되며 shared buffer에 다시 채워지기 전까지 해당 데이터에 접근하면 쿼리 성능이 떨어진다.

이때 pg_prewarm을 사용하면 수동 캐싱을 하거나 환경설정을 통해 자동 캐싱을 할 수 있다.

1. 수동 캐싱
   평소에 자주 사용하는 대량의 테이블의 데이터를 캐싱하지 않아서 디스크 엑세스로 인해 성능저하가 예상이 된다면 수동 기능을 통해서 캐싱을 시킬수 있다.

> ## 결과
> 
> | 실행              | 결과                   | 의미                                          |
> | --------------- | -------------------- | ------------------------------------------- |
> | 1회차             | `read=4480`          | shared_buffers에 아무것도 없음. 실제 디스크에서 읽음        |
> | 2회차             | `hit=33 / read=4447` | 반복해도 캐시가 안 채워짐 (링 버퍼 전략). OS 페이지 캐시에서 읽었을 것 |
> | 3회차 (prewarm 후) | `hit=4480`           | 100% shared_buffers 적중                      |
> 
> **핵심 3가지**
> 
> 1. **`read` ≠ 디스크 I/O** — "shared_buffers에 없었다"는 뜻일 뿐. 뒤에 OS 페이지 캐시가 있어서 실제 디스크까지 안 갔을 수 있음. 구분하려면 `track_io_timing = on`.
> 
> 2. **큰 테이블 Seq Scan은 반복해도 캐시가 안 쌓인다** — 테이블이 `shared_buffers / 4`보다 크면 256KB 링 버퍼만 재사용. 버그가 아니라 다른 쿼리의 캐시를 보호하려는 의도된 동작. 단, **이미 캐시에 있는 블록은 정상적으로 hit** 되므로 prewarm 효과는 유지됨.
> 
> 3. **해법** — 즉시 채우려면 `pg_prewarm`, 계속 유지하려면 `shared_buffers`를 테이블 크기의 4배 이상으로. 재시작 후 자동 복원은 autoprewarm.
> 
> **캐싱 명령**
> 
> ```sql
> create extension pg_prewarm;
> 
> select pg_prewarm('public.tb_warm');
> ```
> 
> 두 번째 인자를 생략하면 기본값이 `'buffer'`라서 `pg_prewarm('public.tb_warm', 'buffer')`와 동일하게 shared_buffers까지 적재됩니다.
> 
> **확인 명령**
> 
> ```sql
> SELECT count(*) FROM pg_buffercache
> WHERE relfilenode = pg_relation_filenode('tb_warm');
> ```

2. 자동 캐싱
   pg_prewarm.autoprewarm 기능을 사용하면 shared buffer 영역에 있는 페이지들을 자동으로 미리 워밍업할 수 있다. 그로 인해 디스크IO에 대한 비용을 절감시킬 수 있다. 해당 기능을 적용하면 재시작이 필요하다.

```
postgresql.conf 파일 설정
shared_preload_libraries = 'pg_prewarm' -- 서버가 시작될때 로드해야되는 라이브러리 설정
pg_prewarm.autoprewarm = true -- 작업자 실행 여부,기본값 true, 변경시 재시작 필요
pg_prewarm.autoprewarm_interval = 300s -- 파일변경에 대한 시간간격 설정
```

위의 설정을 하면 autoprewarm master 백그라운드 프로세스가 생성되어 autoprewarm_interval 설정값에 따라 shared-buffer 영역에 있는 데이터들을 autoprewarm.blocks 파일에 저장한다.

정상 종료시에도 저장하며 실제 데이터는 저장하지 않아서 파일이 작다.

재시작 되면 설정대로 데이터 복원을 시작한다.

```
[Master]  autoprewarm.blocks 읽기
             ↓
          목록 정렬(정렬하는 이유는 순서대로 읽어야지 sequential I/O 적용됨)
             ↓
[Worker]  shared_buffers로 블록 로드
             ↓
          Worker 종료 → Master는 다시 주기적 저장 모드로
```

autoprewarm.blocks 파일을 수동으로 변경하는 법이 있는데

```
select autoprewarm_dump_now();
```

![](/images/pg_prewarm/img_1.png)

위의 쿼리를 날리고 volumes로 지정된 디렉토리로 이동하면 아래와 같이 autoprewarm.blocks 파일이 생긴것을 볼 수 있다.

![](/images/pg_prewarm/img_2.png)

해당 파일을 확인해보면

![](/images/pg_prewarm/img_3.png)

사진과 같이 텍스트 형식으로 저장된다. 해당 데이터는 데이터베이스 id, 테이블 스페이스 id, 파일 id, 포크, 세그먼트 값들을 볼 수 있다.

근데 나는 여기서 실제로 맵핑된 값인지 보고 싶어서 쿼리를 이용해서 실제 데이터인지 확인해봤다.

(모자이크된 값들은 실제 내가 테스트하는 테이블이 아닌 pg에서 관리하는 데이터라서 포커스를 내가 만든 테이블을 위해 모자이크했다.)

![](/images/pg_prewarm/img_4.png)

autoprewarm.blocks 파일에서 확인한 값과 위에서 쿼리로 확인한 값을 비교해보면

데이터베이스 id, 테이블 스페이스 id값이 같은것을 보면 캐싱된 데이터를 백업하고 있는것을 알 수 있다.

이제 auto prewarm이 적용되는지 테스트를 시작하기 전에 db를 재시작하여 shared-buffer영역이 초기화 되었는지 확인한다.

![](/images/pg_prewarm/img_5.png)

volumes로 지정된 디렉토리로 이동해서 postgresql.conf 파일중에서 아래 키값들을 추가한다.

![](/images/pg_prewarm/img_6.png)

첫째줄 주석과 같이 해당 키값이 변경되면 재시작이 필요하다고 써있다.

다시 db를 재시작하면 autoprewarm.blocks 파일이 생성된 것을 확인할 수 있다. 근데 나는 위에서 먼저 테스트 했기 때문에 해당 파일이 이전에 생성되었을 것이다.

![](/images/pg_prewarm/img_7.png)

위의 쿼리를 날렸을때 결과를 보면 디스크에서 데이터들을 읽었음을 알 수 있다.

![](/images/pg_prewarm/img_8.png)

해당 쿼리를 날려서 autoprewarm.blocks 파일을 수동으로 업데이트 했다.

![](/images/pg_prewarm/img_9.png)

db를 재시작하고 캐싱된 데이터 갯수를 조회했는데 결과를 보면 직접 캐싱하지 않아도 서버가 재시작되면 자동으로 캐싱되는것을 알 수 있다.

{% endraw %}
