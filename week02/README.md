# 2주차 - 실습 환경 구축과 버전 관리 기초

## 1. 학습 목표
- WSL2와 Ubuntu를 이용하여 Linux 실습 환경 구축
- Linux 기본 명령어 익히기
- Git으로 파일의 변경 이력 관리
- GitHub 저장소 생성 및 공유

## 2. 주요 학습 내용

### WSL2와 Ubuntu
WSL2를 사용하면 Windows에서도 Linux 환경을 사용할 수 있음.

설치 명령어:
~~~bash
wsl --install
~~~

### Git과 GitHub
- Git: 파일의 변경 이력을 관리하는 버전 관리 도구
- GitHub: Git 저장소를 온라인에 공유하고 협업할 수 있는 서비스
- Commit: 현재 변경 사항을 하나의 버전으로 기록
- Branch: 기존 작업과 분리하여 변경 사항을 관리

## 3. Git 실습 명령어

2주차 교안에서 다룬 실습 순서.

~~~bash
cd ~/devops
mkdir week02
cd week02
echo "Hello, DevOps!" > text.txt
git status
git add text.txt
git commit -m "first commit"
git log
~~~

### 명령어 설명
| 명령어 | 설명 |
|---|---|
| cd | 디렉터리 이동 |
| mkdir | 디렉터리 생성 |
| echo | 문자열 출력 및 파일 작성에 활용 |
| git status | Git 작업 상태 확인 |
| git add | 커밋할 변경 사항 선택 |
| git commit | 변경 사항을 하나의 버전으로 기록 |
| git log | 커밋 기록 확인 |

※ 위 명령어는 ~/devops가 이미 Git 저장소로 초기화된 상태를 전제로 함.

## 4. GitHub 저장소
- 저장소: https://github.com/youmji/software-development-practice
- 공개 설정: Public

## 5. 실습 결과
실제 실습 화면을 확인한 뒤 캡처와 결과를 추가할 예정.

## 6. 오류 및 해결 과정
실습 중 오류가 발생하면 원인과 해결 방법을 기록.

## 7. 학습 정리
Git을 이용하면 파일의 변경 사항을 기록할 수 있고, GitHub를 통해 작업 내용을 공유할 수 있다는 점을 학습.
