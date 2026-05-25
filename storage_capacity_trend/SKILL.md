---
name: storage_capacity_trend
description: 存储容量趋势分析 — 分析应用存储使用趋势，计算空闲率变化，提前发现容量瓶颈，输出容量预警列表。Use when user asks about storage, 存储容量, 磁盘空间, 空闲率, or wants to know 'when will we run out of disk space'. Trigger on keywords: 存储, storage, 磁盘, disk, 容量, capacity, 空间不足, 空闲率.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 存储容量趋势分析

## 概述

分析各系统应用文件使用空间和应用空间空闲率(%)的多周变化趋势，通过阈值报警提前发现容量瓶颈，输出趋势图和容量预警列表。

## 适用场景

- 每周监控存储容量变化
- 空闲率持续下降时提前预警
- 制定扩容计划时需要容量趋势数据

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
**关键列**: 业务线, 周次(YYYYWww), 应用文件使用空间(GB), 应用空间空闲率(%)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 3**: 应用文件使用空间、应用空间空闲率(%)

## 分析流程

存储容量不是瞬时告警，而是渐进消耗。趋势分析的价值在于提前几周甚至几个月预警，给扩容留出采购和实施时间，避免紧急扩容的风险和成本。

### 步骤 1：数据提取
解析所有历史周的数据，提取各业务线的存储空间数据。

### 步骤 2：趋势分析
- 生成各业务线存储使用量的周趋势折线图
- 生成空闲率的周趋势折线图
- 计算周均增长量

### 步骤 3：容量预测
- 基于使用量增长速度，线性外推预计满时间
- 空闲率 < 20% → 预警；< 10% → 告警；< 5% → 严重告警

### 步骤 4：生成输出
- 存储使用趋势图 → `output/charts/storage_trend_<date>.png`
- 空闲率趋势图 → `output/charts/storage_free_trend_<date>.png`
- 容量预警列表 CSV → `output/storage_capacity_alert_<date>.csv`
- Markdown 报告 → `output/storage_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/storage_trend_<date>.png` | 存储使用趋势图 |
| `output/charts/storage_free_trend_<date>.png` | 空闲率趋势图 |
| `output/storage_capacity_alert_<date>.csv` | 容量预警 CSV |
| `output/storage_report_<date>.md` | 存储容量分析报告 |

### CSV 字段
业务线, 周次, 应用文件使用空间, 应用空间空闲率(%), 使用量周增长, 预计满时间(周), 告警级别

### 图表要求
双图布局：上图=使用空间趋势，下图=空闲率趋势。X轴=周次，空闲率图添加 20%/10%/5% 阈值线，标注告警点。

### 报告章节
1. 存储容量总体概述
2. 各业务线存储趋势表
3. 容量预警清单（按紧急程度排序）
4. 扩容建议
5. 图表引用

## 告警规则

- 空闲率 < 5% → 🔴 严重告警（需立即扩容）
- 空闲率 < 10% → ⚠️ 告警（本周需扩容）
- 空闲率 < 20% → ⚡ 预警（2周内需扩容）
- 周使用量增长 > 10% → ⚠️ 增长加速告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/storage_capacity_trend
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「分析应用存储空间的使用趋势，预测什么时候会满」
- 「哪些系统的空闲率下降最快？」
- 「存储容量的周变化趋势图」
