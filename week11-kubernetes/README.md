# Week 11 - Kubernetes 설정 관리 및 상태 점검

## 1. 실습 목표

Kubernetes의 ConfigMap, Secret, Scaling, Rolling Update,
Liveness Probe, Readiness Probe를 이해하고 직접 적용한다.

## 2. 실습 환경

- Ubuntu (WSL2)
- Docker
- Minikube (devops11 프로필)
- Kubernetes v1.37.0
- Python 3.12
- Flask 3.1.1

## 3. 프로젝트 구조

```text
week11-kubernetes/
├── guestbook/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── redis.yaml
│   └── guestbook.yaml
├── .gitignore
└── README.md

```

## 4. 주요 실습 내용

### ConfigMap 및 Secret
- ConfigMap으로 APP_TITLE, THEME_COLOR, REDIS_HOST, REDIS_PORT 관리
- Secret으로 Redis 비밀번호 관리
- Guestbook에 환경변수로 전달
- ConfigMap 변경 후 Deployment 재시작하여 변경 사항 확인
- GitHub 제출용 Secret에는 예시 값 CHANGE_ME 사용

### Scaling
Guestbook Pod를 2개에서 4개로 확장했다.

명령어:
- kubectl scale deployment guestbook --replicas=4
- kubectl get deployment guestbook

결과: 4/4 Available

### Rolling Update
Guestbook에 상태 점검 기능을 추가하고 v2 이미지를 생성했다.

명령어:
- docker build -t ghcr.io/youmji/guestbook:v2 ./guestbook
- minikube image load ghcr.io/youmji/guestbook:v2 -p devops11
- kubectl apply -f k8s/guestbook.yaml
- kubectl rollout status deployment/guestbook

결과: successfully rolled out

### Liveness Probe
- 경로: /healthz
- 포트: 5000
- 점검 주기: 10초
- 응답: HTTP 200

### Readiness Probe
- 경로: /readyz
- 포트: 5000
- 점검 주기: 5초
- 응답: HTTP 200

현재 Readiness Probe는 Flask 서버의 기본 응답 상태를 확인한다.
Redis 연결 상태까지 검사하지는 않는다.

## 5. 최종 실습 결과

| 항목 | 결과 |
|---|---|
| ConfigMap 적용 | 성공 |
| Secret 적용 | 성공 |
| Redis 실행 | 성공 |
| Scaling | 4/4 |
| ConfigMap 변경 반영 | 성공 |
| Rolling Update | 성공 |
| Liveness Probe | HTTP 200 |
| Readiness Probe | HTTP 200 |

## 6. 실행 방법

1. Minikube 클러스터를 실행한다.
2. Guestbook v2 이미지를 빌드하고 Minikube에 로드한다.
3. ConfigMap, Secret, Redis, Guestbook 리소스를 적용한다.
4. Deployment와 Pod 상태를 확인한다.

실행 명령어:

- kubectl apply -f k8s/configmap.yaml
- kubectl apply -f k8s/secret.yaml
- kubectl apply -f k8s/redis.yaml
- kubectl apply -f k8s/guestbook.yaml
- kubectl get deployments
- kubectl get pods

주의: secret.yaml의 CHANGE_ME는 예시 값이므로
실제 배포 시 안전한 비밀번호로 변경해야 한다.

## 7. 실습을 통해 배운 점

ConfigMap과 Secret을 이용해 애플리케이션 설정을
컨테이너 이미지와 분리하는 방법을 학습했다.

Scaling으로 Pod 수를 확장하고, Rolling Update를 통해
서비스를 새로운 이미지 버전으로 교체했다.

Liveness Probe와 Readiness Probe를 설정하여
컨테이너 상태를 점검하고 HTTP 200 응답을 확인했다.
