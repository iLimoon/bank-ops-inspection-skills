---
name: dependency_performance_analysis
description: 依赖系统性能分析 — 分析外部依赖对本系统性能的影响，超设计值检测，输出性能瓶颈报告。Use when user asks about external dependencies, 依赖系统, 超设计值, or wants to check if downstream systems are overloaded. Trigger on keywords: 依赖, dependency, 设计值, 接入方式, 'external system impact', 依赖TPS.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 依赖系统性能分析

## 概述

分析各业务系统对外部依赖系统的调用性能，包括依赖系统名称、接入方式/地址、最大请求TPS（依赖接口），通过超设计值检测和依赖系统与本系统TPS相关性分析，评估外部依赖对系统性能的影响。

## 适用场景

- 检查外部依赖是否超设计值运行
- 依赖系统性能下降影响本系统时排查
- 评估依赖系统的容量余量
- 新增依赖系统时的基准评估

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

**Sheet**: "4-依赖系统"
**关键列**: 业务线, 依赖系统名称, 接入方式, 接入地址, 周次(YYYYWww), 最大请求TPS(设计值), 本周实际最大TPS, 是否超设计值
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- 各业务线的依赖系统信息（名称、接入方式、地址）
- 依赖接口的最大请求TPS
- 本系统 TPS 数据

## 分析流程

外部依赖系统是本系统的单点故障源。依赖超设计值运行意味着下游系统正在透支容量，随时可能成为全链路瓶颈，需在依赖方出问题前推动扩容。

### 步骤 1：依赖关系梳理
- 提取各业务系统的外部依赖清单
- 整理依赖系统的接入方式和地址
- 建立系统-依赖映射表

### 步骤 2：依赖接口性能分析
- 统计每个依赖接口的最大请求TPS
- 对比设计值/容量上限
- 标记超设计值的依赖调用

### 步骤 3：依赖-本系统相关性分析
- 计算依赖TPS与本系统TPS的Pearson相关系数
- 分析依赖系统性能是否成为本系统瓶颈
- 识别关键依赖（高度相关 + 高负载）

### 步骤 4：生成输出
- 依赖TPS趋势图 → `output/charts/dependency_tps_trend_<date>.png`
- 依赖-本系统相关图 → `output/charts/dependency_correlation_<date>.png`
- 依赖性能报告 CSV → `output/dependency_performance_<date>.csv`
- 性能瓶颈报告 Markdown → `output/dependency_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/dependency_tps_trend_<date>.png` | 依赖TPS趋势图 |
| `output/charts/dependency_correlation_<date>.png` | 依赖-本系统相关图 |
| `output/dependency_performance_<date>.csv` | 依赖性能数据 CSV |
| `output/dependency_report_<date>.md` | 依赖系统分析报告 |

### CSV 字段
业务系统, 依赖系统名称, 接入方式, 地址, 依赖接口最大TPS, 设计值, 使用率(%), 本系统TPS, 相关系数, 是否瓶颈, 告警级别

### 图表要求
**趋势图**：折线图，各依赖系统最大请求TPS周变化，添加设计值容量线（红色虚线），标注超设计值点。

**关联图**：散点图，X轴=依赖TPS，Y轴=本系统TPS，添加线性回归线，标注高度相关的依赖系统。

### 报告章节
1. 依赖系统概览
2. 超设计值的依赖接口列表
3. 关键依赖识别（高相关+高负载）
4. 依赖瓶颈分析
5. 优化建议
6. 图表引用

## 告警规则

- 依赖TPS > 设计值的 100% → 🔴 严重告警（超容量）
- 依赖TPS > 设计值的 80% → ⚠️ 告警（接近容量上限）
- 依赖与本系统相关系数 > 0.8 且依赖高负载 → 🔴 关键瓶颈
- 依赖接口不可用 → 🔴 严重告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/dependency_performance_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「检查外部依赖系统的TPS有没有超过设计值」
- 「分析一下各业务线的依赖系统是否存在瓶颈」
- 「依赖系统的性能和本系统的TPS有关联吗？」
