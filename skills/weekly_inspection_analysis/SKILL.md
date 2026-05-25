---
name: weekly_inspection_analysis
description: 运维周报编排入口 — 串联全部12项专项分析技能，协调数据提取、多维度分析和最终周报汇总。Use when user wants a complete weekly inspection report, 周报, 运维巡检, or says 'run the full inspection', 'generate weekly report'. Trigger on keywords: 周报, 巡检, inspection, 运维报告, 总报告, 'run all analyses', 全面分析.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 运维周报编排入口

## 概述

作为运维周报生成的**编排器**，负责：
1. 扫描数据目录，识别本周数据
2. 按顺序调度各专项分析技能，收集各技能的输出
3. 汇总生成最终的运维周报 Markdown 文档

**不再重复执行各专项技能的分析逻辑**，而是调用它们获取结果后汇总。

## 适用场景

- 每周固定生成运维周报
- 需要一站式运行全部 12 项分析
- 汇总各专项技能发现的异常和告警

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

### 汇总大表 Excel（优先）

后续周的数据可能以**巡检数据汇总大表 Excel** 形式提交，文件匹配模式：`*巡检数据汇总*.xlsx`。

Excel 包含 7 个 Sheet，覆盖全部数据维度：

| Sheet | 内容 | 对应专项技能 |
|-------|------|-------------|
| "1-交易性能" | 8业务线交易指标 | transaction_performance_analysis / error_timeout_analysis / system_availability_analysis / storage_capacity_trend |
| "2-服务器资源" | 8业务线服务器指标 | server_resource_analysis |
| "3-数据库巡检" | 43系统数据库指标 | database_capacity_analysis |
| "4-依赖系统" | 外部依赖TPS | dependency_performance_analysis |
| "5-变更与事件" | 变更事件记录 | change_event_correlation |
| "6-第三方服务商摘要" | 服务商周报摘要 | 本技能直接汇总 |
| "0-本周概览" | 使用说明 | 自动汇总 |

### DOCX 巡检报告（回退）

当汇总 Excel 不存在时，回退解析 `*巡检报告*.docx` 文件。

**文件模式**: `*巡检报告*.docx`、`*巡检周报*.docx`

表格结构：
- **Table 3**: 交易量/差错笔数/超时笔数/系统可用率/应用文件空间/数据库空间
- **Table 4**: 日均TPS/峰值TPS/平均交易时间
- **Table 5**: 各节点硬件指标（CPU/内存/运行主目录）
- **Table 6**: 各节点磁盘使用率
- **Table 7/8**: 表空间使用情况

### 第三方服务商周报（Excel/Word）

**文件模式**: `华讯网络*.*xl*`、`H3C周报*.xlsx` 等，独立于汇总大表。

## 编排流程

按以下顺序调度专项技能，收集各技能输出后汇总到最终周报：

### 第一步：基础指标分析（可并行）
1. **交易性能分析** — `/transaction_performance_analysis`
2. **差错与超时分析** — `/error_timeout_analysis`
3. **系统可用率分析** — `/system_availability_analysis`

### 第二步：资源层面分析（可并行）
4. **存储容量趋势分析** — `/storage_capacity_trend`
5. **数据库容量分析** — `/database_capacity_analysis`
6. **服务器资源分析** — `/server_resource_analysis`

### 第三步：关联与深度分析（可并行）
7. **综合指标相关性热力图** — `/comprehensive_correlation_heatmap`
8. **依赖系统性能分析** — `/dependency_performance_analysis`
9. **变更与事件关联分析** — `/change_event_correlation`
10. **多系统指标对比** — `/multi_system_comparison`
11. **主成分分析与聚类** — `/pca_cluster_analysis`
12. **趋势预测与容量预警** — `/trend_prediction_capacity_alert`

### 第四步：生成日常巡检结论

在所有专项技能执行完毕后，汇总各技能发现的异常/告警总数，生成巡检结论：
- **若所有技能均未发现异常**：日常巡检无故障
- **若存在异常**：日常巡检发现以下隐患 + 隐患清单

> 生产事件信息由人工补充。

### 第五步：汇总生成周报

汇总所有技能输出 + 日常巡检结论，生成最终周报保存到 `output/report_<date>.md`。

## 输出产物

### 周报结构

```markdown
# 运维周报
周期: YYYY-MM-DD ~ YYYY-MM-DD

## 一、整体运行状态摘要
总体评价 + 事件统计表 + 各业务线概览表 + 日常巡检隐患列表

## 二、交易性能分析
12周交易量表格、环比变化、差错超时排行、系统可用率

## 三、资源容量分析
存储容量告警、数据库使用率

## 四、第三方服务商周报摘要
华讯/海量/中电金信/H3C 周报要点

## 五、深度分析
指标相关性热力图、系统对比、PCA 聚类、趋势预测

## 六、异常问题汇总
所有隐患/异常按优先级排序

## 七、结论与建议
短期措施 + 中长期措施 + 重点关注系统表
```

### 输出目录

```
output/
├── report_<date>.md                    ← 总报告（唯一入口）
├── transaction_performance_report_*.md   # 交易性能综合分析
├── error_timeout_report_*.md             # 差错与超时分析
├── availability_report_*.md              # 系统可用率分析
├── storage_report_*.md                   # 存储容量趋势分析
├── db_capacity_report_*.md               # 数据库容量分析
├── server_resource_report_*.md           # 服务器资源分析
├── dependency_report_*.md                # 依赖系统性能分析
├── change_event_report_*.md              # 变更与事件关联分析
├── system_comparison_report_*.md         # 多系统指标对比
├── capacity_forecast_report_*.md         # 趋势预测与容量预警
├── pca_cluster_report_*.md               # 主成分分析与聚类
├── bottleneck_report_*.md                # 性能瓶颈分析
├── CSV 数据文件: metrics_*.csv, forecast_data_*.csv, *_alert_*.csv 等
└── charts/: 所有 PNG 图表
```

## 告警规则汇总

| 指标 | 阈值 | 级别 | 来源技能 |
|------|------|------|----------|
| 超时笔数 > 0 | - | 🔴 | error_timeout_analysis |
| 差错笔数 > 0 | - | ⚠️ | error_timeout_analysis |
| 系统可用率 < 99% | < 99% | ⚠️ | system_availability_analysis |
| 磁盘使用率 > 80% | > 80% | 🔴 | storage_capacity_trend |
| 数据库使用率 > 80% | > 80% | ⚠️ | database_capacity_analysis |
| CPU使用率 > 85% | > 85% | ⚠️ | server_resource_analysis |
| pg_xlog > 10 | > 10 | 🔴 | database_capacity_analysis |
| 备份状态异常 | - | ⚠️ | database_capacity_analysis |
| 依赖TPS超设计值 | - | ⚠️ | dependency_performance_analysis |
| 预计2周内到达容量阈值 | - | 🔴 | trend_prediction_capacity_alert |

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/weekly_inspection_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「生成这周的完整运维周报」
- 「运行全部巡检分析」
- 「帮我出一份包含交易、资源、数据库、依赖的全面周报」

