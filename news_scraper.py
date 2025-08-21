#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ニュースサイトのスクレイピングスクリプト
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import json
from datetime import datetime
import re

class NewsScraper:
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
    
    def scrape_news_site(self, url, max_articles=10):
        """ニュースサイトから記事情報を取得"""
        try:
            print(f"ニュースサイトをスクレイピング中: {url}")
            
            # ページを取得
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            articles = []
            
            # 記事のリンクを探す（一般的なパターン）
            article_links = soup.find_all('a', href=True)
            
            for link in article_links:
                if len(articles) >= max_articles:
                    break
                
                href = link.get('href')
                text = link.get_text().strip()
                
                # 記事らしいリンクかチェック
                if self._is_article_link(href, text):
                    # 相対URLを絶対URLに変換
                    if href.startswith('/'):
                        full_url = url.rstrip('/') + href
                    elif href.startswith('http'):
                        full_url = href
                    else:
                        continue
                    
                    # 記事の詳細を取得
                    article_info = self._get_article_info(full_url)
                    if article_info:
                        articles.append(article_info)
                        time.sleep(1)  # サーバーに負荷をかけないよう待機
            
            return articles
            
        except Exception as e:
            print(f"エラー: {e}")
            return []
    
    def _is_article_link(self, href, text):
        """記事のリンクかどうかを判定"""
        if not href or not text:
            return False
        
        # 記事らしいパターンをチェック
        article_patterns = [
            r'/article/',
            r'/news/',
            r'/story/',
            r'/post/',
            r'\d{4}/\d{2}/\d{2}',  # 日付パターン
        ]
        
        for pattern in article_patterns:
            if re.search(pattern, href):
                return True
        
        # テキストの長さで判定
        if len(text) > 20 and len(text) < 200:
            return True
        
        return False
    
    def _get_article_info(self, url):
        """記事の詳細情報を取得"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # タイトルを取得
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "タイトルなし"
            
            # 見出しを取得
            h1 = soup.find('h1')
            h1_text = h1.get_text().strip() if h1 else ""
            
            # メタディスクリプションを取得
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            # 日付を探す
            date_text = self._extract_date(soup)
            
            # 本文の一部を取得
            content = self._extract_content(soup)
            
            return {
                'url': url,
                'title': title_text,
                'h1': h1_text,
                'description': description,
                'date': date_text,
                'content_preview': content[:200] + "..." if len(content) > 200 else content,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"記事の取得に失敗: {url} - {e}")
            return None
    
    def _extract_date(self, soup):
        """ページから日付を抽出"""
        # 様々な日付パターンを試す
        date_patterns = [
            r'\d{4}年\d{1,2}月\d{1,2}日',
            r'\d{4}-\d{1,2}-\d{1,2}',
            r'\d{4}/\d{1,2}/\d{1,2}',
            r'\d{1,2}/\d{1,2}/\d{4}',
        ]
        
        # テキストから日付を探す
        text = soup.get_text()
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return "日付不明"
    
    def _extract_content(self, soup):
        """ページから本文を抽出"""
        # 一般的な本文の要素を探す
        content_selectors = [
            'article',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-body',
            'main',
            'p'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                # 最初の要素からテキストを取得
                text = elements[0].get_text().strip()
                if len(text) > 100:  # 十分な長さのテキストがある場合
                    return text
        
        return "本文なし"
    
    def save_articles(self, articles, filename='news_articles.json'):
        """記事データをJSONファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"記事データを {filename} に保存しました")
        except Exception as e:
            print(f"保存エラー: {e}")
    
    def save_to_csv(self, articles, filename='news_articles.csv'):
        """記事データをCSVファイルに保存"""
        try:
            if articles:
                df = pd.DataFrame(articles)
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"記事データを {filename} に保存しました")
        except Exception as e:
            print(f"CSV保存エラー: {e}")

def main():
    """メイン関数"""
    print("=== ニュースサイトスクレイピング開始 ===")
    
    scraper = NewsScraper()
    
    # スクレイピング対象のサイト（例）
    target_sites = [
        "https://www.yahoo.co.jp/news/",
        "https://www.asahi.com/",
        "https://www.mainichi.jp/",
    ]
    
    all_articles = []
    
    for site in target_sites:
        print(f"\n{site} を処理中...")
        articles = scraper.scrape_news_site(site, max_articles=5)
        all_articles.extend(articles)
        print(f"{len(articles)} 件の記事を取得")
    
    if all_articles:
        print(f"\n合計 {len(all_articles)} 件の記事を取得しました")
        
        # データを保存
        scraper.save_articles(all_articles)
        scraper.save_to_csv(all_articles)
        
        # 最初の3件を表示
        print("\n取得した記事の例:")
        for i, article in enumerate(all_articles[:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   URL: {article['url']}")
            print(f"   日付: {article['date']}")
            print(f"   説明: {article['description'][:100]}...")
    else:
        print("記事の取得に失敗しました")

if __name__ == "__main__":
    main()
