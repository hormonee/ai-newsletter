import os
import logging
import sys
import contextlib
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Domain 레이어와 Infrastructure 레이어의 의존성 주입
from core.crew import NewsCrew
from infrastructure.email.smtp_adapter import SmtpEmailAdapter

class NewsAutomationService:
    """전체 자동화 유스케이스를 조율하며 로그를 기록하는 서비스 클래스"""
    
    def _setup_logging(self):
        """로그 파일 및 포맷을 설정합니다."""
        # 프로젝트 루트의 logs 디렉토리 설정
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_dir = os.path.normpath(os.path.join(current_dir, '..', '..', 'logs'))
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_file = os.path.join(self.log_dir, 'automation.log')
        
        # 로거 초기화
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler() # 터미널 출력도 병행
            ]
        )
        self.logger = logging.getLogger(__name__)

    def __init__(self):
        # 1. 로그 설정 우선 실행
        self._setup_logging()
        
        # 2. .env.local에서 환경 변수 로드
        load_dotenv('.env.local')
        
        # 설정 파일(YAML) 경로 계산 (src/config)
        # __file__은 src/application/service.py 이므로 
        # 부모 디렉토리의 동생인 src/config를 가리킵니다.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.normpath(os.path.join(current_dir, '..', 'config'))
        
        # 레이어 초기화
        self.crew = NewsCrew(self.config_path)
        self.email_adapter = SmtpEmailAdapter(
            sender=os.getenv("EMAIL_SENDER"),
            password=os.getenv("EMAIL_PASSWORD")
        )

    def run_daily_automation(self):
        """뉴스 조사부터 발송까지의 전체 자동화 프로세스를 안전하게 기동합니다."""
        # 현재 한국 시간(시:분) 및 어제 날짜 계산
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        
        current_time_str = now.strftime('%H:%M')
        yesterday_date_str = yesterday.strftime('%Y-%m-%d')
        
        self.logger.info(f"🚀 AI 뉴스 및 대한민국 트렌드 수집 시작... (대상 일자: {yesterday_date_str}, 현재 시각: {current_time_str})")
        
        # 1. 비즈니스 도메인 로직 실행 (전날 날짜와 현재 시각 전달)
        # CrewAI의 verbose 출력을 파일로 캡처하여 사고과정 디버깅
        thought_log_path = os.path.join(self.log_dir, 'agent_thoughts.log')
        with open(thought_log_path, 'w', encoding='utf-8') as f:
            with contextlib.redirect_stdout(f):
                result = self.crew.run(current_time=current_time_str, yesterday_date=yesterday_date_str)
        
        self.logger.info("✅ CrewAI 작업 완료")
        
        # 2. 인프라 레이어를 통해 이메일 발송
        raw_receivers = os.getenv("EMAIL_RECEIVER", "")
        receiver_list = [r.strip() for r in raw_receivers.split(',') if r.strip()]
        
        if receiver_list:
            self.email_adapter.send_report(receiver_list, str(result))
        else:
            self.logger.warning("⚠️ 수신자 목록(EMAIL_RECEIVER)이 비어있어 메일을 발송하지 못했습니다.")
