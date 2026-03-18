import os
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from crewai import LLM, Agent, Task, Crew, Process
from crewai.tools import tool

# 1. 환경 변수 로드 (.env.local 사용)
load_dotenv(".env.local")

# 2. 무료 검색 도구 (DuckDuckGo)
@tool("DuckDuckGoSearch")
def duckduckgo_search(query: str):
    """인터넷 검색을 통해 24시간 이내 발생한 최신 AI 이슈를 찾아냅니다."""
    return DuckDuckGoSearchRun(backend='news', timelimit='d').run(query)

class AiNewsAutomation:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(base_dir, 'config')
        
        self.agents_config = self._load_yaml('agents.yaml')
        self.tasks_config = self._load_yaml('tasks.yaml')

        # Qwen 3.5 모델
        self.llm = LLM(
            model="ollama/qwen3.5:latest",
            base_url="http://127.0.0.1:11434",
            config=dict(
                num_ctx=32768,
                temperature=0.7
            )
        )

    def _load_yaml(self, filename):
        path = os.path.join(self.config_path, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def send_email(self, content):
        """다중 수신자에게 메일을 발송하는 핵심 로직"""
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")
        
        
        # .env.local에서 읽어온 문자열을 리스트로 변환 (공백 제거 포함)
        raw_receivers = os.getenv("EMAIL_RECEIVER", "")
        receiver_list = [r.strip() for r in raw_receivers.split(',') if r.strip()]

        if not receiver_list:
            print("⚠️ 수신자 메일 주소가 설정되지 않았습니다.")
            return

        msg = MIMEMultipart()
        msg['From'] = sender
        # 메일함 상단에 수신자 전원이 표시되도록 처리 (없으면 숨긴 참조 처리)
        msg['To'] = ", ".join(receiver_list)
        msg['Subject'] = "오늘의 AI 핵심 이슈 요약 리포트 (다중 발송)"

        msg.attach(MIMEText(content, 'plain'))

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                # 리스트 형태로 수신자를 전달하여 일괄 발송
                server.sendmail(sender, receiver_list, msg.as_string())
            print(f"✅ 총 {len(receiver_list)}명에게 메일 발송 성공!")
            print(f"📧 수신자: {', '.join(receiver_list)}")
        except Exception as e:
            print(f"❌ 메일 발송 실패: {e}")

    def run(self):
        # 오늘 날짜 주입
        today = datetime.now().strftime('%Y-%m-%d')
        
        # YAML 설정을 기반으로 에이전트 생성
        researcher = Agent(
            config=self.agents_config['news_researcher'],
            tools=[duckduckgo_search],
            llm=self.llm,
            verbose=True
        )

        editor = Agent(
            config=self.agents_config['summary_editor'],
            llm=self.llm,
            verbose=True
        )

        # YAML 내용을 가져와서 날짜만 치환(format)합니다.
        research_task_description = self.tasks_config['research_task']['description'].format(current_date=today)

        # YAML 설정을 기반으로 작업 생성
        task1 = Task(
            config=self.tasks_config['research_task'],
            description=research_task_description,
            agent=researcher
        )

        task2 = Task(
            config=self.tasks_config['email_formatting_task'],
            agent=editor
        )

        crew = Crew(
            agents=[researcher, editor],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
        )

        print("🚀 [CrewAI] AI 뉴스 수집 및 요약 작업을 시작합니다...")
        result = crew.kickoff()
        
        # 최종 결과물 전송
        self.send_email(str(result))

if __name__ == "__main__":
    automation = AiNewsAutomation()
    automation.run()