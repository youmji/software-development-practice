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
week10-kubernetes/
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
kubectl apply -f week10-kubernetes/k8s/deployment.yaml
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
kubectl apply -f week10-kubernetes/k8s/service.yaml
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
```
## 10. Kubernetes 과제

### 10.1 실습 목적

9주차에 구축한 Kubernetes Deployment 및 Service 환경을 활용하여 다음 기능을 실습하였다.

- Scaling: Deployment 복제본 수 확장
- Load Balancing: Service를 통한 요청 분산
- Self-healing: Pod 삭제 후 자동 복구
- Rolling Update: 컨테이너 이미지 v1에서 v2로 변경
- Rollout History: 배포 변경 이력 확인
- Rollback: 이전 버전으로 복구

실습 환경은 Minikube `devops09` 프로필이며, 기존 `week10-kubernetes/k8s/`의 Deployment 및 Service 설정을 활용하였다.

### 10.2 Deployment Scaling (3개 → 5개)

기존 Deployment의 복제본 수를 3개에서 5개로 확장하였다.

**실행 명령어**

```bash
kubectl --context=devops09 scale deployment guestbook --replicas=5
kubectl --context=devops09 rollout status deployment/guestbook --timeout=180s
kubectl --context=devops09 get deployment guestbook
kubectl --context=devops09 get pods -o wide
```

**실습 결과**

- Deployment READY: `5/5`
- Pod 5개 모두 `Running`
- 복제본 수 확장 성공

기존 `deployment.yaml`에는 `replicas: 3`이 설정되어 있으며, 이번 실습에서는 `kubectl scale` 명령어를 통해 실행 중인 Deployment를 5개로 확장하였다.

### 10.3 Pod Hostname 및 Service Load Balancing 확인

먼저 각 Pod의 hostname을 확인하였다.

```bash
kubectl --context=devops09 get pods -l app=guestbook -o name | while read pod; do
  kubectl --context=devops09 exec "$pod" -- printenv HOSTNAME
done
```

확인된 Pod hostname은 다음과 같다.

- `guestbook-fb8cd5fd8-78pqd`
- `guestbook-fb8cd5fd8-8ddpx`
- `guestbook-fb8cd5fd8-bkd5j`
- `guestbook-fb8cd5fd8-wpw69`
- `guestbook-fb8cd5fd8-xzdsb`

이후 Kubernetes Service를 통해 HTTP 요청 30회를 실행하였다.

```bash
kubectl --context=devops09 exec deployment/guestbook -- python -c '
import urllib.request
for i in range(30):
    req = urllib.request.Request(
        "http://guestbook.default.svc.cluster.local/",
        headers={"Connection": "close"}
    )
    with urllib.request.urlopen(req, timeout=5) as response:
        print(f"요청 {i+1}: HTTP {response.status}")
'
```

Pod별 요청 처리 로그를 확인하였다.

```bash
kubectl --context=devops09 logs -l app=guestbook \
  --all-containers=true \
  --prefix=true \
  --since=5m \
  --max-log-requests=10 | grep 'GET / HTTP'
```

**실습 결과**

| Pod hostname 끝부분 | HTTP 요청 처리 횟수 |
|---|---:|
| `78pqd` | 7회 |
| `8ddpx` | 2회 |
| `bkd5j` | 8회 |
| `wpw69` | 8회 |
| `xzdsb` | 5회 |
| **합계** | **30회** |

30회의 HTTP 요청이 모두 `200 OK`로 처리되었으며, 5개의 Pod에서 요청 처리 로그가 확인되었다.

이를 통해 Kubernetes Service가 여러 Pod로 요청을 분산하는 것을 확인하였다.

### 10.4 Pod 강제 삭제 및 Self-healing

실행 중인 Pod 하나를 강제로 삭제하고 Kubernetes가 새로운 Pod를 생성하는지 확인하였다.

**실행 명령어**

```bash
kubectl --context=devops09 delete pod guestbook-fb8cd5fd8-78pqd --grace-period=0 --force

kubectl --context=devops09 rollout status deployment/guestbook --timeout=180s
kubectl --context=devops09 get pods
kubectl --context=devops09 get deployment guestbook
```

**실습 결과**

| 항목 | 결과 |
|---|---|
| 삭제한 Pod | `guestbook-fb8cd5fd8-78pqd` |
| 새로 생성된 Pod | `guestbook-fb8cd5fd8-2nhrg` |
| 새 Pod 상태 | `1/1 Running` |
| Deployment READY | `5/5` |

Pod가 삭제된 후 Deployment가 새로운 Pod를 자동 생성하여 원하는 복제본 수인 5개를 유지하였다.

이를 통해 Kubernetes의 Self-healing 기능을 확인하였다.

### 10.5 Rolling Update (v1 → v2)

기존 Guestbook 컨테이너 이미지를 v1에서 v2로 변경하였다.

먼저 로컬 Docker에 v2 이미지가 존재하는지 확인하고 Minikube 클러스터에 로드하였다.

```bash
docker image inspect ghcr.io/youmji/guestbook:v2 --format '{{.RepoTags}}'

minikube image load ghcr.io/youmji/guestbook:v2 -p devops09
```

이후 Deployment 이미지를 변경하였다.

```bash
kubectl --context=devops09 set image deployment/guestbook \
  web=ghcr.io/youmji/guestbook:v2

kubectl --context=devops09 rollout status deployment/guestbook --timeout=180s
kubectl --context=devops09 get deployment guestbook
kubectl --context=devops09 get pods
```

**실습 결과**

- 기존 이미지: `ghcr.io/youmji/guestbook:v1`
- 변경 이미지: `ghcr.io/youmji/guestbook:v2`
- Deployment READY: `5/5`
- 새로운 v2 Pod 5개 `Running`
- 기존 v1 Pod들은 `Terminating` 상태로 전환

Rolling Update가 정상적으로 완료되었으며, Deployment가 새로운 이미지의 Pod로 교체된 것을 확인하였다.

### 10.6 Rollout History 확인

Rolling Update 이후 배포 변경 이력을 조회하였다.

```bash
kubectl --context=devops09 rollout history deployment/guestbook

kubectl --context=devops09 rollout history deployment/guestbook --revision=1

kubectl --context=devops09 rollout history deployment/guestbook --revision=2
```

**실습 결과**

| Revision | 이미지 |
|---|---|
| 1 | `ghcr.io/youmji/guestbook:v1` |
| 2 | `ghcr.io/youmji/guestbook:v2` |

Kubernetes가 이전 버전과 업데이트된 버전의 Pod 템플릿을 Revision으로 관리한다는 것을 확인하였다.

### 10.7 Rollback (v2 → v1)

Rolling Update 이후 이전 버전인 v1으로 롤백하였다.

**실행 명령어**

```bash
kubectl --context=devops09 rollout undo deployment/guestbook --to-revision=1

kubectl --context=devops09 rollout status deployment/guestbook --timeout=180s

kubectl --context=devops09 get deployment guestbook
kubectl --context=devops09 get pods
```

롤백 이후 컨테이너 이미지와 배포 이력을 확인하였다.

```bash
kubectl --context=devops09 get deployment guestbook \
  -o jsonpath='{.spec.template.spec.containers[0].image}{"\n"}'

kubectl --context=devops09 rollout history deployment/guestbook
```

**실습 결과**

- 최종 이미지: `ghcr.io/youmji/guestbook:v1`
- Deployment READY: `5/5`
- v1 Pod 5개 모두 `Running`
- 최종 Rollout History: Revision 2, Revision 3

롤백을 통해 v1 이미지가 다시 배포되었으며, 이전 버전으로 복구하는 과정에서도 새로운 Revision이 생성되는 것을 확인하였다.

### 10.8 최종 실습 결과

| 실습 항목 | 결과 |
|---|---|
| Scaling (3 → 5) | 성공 |
| Pod Hostname 확인 | 성공 |
| Service Load Balancing | 성공 |
| Pod Self-healing | 성공 |
| Rolling Update (v1 → v2) | 성공 |
| Rollout History | 성공 |
| Rollback (v2 → v1) | 성공 |

### 10.9 실습을 통해 배운 점

이번 실습을 통해 Kubernetes Deployment가 원하는 복제본 수를 유지하고, Pod에 장애가 발생했을 때 자동으로 새로운 Pod를 생성하는 과정을 확인하였다.

또한 Service를 통해 HTTP 요청이 여러 Pod에 분산되는 것을 확인하였으며, Rolling Update와 Rollback을 이용하여 애플리케이션 버전을 변경하고 복구하는 방법을 익혔다.

특히 Deployment가 배포 이력을 Revision 단위로 관리하기 때문에 업데이트 이후에도 이전 버전으로 복구할 수 있다는 점을 이해하였다.
