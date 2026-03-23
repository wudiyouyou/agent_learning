# Runtime 学习计划执行报告

## 已完成事项

1. Runtime 核心概念学习材料  
   - `docs/runtime-concepts.md`

2. 最小闭环（MVP）落地  
   - Runtime 应用：`examples/app_runtime_mvp.py`
   - API 调用脚本：`examples/call_process_api.py`
   - 2小时执行清单：`checklists/mvp-2hour-runbook.md`
   - 已验证：
     - `/process` SSE 正常返回
     - `agentscope chat` 单轮查询正常返回
     - `agentscope run` 可拉起独立服务并可调用

3. Sandbox 学习与越权拦截演练  
   - 权限矩阵：`checklists/sandbox-permission-matrix.md`
   - 演练脚本：`examples/sandbox_guard_demo.py`
   - 已验证输出：
     - `ALLOWED_READ_OK`
     - `BLOCKED_AS_EXPECTED`

4. 可观测与故障复盘  
   - 观测脚本：`examples/observe_process_health.py`
   - 复盘文档：`checklists/tracing-failure-replay.md`
   - 已验证：
     - 成功请求链路可采集耗时与 SSE chunk
     - 非法 payload 可稳定复现 validation error

5. 部署路径建议  
   - 部署建议：`checklists/deployment-path.md`
   - Simple Deployment 已实测：
     - `agentscope run examples/app_runtime_mvp.py --host 127.0.0.1 --port 8091`
     - `POST /process` 可返回 SSE

## 关键说明

- 你已在 `config/config.yaml` 配置 DashScope 参数，MVP 已读取该配置并成功调用。
- WebUI 命令已可启动后端；前端是否可访问取决于本机 Node/npm 与 npx 前端依赖安装过程。
- 本次已将 Node 从 `v12` 升级到 `v20`，用于解决旧语法兼容问题。

## 建议下一步（1天）

1. 在浏览器手动验证 `agentscope web ...` 的前端页面是否能打开并发起对话。  
2. 将 `session_id/user_id` 接入到 `app_runtime_mvp.py` 的持久化服务（RedisSession）。  
3. 把 `observe_process_health.py` 接入 CI 作为冒烟探针。  
