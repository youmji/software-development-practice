# 7주차 - Docker Compose 실습

## 1. 실습 목표

- Docker Compose 설정 파일 작성하기
- Nginx 웹 서버 실행하기
- web 서비스의 컨테이너를 3개로 확장하기
- 컨테이너 중지 및 복구 과정 확인하기

## 2. 실습 환경

- Windows WSL2 Ubuntu
- Docker Desktop
- Docker Compose
- nginx:alpine 이미지

## 3. 실습 과정

### 3-1. Docker Compose 파일 작성

`week07/compose.yaml` 파일을 작성.

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80"
```

Nginx 웹 서버를 실행하도록 설정. 호스트 포트는 자동으로 할당되도록 함.

### 3-2. Docker Compose 실행

```bash
docker compose -f week07/compose.yaml -p week07 up -d
docker compose -f week07/compose.yaml -p week07 ps
```

**실행 결과**

`week07-web-1` 컨테이너가 정상적으로 실행됨.

### 3-3. web 컨테이너 3개로 확장

```bash
docker compose -f week07/compose.yaml -p week07 up -d --scale web=3
```

**실행 결과**

- week07-web-1: Up
- week07-web-2: Up
- week07-web-3: Up

web 서비스의 컨테이너가 3개 실행되는 것을 확인.

### 3-4. 컨테이너 하나 중지

```bash
docker stop week07-web-2
docker compose -f week07/compose.yaml -p week07 ps
```

**실행 결과**

web-2가 중지되면서 실행 중인 컨테이너가 2개로 줄었다.

### 3-5. 컨테이너 수 복구

```bash
docker compose -f week07/compose.yaml -p week07 up -d --scale web=3
docker compose -f week07/compose.yaml -p week07 ps
```

**실행 결과**

중지됐던 web-2가 다시 실행됐으며, 세 컨테이너 모두 Up 상태로 복구됨.

## 4. 실습하면서 알게 된 점

- Docker Compose를 사용하면 여러 컨테이너를 하나의 설정 파일로 관리할 수 있음.
- `--scale web=3`으로 web 서비스의 컨테이너 수를 3개로 맞출 수 있음.
- 컨테이너 하나를 중지했을 때 자동으로 즉시 복구되지는 않음.
- `docker compose up -d --scale web=3`을 다시 실행해 컨테이너 수를 복구할 수 있음.
- 호스트 포트를 자동 할당하면 컨테이너 재실행 시 포트 번호가 달라질 수 있음.

## 5. web 컨테이너 3개 유지 방법과 한계

이번 실습에서는 `--scale web=3` 명령어를 이용해 컨테이너 3개를 실행하고, 중지된 컨테이너를 수동으로 복구.

**장점**
- 명령어 하나로 컨테이너 수를 조절할 수 있음.
- 설정 파일이 간단.
- 여러 컨테이너를 한꺼번에 관리할 수 있음.

**단점 및 한계**
- 이번 설정만으로는 컨테이너가 중지됐을 때 항상 3개가 자동 유지되지는 않음.
- 장애를 감지하고 복구 명령어를 실행하는 별도의 관리 방식이 필요할 수 있음.
- 단일 Docker 호스트 자체에 장애가 발생하면 모든 컨테이너가 영향을 받을 수 있음.

## 6. 실습 결과

Docker Compose로 Nginx 웹 서버를 실행한 뒤 web 컨테이너를 3개로 확장. 
컨테이너 하나를 중지하고 다시 복구하는 과정을 통해 컨테이너 수를 관리하는 방법과 한계를 이해함.


## Docker Compose 자동 감시 및 복구 실습

### 실습 목적
Docker Compose로 실행한 web 컨테이너 3개 중 하나가 중지되었을 때, 실행 중인 컨테이너 수를 확인하고 부족한 컨테이너를 자동으로 복구.

### 실습 방법
1. `auto-recover.sh` 스크립트를 작성.
2. 스크립트가 10초마다 실행 중인 컨테이너 수를 확인하도록 함.
3. `bash week07/auto-recover.sh` 명령어로 감시를 시작.
4. 다른 터미널에서 `docker stop week07-web-2` 명령어로 컨테이너 하나를 중지.
5. 컨테이너 수가 2개로 감소하면 `docker compose -f week07/compose.yaml -p week07 up -d --scale web=3` 명령어로 복구.

### 실행 결과
- 최초 실행 중인 web 컨테이너: 3개
- `week07-web-2` 중지 후: 2개
- 자동 복구 명령어 실행 후: 3개
- 중지된 컨테이너가 다시 시작되는 것을 확인.

### 장점
- 컨테이너 수가 부족할 때 자동으로 복구할 수 있음.
- 반복적으로 상태를 확인하므로 사람이 직접 명령어를 입력하는 횟수를 줄일 수 있음.
- Bash와 Docker Compose 명령어만으로 구현할 수 있음.

### 단점 및 한계
- 스크립트가 종료되면 자동 감시도 중단됨.
- 10초 간격으로 검사하므로 장애를 즉시 발견하지 못할 수 있음.
- 실행 중인 컨테이너 개수만 확인하므로 웹 서비스가 실제로 정상 응답하는지는 보장할 수 없음.
- Docker 엔진 자체가 중단되면 이 스크립트만으로 복구할 수 없음.
- 여러 서버에 분산된 컨테이너를 관리하는 용도로는 한계가 있음.
