# AgentScope Runtime 核心概念速查（仅 Runtime）

参考官方文档：
- https://runtime.agentscope.io/en/intro.html
- https://runtime.agentscope.io/en/concept.html

## 1) Runtime 的定位

AgentScope Runtime 是平台层，不是 Agent 业务逻辑本身。它解决的是：

- Agent 如何服务化（Agent as API）
- Agent 如何在受控环境安全调用工具（Sandbox）
- Agent 如何部署、运行、扩缩容（Engine + Deployer）
- Agent 如何可观测、可排障（Logs + Tracing）

一句话：

Runtime = Tool Sandboxing + AaaS APIs + Scalable Deployment + Observability + Framework Compatibility

## 2) 关键组件

### Agent
- 你写的业务智能体逻辑（例如电力交易分析、风控、执行建议）
- Runtime 不替换你的 Agent，只做运行时增强（白盒适配）

### AgentApp
- Runtime 主入口，承载 API 路由与生命周期
- 对外暴露服务接口（如 `/process` 等）

### Runner
- 调度 Agent 执行，串联会话、状态、流式输出
- 管理一次请求从输入到输出的执行流程

### Deployer
- 把 Runner 作为服务运行起来
- 负责启动、健康检查、异常与关闭流程

### Services
- Session/State/Memory/Sandbox 等运行时服务能力
- 提供“多轮、持久化、隔离执行”基础设施

### Sandbox
- Browser/FileSystem/GUI/Mobile/Cloud 等隔离环境
- 工具调用不直接暴露宿主机，降低越权风险

## 3) 与“本地直接跑 Agent 脚本”的区别

- 本地脚本：开发快，但服务化、隔离、可观测、治理能力弱
- Runtime：统一 API、可部署、可治理、可监控，适合生产

## 4) 电力交易场景映射

- Agent as API：为交易前台/策略平台提供统一调用接口
- Session/State：保持交易会话上下文（用户偏好、风控阈值）
- Sandbox：约束高风险工具（文件、网络、浏览器操作）
- Tracing：排查“模型慢、工具慢、上游慢”是哪一段
- Deployment：支持从单机验证到容器/K8s 迁移

## 5) 学习优先级建议

1. Quick Start 跑通最小闭环
2. API Invocation + WebUI 验证链路
3. Sandbox 权限矩阵与越权演练
4. Tracing 与故障复盘
5. Simple Deployment 到 Advanced Deployment 迁移
