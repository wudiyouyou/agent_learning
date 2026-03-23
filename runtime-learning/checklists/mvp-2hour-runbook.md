# Runtime MVP 2小时跑通清单

## 0. 前置条件（5分钟）

- 已激活 conda 环境：`agent_learning`
- 已安装 `agentscope-runtime`
- 已在 `config/config.yaml` 填入 DashScope Key

## 1. 启动 Runtime 应用（10分钟）

```bash
cd /home/wudiyouyou/agent_learning/runtime-learning
python examples/app_runtime_mvp.py
```

预期：
- API 服务：`http://127.0.0.1:8090`
- WebUI 会自动启动（同进程输出会提示前端地址）

## 2. 验证 API 流式调用（15分钟）

新开终端执行：

```bash
cd /home/wudiyouyou/agent_learning/runtime-learning
python examples/call_process_api.py
```

预期：
- 持续输出 SSE `data:` 事件
- 最后出现 `[DONE]`

## 3. 验证 CLI（15分钟）

```bash
cd /home/wudiyouyou/agent_learning/runtime-learning
agentscope chat examples/app_runtime_mvp.py --query "给我一个电力交易日内策略框架"
```

预期：
- CLI 返回模型回答

## 4. 验证 WebUI（15分钟）

- 打开浏览器访问运行日志中给出的 WebUI 地址（通常是 `http://localhost:5173`）
- 输入一条电力交易相关问题
- 观察返回是否正常

## 5. MVP 完成标准（5分钟）

以下 4 项全满足即完成：
- API `POST /process` 返回流式结果
- CLI `agentscope chat` 可返回结果
- WebUI 能对话
- 代码可重复运行（重启后仍可用）

## 6. 常见问题快速排查（15-30分钟）

- 401/鉴权失败：检查 `config.yaml` 中 key 是否正确
- 模型报错：确认 `model_name` 在账号可用范围
- 端口冲突：改成 `port=8091` 重新启动
- WebUI 未起来：先确保 API 正常，再单独执行 `agentscope web examples/app_runtime_mvp.py`
