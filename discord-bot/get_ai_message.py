import os

from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def remove_surrounding_brackets(text, left_bracket="「", right_bracket="」"):
    """
    文字列の両端に指定されたカッコがあれば削除する。

    Args:
        text (str): 入力文字列。
        left_bracket (str): 左側のカッコ（デフォルトは「）。
        right_bracket (str): 右側のカッコ（デフォルトは」）。

    Returns:
        str: カッコが削除された文字列。
    """
    if text.startswith(left_bracket) and text.endswith(right_bracket):
        return text[len(left_bracket) : -len(right_bracket)]
    return text


def create_ai_comment(message, reaction):
    prompt = f"""
    「{message}」というコメントに{reaction}のリアクションをしたユーザーが発言しそうなことを生成して．
    長さは短めで気軽な発言系でお願いします。
    """

    completion = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])

    raw_text = completion.choices[0].message.content

    return remove_surrounding_brackets(raw_text)
