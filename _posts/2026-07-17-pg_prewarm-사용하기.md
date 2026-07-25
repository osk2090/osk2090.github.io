---
layout: default
title: "pg_prewarm 사용하기"
date: 2026-07-17 12:40:01 +0900
categories: [Database]
slug: pg_prewarm-사용하기

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

{% endraw %}
