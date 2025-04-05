import psycopg2
import csv


DB_HOST = "localhost"
DB_NAME = "tri_db"
DB_USER = "admin"
DB_PASSWORD = "admin"


CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    summary TEXT,
    time TEXT,
    author TEXT
);
"""


try:
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Kết nối cơ sở dữ liệu thành công.")

    # Create the articles table if it doesn't exist
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    print("Bảng 'articles' đã được tạo hoặc đã tồn tại.")

    # Read data from articles.csv
    with open('C:/2024-2025/NMKTDL/25_NguyenThiQuynhTrang_GK_IDE/articles.csv', 'r', encoding='utf-8') as f:

        reader = csv.DictReader(f)
        articles = [row for row in reader]

    # Insert data into the articles table
    INSERT_QUERY = """
    INSERT INTO articles (title, url, summary, time, author)
    VALUES (%s, %s, %s, %s, %s)
    """
    for article in articles:
        cursor.execute(INSERT_QUERY, (
            article['title'],
            article['url'],
            article['summary'],
            article['time'],
            article['author']
        ))
    conn.commit()
    print(f"Đã lưu {len(articles)} bài viết vào cơ sở dữ liệu.")

except Exception as e:
    print(f"Lỗi: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    print("Đã đóng kết nối cơ sở dữ liệu.")