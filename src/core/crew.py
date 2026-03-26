import os
import yaml
from datetime import datetime
from crewai import Agent, Task, Crew, Process, LLM
from infrastructure.search.searxng_adapter import searxng_search
from infrastructure.search.rss_adapter import rss_news_fetcher

class NewsCrew:
    def __init__(self, config_path):
        self.config_path = config_path
        self.agents_config = self._load_yaml('agents.yaml')
        self.tasks_config = self._load_yaml('tasks.yaml')
        # CrewAI LLM 클래스를 사용하여 로컬 Ollama 호출
        self.llm = LLM(
            model="ollama/qwen3.5",
            base_url="http://localhost:11434"
        )

    def _load_yaml(self, filename):
        path = os.path.join(self.config_path, filename)
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def run(self, current_time, yesterday_date):
        """CrewAI 에이전트들을 기동하여 AI 뉴스 수집 및 요약을 수행합니다."""
        today_date = datetime.now().strftime('%Y-%m-%d')

        # 1. 에이전트 설정 동적 포맷팅 (오늘 날짜 및 어제 날짜 주입)
        formatted_agents = {}
        for key, cfg in self.agents_config.items():
            # 사용 중인 에이전트만 포맷팅
            if key in ['news_researcher', 'summary_editor']:
                formatted_agents[key] = {
                    'role': cfg['role'],
                    'goal': cfg['goal'].format(today_date=today_date, yesterday_date=yesterday_date),
                    'backstory': cfg['backstory'].format(today_date=today_date, yesterday_date=yesterday_date)
                }

        # 사고과정 캡처를 위한 콜백 함수
        def step_callback(agent_output):
            # stdout 리다이렉션으로 인해 이 출력은 logs/agent_thoughts.log에 기록됩니다.
            print(f"\n[STEP CALLBACK]\n{agent_output}\n")

        # 2. 에이전트 생성
        ai_researcher = Agent(
            config=formatted_agents['news_researcher'],
            tools=[searxng_search, rss_news_fetcher],
            llm=self.llm,
            verbose=True,
            step_callback=step_callback
        )

        editor = Agent(
            config=formatted_agents['summary_editor'],
            llm=self.llm,
            verbose=True,
            step_callback=step_callback
        )

        # 3. 작업 정의 (AI 뉴스 전용)
        ai_research_desc = self.tasks_config['ai_research_task']['description'].format(
            today_date=today_date, yesterday_date=yesterday_date
        )

        task1 = Task(
            config=self.tasks_config['ai_research_task'],
            description=ai_research_desc,
            agent=ai_researcher
        )

        # AI 수집 결과를 에디터에게 전달
        task_summary = Task(
            config=self.tasks_config['email_formatting_task'],
            description=self.tasks_config['email_formatting_task']['description'].format(
                current_time=current_time, 
                today_date=today_date, 
                yesterday_date=yesterday_date
            ),
            agent=editor,
            context=[task1] # AI 수집 결과만 전달
        )

        # 3. 크루 구성 및 실행
        crew = Crew(
            agents=[ai_researcher, editor],
            tasks=[task1, task_summary],
            process=Process.sequential,
            verbose=True,
            manager_llm=self.llm
        )

        return crew.kickoff()
