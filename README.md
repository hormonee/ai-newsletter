# AI News Automation

이 프로젝트는 **CrewAI**와 **Ollama (Qwen 3.5)**를 활용하여 매일 최신 글로벌 AI 뉴스를 자동으로 수집하고, 친근한 블로그 스타일의 **Markdown-Free HTML 뉴스레터**로 제작하여 발송하는 고성능 자동화 시스템입니다.

## 🚀 주요 기능

1.  **AI-Only 큐레이션**: 불필요한 단계를 과감히 제거하고 전날 발행된 글로벌 AI 핵심 이슈 **10개** 선정에만 집중합니다.
2.  **안정적인 파이프라인**:
    *   **팩트 체커 단계 제거**: RSS 피드의 물리적 신뢰성을 바탕으로 중복 검증 단계를 제거하여 데이터 유실을 방지하고 실행 속도를 3배 이상 향상시켰습니다.
    *   **직렬 오케스트레이션**: 조사관(Researcher) → 에디터(Editor)로 이어지는 심플한 직렬 체계로 안정성을 극대화했습니다.
3.  **Markdown-Free HTML 레터**:
    *   마크다운 기호를 완전히 배제하고, 구글 메일 및 모바일 환경에 최적화된 **순수 HTML/CSS** 디자인을 적용했습니다.
    *   시각 숫자나 기술적 노이즈 없이 부드러운 읽기 경험을 제공합니다.
4.  **한국 시간(KST) 기반 필터링**: 실행 시점의 한국 시각을 정확히 인식하여 전날(Yesterday) 기준의 뉴스만 100% 실시간 수집합니다.
5.  **사고 과정 기록 (Thought Logs)**: 에이전트의 상세한 추론 과정이 `logs/agent_thoughts.log`에 실시간 기록되어 투명한 디버깅이 가능합니다.

## 🛠 기술 스택

*   **Orchestration**: CrewAI
*   **LLM**: Ollama (qwen3.5)
*   **Search Engine**: SearXNG (Docker)
*   **Infrastructure**: Python 3.12+, Conda

## ⚙️ 설정 및 실행 방법

### 1. 환경 변수 설정
`.env.local` 파일에 다음 정보를 입력합니다:
```env
EMAIL_SENDER=보내는사람@gmail.com
EMAIL_PASSWORD=구글앱비밀번호
EMAIL_RECEIVER=수신자1@example.com, 수신자2@example.com
```

### 2. 자동화 실행 (워크플로우)
에이전트에게 다음 슬래시 명령어를 사용하세요:
*   **/run-news-crew**: 로컬 AI 인프라(Docker, Ollama) 기동부터 뉴스 수집, 발송, 종료까지의 전 과정을 자동 수행합니다.

## 📂 프로젝트 구조
*   `src/core/`: 크루 에이전트 페르소나 및 태스크 지침 정의 (V3 최적화)
*   `src/application/`: 로그 리다이렉션 및 전체 자동화 유스케이스 조율
*   `src/infrastructure/`: RSS 페처, SearXNG 어댑터, SMTP 발송 처리
*   `logs/`: `agent_thoughts.log`를 통한 에이전트 사고 과정 추적
