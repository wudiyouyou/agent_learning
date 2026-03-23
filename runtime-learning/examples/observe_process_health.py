#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple observability probe for Runtime /process endpoint."""

import json
import time
import requests

URL = "http://127.0.0.1:8090/process"


def probe_success() -> None:
    payload = {
        "input": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "一句话说明电力交易中的偏差考核。"}],
            },
        ],
        "session_id": "obs-session-ok",
    }
    t0 = time.time()
    done = False
    chunks = 0
    with requests.post(URL, json=payload, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            chunks += 1
            data_str = line[len("data:") :].strip()
            if data_str == "[DONE]":
                done = True
                break
    elapsed = time.time() - t0
    print(
        json.dumps(
            {
                "probe": "success",
                "http_status": 200,
                "sse_chunks": chunks,
                "done": done,
                "elapsed_sec": round(elapsed, 3),
            },
            ensure_ascii=False,
        ),
    )


def probe_validation_error() -> None:
    bad_payload = {"bad": "payload"}
    t0 = time.time()
    with requests.post(URL, json=bad_payload, stream=True, timeout=30) as resp:
        body = "".join(
            [line for line in resp.iter_lines(decode_unicode=True) if line],
        )
    elapsed = time.time() - t0
    print(
        json.dumps(
            {
                "probe": "validation_error",
                "http_status": 200,
                "contains_validation_error": "validation error" in body.lower(),
                "elapsed_sec": round(elapsed, 3),
            },
            ensure_ascii=False,
        ),
    )


if __name__ == "__main__":
    probe_success()
    probe_validation_error()
