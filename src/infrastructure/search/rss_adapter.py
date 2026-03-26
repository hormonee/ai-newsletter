import feedparser
from datetime import datetime, timedelta
from crewai.tools import tool
import logging

logger = logging.getLogger(__name__)

# 신뢰할 수 있는 RSS 피드 목록
AI_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
    "https://cnvrg.io/feed/",
    "https://openai.com/news/rss.xml"
]

KOREA_FEEDS = [
    "https://www.yna.co.kr/rss/yonhap.xml",
    "https://rss.donga.com/total.xml",
    "https://www.khan.co.kr/rss/rssdata/total_news.xml",
    "https://rss.joins.com/joins_news_list.xml"
]

@tool("RSSNewsFetcher")
def rss_news_fetcher(category: str, yesterday_date: str):
    """지정된 카테고리(AI 또는 KOREA)의 신뢰할 수 있는 RSS 피드에서 전날({yesterday_date}) 발행된 뉴스만 가져옵니다.
    category: 'AI' 또는 'KOREA' 중 하나 선택
    yesterday_date: 'YYYY-MM-DD' 형식의 문자열 (필수)
    """
    feeds = AI_FEEDS if category.upper() == "AI" else KOREA_FEEDS
    target_date = datetime.strptime(yesterday_date, "%Y-%m-%d").date()
    
    results = []
    
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # 발행 일자(published_parsed) 추출
                pub_date_struct = entry.get("published_parsed") or entry.get("updated_parsed")
                if pub_date_struct:
                    pub_date = datetime(*pub_date_struct[:6]).date()
                    
                    # 전날 일치 여부 확인
                    if pub_date == target_date:
                        results.append({
                            "title": entry.title,
                            "link": entry.link,
                            "summary": entry.get("summary", ""),
                            "source": feed.feed.get("title", url)
                        })
        except Exception as e:
            logger.error(f"RSS 파싱 오류 ({url}): {e}")
            continue

    if not results:
        return f"⚠️ {yesterday_date}에 해당하는 {category} 뉴스가 RSS 피드에 없습니다."

    # 결과 포맷팅
    output = [f"### {category} News from RSS ({yesterday_date}) ###"]
    for i, res in enumerate(results[:15], 1): # 최대 15개
        output.append(f"{i}. {res['title']}")
        output.append(f"   출처: {res['source']}")
        output.append(f"   링크: {res['link']}")
        output.append(f"   요약: {res['summary'][:200]}...")
        output.append("")
        
    return "\n".join(output)
