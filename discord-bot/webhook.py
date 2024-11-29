import json
import os

from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()


# 環境変数から辞書を読み込む
def get_webhook_urls():
    webhook_urls_str = os.getenv("WEBHOOK_URLS")
    if webhook_urls_str:
        try:
            # 環境変数を辞書形式に変換
            webhook_urls = json.loads(webhook_urls_str)
            return webhook_urls
        except json.JSONDecodeError:
            raise ValueError("環境変数 WEBHOOK_URLS の形式が正しくありません。JSON形式で指定してください。")
    else:
        raise ValueError("環境変数 WEBHOOK_URLS が設定されていません。")


# 実際に使用
try:
    WEBHOOK_URLS = get_webhook_urls()
    print(WEBHOOK_URLS)  # {'1123': 'bbb', '130': 'aaa'}
except ValueError as e:
    print(e)
