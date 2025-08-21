#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seleniumを使った動的コンテンツのスクレイピングスクリプト
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import pandas as pd
from datetime import datetime
import os

class SeleniumScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Chromeドライバーをセットアップ"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # その他のオプション
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # ドライバーを作成
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            
            print("Chromeドライバーのセットアップが完了しました")
            
        except Exception as e:
            print(f"ドライバーのセットアップに失敗: {e}")
            print("ChromeDriverがインストールされているか確認してください")
    
    def scrape_dynamic_content(self, url, wait_time=5):
        """動的コンテンツを含むページをスクレイピング"""
        try:
            print(f"動的コンテンツをスクレイピング中: {url}")
            
            # ページにアクセス
            self.driver.get(url)
            
            # ページの読み込みを待機
            time.sleep(wait_time)
            
            # ページの基本情報を取得
            page_info = {
                'url': url,
                'title': self.driver.title,
                'current_url': self.driver.current_url,
                'scraped_at': datetime.now().isoformat()
            }
            
            return page_info
            
        except Exception as e:
            print(f"ページの取得に失敗: {e}")
            return None
    
    def scrape_social_media_posts(self, url, max_posts=10):
        """ソーシャルメディアの投稿をスクレイピング"""
        try:
            print(f"ソーシャルメディアの投稿をスクレイピング中: {url}")
            
            self.driver.get(url)
            time.sleep(5)  # 投稿の読み込みを待機
            
            posts = []
            
            # 投稿の要素を探す（Twitter風の例）
            post_selectors = [
                '[data-testid="tweet"]',  # Twitter
                '.post',                   # 一般的
                '.tweet',                  # Twitter風
                '[data-testid="post"]',    # Facebook風
            ]
            
            for selector in post_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"セレクター '{selector}' で {len(elements)} 件の要素を発見")
                        
                        for i, element in enumerate(elements[:max_posts]):
                            try:
                                post_data = self._extract_post_data(element, selector)
                                if post_data:
                                    posts.append(post_data)
                            except Exception as e:
                                print(f"投稿データの抽出に失敗: {e}")
                                continue
                        
                        break  # 最初に見つかったセレクターを使用
                        
                except Exception as e:
                    print(f"セレクター '{selector}' の処理に失敗: {e}")
                    continue
            
            return posts
            
        except Exception as e:
            print(f"ソーシャルメディアのスクレイピングに失敗: {e}")
            return []
    
    def _extract_post_data(self, element, selector_type):
        """投稿要素からデータを抽出"""
        try:
            post_data = {
                'selector_type': selector_type,
                'scraped_at': datetime.now().isoformat()
            }
            
            # テキストコンテンツを取得
            try:
                text_elements = element.find_elements(By.CSS_SELECTOR, 'p, span, div')
                text_content = ' '.join([el.text for el in text_elements if el.text.strip()])
                post_data['text_content'] = text_content[:500] + "..." if len(text_content) > 500 else text_content
            except:
                post_data['text_content'] = "テキスト取得失敗"
            
            # 画像URLを取得
            try:
                img_elements = element.find_elements(By.CSS_SELECTOR, 'img')
                image_urls = [img.get_attribute('src') for img in img_elements if img.get_attribute('src')]
                post_data['image_urls'] = image_urls
            except:
                post_data['image_urls'] = []
            
            # リンクを取得
            try:
                link_elements = element.find_elements(By.CSS_SELECTOR, 'a')
                links = [link.get_attribute('href') for link in link_elements if link.get_attribute('href')]
                post_data['links'] = links
            except:
                post_data['links'] = []
            
            # タイムスタンプを取得
            try:
                time_elements = element.find_elements(By.CSS_SELECTOR, 'time, [datetime]')
                if time_elements:
                    timestamp = time_elements[0].get_attribute('datetime') or time_elements[0].text
                    post_data['timestamp'] = timestamp
                else:
                    post_data['timestamp'] = "タイムスタンプなし"
            except:
                post_data['timestamp'] = "タイムスタンプ取得失敗"
            
            return post_data
            
        except Exception as e:
            print(f"投稿データの抽出でエラー: {e}")
            return None
    
    def scroll_and_scrape(self, url, scroll_count=5, scroll_pause=2):
        """ページをスクロールしながらスクレイピング"""
        try:
            print(f"スクロールしながらスクレイピング中: {url}")
            
            self.driver.get(url)
            time.sleep(3)
            
            all_content = []
            
            for i in range(scroll_count):
                print(f"スクロール {i+1}/{scroll_count}")
                
                # 現在のページの高さを取得
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # ページの最下部までスクロール
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # 新しいコンテンツの読み込みを待機
                time.sleep(scroll_pause)
                
                # 新しい高さを取得
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # 現在のページのコンテンツを取得
                current_content = self._get_current_page_content()
                all_content.extend(current_content)
                
                # ページの高さが変わらなければ、これ以上スクロールできない
                if new_height == last_height:
                    print("ページの最下部に到達しました")
                    break
            
            return all_content
            
        except Exception as e:
            print(f"スクロールスクレイピングに失敗: {e}")
            return []
    
    def _get_current_page_content(self):
        """現在のページのコンテンツを取得"""
        try:
            # 一般的なコンテンツ要素を探す
            content_elements = self.driver.find_elements(By.CSS_SELECTOR, 'p, h1, h2, h3, h4, h5, h6, div')
            
            content_list = []
            for element in content_elements:
                text = element.text.strip()
                if text and len(text) > 10:  # 短すぎるテキストは除外
                    content_list.append({
                        'tag': element.tag_name,
                        'text': text,
                        'timestamp': datetime.now().isoformat()
                    })
            
            return content_list
            
        except Exception as e:
            print(f"現在のページコンテンツの取得に失敗: {e}")
            return []
    
    def save_data(self, data, filename='selenium_scraped_data.json'):
        """データをJSONファイルに保存"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"データを {filename} に保存しました")
        except Exception as e:
            print(f"保存エラー: {e}")
    
    def close(self):
        """ドライバーを閉じる"""
        if self.driver:
            self.driver.quit()
            print("Chromeドライバーを閉じました")

def main():
    """メイン関数"""
    print("=== Seleniumスクレイピング開始 ===")
    
    scraper = SeleniumScraper(headless=True)
    
    try:
        # 基本的な動的コンテンツのスクレイピング
        print("\n1. 基本的な動的コンテンツのスクレイピング")
        page_info = scraper.scrape_dynamic_content("https://example.com")
        if page_info:
            print(f"ページタイトル: {page_info['title']}")
        
        # スクロールスクレイピングの例
        print("\n2. スクロールスクレイピング")
        scroll_content = scraper.scroll_and_scrape("https://example.com", scroll_count=3)
        print(f"スクロールで取得したコンテンツ数: {len(scroll_content)}")
        
        # データを保存
        all_data = {
            'page_info': page_info,
            'scroll_content': scroll_content,
            'scraped_at': datetime.now().isoformat()
        }
        
        scraper.save_data(all_data)
        
    except Exception as e:
        print(f"メイン処理でエラー: {e}")
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
