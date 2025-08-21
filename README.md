# Webスクレイピングプロジェクト

このプロジェクトは、Pythonを使ったWebスクレイピングの様々な手法を実装したサンプルコード集です。

## 特徴

- **基本的なスクレイピング**: `requests`と`BeautifulSoup`を使った静的コンテンツの取得
- **ニュースサイトスクレイピング**: 記事のタイトル、本文、日付などの情報を抽出
- **Seleniumスクレイピング**: JavaScriptで動的に生成されるコンテンツの取得
- **データ保存**: JSON、CSV形式でのデータ保存機能

## 必要な環境

- Python 3.7以上
- Chromeブラウザ（Seleniumスクレイピング用）

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. ChromeDriverのインストール（Selenium用）

macOSの場合：
```bash
# Homebrewを使用
brew install chromedriver

# または、手動でダウンロード
# https://chromedriver.chromium.org/ からダウンロード
```

### 3. 仮想環境の作成（推奨）

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

## 使用方法

### 基本的なスクレイピング

```bash
python basic_scraper.py
```

### ニュースサイトのスクレイピング

```bash
python news_scraper.py
```

### Seleniumを使った動的コンテンツのスクレイピング

```bash
python selenium_scraper.py
```

## スクリプトの説明

### 1. `basic_scraper.py`
- `requests`と`BeautifulSoup`を使った基本的なWebスクレイピング
- ページのタイトル、見出し、リンクを取得
- 取得したデータをJSON、CSV形式で保存

### 2. `news_scraper.py`
- ニュースサイトから記事情報を抽出
- 記事のタイトル、説明、日付、本文の一部を取得
- 複数のニュースサイトを一括処理

### 3. `selenium_scraper.py`
- Seleniumを使った動的コンテンツのスクレイピング
- JavaScriptで生成されるコンテンツの取得
- ページのスクロール機能
- ソーシャルメディアの投稿データの抽出

## カスタマイズ

### スクレイピング対象サイトの変更

各スクリプト内のURLを変更することで、異なるサイトをスクレイピングできます。

```python
# basic_scraper.py
data = scraper.scrape_example_site("https://your-target-site.com")

# news_scraper.py
target_sites = [
    "https://your-news-site1.com",
    "https://your-news-site2.com",
]
```

### 取得データの調整

各スクリプト内のセレクターやパターンを調整することで、取得するデータをカスタマイズできます。

## 注意事項

### 法的・倫理的配慮

1. **robots.txtの確認**: スクレイピング対象サイトのrobots.txtを必ず確認してください
2. **利用規約の遵守**: サイトの利用規約に従ってスクレイピングを行ってください
3. **サーバー負荷の配慮**: 適切な間隔を空けてリクエストを送信してください
4. **個人情報の取り扱い**: 取得したデータの取り扱いには十分注意してください

### 技術的配慮

1. **User-Agentの設定**: 適切なUser-Agentを設定してください
2. **エラーハンドリング**: ネットワークエラーやパースエラーへの対応を実装してください
3. **レート制限**: サーバーに負荷をかけないよう適切な待機時間を設定してください

## トラブルシューティング

### よくある問題

1. **ChromeDriverが見つからない**
   - ChromeDriverがインストールされているか確認
   - PATHが正しく設定されているか確認

2. **依存関係のエラー**
   - `pip install -r requirements.txt`を再実行
   - 仮想環境が有効になっているか確認

3. **スクレイピングが失敗する**
   - 対象サイトのHTML構造が変更されていないか確認
   - セレクターを適切に調整

## ライセンス

このプロジェクトは教育目的で作成されています。商用利用の際は、各ライブラリのライセンスを確認してください。

## 貢献

バグ報告や改善提案は歓迎します。プルリクエストも受け付けています。

## 参考資料

- [BeautifulSoup公式ドキュメント](https://www.crummy.com/software/BeautifulSoup/)
- [Selenium公式ドキュメント](https://selenium-python.readthedocs.io/)
- [requests公式ドキュメント](https://requests.readthedocs.io/)
