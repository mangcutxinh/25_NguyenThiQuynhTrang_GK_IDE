import requests
from bs4 import BeautifulSoup
import time
import csv
url = "https://vnexpress.net/cong-nghe/ai"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_url(url, headers, retries=3, delay=2):
    """Fetch a URL with retries and error handling."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            if response.status_code == 200:
                return response
            else:
                print(f"Lỗi HTTP {response.status_code} khi truy cập {url}")
        except requests.exceptions.RequestException as e:
            print(f"Lỗi kết nối: {e}. Thử lại ({attempt + 1}/{retries})...")
        time.sleep(delay)
    print(f"Không thể truy cập {url} sau {retries} lần thử.")
    return None
response = fetch_url(url, headers)
if not response:
    print("Không thể truy cập trang web chính. Thoát chương trình.")
    exit()
soup = BeautifulSoup(response.text, 'html.parser')
articles = soup.find_all('article', class_='item-news')
article_list = []
for article in articles[:5]:   
    title_tag = article.find('h2', class_='title-news') or article.find('h3', class_='title-news')
    if title_tag and title_tag.find('a'):
        title = title_tag.find('a').text.strip()
        article_url = title_tag.find('a')['href']
    else:
        continue
    summary_tag = article.find('p', class_='description')
    summary = summary_tag.text.strip() if summary_tag else "Không có tóm tắt"
    article_response = fetch_url(article_url, headers)
    if not article_response:
        print(f"Bỏ qua bài viết: {title} do không thể truy cập URL.")
        continue
    article_soup = BeautifulSoup(article_response.text, 'html.parser')
    time_tag = article_soup.find('span', class_='date')
    time_value = time_tag.text.strip() if time_tag else "Không có thời gian"
    author_tag = article_soup.find('p', class_='Normal', style='text-align:right;')
    if author_tag:
        author = author_tag.text.strip()
    else:
        author_tag = article_soup.find('p', class_='author_mail')
        author = author_tag.find('strong').text.strip() if author_tag and author_tag.find('strong') else "Không có tác giả"

    
    article_info = {
        'title': title,
        'url': article_url,
        'summary': summary,
        'time': time_value,
        'author': author
    }
    article_list.append(article_info)

    
    time.sleep(1)


for idx, article in enumerate(article_list, 1):
    print(f"Bài viết {idx}:")
    print(f"Tiêu đề: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Tóm tắt: {article['summary']}")
    print(f"Thời gian: {article['time']}")
    print(f"Tác giả: {article['author']}")
    print("-" * 50)
with open('articles.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['title', 'url', 'summary', 'time', 'author'])
    writer.writeheader()
    writer.writerows(article_list)
print("Đã lưu dữ liệu vào file articles.csv")