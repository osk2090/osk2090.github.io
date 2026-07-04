---
layout: default
title: "Kafka-AWS 연동"
date: 2021-10-17 02:53:06 +0900
categories: [Kafka]
slug: post-126-kafka-aws-연동
---

```bash
$ https://archive.apache.org/dist/kafka/3.0.0/kafka_2.12-3.0.0.tgz//자바 설치
$ java -version
$ wget https://archive.apache.org/dist/kafka/3.0.0/kafka_2.12-3.0.0.tgz//카프카 관련 파일 다운로드
$ tar xvf kafka_2.12-3.0.0.tgz//압축해제
$ ll
$ cd kafka_2.12-3.0.0
```

#### 카프카 브로커 힙 메모리 설정

카프카 브로커를 실행하기 위햐서는 힙 메모리 설정이 필요하다.

카프카 브로커는 레코드의 내용은 페이지 캐시로 시스템 메모리를 사용하고 나머지 객체들은 힙 메모리에 저장하여 사용한다는 특징이 있다.이러한 특징으로 카프카 브로커를 운영할 때 힙 메모리를 5GB 이상으로 설정하지 않는 것이 일반적이다.실습이나 테스트 목적이라면 힙 메모리를 작게 설정해서 실행해도 무관하다.

카프카 패키지의 힙 메모리는 카프카 브로커는 1G,주키퍼는 512MB로 기본 설정되어 있다.실습용으로 생성한 인스턴스(t2.mircro)는 1G 메모리를 가지고 있으므로 카프카 브로커와 주키퍼를 기본 설정과 함께 동시에 실행하면 1.5G 메모리가 필요하기 때문에 Cannot allocate memory 에러가 출력되면서 실행되지 않는다.

이를 해결하기 위해 export 명령어를 사용해서 힙 메모리 사이즈를 미리 환경변수로 지정해서 실행해야 주키퍼와 카프카 브로커를 실행할 때 힙 메모리 에러가 발생하지 않는다.만약 t2.micro 인스턴스 서버가 아니라 1.5GB 이상 메모리를 가진 EC2 인스턴스를 실습용으로 실행했다면 환경변수를 지정하지 않아도 된다. 실제 운영환경에서도 마찬가지로 카프카 브로커 실행 시 힙 메모리를 지정하고 싶다면 KAFKA\_HEAP\_OPTS 환경변수를 힙 메모리 사이즈와 함께 지정하면 된다.환경변수를 export 명령어로 선언하고 정상적으로 설정되었는지 확인하려면 echo 명령어와 환경변수를 넣으면 된다.

```bash
export KAFKA_HEAP_OPTS="Xmx400m -Xms400m"
echo $KAFKA_HEAP_OPTS
//-Xmx400m -Xms400m
```

터미널에서 사용자가 입력한 KAFKA\_HEAP\_OPTS 환경변수는 터미널 세선이 종료되고 나면 다시 초기화되어 재사용이 불가하다.이를 해결하기 위해 KAFKA\_HEAP\_OPTS 환경변수 선언문을 ~/.bashrc 파일에 넣으면 된다.실습 중인 Amazon Linux AMI 인스턴스에는 bash 쉘이라고 불리는 유닉스 쉘을 사용하는데 ~/bashrc파일은 bash 쉘이 실행될 때마다 반복적으로 구동되어 적용되는 파일이다.

```bash
vi ~/.bashrc --->편집기로 이동
--------------------
export KAFKA_HEAP_OPTS="Xmx400m -Xms400m" --->환경변수 입력 후 :wq 저장후 종료
--------------------
source ~/.bashrc --->환경변수 적용
echo $KAFKA_HEAP_OPTS ---->해당 환경변수 출력
//Xmx400m -Xms400m
```

카프카 브로커 실행 시 메모리를 설정하는 부분은 카프카를 실행하기 위햐서 사용하는 kafka-server-start.sh 스크립트 내부에서 확인할 수 있다.

```bash
cat bin/kafka-server-start.sh --->해당 파일을 들어가지 않고도 볼 수 있다.
--------------------------------
#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ $# -lt 1 ];
then
	echo "USAGE: $0 [-daemon] server.properties [--override property=value]*"
	exit 1
fi
base_dir=$(dirname $0)

if [ "x$KAFKA_LOG4J_OPTS" = "x" ]; then
    export KAFKA_LOG4J_OPTS="-Dlog4j.configuration=file:$base_dir/../config/log4j.properties"
fi

if [ "x$KAFKA_HEAP_OPTS" = "x" ]; then
    export KAFKA_HEAP_OPTS="-Xmx1G -Xms1G"
fi

EXTRA_ARGS=${EXTRA_ARGS-'-name kafkaServer -loggc'}

COMMAND=$1
case $COMMAND in
  -daemon) ---> -daemon 옵션을 설정하면 백그라운드에서 실행되도록 해준다.
    EXTRA_ARGS="-daemon "$EXTRA_ARGS
    shift
    ;;
  *)
    ;;
esac

exec $base_dir/kafka-run-class.sh $EXTRA_ARGS kafka.Kafka "$@"
--------------------------------
```

#### 카프카 브로커 실행 옵션 설정

config 폴더에 있는 server.properties 파일에는 카프카 브로커가 클러스터 운영에 필요한 옵션들을 지정할 수 있다.

여기서는 실습용 카프카 브로커를 실행할 것이므로 advertiesd.listener만 설정하면 된다.advertised.listener는 카프카 클라이언트 또는 커맨드 라인 툴을 브로커와 연결할 때 사용된다.현재 접속하고 있는 인스턴스의 퍼블릭 IP와 카프카 기본 코프인 9092를 PLAINTEXT://와 함께 붙여놓고 advertised.listeners를 주것에서 해제한다.

이렇게 설정한 옵션은 카프마 브로커를 실행할 때 kafka-server-start.sh 명령어와 함께 지정할 수 있다.

이미 실행되고 있는 카프카 브로커의 설정을 변경하고 싶다면 브로커를 재시작해야 하므로 신중히 설정하는것을 추천한다.

```bash
broker.id=0 --->실행하는 카프카 브로커의 번호(단 하나뿐인 번호로 설정)

#listeners=PLAINTEXT://:9092 --->카프카 브로커가 통신을 위해 열어둘 인터페이스ip,port,프로토콜

//카프카 클라이언트 또는 카프카 커맨드 라인 툴에서 접속할 때 사용하는 ip와 port 정보
advertised.listeners=PLAINTEXT://your.host.name:9092

//보안 설정 시 프로토콜 매핑을 위한 설정
#listener.security.protocol.map=PLAINTEXT:PLAINTEXT,SSL:SSL,SASL_PLAINTEXT:SASL_PLAINTEXT,SASL_SSL:SASL_SSL

//네트워크를 통한 처리를 할때 사용할 네트워크 스레드 개수 설정
num.network.threads=3

//카프카 브로커 내부에서 사용할 스레드 개수 지정
num.io.threads=8

############################# Log Basics #############################
log.dirs=/tmp/kafka-logs --->통신을 통해 가져온 데이터를 파일로 저장할 디렉토리 위치
num.partitions=1 --->파티션 개수를 명시하지 않고 토픽을 생성할 때 디폴트 파티션 갯수(파티션 갯수가 많아지면 병렬처리 데이터양이 늘어난다.)
log.retention.hours=168 --->카프카 브로커가 저장한 파일이 삭제되기까지 걸리는 시간 설정(log.retention.ms 값을 -1로 설정하면 영원히 삭제x)
log.segment.bytes=1073741824 --->카프카 브로커가 저장할 파일의 최대 크기 지정(해당 범위를 벗어나면 새로운 파일 생성)
log.retention.check.interval.ms=300000 --->카프카 브로커가 저장한 파일을 삭제하기 위해 체크하는 간격 지정
zookeeper.connect=localhost:2181 --->카프카 브로커와 연동할 주키퍼의 ip와 port 설정
zookeeper.connection.timeout.ms=18000 --->주키퍼의 세션 타임아웃 시간을 지정한다.
```

#### 주키퍼 실행

카프카 바이너리가 포함된 폴더에는 브로커와 같이 실행할 주키퍼가 준비되어 있다.분산 코디네이션 서비르슷 제공하는 주키퍼는 카프카의 클러스터 설정 리더 정보,컨트롤러 정보를 담고 있어 카프카를 실행하는 데에 필요한 필수 애플리케이션이다.주키퍼를 상용환경에서 안정하게 운영하기 위해서는 3대 이상의 서버로 구성하여 사용하지만 실습에서는 동일한 서버에 카프카와 동시에 1대만 실행시켜 사용할 수도 있다.1대만 실행하는 주키퍼를 "Quick-and-dirty single-node" 라고 부른다.즉 주키퍼를 1대만 실행하여 사용하는 것은 비정상인 운영임을 뜻하므로 실제 서비르 운영환경에서는 1대만 실행하여 사용하면 안되고,테스트 목적으로만 사용해야 한다.

-daemon 옵션과 주키퍼 설정 경로인 config/zookeeper.properties와 함께 주키퍼 시작 스크립트인 bin/zookeeper-server-start.sh를 실행하면 주키퍼를 백그라운드에서 실행할 수 있다.주키퍼가 정상적으로 실행되었느닞 jps 명령어로 확인할 수 있다.jps는 jvm 프로세스 상태를 보는 도구로서 jvm 위에서 동작하는 주키퍼의 프로세스를 확인할 수 있다.

-m 옵션과 함께 사용하면 main 메서드에 전달된 인자를 확인할 수 있고 -v 옵션을 사용하면 jvm에 전달된 인자(힙 메모리 설정 log4j 설정 등)를 함께 확인할 수 있다.만약 주키퍼 시작 스크립트를 넣었는데도 불구하고 정상적으로 실행되지 않는다면 -daemon 옵션을 제외하고 실행해보자.실행과 함께 주키퍼 로그를 확인할 수 있으므로 무엇이 문제인지 확인할 수 있다.

```bash
$ bin/zookeeper-server-start.sh -daemon config/zookeeper.properties
$ jps -vm
```

#### 카프카 브로커 실행 및 로그 확인

이제 카프카 브로커를 실행할 마지만 단계이다.-daemon 옵션과 함께 카프카 프보러를 백그라운드 모드를 실행할 수 있다.

kafka-server-start.sh 명령어를 통해 카프카 브로커를 실행한 뒤 jps 명령어를 통해 주키퍼와 브로커 프로세스의 동작 여부를 알 수 있다.그리고 tail 명령어를 통해 로그를 확인하여 카프카 브로커가 정상 동작하는 지 확인할 수 있다.카프카 브로커의 로그를 확인하는 것은 매우 중요한데,카프카 클라이언트를 개발할 때뿐만 아니라 카프카 클러스터를 운영할 때 이슈가 발생할 경우 모두 카프카 브로커에 로그가 남기 때문이다.카프카 클라이언트를 개발하여 연동할 때 정상적으로 연결되지 않거나 데이터가 전송되지 않는다면 카프카 브로커가 실행되고 있는 서버로 접속하여 로그를 확인한다면 더욱 빠르게 문제를 해결할 수 있다.

```bash
$ bin/kafka-server-start.sh -daemon config/server.properties
$ jps -m
```

### 로컬 컴퓨터에서 카프카와 통신 확인

aws ec2 인스턴스에 테스트용 카프카 브로커를 실행했고 이제 로컬 컴퓨터에서 원격으로 카프카 브로커로 명령을 내려 정상적으로 통신하는지 확인한다.카프카가 정상 동작하는지 확인하는 가장 쉬운 방법은 카프카 브로커 정보를 요청하는 것이다.

카프카 바이너리 패키지는 카프카 브로커에 대한 정보를 가져올 수 있는 kafka-broker-api-versions.sh 명령어를 제공한다.이 명령어를 통해 카프카 브로커와 정상적으로 연동되는지 확인할 수 있다.

kafka-broker-api-version.sh 명령어를 로컬 컴퓨터에서 사용하기 위해서는 로컬 컴퓨터에 카프카 바이너르 패키지를 다운로드해야 한다.패키지를 다운로드 받고 난 이후에 tar 명령어를 사용하여 압축을 풀고 bin 디렉토리에 들어가면 카프카 커맨드 라인 툴들을 확인할 수 있다.

-로컬

```bash
curl https://archive.apache.org/dist/kafka/3.0.0/kafka_2.13-3.0.0.tgz --output kafka.tgz
$ tar -xvf kafka.tgz
$ bin/kafka-broker-api-versions.sh --bootstrap-server 3.34.129.247:9092
```

#### *카프카 브로커와 로컬 커맨드 라인 툴 버전을 맞춰야 하는 이유*

*카프카 브로커로 커맨드 라인 툴 명령을 내릴 때 브로커의 버전과 커맨드 라인 툴 버전을 맞춰서 사용하는 것을 권장한다.브로커의 버전이 업그레이드됨에 따라 커맨드 라인 툴의 상세 옵션이 달라져서 버전 차이로 인해 명령이 정상적으로 실행되지 않을 수도 있기 때문이다.*

kafka-broker-api-versions.sh 명령어와 함께 --bootstrap-server에 인스턴스 ip와 9092포트를 넣으면 원격으로 카프카의 버전과 broker.id,rack 정보,각종 카프카 브로커 옵션들을 확인할 수 있다.

#### 테스트 편의를 위한 hosts 설정

hosts 파일을 설정하면 로컬 컴퓨터에서 aws ec2에 설치한 카프카 클러스터와 통신할 때 실정한 ip를 사용자 지정 문장으로 매핑하여 통신할 수 있다.맥을 포함한 유닉스 계열 운영체제에서는 /etc/hosts 파일에서 설정할 수 있고 윈도우에서는 /system32/drivers/etc/hosts 파일에서 설정할 수 있다.my-kafka를 실습용 카프카 클러스터 ip와 매핑하여 추후에는 my-kafka 호스트 이름으로 통신하도록 설정한다.ip는 카프카 브로커를 설치한 인스턴스 public ip로 설정하면 된다.

```bash
vi /etc/hosts
aws ip 주소입력 my-kafka
```

### 카프카 커맨드 라인 툴

카프카에서 제공하는 카프카 커맨드 라인 툴들은 카프카를 운영할 때 가장 많이 접하는 도구이다.커맨드 라인 툴을 통해 카프카 브로커 운영에 필요한 다양한 명령을 내릴 수 있다.카프카 클라이언트 애플리케이션을 운영할 때는 카프카 클러스터와 연동하여 데이터를 주고받는 것도 중요하지만 토픽이나 파티션 개수 변경과 같은 명령을 실행해야 하는 경우도 자주 발생한다.그렇기 때문에 카프카 커맨드 라인 툴과 각 툴별 옵션에 대해 알고 있어야 한다.카프카 브로커가 설치된 인스턴스에 ssh로 원격 접속하여 명령을 실행해도 되고,브로커에 9092(카프카 기본 설정 포트)로 접근 가능한 컴퓨터에서 명령어를 실행할 수 있다.

커맨드 라인 툴을 통해 토픽 관련 명령을 실행할 때 필수 옵션과 선택 옵션이 있다.선택 옵션은 지정하지 않을 시 브로커에 설정된 기본 설정값 또는 커맨드 라인 툴의 기본값으로 대체되어 설정된다.그러므로 커맨드 라인 툴을 사용하기 전에 현재 브로커에 옵션이 어떻게 설정되어 있는지 확인한 후에 사용하면 커맨드 라인 툴 사용 시 실수할 확률이 줄어든다.

#### kafka-topics.sh

이 커맨드 라인 툴을 통해 토픽과 관련된 명령을 실행할 수 있다.토픽이란 카프카에서 데이터를 구분하는 가장 기본적인 개념이다.마치 RDBMS에서 사용하는 테이블과 유사하다고 볼 수 있다.카프카 클러스터에 토픽은 여러 개 존재할 수 있다.토픽에는 파티션이 존재하는데 파티션 개수는 최소 1개부터 시작한다.파티션은 카프카에서 토픽을 구성하는 데에 아주 중요한 요소이다.파티션을 통해 한 번에 처리할 수 있는 데이터양을 늘릴수 있고 토픽 내부에서도 파티션을 통해 데이터의 종류를 나누어 처리할 수 있기 때문이다.

#### 토픽을 생성하는 2가지 방법

토픽을 생성하는 상황은 크게 2가지가 있다.첫번째는 카프카 컨슈머 또는 프로듀서가 카프카 브로커에 생성되지 않은 포틱에 대해 데이터를 요청할 때,그리고 두번째는 커맨드 라인 툴로 명시적으로 토픽을 생성하는 것이다.

토픽을 효과적으로 유지보수하기 위햐서는 토픽을 명시적으로 생성하는 것을 추천한다.토픽마다 처리되어야 하는 데이터의 특성이 다르기 때문이다.

토픽을 생성할 때는 데이터 특성에 따라 옵션을 다르게 설정할 수 있다.예를 들어 동시 데이터 처리량이 많아야 하는 토픽의 경우 파티션의 개수를 100으로 설정할 수 있다.단기간 데이터 처리만 필요한 경우에는 토픽에 들어온 데이터의 보관기간 옵션을 짧게 설정할 수도 있다.그러므로 토픽에 들어오는 데이터양과 병렬로 처리되어야 하는 용량을 잘 파악하여 생성하는 것이 중요하다.

#### 토픽 생성

kafka-topics.sh를 통해 토픽 관련 명령을 실행할 수 있다.--create 옵션을 사용하여 hello.kafka라는 이름을 가진 토픽을 생성할 수 있다.각 옵션이 어떤 역할을 하는지 살펴보자.

```bash
bin/kafka-topics.sh 
--create --->생성하라는 명령어
--bootstrap-server my-kafka:9092 --->토픽을 생성할 카프카 클러스터를 구성하는 브로커들의 ip와 포트 
--topic hello.kafka --->토픽의 이름(토픽 이름은 내부 데이터가 무엇이 있는지 유추가 가능하게 자세히 기재)
```

hello.kafka 토픽처럼 카프카 클러스터 정보와 토픽 이름만으로 토픽을 생성할 수 있었다.

클러스터 정보와 토픽 이름은 토픽을 만들기 위한 필수 값이다.이렇게 만들어진 토픽은 파티션 개수,복제 개수 등과 같이 다양한 옵션이 포함되어 있지만 모두 브로커에 실정된 기본값으로 생성되었다.만약 파티션 개수,복제 개수,토픽 데이터 유지 기간 옵션들을 지정하여 토픽을 생성하고 싶다면 다음과 같이 명령을 실행하면 된다.

```bash
bin/kafka-topics.sh 
--create
--bootstrap-server my-kafka:9092
--partitions 3 --->파티션 개수
--replication-factor 1 --->파티션을 복제할 복제 개수(1은 복제하지 않고 사용한다는 의미 2는 1개의 복제본을 사용하겠다는 의미)
--config retention.ms=172800000 --->추가적인 설정을 할 수 있다.(현재는 토픽 데이터를 유지하는 기간을 정한다.)
--topic hello.kafka
```

#### 토픽 리스트 조회

```bash
bin/kafka-topics.sh --bootstrap-server my-kafka:9092 --list
```

카프카 클러스터에 생성되 토픽들의 이름을 --list 옵션을 사용하여 확인할 수 있다.

카프카를 운영할 때 토픽이 몇 개나 생성되었는지,어떤 이름의 토픽이 있는지 확인하기 위해 사용한다.

카프카 내부 관리를 위한 인터널 토픽(internal topic)이 존재하는데 실질적으로 운영하는데에 사용하지 않으므로 --exclude-internal 옵션을 추가하여 조회 사 목록에서 제외할 수도 있다.

토픽 상세 조회

```html
bin/kafka-configs.sh --bootstrap-server 192.168.226.130:9092 --describe --topic mytopic
```

이미 생성된 토픽의 상트래르 --describe 옵션을 사용하여 확인할 수 있다.파티션 개수가 몇 개 인지 복제된 파티션이 위치한 브로커의 번호,기타 토픽을 구성하는 설절들을 출력한다.

토픽 옵션 수정

```bash
bin/kafka-topics.sh --bootstrap-server ip:9092 --topic mytopic --alter --partitions 4

bin/kafka-configs.sh --bootstrap-server 192.168.226.130:9092 
--entity-type topics 
--entity-name mytopic 
--alter --add-config retention.ms=86400000

bin/kafka-configs.sh --bootstrap-server 192.168.226.130:9092 --entity-type topics --entity-name mytopic --describe
```

생성된 토픽에 데이터를 넣을 수 있는 kafka-console-producer.sh 명령어를 실행   
토픽에 넣는 데이터를 레코드라고 부르며 메시지 키와 메시지 값으로 이루어져 있다.

```bash
bin/kafka-console-producer.sh --bootstrap-server 192.168.226.130:9092 --topic mytopic
```

키보드로 문자를 작성하고 엔터 키를 누르면 별다른 응답 없이 메시지 값이 전송된다.   
여기서 주의할 점은 kafka-console-procuder.sh로 전송되는 레코드 값은 utf-8을 기반으로 바이트로 변환되고 byteArrayserializer로만 직렬화된다는 점이다.즉 string이 아닌 타입으로 직렬화하여 데이터를 브로커로 전송하고 싶다면 카프카 프로듀서 애플리케이션을 직접 개발해야 한다.   
이제 메시지 키를 가지는 레코드를 전송해보자   
메시지 키를 가지는 레코드를 전송하기 위해서는 몇 가지 추가 옵션을 작성해야 한다.

```bash
bin/kafka-console-producer.sh --bootstrap-server 192.168.226.130:9092 --topic mytopic --property "parse.key=true" --property "key.seperator=:"
```

메시지 키와 메시지 값을 함께 전송한 레코드는 토픽의 파티션에 저장된다.   
메시지 키가 null인 경우에는 프로듀서가 파티션으로 전송할 때 레코드 배치 단위(레코드 전송 묶음)로 라운드로빈으로 전송한다.   
다만 이런 메시지 키와 피티션 할당은 프로듀서에서 설정된 파티셔너에 의해 결정되는데   
기본 파티셔너의 경우 이와 같은 동작을 보장한다.커스텀 파티셔너를 사용할 경우에는 메시지 키에 따른 파티션 할당이 다르게 동작할 수도 있다.   
  
토픽으로 전송한 데이터는 kafka-console-consumer.sh 명령어로 확인할 수 있다.이때 필수 옵션으로 --bootstrap-server에 카프카 클러스터 정보,--topic에 토픽 이름이 필요하다.추가로 --from-beginning 옵션을 주면 토픽에 저장된 가장 처음 데이터부터 출력한다.

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server 192.168.226.130:9092 --topic mytopic --from-beginning
```

kafka-console-producer.sh로 보낸 메시지 값이 출력된 것을 확인할 수 있다.만약 데이터의 메시지 키와 값을 확인하고 싶다면 --property 옵션을 사용하면 된다.

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server 192.168.226.130:9092 --topic mytopic 
--property print.key=true 메시지 키 확인
--property key.seperator="-" 키와 값을 구분 짓는 기호 선언
--group testmytopic 그룹 확인
--from-beginning 가장 처음부터 출력
```

여기서 주목할 점이 컨슈머 그룹을 통해 가져간 토픽의 메시지는 가져간 메시지에 대해 커밋을 한다.

여기서 커밋이란 컨슈머가 특정 레코드까지 처리를 완료했다고 레코드의 오프셋 번호를 카프카 브로커에 저장하는 것이다.

커밋 정보는 \_\_consumer\_offsets 이름의 내부 토픽에 저장된다.

메시지 키를 넣지 않은 데이터는 null과 메시지 값이 함께 보이고 메시지 키를 넣은 데이터는 메시지 키와 메시지 값이 함께 묶여서 한줄에 보이는 것을 확인할 수 있다.여기서 특이한 점은 kafka-console-producer.sh로 전송했던 데이터의 순서가 현재 출력되는 순서와 다르다는 것이다.이는 카프카의 핵심인 파티션의 개념 때문에 생기는 현상이다.

kafka-console.consumer.sh 명령어를 통해 토픽의 데이터를 가져가게 되면 토픽의 모든 파티션으로부터 동일한 중요도로 데이터를 가져간다.이로 인해 프로듀서가 토픽에 넣은 데이터의 순서와 컨슈머가 토픽에서 가져간 데이터의 순서가 달라지게 되는 것이다.만약 토픽에 넣은 데이터의 순서를 보장하고 싶다면 가장좋은 방법은 파티션 1개로 구성된 토픽을 만드는 것이다.한 개의 파티션에는 데이터의 순서를 보장하기 때문이다.

#### kafka-consumer-groups.sh

testmytopic 이름의 컨슈머 그룹으로 생성된 컨슈머로 mytopic 토픽의 데이터를 가져갔다.

컨슈머 그룹은 따로 생성하는 명령을 날리지 않고 컨슈머를 동작할 때 컨슈머 그룹 이름을 지정하면 새로 생성된다.

생성된 컨슈머 그룹의 리스트는 kafka-consumer-gropus.sh 명령어로 확인할 수 있다.

```bash
$ bin/kafka-consumer-groups.sh --bootstrap-server 192.168.226.130:9092 --list testmytopic
```

--list는 컨슈머 그룹의 리스트를 확인하는 옵션이다.컨슈머 그룹을 통해 현재 컨슈머 그룹이 몇 개나 생성되었는지 어떤 이름의 컨슈머 그룹이 존재하는지 확인할 수 있다.이렇게 확인한 컨슈머 그룹 이름을 토대로 컨슈머 그룹이 어떤 토픽의 데이터를 가져가는지 확인할 때 쓰인다.

```bash
$ bin/kafka-consumer-groups.sh --bootstrap-server 192.168.226.130:9092 --group testmytopic 어떤 그룹인지 지정

 --describe 상세 내용 출력
```

GROUP           TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG               
testmytopic     mytopic         3          1               1               0               
testmytopic     mytopic         2          3152            3152            0             
testmytopic     mytopic         1          3084            3084            0            
testmytopic     mytopic         0          3097            3097            0

여기서 확인 해야될점이 첫번째 줄의 토픽과 파티션이 가장 최근에 쓰였던 저장공간이라는 것이다.(커밋)

컨슈머 그룹의 상세 정보를 확인하는 것은 컨슈머를 개발할 때 카프카를 운영할 때 둘 다 중요하게 활용된다.

컨슈머 그룹이 중복되지는 않는지 확인하거나 운영하고 있는 컨슈머가 랙이 얼마인지 확인하여 컨슈머의 상태를 최적화하는데에 사용한다.컨슈머의 랙이 증가하고 있다는 의미는 프로듀서가 테이터를 토픽으로 전달하는 속도에 비해 컨슈머의 처리량이 느리다는 증거이기 때문이다.카프카를 운영할 때 컨슈머 그룹 이름을 알아내고 컨슈머 그룹의 상태 정보를 파악하면 카프카에 연결된 컨슈머의 호스트명 또는 ip를 알아낼 수 있다.접근 중인 컨슈머의 정보를 토대로 카프카가 인가된 사람에게만 사용중인지 알 수 있다.

#### akfka-verifiable-produer,consumer.sh

kafka-verifiable로 시작하는 2개의 스크립트를 사용하면 string 타입 메시지 값을 코드 없이 주고 받을 수 있다.

카프카 클러스터 설치가 완료된 이후에 토픽에 데이터를 전송하여 간단한 네트워크 통신 데스트를 할 때 유용하다.

```bash
$ bin/kafka-verifiable-producer.sh --bootstrap-server 192.168.226.130:9092
 --max-message 10 --->kafka-verifiable-producer.sh에 보내는 데이터 개수 지정 만약 -1이면 kafka-verifiable-producer.sh가 종료 전까지 계속 값을 보낸다.
 --topic verify-test 토픽 지정
```
```bash
{"timestamp":1634804744811,"name":"startup_complete"}//최초 실행 시점
//메시지별로 보낸 시간과 메시지 키,메시지 값,토픽,저장된 파티션,저장된 오프셋 번호 출력
{"timestamp":1634804745096,"name":"producer_send_success","key":null,"value":"0","offset":0,"topic":"verify-test","partition":0}
{"timestamp":1634804745100,"name":"producer_send_success","key":null,"value":"1","offset":1,"topic":"verify-test","partition":0}
{"timestamp":1634804745101,"name":"producer_send_success","key":null,"value":"2","offset":2,"topic":"verify-test","partition":0}
{"timestamp":1634804745101,"name":"producer_send_success","key":null,"value":"3","offset":3,"topic":"verify-test","partition":0}
{"timestamp":1634804745104,"name":"producer_send_success","key":null,"value":"4","offset":4,"topic":"verify-test","partition":0}
{"timestamp":1634804745104,"name":"producer_send_success","key":null,"value":"5","offset":5,"topic":"verify-test","partition":0}
{"timestamp":1634804745105,"name":"producer_send_success","key":null,"value":"6","offset":6,"topic":"verify-test","partition":0}
{"timestamp":1634804745105,"name":"producer_send_success","key":null,"value":"7","offset":7,"topic":"verify-test","partition":0}
{"timestamp":1634804745105,"name":"producer_send_success","key":null,"value":"8","offset":8,"topic":"verify-test","partition":0}
{"timestamp":1634804745105,"name":"producer_send_success","key":null,"value":"9","offset":9,"topic":"verify-test","partition":0}
{"timestamp":1634804745111,"name":"shutdown_complete"}
//결과값
{"timestamp":1634804745112,"name":"tool_data","sent":10,"acked":10,"target_throughput":-1,"avg_throughput":33.003300330033}
```

전송한 데이터 확인

```bash
$ bin/kafka-verifiable-consumer.sh --bootstrap-server 192.168.226.130:9092 --topic verify-test --group-id test-group
```
```bash
{"timestamp":1634805285805,"name":"startup_complete"}
{"timestamp":1634805286062,"name":"partitions_assigned","partitions":[{"topic":"verify-test","partition":0}]}
{"timestamp":1634805286120,"name":"records_consumed","count":10,"partitions":[{"topic":"verify-test","partition":0,"count":10,"minOffset":0,"maxOffset":9}]}
{"timestamp":1634805286127,"name":"offsets_committed","offsets":[{"topic":"verify-test","partition":0,"offset":10}],"success":true}
```

#### kafka-delete-records.sh

이미 적재된 토픽의 데이터를 지우는 방법으로 kafka-delete-records.sh 를 사용할 수 있다.

이미 적재된 데이터 중 가장 오래된 데이터(가장 낮은 숫자의 오프셋)부터 특정 시점의 오프셋가지 삭제 할 수 있다.

예를 들어 test 토픽의 0번 파티션에 0부터 100까지 데이터가 들어 있다고 가정하자 test 토픽의 0번 파티션에 저장된 데이터중 0부터 30 오프셋 데이터까지 지우고 싶다면 다음과 같이 입력한다.

```bash
$ vi delete-topic.json
```
```bash
{"partitions":[{"topic":"test","partition":0,"offset":50}],"version":1}
```
```bash
$ bin/kafka-delete-records.sh --bootstrap-server 192.168.226.130:9092
 --offset-json-file delete-topic.json --->해당 파일 데이터 읽는다.
```
```bash
//삭제 완료
Executing records delete operation
Records delete operation completed:
partition: test-0       low_watermark: 50
```

여기서 주의해야 할 점은 토픽의 특정 레코드 하나만 삭제되는 것이 아니라 파티션에 존재하는 가장 오래된 오프셋부터 지정한 오프셋까지 삭제된다는 점이다.카프카에서는 토픽의 파티션에 저장된 특정 데이터만 삭제할 수 없나는 점 명심해야 한다.