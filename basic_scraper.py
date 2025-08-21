#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本的なWebスクレイピングのサンプルスクリプト
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import json

class BasicScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_page(self, url, delay=1):
        """指定されたURLからページを取得"""
        try:
            print(f"取得中: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            time.sleep(delay)  # サーバーに負荷をかけないよう待機
            return response.text
        except requests.RequestException as e:
            print(f"エラー: {e}")
            return None
    
    def parse_html(self, html_content):
        """HTMLコンテンツをパース"""
        if html_content:
            return BeautifulSoup(html_content, 'lxml')
        return None
    
    def scrape_example_site(self, url="https://example.com"):
        """サンプルサイトのスクレイピング"""
        html = self.get_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        if not soup:
            return None
        
        # タイトルを取得
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "タイトルなし"
        
        # 見出しを取得
        headings = soup.find_all(['h1', 'h2', 'h3'])
        heading_texts = [h.get_text().strip() for h in headings]
        
        # リンクを取得
        links = soup.find_all('a', href=True)
        link_data = [{'text': a.get_text().strip(), 'href': a['href']} for a in links]
        
        return {
            'title': title_text,
            'headings': heading_texts,
            'links': link_data,
            'url': url
        }
    
    def save_to_json(self, data, filename='scraped_data.json'):
        """データをJSONファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"データを {filename} に保存しました")
        except Exception as e:
            print(f"保存エラー: {e}")
    
    def save_to_csv(self, data, filename='scraped_data.csv'):
        """データをCSVファイルに保存"""
        try:
            # リンクデータをDataFrameに変換
            if data.get('links'):
                df = pd.DataFrame(data['links'])
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"データを {filename} に保存しました")
        except Exception as e:
            print(f"保存エラー: {e}")

def main():
    """メイン関数"""
    print("=== 基本的なWebスクレイピング開始 ===")
    
    scraper = BasicScraper()
    
    # サンプルサイトをスクレイピング
    data = scraper.scrape_example_site()
    
    if data:
        print("\n取得したデータ:")
        print(f"タイトル: {data['title']}")
        print(f"見出し数: {len(data['headings'])}")
        print(f"リンク数: {len(data['links'])}")
        
        # データを保存
        scraper.save_to_json(data)
        scraper.save_to_csv(data)
        
        # 最初の5つのリンクを表示
        print("\n最初の5つのリンク:")
        for i, link in enumerate(data['links'][:5], 1):
            print(f"{i}. {link['text']} -> {link['href']}")
    else:
        print("データの取得に失敗しました")

if __name__ == "__main__":
    main()
