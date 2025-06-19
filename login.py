import logging
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ログ設定
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def dump_slack_state():
    logging.info("=== Slack ログイン状態ダンプ 開始 ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        logging.info("ブラウザを起動しました")

        context = browser.new_context()
        page = context.new_page()
        logging.info("新規ページを開き、Slack Web にアクセスします")

        page.goto("https://app.slack.com/client")
        logging.info("Slack Web へナビゲート完了")

        # ここで手動ログイン操作を行ってください
        logging.info("手動ログインを待機中…（最大 3 分）")
        try:
            page.wait_for_selector(
                "[data-qa='message_input']", timeout=180_000  # 180,000 ms = 3 分
            )
            logging.info("ログイン完了を検出しました")
        except PlaywrightTimeoutError:
            logging.error(
                "3分経過してもログイン完了を検出できませんでした。処理を中断します。"
            )
            browser.close()
            return

        # ログイン完了後に状態をファイルに保存
        state_path = "state.json"
        context.storage_state(path=state_path)
        logging.info(f"ストレージ状態を '{state_path}' に保存しました")

        browser.close()
        logging.info("ブラウザを閉じました")
    logging.info("=== Slack ログイン状態ダンプ 完了 ===")


if __name__ == "__main__":
    dump_slack_state()
