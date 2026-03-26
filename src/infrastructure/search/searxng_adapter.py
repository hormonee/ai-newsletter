from crewai.tools import tool
from langchain_community.utilities import SearxSearchWrapper

@tool("SearXNGSearch")
def searxng_search(query: str):
    """인터넷 검색을 통해 24시간 이내 발생한 최신 이슈를 찾아냅니다. (SearXNG 이용)
    검색 시 ':day' 접두사와 SearXNG의 time_range 파라미터를 사용하여 최근 24시간 결과만 필터링합니다.
    """
    search = SearxSearchWrapper(
        searx_host="http://localhost:9090",
        engines=["google", "duckduckgo", "bing", "brave"],
        params={"time_range": "day"}
    )
    return search.run(f":day {query}")
