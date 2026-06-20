---
layout: default
title: "InnoDB 클러스터링 및 세컨더리 인덱스: 페이지 분할(.ibd파일)"
date: 2024-12-26 14:47:14 +0900
categories: [Database]
slug: post-148-innodb-클러스터링-및-세컨더리-인덱스-페이지-분할ibd파일
image: /images/148/img.png
---
{% raw %}

![](/images/148/img.png)

테이블 최소 생성시

여기서 볼수 있는 포인트는 인덱스도 페이지로 관리된다.

![](/images/148/img_1.png)

테이블 최초생성후 세컨더리 인덱스 생성시

세컨더리 인덱스도 별도의 페이지로 추가됨을 확인할 수 있다.

![](/images/148/img_2.png)

327개 로우 추가시

클러스터링 인덱스는 데이터가 증가함에 따라 2개의 페이지(leaf page)로 분리되고 기존의 인덱스(root page)는 새로 분리된 2개의 페이지에 대한 주소값을 갖는다.

![](/images/148/img_3.png)

위에서 1개 로우 추가시

![](/images/148/img_4.png)

위에서 330개 로우 추가시

![](/images/148/img_5.png)

위에서 1개 로우 추가시
{% endraw %}