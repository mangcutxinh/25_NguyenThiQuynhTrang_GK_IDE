import requests
from bs4 import BeautifulSoup
import time

# URL của trang danh sách bài viết
url = "https://vnexpress.net/cong-nghe/ai"

# Gửi yêu cầu HTTP để lấy nội dung trang web
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # Đảm bảo mã hóa UTF-8 để hiển thị đúng tiếng Việt

# Kiểm tra nếu yêu cầu thành công
if response.status_code != 200:
    print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
    exit()

# Phân tích HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Tìm các bài viết trong trang (dựa trên thẻ <article> với class="item-news")
articles = soup.find_all('article', class_='item-news')

# Danh sách để lưu trữ thông tin bài viết
article_list = []

# Crawl ít nhất 5 bài viết
for article in articles[:5]:  # Lấy 5 bài đầu tiên
    # Lấy tiêu đề và URL
    title_tag = article.find('h2', class_='title-news') or article.find('h3', class_='title-news')
    if title_tag and title_tag.find('a'):
        title = title_tag.find('a').text.strip()
        article_url = title_tag.find('a')['href']
    else:
        continue

    # Lấy tóm tắt
    summary_tag = article.find('p', class_='description')
    summary = summary_tag.text.strip() if summary_tag else "Không có tóm tắt"

    # Truy cập vào URL của bài viết để lấy time và author
    article_response = requests.get(article_url, headers=headers)
    article_response.encoding = 'utf-8'
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # Lấy thời gian đăng bài (dựa trên thẻ <span class="date">)
    time_tag = article_soup.find('span', class_='date')
    time_value = time_tag.text.strip() if time_tag else "Không có thời gian"

    # Lấy tác giả
    author_tag = article_soup.find('p', class_='Normal', style='text-align:right;')
    if author_tag:
        author = author_tag.text.strip()
    else:
        # Trường hợp 2: Tác giả nằm trong <p class="author_mail"><strong>
        author_tag = article_soup.find('p', class_='author_mail')
        author = author_tag.find('strong').text.strip() if author_tag and author_tag.find('strong') else "Không có tác giả"

    # Làm sạch dữ liệu
    # Loại bỏ tất cả các thẻ HTML trong summary, title, author, và time
    clean_title = BeautifulSoup(title, "html.parser").get_text()
    clean_summary = BeautifulSoup(summary, "html.parser").get_text()
    clean_time = BeautifulSoup(time_value, "html.parser").get_text()
    clean_author = BeautifulSoup(author, "html.parser").get_text()

    # Lưu thông tin bài viết vào dictionary
    article_info = {
        'title': clean_title,
        'url': article_url,
'summary': clean_summary,
        'time': clean_time,
        'author': clean_author
    }
    article_list.append(article_info)

    # Thêm độ trễ để tránh bị chặn bởi server
    time.sleep(1)

# In kết quả sau khi làm sạch dữ liệu
for idx, article in enumerate(article_list, 1):
    print(f"Bài viết {idx}:")
    print(f"Tiêu đề: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Tóm tắt: {article['summary']}")
    print(f"Thời gian: {article['time']}")
    print(f"Tác giả: {article['author']}")
    print("-" * 50)