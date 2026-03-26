---
description: AI 뉴스 수집 크루를 실행하기 위해 환경을 설정하고, 작업을 마친 후 리소스를 정리합니다.
---

// turbo-all

1. AI 로컬 환경 기동 (startup-ai-toolkit)
run_command: docker-compose -f /Users/jm/ai/tool/searxng-app/docker-compose.yml up -d && ollama run qwen3.5

2. 뉴스 자동화 크루 실행 (main.py)
run_command: conda run -n crewai python src/main.py

3. AI 로컬 환경 종료 (shutdown-ai-toolkit)
run_command: docker-compose -f /Users/jm/ai/tool/searxng-app/docker-compose.yml down && ollama stop qwen3.5