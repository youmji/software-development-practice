# 3주차 - Qwen AI 웹앱 실습

## 1. 실습 목표
- Ubuntu 환경에서 Python 웹앱 실행
- Ollama 설치 및 Qwen 모델 사용
- 로컬 웹페이지에서 AI 질문과 답변 확인

## 2. 실습 환경
- WSL2 / Ubuntu
- Python 3.14.4
- Ollama 0.40.7
- Qwen3 0.6B

## 3. 실습 과정

### Python 가상환경 생성
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Ollama 모델 확인
```bash
ollama --version
ollama list
```

### 웹서버 실행
```bash
./start.sh
```

웹 접속 주소: http://localhost:8000

## 4. 실습 결과
- Qwen 웹페이지 접속 성공
- 질문 입력 후 AI 답변 출력 확인
- start.sh 실행 스크립트 작성 및 실행 확인

## 5. 학습 정리
Python 가상환경을 구성하고 Ollama와 Qwen 모델을 활용하여 로컬 AI 웹앱을 실행했다. 또한 실행 스크립트를 작성하여 웹서버를 간편하게 실행할 수 있도록 함.
