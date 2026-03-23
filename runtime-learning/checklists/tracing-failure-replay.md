# Runtime 观测与故障复盘（MVP）

## 已完成的观测动作

- 成功链路探测：`examples/observe_process_health.py` 的 `probe_success`
- 失败链路探测：向 `/process` 发送非法 payload，触发参数校验错误

## 运行命令

```bash
cd /home/wudiyouyou/agent_learning/runtime-learning
python examples/observe_process_health.py
```

## 当前探测指标

- `http_status`
- `sse_chunks`
- `elapsed_sec`
- `contains_validation_error`

## 失败复盘样例（已验证）

请求：
- Endpoint: `POST /process`
- Body: `{"bad":"payload"}`

返回：
- HTTP 状态保持 200（SSE 通道）
- 事件体包含 `validation error`，指出缺少 `input` 字段

结论：
- 这类错误属于 **请求参数层**，不是模型层、工具层或网络层

## 排障分层建议（按优先级）

1. 输入层：payload schema、session_id、user_id
2. 模型层：key/model_name/base_url、配额、超时
3. 工具层：工具超时、参数不合法、权限不足
4. 基础设施层：端口冲突、进程崩溃、依赖缺失

## 下一步接入完整 Tracing

参考官方章节：
- https://runtime.agentscope.io/en/tracing.html

建议最小目标：
- 记录 request_id / session_id
- 打点模型调用时长、工具调用时长
- 把失败类型按输入/模型/工具三类聚合统计
