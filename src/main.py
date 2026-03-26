import sys
import os

# src 디렉토리를 Python 경로에 추가하여 
# core, application, infrastructure 모듈을 올바르게 임포트할 수 있도록 합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from application.service import NewsAutomationService

def main():
    """애플리케이션의 입구(Entry point) 입니다."""
    try:
        # 서비스 레이어를 통해 자동화 프로세스 실행
        service = NewsAutomationService()
        service.run_daily_automation()
    except KeyboardInterrupt:
        print("\n👋 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"👻 시스템 오류 발생: {e}")

if __name__ == "__main__":
    main()
