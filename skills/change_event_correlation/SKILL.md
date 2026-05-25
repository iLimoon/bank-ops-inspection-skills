---
name: change_event_correlation
description: 变更与事件关联分析 — 分析变更/事件对系统性能和容量的影响，输出事件影响报告。Use whenever the user asks about change impact, incident analysis, 变更影响, or wants to correlate production changes with metric anomalies. Trigger on keywords: 变更, 事件, 生产事件, incident, 'what caused this spike', 变更关联.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 变更与事件关联分析

## 概述

分析本周环境/应用/数据库变更情况和容量异常预警/生产事件对系统各性能指标的影响，通过叠加变更事件到指标趋势图、二分类分析（事件/非事件）等方法，评估变更和事件的影响范围。

## 适用场景

- 变更或事件发生后评估影响范围
- 需要判断事件是否对指标产生显著影响
- 追踪事件恢复情况
- 识别频繁变更的高风险系统

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

**Sheet**: "5-变更与事件"
**关键列**: 周次(YYYYWww), 日期(YYYY-MM-DD), 类型, 变更/事件描述, 原因, 整改措施, 建议, 影响系统, 影响程度, 处理状态
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- 本周环境/应用/数据库变更情况
- 容量异常预警 / 生产事件记录
- 各性能指标（TPS、交易量、可用率、CPU、内存、磁盘等）

## 分析流程

变更和事件是系统异常的主要诱因。通过将变更/事件时间线与指标波动叠加，可以量化变更对系统行为的影响程度，为变更审批和风险控制提供数据支撑。

### 步骤 1：变更和事件提取
- 从数据中提取所有变更记录（环境变更、应用变更、数据库变更）
- 提取生产事件和异常预警记录
- 标注事件发生时间和受影响的系统

### 步骤 2：指标-事件叠加分析
- 将变更/事件时间点叠加到各指标趋势图上
- 使用竖线或阴影标注事件窗口
- 对比事件前后指标变化

### 步骤 3：二分类统计分析
- 将数据分为「事件周」和「非事件周」
- 对比两组各指标的均值、方差
- 使用 t 检验判断差异显著性
- 识别受事件影响最大的指标

### 步骤 4：事件影响量化
- 计算事件前后各指标的变化幅度(%)
- 估算事件影响的持续时间（周）
- 评估恢复情况

### 步骤 5：生成输出
- 变更-指标叠加图 → `output/charts/change_impact_<date>.png`
- 事件影响分析 CSV → `output/change_event_impact_<date>.csv`
- 事件影响报告 Markdown → `output/change_event_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/change_impact_<date>.png` | 变更-指标叠加图 |
| `output/change_event_impact_<date>.csv` | 事件影响分析 CSV |
| `output/change_event_list_<date>.csv` | 变更事件列表 CSV |
| `output/change_event_report_<date>.md` | 事件影响报告 |

### CSV 字段
事件/变更描述, 发生周, 影响系统, 事件类型, 受影响指标, 事件前值, 事件后值, 变化幅度(%), 恢复周数, 显著性p值

### 图表要求
折线图显示指标趋势，事件时间点用红色竖线标注，事件窗口用灰色半透明阴影，图例包含事件标签。

### 报告章节
1. 本周变更和事件概览
2. 事件影响量化分析表
3. 各指标受事件影响程度排名
4. 事件前后对比统计
5. 恢复情况追踪
6. 建议
7. 图表引用

## 告警规则

- 事件后指标变化 > 30% 且 p < 0.05 → 🔴 显著影响告警
- 事件后指标变化 > 15% → ⚠️ 中等影响关注
- 事件恢复时间 > 3 周 → 🔴 长期影响告警（系统弹性不足）
- 同一系统累计事件 > 5 次/季度 → ⚠️ 高频事件关注
- 变更后连续 2 周指标未恢复 → ⚠️ 变更影响持续告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/change_event_correlation
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「帮我看下这周的变更和事件有没有导致性能指标异常」
- 「分析一下最近的生产事件对TPS有什么影响」
- 「对比事件周和非事件周的各指标差异」
