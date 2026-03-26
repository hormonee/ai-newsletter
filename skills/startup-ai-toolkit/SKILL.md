---
name: startup-ai-toolkit
description: AI 구동을 위한 로컬 환경(Docker, SearXNG, Ollama)을 시작합니다.
---

# startup-ai-toolkit

이 스킬은 뉴스 자동화 시스템을 실행하기 위해 필요한 로컬 인프라를 구축합니다.

## 실행 단계

1. **Docker 데스크톱 앱 실행**
   - 명령어: `open -a Docker`
   - 설명: macOS에서 Docker 엔진을 백그라운드에서 구동합니다.

2. **SearXNG 서비스 시작**
   - 명령어: `docker-compose -f /Users/jm/ai/tool/searxng-app/docker-compose.yml up -d`
   - 설명: 지정된 경로의 `docker-compose.yml` 파일을 사용하여 SearXNG 컨테이너를 백그라운드로 실행합니다.

3. **Ollama 모델 활성화**
   - 명령어: `ollama run qwen3.5`
   - 설명: Qwen 3.5 모델을 불러와 추론 준비 상태로 만듭니다.
