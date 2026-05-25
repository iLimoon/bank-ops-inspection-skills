---
name: server_resource_analysis
description: 服务器资源分析 — 监控CPU、内存、TIME-WAIT、网卡错误、磁盘使用率，识别高负载服务器和资源瓶颈。Use when user asks about server resources, CPU, 内存, TIME-WAIT, 磁盘, or wants a server health check / resource audit. Trigger on keywords: CPU, 内存, 服务器, server, 高负载, TIME-WAIT, 网卡, 资源使用率.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 服务器资源分析

## 概述

监控各系统服务器的性能指标，包括CPU平均/最大负载、CPU总核数、内存使用率(%)、TIME-WAIT套接字个数、网卡收发错误数、运行主目录使用率/容量等，进行趋势分析和TPS关联分析，识别潜在瓶颈和异常。

## 适用场景

- 每周检查服务器资源使用情况
- CPU/内存持续高负载时排查原因
- 网络连接数异常积压时分析
- 运行主目录空间不足时提前预警

## 环境准备

```bash
pip install matplotlib openpyxl python-docx numpy scipy -q
```
## 数据发现

详细的数据发现策略和业务线映射见 `references/data-discovery.md`。

核心要点：
- 从当前目录向上查找 `data/raw_data/`，或通过 `INSPECTION_DATA_DIR` 环境变量指定
- 识别名称含「周」的子目录作为周次数据源
- 优先解析 `*巡检数据汇总*.xlsx`（汇总大表），不存在时回退解析 `*巡检报告*.docx`
- 8 条业务线（ESB/银联无卡/银联前置/超级网银/人行大小额/农信银/核心/校园一卡通）映射已内置
- 输出默认到 `./output/`，可通过 `INSPECTION_OUTPUT_DIR` 覆盖
## 数据提取

### 方式A（优先）：从汇总大表 Excel 提取

**Sheet**: "2-服务器资源"
**关键列**: 系统名称, 节点, 主机名/IP, 周次(YYYYWww), CPU平均负载, CPU最大负载, CPU总核数, CPU使用率(%), 内存使用率(%), TIME-WAIT套接字数, 网卡收/发错误数, 运行主目录使用率(%), 运行主目录容量(GB)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 5**: 各节点 CPU平均负载、CPU最大负载、CPU总核数、内存使用率(%)、TIME-WAIT套接字数、网卡收发错误数、运行主目录使用率/容量
- **Table 4**: 日均TPS、峰值TPS

## 分析流程

服务器资源（CPU/内存/网络/磁盘）是交易性能的基础承载层。资源瓶颈会导致延迟增加、超时增多、甚至服务不可用，需在所有指标之前优先关注。

### 步骤 1：数据提取
解析所有历史周的数据，提取各节点硬件指标。

### 步骤 2：CPU 分析
- 计算 CPU 使用率 = CPU平均负载 / CPU总核数 × 100%
- 生成各节点 CPU 使用率多周趋势图
- 标记 CPU 使用率 > 80% 的节点

### 步骤 3：内存分析
- 生成各节点内存使用率趋势图
- 标记内存使用率 > 85% 的节点

### 步骤 4：网络分析
- 统计 TIME-WAIT 套接字数量趋势
- 标记 TIME-WAIT > 1000 的连接积压
- 统计网卡收发错误数

### 步骤 5：运行主目录分析
- 生成运行主目录使用率趋势图
- 标记使用率 > 80% 的节点

### 步骤 6：TPS-资源关联分析
- 散点图：TPS vs CPU使用率、TPS vs 内存使用率
- 计算Pearson相关系数，分析高TPS时资源消耗模式

### 步骤 7：生成输出
- CPU/内存趋势图 → `output/charts/server_resource_trend_<date>.png`
- TPS-资源关联图 → `output/charts/tps_resource_corr_<date>.png`
- 高负载服务器列表 CSV → `output/server_alert_<date>.csv`
- 资源异常报告 Markdown → `output/server_resource_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/server_resource_trend_<date>.png` | 服务器资源趋势图 |
| `output/charts/tps_resource_corr_<date>.png` | TPS-资源关联图 |
| `output/server_alert_<date>.csv` | 高负载服务器 CSV |
| `output/server_resource_report_<date>.md` | 服务器资源分析报告 |

### CSV 字段
系统名称, 节点, 周次, CPU使用率(%), 内存使用率(%), TIME-WAIT数, 网卡错误数, 运行主目录使用率(%), 告警项, 告警级别

### 图表要求
多子图布局：CPU使用率、内存使用率、TIME-WAIT、目录使用率。各节点不同颜色折线，添加阈值线（CPU 80%, 内存 85%, 目录 80%），标注告警点。

### 报告章节
1. 服务器资源总体概述
2. CPU 负载 TOP 10 节点
3. 内存使用 TOP 10 节点
4. 网络连接异常节点
5. 运行主目录空间告警节点
6. TPS-资源关联分析
7. 图表引用

## 告警规则

- CPU使用率 > 90% → 🔴 严重告警
- CPU使用率 > 80% → ⚠️ 告警
- 内存使用率 > 90% → 🔴 严重告警
- 内存使用率 > 85% → ⚠️ 告警
- TIME-WAIT > 2000 → 🔴 连接积压告警
- TIME-WAIT > 1000 → ⚠️ 关注
- 网卡错误数 > 0 → ⚠️ 异常
- 运行主目录使用率 > 80% → 🔴 磁盘告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/server_resource_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「检查所有服务器的CPU、内存、磁盘使用率」
- 「有没有服务器高负载？TIME-WAIT连接数正常吗？」
- 「各节点运行主目录的使用率趋势如何？」
