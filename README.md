# slack_python

シンプルな Playwright + Python を使った Slack 操作スクリプトです。
ブラウザで手動ログインしてセッションを保存し、その後保存した状態で自動処理を実行します。

## セットアップ

```bash
# (1) Python3 がインストールされていない場合
brew install python

# (2) 必要なパッケージをインストール
pip3 install playwright

# (3) Playwright のブラウザをインストール
playwright install
```

## 実行手順

### ログイン状態の保存 (初回のみ)

```bash
# 手動ログインしてセッション情報を state.json に保存
python3 login.py
```

- ブラウザが起動したら Slack にログインしてください。
- ログイン完了後、`state.json` が作成されます。

### 自動処理の実行

```bash
python3 script.py
```

- `state.json` を利用して Slack に自動ログインし、所定の処理を実行します。

### 2 回目以降の実行

以降はログイン状態が保存されているため、以下だけで OK です。

```bash
python3 script.py
```

## ファイル構成

- `login.py` … 手動ログインしてセッション状態を `state.json` に保存するスクリプト
- `script.py` … 保存したセッション情報を使って自動処理を行うメインスクリプト
