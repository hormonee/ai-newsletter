---
name: shutdown-ai-toolkit
description: 사용 중인 AI 로컬 환경(SearXNG, Ollama)을 종료하여 리소스를 정리합니다.
---

# shutdown-ai-toolkit

이 스킬은 뉴스 자동화 시스템 종료 후 로컬 시스템의 리소스를 해제하기 위해 사용됩니다.

## 실행 단계

1. **SearXNG 서비스 종료**
   - 명령어: `docker compose -f /Users/jm/ai/tool/searxng-app/docker-compose.yml down`
   - 설명: 실행 중인 SearXNG 컨테이너를 중지하고 제거합니다.

2. **Ollama 모델 중지**
   - 명령어: `ollama stop qwen3.5`
   - 설명: 메모리에 상주 중인 Qwen 3.5 모델 프로세스를 종료합니다.
