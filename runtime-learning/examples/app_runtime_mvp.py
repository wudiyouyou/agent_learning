#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AgentScope Runtime MVP application for local learning."""

import os
from pathlib import Path
from typing import Any

import yaml

from agentscope.agent import ReActAgent
from agentscope.formatter import DashScopeChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import DashScopeChatModel
from agentscope.pipeline import stream_printing_messages
from agentscope_runtime.engine import AgentApp
from agentscope_runtime.engine.schemas.agent_schemas import AgentRequest


def load_llm_config(config_path: Path) -> dict[str, Any]:
    """Load and validate LLM config from yaml."""
    with config_path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    llm = cfg.get("llm", {})
    required = ["provider", "model_name", "api_key", "base_url", "stream"]
    missing = [k for k in required if k not in llm]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    return llm


BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
LLM_CFG = load_llm_config(CONFIG_PATH)

# Allow users to override key by environment variable first.
API_KEY = os.getenv("DASHSCOPE_API_KEY", LLM_CFG["api_key"])
os.environ["DASHSCOPE_API_KEY"] = API_KEY

agent_app = AgentApp(
    app_name="power-trading-mvp",
    app_description="Runtime MVP for power trading assistant",
)


@agent_app.query(framework="agentscope")
async def query_func(
    self: AgentApp,
    msgs: Any,
    request: AgentRequest | None = None,
    **kwargs: Any,
) -> Any:
    """Create a per-request agent and stream response chunks."""
    _ = kwargs
    _request = request  # keep for future session integration

    agent = ReActAgent(
        name="PowerTrader",
        sys_prompt=(
            "你是电力交易分析助理。你的回答需要包含：市场判断、风险点、"
            "建议动作。保持简洁清晰。"
        ),
        model=DashScopeChatModel(
            model_name=LLM_CFG["model_name"],
            api_key=API_KEY,
            base_url=LLM_CFG["base_url"],
            stream=bool(LLM_CFG["stream"]),
        ),
        formatter=DashScopeChatFormatter(),
        memory=InMemoryMemory(),
    )
    agent.set_console_output_enabled(False)

    async for msg, last in stream_printing_messages(
        agents=[agent],
        coroutine_task=agent(msgs),
    ):
        yield msg, last


if __name__ == "__main__":
    agent_app.run(host="0.0.0.0", port=8090, web_ui=True)
