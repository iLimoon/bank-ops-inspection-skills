---
name: multi_system_comparison
description: 多系统指标对比 — 使用雷达图和条形图对比多个系统在同一指标上的表现，输出系统综合排名。Use when user wants to compare systems side by side, 系统对比, 雷达图, or asks 'which system performs best/worst', 'compare all systems'. Trigger on keywords: 对比, 排名, 雷达图, radar, comparison, 横向对比, 综合排名.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 多系统指标对比

## 概述

对比多个业务系统在同一性能指标上的表现，使用雷达图和条形图直观展示系统间的能力差异，帮助识别表现最差和最优的系统。

## 适用场景

- 横向对比各业务线的综合能力
- 识别全面领先或全面落后的系统
- 评估系统间的能力差异程度
- 资源分配决策参考

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
**关键列**: 业务线, 周次(YYYYWww), 系统可用率(%), 日均TPS, 峰值TPS, 平均交易时间(ms), 差错率(%), 超时率(%)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- 系统可用率(%)、日均TPS、峰值TPS、平均交易时间(ms)（Table 3, Table 4）
- CPU/内存/磁盘使用率（Table 5）

## 分析流程

横向对比帮助定位：相同的外部环境和业务压力下，哪些系统表现异常。表现最差的系统往往是最优先的优化目标，表现最优的系统的实践可以推广复用。

### 步骤 1：指标对齐
- 提取所有系统在各指标上的最新一周数据
- 对于多节点系统，取平均值或最大值（根据指标类型）
- 标准化处理（用于不同量纲指标放在同一雷达图）

### 步骤 2：雷达图生成
- 每个系统一条多边形
- 轴为各项标准化指标
- 识别形状相似的系统（相似的性能特征）

### 步骤 3：条形图生成
- 每个指标生成独立的横向条形图
- 系统按指标值排序
- 标注最高/最低系统
- 添加阈值线

### 步骤 4：综合排名
- 对各指标进行加权评分
- 生成系统综合性能排名
- 识别全面领先和全面落后的系统

### 步骤 5：生成输出
- 雷达图 → `output/charts/system_radar_<date>.png`
- 各指标条形图 → `output/charts/system_bar_<date>.png`
- 系统对比数据 CSV → `output/system_comparison_<date>.csv`
- 系统对比报告 Markdown → `output/system_comparison_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/system_radar_<date>.png` | 系统性能雷达图 |
| `output/charts/system_bar_<date>.png` | 指标条形对比图 |
| `output/system_comparison_<date>.csv` | 系统对比数据 CSV |
| `output/system_comparison_report_<date>.md` | 系统对比报告 |

### CSV 字段
系统名称, 可用率(%), 日均TPS, 峰值TPS, 平均交易时间(ms), CPU使用率(%), 内存使用率(%), 差错率(%), 磁盘使用率(%), 综合评分

### 图表要求
**雷达图**：多边形填充半透明，各系统不同颜色，轴标签为指标名称，建议每次最多展示 6-8 个系统。

**条形图**：横向条形图，按值排序，添加阈值线，标注极值系统。

### 报告章节
1. 系统对比总体概述
2. 各指标系统排名表
3. 综合性能排名
4. 雷达图解读
5. 需重点关注的系统
6. 图表引用

## 告警规则

- 可用率 < 99% → 告警（越高越好）
- 交易时间 > 200ms → 需关注（越低越好）
- CPU/内存/磁盘使用率 > 80% → 告警（越低越好）
- 差错率 > 1% → 告警（越低越好）
- 综合评分排名末位且与首位差距 > 30% → 需重点关注

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/multi_system_comparison
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「用雷达图对比8条业务线的综合性能」
- 「哪个系统的处理能力最强？哪个最弱？」
- 「各系统在可用率、TPS、交易时间上的排名是怎样的？」
