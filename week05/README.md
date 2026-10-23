# 5주차 - Docker 기본 실습

## 1. 실습 목표
- Docker 이미지와 컨테이너의 차이 이해하기
- Docker 컨테이너 생성 및 실행하기
- 실행 중인 컨테이너에 접속하기
- 컨테이너 중지 및 재시작하기
- Docker 로그 확인하기

## 2. 실습 환경
- Windows WSL2 Ubuntu
- Docker Desktop
- Docker 29.8.1
- Ubuntu 24.04 컨테이너

## 3. 실습 과정

### 3-1. Docker 설치 확인

```bash
docker --version
docker ps
```

Docker 명령어가 정상적으로 실행되는 것을 확인했다.

### 3-2. Hello World 컨테이너 실행

```bash
docker run hello-world
docker ps -a
```

**실행 결과**
```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

`hello-world` 컨테이너는 메시지를 출력한 뒤 종료되었으며, `docker ps -a`에서 `Exited (0)` 상태를 확인했다.

### 3-3. Ubuntu 컨테이너 생성 및 실행

```bash
docker run -dit --name week05-ubuntu ubuntu:24.04 bash
docker ps
```

**실행 결과**
```text
IMAGE          STATUS       NAMES
ubuntu:24.04   Up           week05-ubuntu
```

Ubuntu 컨테이너가 실행 중인 것을 확인했다.

### 3-4. 컨테이너 내부 접속

```bash
docker exec -it week05-ubuntu bash
pwd
cat /etc/os-release
```

**실행 결과**
```text
/
Ubuntu 24.04.5 LTS
```

컨테이너 내부에서 Ubuntu 버전을 확인했다.

### 3-5. 컨테이너 내부 파일 생성

```bash
echo "Docker week05 practice" > /practice.txt
cat /practice.txt
ls -l /practice.txt
```

**실행 결과**
```text
Docker week05 practice
```

컨테이너 내부에 파일을 생성하고 내용을 확인했다.

### 3-6. 컨테이너 중지 및 재시작

컨테이너에서 `exit` 명령어로 나온 뒤 다음 명령어를 실행했다.

```bash
docker stop week05-ubuntu
docker ps -a
docker start week05-ubuntu
docker exec week05-ubuntu cat /practice.txt
```

**실행 결과**
```text
Docker week05 practice
```

컨테이너를 중지했다가 다시 실행해도 기존에 만든 파일이 유지되는 것을 확인했다.

### 3-7. Docker 로그 확인

```bash
docker logs week05-ubuntu
docker logs sharp_dirac
```

`week05-ubuntu`는 로그가 비어 있었고, 
`hello-world` 컨테이너에서는 실행 당시 출력된 메시지를 다시 확인할 수 있음.

## 4. 실습하면서 알게 된 점

- Docker 이미지는 컨테이너를 만들기 위한 실행 환경과 파일을 담고 있음.
- 컨테이너는 이미지를 바탕으로 생성하고 실행.
- `docker ps`는 실행 중인 컨테이너만 보여줌.
- `docker ps -a`는 종료된 컨테이너까지 보여줌.
- `docker exec`로 실행 중인 컨테이너 안에서 명령어를 실행할 수 있음.
- 컨테이너를 중지하고 다시 시작해도 내부 파일은 유지.
- 컨테이너를 삭제하고 새로 만들면 내부에 저장한 데이터는 사라질 수 있으므로 
볼륨 등을 활용해야 함.

## 5. 실습 결과

Docker 명령어를 사용해 컨테이너를 직접 생성하고 실행. 
Ubuntu 컨테이너 내부에서 파일을 만든 뒤 중지와 재시작을 진행했고, 
파일이 그대로 남아 있는 것도 확인.

이번 실습을 통해 Docker 컨테이너의 기본적인 실행 및 관리 방법을 배움.
