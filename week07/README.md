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

`week07/compose.yaml` 파일을 작성했다.

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80"
```

Nginx 웹 서버를 실행하도록 설정했다. 호스트 포트는 자동으로 할당되도록 했다.

### 3-2. Docker Compose 실행

```bash
docker compose -f week07/compose.yaml -p week07 up -d
docker compose -f week07/compose.yaml -p week07 ps
```

**실행 결과**

`week07-web-1` 컨테이너가 정상적으로 실행됐다.

### 3-3. web 컨테이너 3개로 확장

```bash
docker compose -f week07/compose.yaml -p week07 up -d --scale web=3
```

**실행 결과**

- week07-web-1: Up
- week07-web-2: Up
- week07-web-3: Up

web 서비스의 컨테이너가 3개 실행되는 것을 확인했다.

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

중지됐던 web-2가 다시 실행됐으며, 세 컨테이너 모두 Up 상태로 복구됐다.

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
