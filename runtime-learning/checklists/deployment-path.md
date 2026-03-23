# Runtime 部署路径建议（电力交易项目）

## 已完成：Simple Deployment 实测

已用 CLI 成功启动：

```bash
agentscope run examples/app_runtime_mvp.py --host 127.0.0.1 --port 8091
```

并验证：
- `POST /process` 返回 SSE 流（服务可用）

## 推荐迁移路径（从开发到生产）

### 阶段 A：单机开发（当前）
- 方式：`python app.py` 或 `agentscope run`
- 目标：快速迭代 Prompt/工具链路
- 风险：无高可用、资源隔离弱

### 阶段 B：容器化部署（建议下一步）
- 方式：Docker + 固定镜像依赖
- 目标：环境一致性、便于回滚
- 关键动作：
  - 配置文件与密钥分离（环境变量 / secret）
  - 暴露健康检查接口
  - 日志集中采集

### 阶段 C：集群化（K8s）
- 方式：Deployment + HPA + Ingress
- 目标：弹性扩缩容与故障自愈
- 关键动作：
  - 按 QPS/延迟设置 HPA 指标
  - 灰度发布策略（canary）
  - 配置 tracing/metrics backend

## 选型建议（电力交易业务）

- 日内策略与风控请求峰值明显，建议至少容器化
- 生产优先保障：
  1. 稳定性（重启恢复/限流）
  2. 安全性（Sandbox 与工具权限）
  3. 可观测（trace + metrics + logs）

## 上线前最低检查清单

- [ ] 密钥不落盘，全部走 secret 管理
- [ ] 关键接口限流与超时配置完成
- [ ] 失败降级策略可用（模型异常时返回可解释兜底）
- [ ] 一次完整故障演练与复盘完成
