#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Call Runtime /process endpoint and print SSE events."""

import json
import requests


URL = "http://127.0.0.1:8090/process"
PAYLOAD = {
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请给我一个今日电力现货交易的简要分析模板。",
                },
            ],
        },
    ],
    "session_id": "mvp-session-1",
    "user_id": "demo-user",
}


def main() -> None:
    with requests.post(URL, json=PAYLOAD, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for raw_line in resp.iter_lines(decode_unicode=True):
            if not raw_line or not raw_line.startswith("data:"):
                continue
            data_str = raw_line[len("data:") :].strip()
            if data_str == "[DONE]":
                print("[DONE]")
                break
            try:
                event = json.loads(data_str)
            except json.JSONDecodeError:
                print(data_str)
                continue
            print(json.dumps(event, ensure_ascii=False))


if __name__ == "__main__":
    main()
