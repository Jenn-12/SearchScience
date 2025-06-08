import requests
from bs4 import BeautifulSoup

TARGET_SITES = [
    "https://www.sciencetimes.co.kr",
    "https://www.kisti.re.kr",
    "https://www.konas.net"
]

def crawl_site(url, keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        results = []

        for a in soup.find_all('a', href=True):
            title = a.get_text(strip=True)
            href = a['href']
            if keyword in title:
                full_url = href if href.startswith("http") else url + href
                results.append({'title': title, 'url': full_url})
        return results
    except Exception as e:
        print(f"[오류] {url} 에서 데이터를 가져오지 못했습니다: {e}")
        return []

def search_all(keyword):
    all_results = []
    for site in TARGET_SITES:
        print(f"{site} 크롤링 중...")
        all_results.extend(crawl_site(site, keyword))
    return all_results

if __name__ == "__main__":
    query = input("검색어를 입력하세요: ")
    results = search_all(query)
    for r in results:
        print(f"{r['title']} - {r['url']}")
