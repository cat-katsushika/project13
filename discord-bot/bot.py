import os
import re

import discord
import requests

from get_ai_message import create_ai_comment
from webhook import WEBHOOK_URLS

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # メンバーの状態変更を受け取るために必要

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
    channel = client.get_channel(channel_id)
    if channel is None:
        print("チャンネルが見つかりません。DISCORD_CHANNEL_IDを確認してください。")
    else:
        await channel.send(f"{WEBHOOK_URLS}ボットがオンラインになりました。")


@client.event
async def on_raw_reaction_add(payload):
    """
    リアクションの追加イベント
    """
    # リアクションを押したユーザーがボットの場合は無視
    if payload.member.bot:
        return

    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    message_content = message.content
    message_user_id = message.author.id
    reaction_emoji = payload.emoji.name
    print(payload.channel_id)

    text = create_ai_comment(message_content, reaction_emoji)

    webhook_url = WEBHOOK_URLS[str(payload.channel_id)]
    if webhook_url is None:
        print("Webhook URLが見つかりません。")
        return

    # 引用を含む形でメッセいーじを構成
    formatted_message = format_quoted_message(message_user_id, message.author.display_name, message_content, text)
    username = payload.member.display_name
    avatar_url = payload.member.avatar.url if payload.member.avatar else payload.member.default_avatar.url

    # Webhookでメッセージ送信
    send_webhook_reply(webhook_url, formatted_message, username, avatar_url)


def send_webhook_reply(webhook_url, message, username, avatar_url):
    data = {
        "content": message,
        "username": username,
        "avatar_url": avatar_url,
    }
    requests.post(webhook_url, data=data, timeout=10)


def format_quoted_message(user_id: int, username: str, message_content: str, reply_text: str) -> str:
    """
    引用形式でメッセージをフォーマットする。

    Args:
        user_id (int): 引用元メッセージの送信者のID。
        username (str): 引用元メッセージの送信者の名前。
        message_content (str): 引用元メッセージの内容。
        reply_text (str): 引用メッセージに追加する返信内容。

    Returns:
        str: 引用形式にフォーマットされたメッセージ。
    """
    # 元メッセージを引用形式に整形（改行対応）

    quoted_message = "\n".join(
        f"> {line}" for line in message_content.splitlines()
        if not re.search(r'https?://', line)
    )

    # 全体のメッセージを構築
    formatted_message = f"<@{user_id}> ({username}) さんのメッセージ:\n" f"{quoted_message}\n\n" f"{reply_text}"

    return formatted_message


client.run(os.getenv("DISCORD_TOKEN"))
