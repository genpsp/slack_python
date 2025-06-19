import time
import random
import logging
from playwright.sync_api import sync_playwright

# ログ設定
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def keep_slack_online():
    logging.info("=== Slack Online Keeper を開始 ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        logging.info("ブラウザを起動しました")

        context = browser.new_context(storage_state="state.json")
        logging.info("storage_state を復元しました")

        page = context.new_page()
        page.goto("https://app.slack.com/client")
        logging.info("Slack Web にアクセスしました")

        page.wait_for_selector("[data-qa='message_input']", timeout=60000)
        logging.info("ログイン完了を検出しました")

        # ページにフォーカス
        page.bring_to_front()
        page.click("body")

        # ビューポート中央の y 座標を取得
        vp = page.viewport_size
        cy = vp["height"] // 2
        logging.info(f"ビューポート中央 y: {cy}")

        # サイドバー内での動きを想定した X 座標
        sidebar_x = 100
        logging.info(f"サイドバー想定 x: {sidebar_x}")

        iteration = 0

        while True:
            # ランダムに±10px移動
            dx = random.randint(-10, 10)
            dy = random.randint(-10, 10)
            x = sidebar_x + dx
            y = cy + dy
            steps = random.randint(5, 15)
            page.mouse.move(x, y, steps=steps)
            iteration += 1
            logging.info(
                f"[{iteration}] サイドバー上で仮想マウス移動: ({x}, {y}) steps={steps}"
            )

            # スクリーンショット保存
            # ts = int(time.time())
            # shot_path = f"screenshots/iter_{iteration}_{ts}.png"
            # page.screenshot(path=shot_path, full_page=False)
            # logging.info(f"[{iteration}] スクリーンショット保存: {shot_path}")

            # Quick Switcher を開くかどうか（40% の確率で開閉操作）
            if random.random() < 0.4:
                logging.info("検索欄（Quick Switcher）を開きます")
                page.keyboard.press("Meta+K")
                page.wait_for_timeout(1000)
                logging.info("検索欄を閉じます")
                page.keyboard.press("Escape")
                page.wait_for_timeout(500)
            else:
                logging.info("検索欄操作はスキップしました")

            # 次の操作までランダムに 7〜30 秒待機
            sleep_time = random.randint(7, 30)
            logging.info(f"{sleep_time}秒待機します")
            time.sleep(sleep_time)


if __name__ == "__main__":
    keep_slack_online()
