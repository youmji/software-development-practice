# Kubernetes Deployment 및 Service 실습

## 1. 실습 목적

Kubernetes 환경에서 웹 애플리케이션을 배포하고, Deployment와 Service를 이용하여 컨테이너의 실행 및 네트워크 연결을 관리한다.

Pod의 자동 복구(Self-healing), 확장(Scaling), 로드 밸런싱(Load Balancing), 롤링 업데이트(Rolling Update), 롤백(Rollback)을 직접 실습하고 동작을 확인한다.

## 2. 실습 환경

- OS: Ubuntu (WSL2)
- 컨테이너 환경: Docker Desktop
- Kubernetes: Minikube (`devops09` 프로필)
- Kubernetes 관리 도구: kubectl
- 애플리케이션: Python Flask 방명록
- 컨테이너 이미지: `ghcr.io/youmji/guestbook:v1`

## 3. 프로젝트 구조

```text
week09-kubernetes/
├── README.md
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

## 4. Deployment 생성

`deployment.yaml`을 작성하여 Flask 방명록 애플리케이션을 Kubernetes에 배포하였다.

주요 설정은 다음과 같다.

- Deployment 이름: `guestbook`
- 컨테이너 이미지: `ghcr.io/youmji/guestbook:v1`
- 컨테이너 포트: `5000`
- 최종 설정한 복제본 수: `3`

초기에는 복제본 2개로 배포한 뒤 Scaling 실습을 통해 3개로 확장하였다.

```bash
kubectl apply -f week09-kubernetes/k8s/deployment.yaml
kubectl get deployment guestbook
kubectl get pods
```

## 5. Self-healing 실습

Deployment가 관리하는 Pod 중 하나를 삭제하고 Kubernetes가 새로운 Pod를 생성하는지 확인하였다.

```bash
kubectl delete pod <삭제할-Pod-이름>
kubectl get pods
kubectl get deployment guestbook
```

실습 결과, 삭제한 Pod 대신 새로운 Pod가 생성되었으며 Deployment가 지정된 복제본 수를 유지하는 것을 확인하였다.

## 6. NodePort Service 생성

`service.yaml`을 작성하여 방명록 애플리케이션에 접근할 수 있도록 Service를 생성하였다.

주요 설정은 다음과 같다.

- Service 이름: `guestbook`
- Service 유형: `NodePort`
- Service 포트: `80`
- 컨테이너 대상 포트: `5000`
- NodePort: `30080`

```bash
kubectl apply -f week09-kubernetes/k8s/service.yaml
kubectl get svc guestbook
```

Minikube의 Service 연결 기능을 사용하여 웹 브라우저에서 방명록 페이지에 접근하였다.

```bash
minikube service guestbook -p devops09 --url
```

또한 포트 포워딩을 통해 HTTP 요청이 정상적으로 처리되는 것을 확인하였다.

```bash
kubectl port-forward service/guestbook 8080:80
```

별도 터미널에서 다음 명령어를 실행하였다.

```bash
curl -i http://127.0.0.1:8080/
```

실행 결과 `HTTP/1.1 200 OK`가 반환되었다.

## 7. Scaling 실습

Deployment의 복제본 수를 2개에서 3개로 확장하였다.

```bash
kubectl scale deployment guestbook --replicas=3
kubectl get deployment guestbook
kubectl get pods
```

실행 결과, Deployment의 READY 상태가 `3/3`으로 표시되었으며 세 Pod가 실행되는 것을 확인하였다.

최종 `deployment.yaml`에도 `replicas: 3`을 반영하였다.

## 8. Load Balancing 실습

Kubernetes Service가 여러 Pod에 요청을 분산하는지 확인하기 위해 클러스터 내부에서 HTTP 요청 30회를 실행하였다.

```bash
kubectl run curl-test --image=curlimages/curl:8.12.1 --restart=Never --command -- sh -c 'for i in $(seq 1 30); do curl -s -o /dev/null -w "요청 $i: HTTP %{http_code}\n" -H "Connection: close" http://guestbook.default.svc.cluster.local/; done'
```

테스트 Pod의 실행 완료를 기다린 뒤 로그를 확인하였다.

```bash
kubectl wait --for=jsonpath='{.status.phase}'=Succeeded pod/curl-test --timeout=120s
kubectl logs curl-test
```

### 실습 결과

- HTTP 요청 30회 모두 `200` 응답
- 서로 다른 세 Pod에서 요청 처리 로그 확인
- 세 Pod에 요청이 분산되는 것을 확인

Pod별 처리 횟수는 제공된 로그 기준 다음과 같다.

| Pod 이름(끝부분) | 처리 횟수 |
|---|---:|
| `gz4nf` | 6회 |
| `m9mgj` | 15회 |
| `cgzws` | 9회 |
| **합계** | **30회** |

Pod별 로그는 다음 명령어로 확인하였다.

```bash
kubectl logs -l app=guestbook --all-containers=true --prefix=true --since=3m --max-log-requests=10
```

테스트 후 임시 Pod를 삭제하였다.

```bash
kubectl delete pod curl-test
```

이를 통해 Service가 여러 Pod에 요청을 전달한다는 것을 확인하였다.

## 9. Rolling Update 실습

Deployment의 Pod 템플릿에 환경변수를 추가하여 Rolling Update를 수행하였다.

```bash
kubectl set env deployment/guestbook APP_VERSION=v2
kubectl rollout status deployment/guestbook
