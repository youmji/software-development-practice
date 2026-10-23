# 6주차 - Dockerfile 실습

## 1. 실습 목표
- Dockerfile의 기본 명령어 이해하기
- Dockerfile을 이용해 이미지 직접 생성하기
- 직접 만든 이미지로 컨테이너 실행하기
- 컨테이너 로그와 종료 상태 확인하기

## 2. 실습 환경
- Windows WSL2 Ubuntu
- Docker Desktop
- Docker 29.8.1
- Python 3.12-slim 이미지

## 3. 실습 과정

### 3-1. Dockerfile 작성

`week06/Dockerfile` 파일을 작성했다.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
```

- `FROM`: 기본 이미지 지정
- `WORKDIR`: 컨테이너 내부 작업 폴더 지정
- `COPY`: 프로그램 파일 복사
- `CMD`: 컨테이너 실행 시 수행할 명령어 지정

### 3-2. Python 프로그램 작성

`week06/app.py` 파일을 작성했다.

```python
print("Dockerfile 실습 성공!")
print("6주차 Docker 이미지 실행 완료")
```

### 3-3. Docker 이미지 빌드

```bash
docker build -t week06-python:1.0 ./week06
docker images week06-python
```

**실행 결과**

Docker 이미지 빌드가 정상적으로 완료됐으며, `week06-python:1.0` 이미지가 생성된 것을 확인했다.

### 3-4. 컨테이너 실행

```bash
docker run --name week06-test week06-python:1.0
```

**실행 결과**

```text
Dockerfile 실습 성공!
6주차 Docker 이미지 실행 완료
```

직접 만든 이미지로 Python 프로그램을 정상 실행했다.

### 3-5. 컨테이너 상태 확인

```bash
docker ps -a --filter "name=week06-test"
```

컨테이너가 `Exited (0)` 상태인 것을 확인했다.

### 3-6. 로그 및 종료 코드 확인

```bash
docker logs week06-test
docker inspect -f '{{.State.Status}} / 종료 코드: {{.State.ExitCode}}' week06-test
```

**실행 결과**

```text
Dockerfile 실습 성공!
6주차 Docker 이미지 실행 완료
exited / 종료 코드: 0
```

컨테이너가 정상적으로 실행되고 종료된 것을 확인.

## 4. 실습하면서 알게 된 점

- Dockerfile을 작성하면 필요한 실행 환경을 이미지로 만들 수 있음.
- `docker build`는 Dockerfile을 바탕으로 이미지를 생성.
- `docker run`은 생성된 이미지로 컨테이너를 실행.
- `docker logs`를 이용하면 종료된 컨테이너의 출력도 확인할 수 있음.
- 종료 코드가 `0`이면 프로그램이 정상적으로 종료됐다는 뜻.

## 5. 실습 결과

Dockerfile과 Python 프로그램을 직접 작성한 뒤 Docker 이미지를 빌드. 
생성한 이미지로 컨테이너를 실행했고, 로그와 종료 코드를 통해 정상적으로 작동한 것을 확인.
