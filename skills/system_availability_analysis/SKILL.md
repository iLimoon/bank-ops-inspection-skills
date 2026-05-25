---
name: system_availability_analysis
description: 系统可用率分析 — 监控各业务线系统可用率（<99%告警），生成可用率趋势图和异常事件列表。Use when user asks about 可用率, availability, SLA, uptime, or wants to check system reliability. Trigger on keywords: 可用率, availability, SLA, 不可用, downtime, 系统可用.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 系统可用率分析

## 概述

分析各周巡检报告中的系统可用率(%)数据，监控可用率变化趋势，对低于 99% 阈值的周次生成报警，输出异常事件列表和趋势图。

## 适用场景

- 每周固定检查各业务线可用率
- 可用率出现下降趋势时预警
- 需要汇总可用率 < 99% 的异常事件供周报引用

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

**Sheet**: "1-交易性能"
**关键列**: 业务线, 周次(YYYYWww), 系统可用率(%)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 3**: 系统可用率(%)

## 分析流程

系统可用率是运维SLA的核心指标。即使单次不可用只有几分钟，累计起来可能突破年度99.9%的目标线。趋势监控帮助及早发现可用率劣化。

### 步骤 1：数据提取
解析所有历史周的数据，提取各业务线的系统可用率。

### 步骤 2：阈值检测
- 系统可用率 < 99% → 严重告警
- 系统可用率 < 99.5% → 预警
- 系统可用率 < 100% 但 ≥ 99.5% → 关注

### 步骤 3：趋势分析
- 计算各业务线可用率周变化趋势
- 识别持续下降的业务线
- 计算平均可用率和最低可用率

### 步骤 4：生成输出
- 可用率趋势折线图 → `output/charts/availability_trend_<date>.png`
- 异常事件列表 CSV → `output/availability_anomaly_<date>.csv`
- Markdown 报告 → `output/availability_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/availability_trend_<date>.png` | 可用率趋势图 |
| `output/availability_anomaly_<date>.csv` | 可用率异常 CSV |
| `output/availability_report_<date>.md` | 可用率分析报告 |

### CSV 字段
业务线, 周次, 系统可用率(%), 是否告警, 告警级别, 环比变化(%)

### 图表要求
折线图：X轴=周次，Y轴=系统可用率(%)（范围 95%-100%），多条折线（各业务线不同颜色），99% 阈值线（红色虚线），标注告警点。

### 报告章节
1. 总体可用率概述
2. 各业务线可用率趋势表
3. 告警事件清单
4. 可用率下降趋势分析
5. 图表引用

## 告警规则

- 系统可用率 < 99% → 🔴 严重告警
- 系统可用率 < 99.5% → ⚠️ 预警
- 连续两周可用率下降 → ⚠️ 趋势告警
- 可用率 = 100% → ✅ 正常

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/system_availability_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「检查这周各业务线的系统可用率，有没有低于99%的？」
- 「生成可用率的周趋势图」
- 「最近12周的系统可用率变化」
