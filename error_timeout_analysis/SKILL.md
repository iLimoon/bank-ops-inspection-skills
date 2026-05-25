---
name: error_timeout_analysis
description: 差错与超时分析 — 监控业务异常，计算差错率/超时率，识别异常高峰周，输出异常列表和折线图。Use when user asks about 差错, 超时, error rate, timeout, or wants to find problematic weeks with high failure rates. Trigger on keywords: 差错率, 超时率, 异常周, 业务异常, error, timeout, 失败.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 差错与超时分析

## 概述

分析各周巡检报告中的差错笔数和超时笔数，计算差错率（差错笔数/交易量）和超时率（超时笔数/交易量），识别异常高峰周，输出异常周列表和时间序列折线图。

## 适用场景

- 每周固定检查差错和超时状态
- 某业务线出现差错或超时笔数突增时
- 需要追踪差错率/超时率的长期趋势
- 生成异常周列表供周报引用

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
**关键列**: 业务线, 周次(YYYYWww), 巡检周期内总笔数(笔), 差错笔数, 超时笔数, 差错率(%), 超时率(%)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 3**: 差错笔数、超时笔数、交易量/业务量（笔）

## 分析流程

差错和超时直接反映服务质量和用户体验。即使总体可用率正常，差错率的突然升高也可能是系统容量不足或下游故障的前兆。

### 步骤 1：数据提取
解析所有历史周的数据（Excel 或 DOCX），提取各业务线的差错笔数、超时笔数和交易量。

### 步骤 2：计算差错率和超时率
- 差错率 = 差错笔数 / 交易量 × 100%
- 超时率 = 超时笔数 / 交易量 × 100%

### 步骤 3：异常识别
- 标记差错率 > 1% 的周为「异常周」
- 标记超时率 > 0.5% 的周为「超时异常周」
- 统计各业务线的累计差错/超时趋势

### 步骤 4：生成输出
- 时间序列折线图 → `output/charts/error_timeout_trend_<date>.png`
- 异常周列表 CSV → `output/error_timeout_summary_<date>.csv`
- Markdown 报告 → `output/error_timeout_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/error_timeout_trend_<date>.png` | 差错超时趋势图 |
| `output/error_timeout_summary_<date>.csv` | 差错超时汇总 CSV |
| `output/error_timeout_report_<date>.md` | 差错超时分析报告 |

### CSV 字段
业务线, 周次, 差错笔数, 超时笔数, 交易量, 差错率(%), 超时率(%), 是否异常

### 图表要求
双Y轴折线图：左轴为差错/超时笔数（柱状图），右轴为差错率/超时率（折线）。X轴=周次，标注异常周（红色高亮）。

### 报告章节
1. 总体异常概述
2. 各业务线差错/超时趋势
3. 异常周详细列表
4. 差错率排名
5. 图表引用

## 告警规则

- 差错笔数 > 0 → ⚠️ 异常
- 超时笔数 > 0 → 🔴 告警
- 差错率 > 1% → 🔴 严重告警
- 超时率 > 0.5% → ⚠️ 关注
- 连续两周差错增长 → ⚠️ 趋势告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/error_timeout_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「这周哪些业务线有差错和超时？计算一下差错率」
- 「最近几周差错和超时趋势怎么样？」
- 「有没有异常周（差错率>1%或超时率>0.5%）？」
