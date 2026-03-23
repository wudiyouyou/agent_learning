# Sandbox 权限矩阵（电力交易 Agent）

## 1. 工具分级

| 工具类型 | 典型用途 | 风险等级 | 默认策略 |
|---|---|---|---|
| 市场数据查询 API | 拉取电价/负荷/气象 | 中 | 仅允许白名单域名出网 |
| 文件读取 | 读取策略模板/日报 | 中 | 仅允许工作目录白名单 |
| 文件写入 | 生成分析报告 | 中 | 仅允许输出目录白名单 |
| Shell 命令 | 运维/诊断 | 高 | 默认禁用，仅在沙箱短时开启 |
| Python 执行 | 数据计算/回测 | 高 | 限制依赖与运行时长，禁系统调用 |
| 浏览器自动化 | 行情网站抓取 | 高 | 仅沙箱浏览器，禁宿主机访问 |
| 外部支付/下单 | 实盘动作 | 严重 | 双重审批 + 人工确认 + 审计日志 |

## 2. 最小权限原则

- 路径最小化：只开放 `runtime-learning/data` 与 `runtime-learning/output`
- 网络最小化：只开放交易必需域名
- 执行最小化：默认无 shell/popen 权限
- 时间最小化：每次工具调用设置超时
- 审计最小化：记录 tool_name、input、output、duration、status

## 3. 越权拦截演练（已落地脚本）

脚本：`examples/sandbox_guard_demo.py`

演练目标：
- 允许访问白名单目录
- 拦截越权访问系统目录（如 `/etc/hosts`）

执行命令：

```bash
cd /home/wudiyouyou/agent_learning/runtime-learning
python examples/sandbox_guard_demo.py
```

成功标准：
- 输出 `ALLOWED_READ_OK`
- 输出 `BLOCKED_AS_EXPECTED`

## 4. 上线前检查项

- 白名单目录是否仅包含业务必需目录
- 是否禁用高风险工具的默认开放
- 是否存在“工具回退到宿主机执行”的路径
- 审计日志是否可关联 `session_id / user_id`
