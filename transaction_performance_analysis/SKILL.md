---
name: transaction_performance_analysis
description: 交易性能综合分析 — 监控交易量/TPS趋势、TPS-延迟关联分析（Pearson/Spearman），识别高峰低谷和性能瓶颈。Use when user asks about 交易量, TPS, 交易时间, transaction performance, or wants to analyze throughput vs latency, 环比变化, performance trends. Trigger on keywords: 交易量, TPS, transaction, 性能, performance, 延迟, latency, 环比, 吞吐量.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 交易性能综合分析

## 概述

统一分析各业务线的交易量和 TPS 相关指标：
1. **交易量趋势** — 每周交易量变化、环比、高峰低谷识别
2. **TPS 趋势** — 日均TPS/峰值TPS 多周变化趋势
3. **TPS-交易时间关联** — 散点图 + Pearson/Spearman 相关系数，识别高负载下性能退化

## 适用场景

- 每周固定生成交易性能周报
- 交易量出现异常波动时深入分析
- TPS 升高伴随交易时间增加时排查性能瓶颈
- 需要对比各业务线的处理能力时

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
**关键列**: 业务线, 周次(YYYYWww), 巡检周期内总笔数(笔), 日均TPS, 峰值TPS, 平均交易时间(ms)
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- **Table 3**: 交易量/业务量（笔）
- **Table 4**: 日均TPS、峰值TPS、平均交易时间(ms)

## 分析流程

交易性能是用户体验和系统容量的直接体现。TPS反映处理能力，交易时间反映响应质量。TPS-延迟关联分析特别关键：如果TPS升高导致延迟非线性飙升，说明系统已接近容量拐点。

### 步骤 1：扫描历史数据
扫描所有周目录，识别数据格式（Excel 或 DOCX），按周次归类。

### 步骤 2：一次性提取全部指标
从每个周的数据中提取各业务线的：交易量（笔）、日均TPS、峰值TPS、平均交易时间(ms)。

### 步骤 3：交易量趋势分析
- 环比变化(%) = (本周值 - 上周值) / 上周值 × 100%
- 标记环比增长 > 20% 的周为「高峰」
- 标记环比下降 > 20% 的周为「低谷」
- 告警：环比下降 > 30% → 异常下降；环比增长 > 50% → 异常增长

### 步骤 4：TPS 趋势分析
- 生成各业务线日均TPS和峰值TPS的周趋势折线图（双Y轴：左=TPS，右=交易时间）
- 计算 TPS 环比变化
- 识别 TPS 异常波动（变化 > 30%）

### 步骤 5：TPS-交易时间相关性分析
- 散点图：X轴=TPS，Y轴=平均交易时间
- 线性回归拟合线 + 置信区间
- 计算 Pearson 和 Spearman 相关系数
- 分析是否存在「TPS升高导致交易时间变长」的瓶颈信号

### 步骤 6：生成输出
- 交易量趋势图 → `output/charts/volume_trend_<date>.png`
- TPS+交易时间趋势图 → `output/charts/tps_trend_<date>.png`
- TPS-交易时间散点图 → `output/charts/tps_latency_scatter_<date>.png`
- 完整 CSV → `output/transaction_performance_<date>.csv`
- Markdown 报告 → `output/transaction_performance_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/volume_trend_<date>.png` | 交易量趋势图 |
| `output/charts/tps_trend_<date>.png` | TPS与交易时间趋势图 |
| `output/charts/tps_latency_scatter_<date>.png` | TPS-交易时间散点图 |
| `output/transaction_performance_<date>.csv` | 交易性能数据 CSV |
| `output/transaction_performance_report_<date>.md` | 交易性能分析报告 |

### CSV 字段
业务线, 周次, 交易量(笔), 交易量环比(%), 标注(高峰/低谷/正常), 日均TPS, 峰值TPS, TPS环比(%), 平均交易时间(ms), 交易时间环比(%)

### 图表要求
**交易量趋势图**：多条折线（各业务线不同颜色），X轴=周次，Y轴=交易量，标注高峰和低谷点。

**TPS趋势图**：双Y轴（左=TPS，右=交易时间ms），X轴=周次，标注峰值点。

**TPS-交易时间散点图**：各业务线不同颜色/标记，添加线性回归线和置信区间，标注相关系数和p值。

### 报告章节
1. 交易量趋势概述 + 环比变化统计
2. TPS 趋势概述 + 周变化表
3. TPS-交易时间相关性分析 + 瓶颈识别
4. 高峰/低谷周识别
5. 各业务线综合评述
6. 图表引用

## 告警规则

- 交易量环比下降 > 30% → ⚠️ 异常下降，需排查
- 交易量环比增长 > 50% → 🔴 异常增长，需关注
- TPS 环比变化 > 50% → ⚠️ 异常波动
- 平均交易时间 > 200ms → ⚠️ 性能预警
- 相关系数 > 0.7 且显著 → 🔴 潜在瓶颈信号（高TPS导致延迟增加）

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/transaction_performance_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「分析这周各业务线的交易量和TPS趋势」
- 「交易时间有没有随TPS升高而增加？散点图+相关系数」
- 「哪些业务线出现了交易量高峰或低谷？」
