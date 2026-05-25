---
name: database_capacity_analysis
description: 数据库容量分析 — 监控数据库存储、表空间使用率、连接数和备份状态，发现容量瓶颈，输出高风险数据库列表。Use when user asks about database storage, 数据库容量, tablespace, pg_xlog, backup status, or wants a database health check. Trigger on keywords: 数据库, database, 表空间, 存储空间, 备份, Vastbase, xlog.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 数据库容量分析

## 概述

监控各系统数据库的存储容量指标，包括数据库占用存储空间(GB)、数据库空间使用率(%)、表空间分配/使用/增量/使用率，以及最大请求数（数据库设计值），识别容量紧张和潜在性能瓶颈。涵盖全部 43 个数据库系统。

## 适用场景

- 每周检查数据库容量状态
- pg_xlog 堆积超过阈值时告警
- 表空间使用率持续增长时提前预警
- 备份状态异常时告警
- 数据库使用率接近设计值上限时预警

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

**Sheet**: "3-数据库巡检"
**关键列**: 系统名称, 节点, 数据库名称, 实例名, 周次(YYYYWww), 数据库占用空间(GB), 数据库使用率(%), /data磁盘使用率(%), pg_xlog数量, Uptime(天), 备份状态, 表空间名称, 表空间分配/使用/月增量/使用率, 最大请求数(设计值)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 3**: 数据库占用存储空间(GB)、数据库空间使用率(%)
- **Table 7/8**: 表空间名称、分配、使用、增量、使用率
- 最大请求数（数据库设计值）

## 分析流程

数据库容量直接关乎业务连续性。存储空间耗尽会导致数据库不可写、交易中断。表空间异常增长和备份失败是数据安全的高危信号，需提前预警。

### 步骤 1：数据提取
解析所有历史周的数据，提取数据库容量相关指标。数据可能来自 43 个数据库系统。

### 步骤 2：数据库级分析
- 统计每个数据库的总占用空间和使用率
- 生成各数据库空间使用率多周趋势
- 标记使用率 > 80% 的数据库

### 步骤 3：表空间级分析
- 分析各表空间的使用率分布
- 标记使用率 > 80% 的表空间
- 识别增量较大的表空间（增长热点）
- 列出 TOP 10 增长最快的表空间

### 步骤 4：最大请求数分析
- 对比当前请求数与设计值
- 标记接近设计值（> 80%）的数据库

### 步骤 5：数据库专项检查
- /data磁盘使用率 > 80% 的数据库
- pg_xlog 堆积 > 10
- 备份状态异常/未挂载

### 步骤 6：生成输出
- 数据库使用率趋势图 → `output/charts/db_usage_trend_<date>.png`
- 表空间增长排行图 → `output/charts/tablespace_growth_<date>.png`
- 高风险数据库列表 CSV → `output/db_capacity_alert_<date>.csv`
- 容量瓶颈报告 Markdown → `output/db_capacity_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/db_usage_trend_<date>.png` | 数据库使用率趋势图 |
| `output/charts/tablespace_growth_<date>.png` | 表空间增长排行图 |
| `output/db_capacity_alert_<date>.csv` | 高风险数据库 CSV |
| `output/db_capacity_report_<date>.md` | 数据库容量分析报告 |

### CSV 字段
系统名称, 数据库名称, 数据库类型, 占用存储(GB), 使用率(%), 最大请求数, 当前请求数, 请求数使用率(%), 表空间总数, 高使用率表空间数, 告警级别

### 图表要求
多子图布局：每个数据库一个子图，折线图显示使用率周变化，80% 阈值线（红色虚线），标注增长热点。

### 报告章节
1. 数据库容量总体概述
2. 高风险数据库列表（使用率排序）
3. /data磁盘使用率 > 80% 的数据库
4. pg_xlog 堆积
5. 备份状态异常
6. 表空间增长热点 TOP 10
7. 最大请求数接近设计值的数据库
8. 图表引用

## 告警规则

- 数据库使用率 > 90% → 🔴 严重告警
- 数据库使用率 > 80% → ⚠️ 告警
- 表空间使用率 > 80% → ⚠️ 告警
- 表空间周增量 > 10GB → ⚡ 增长异常
- /data磁盘使用率 > 80% → 🔴 告警
- pg_xlog > 10 → 🔴 堆积告警
- 备份状态 = 异常/未挂载 → ⚠️ 告警
- 请求数使用率 > 80% → ⚡ 性能预警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/database_capacity_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「检查所有数据库的容量使用情况，找出高风险数据库」
- 「pg_xlog有没有堆积？备份状态是否正常？」
- 「哪些数据库的磁盘使用率超过80%了？」
