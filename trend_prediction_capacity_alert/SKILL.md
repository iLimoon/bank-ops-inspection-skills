---
name: trend_prediction_capacity_alert
description: 趋势预测与容量预警 — 时间序列预测（线性回归+指数平滑）关键指标未来4-8周趋势，估算容量耗尽时间。Use when user asks about 预测, 趋势, capacity forecasting, 'when will disk be full', 'predict future usage', or wants capacity planning. Trigger on keywords: 预测, forecast, 趋势预测, 容量预警, 耗尽, 扩容, linear regression prediction.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 趋势预测与容量预警

## 概述

对关键运维指标（TPS、交易量、存储空间、CPU、内存）进行时间序列预测，提前识别容量风险，生成未来趋势预测图和容量预警。预测基于历史趋势外推，结果可靠性随预测周期增长而降低，建议结合变更事件分析修正预测。

## 适用场景

- 预测磁盘/数据库空间何时满
- 提前制定扩容计划
- 评估CPU/内存趋势是否需要扩容
- 容量规划决策支持

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

**Sheet**: "1-交易性能" + "2-服务器资源" + "3-数据库巡检"
**关键列**: - 应用空间空闲率（Sheet "1-交易性能"）
- 运行主目录使用率、CPU使用率、内存使用率（Sheet "2-服务器资源"）
- 数据库使用率、/data磁盘使用率（Sheet "3-数据库巡检"）
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- TPS、交易量（Table 3, Table 4）
- 存储空间（Table 3）
- CPU/内存使用率（Table 5）
- 数据库空间使用率（Table 3）

## 分析流程

容量规划的本质是在故障发生之前行动。基于历史增长速率外推未来消耗，可以给运维团队提供可量化的扩容时间窗口——不再凭经验拍脑袋，而是用数据说话。

### 步骤 1：时间序列构建
- 按周整理各指标的历史数据
- 确保时间序列的连续性
- 处理缺失值（线性插值）

### 步骤 2：趋势分解
- 使用移动平均平滑短期波动
- 分解趋势成分、季节成分和残差成分
- 判断趋势类型：线性增长、指数增长、平稳波动

### 步骤 3：时间序列预测
- 线性回归预测（基线方法）
- 基于最近 N 周的平均增长率外推
- 预测未来 4-8 周的各指标值
- 计算预测置信区间

### 步骤 4：容量预警
- 基于预测值，判断何时会触发阈值
- 计算容量耗尽预计时间：磁盘空间、CPU/内存、数据库使用率
- 按紧急程度排序

### 步骤 5：生成输出
- 各指标预测趋势图 → `output/charts/forecast_trend_<date>.png`
- 容量预警时间线图 → `output/charts/capacity_timeline_<date>.png`
- 预测数据 CSV → `output/forecast_data_<date>.csv`
- 容量风险预警 Markdown → `output/capacity_forecast_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/forecast_trend_<date>.png` | 预测趋势图 |
| `output/charts/capacity_timeline_<date>.png` | 容量预警时间线图 |
| `output/forecast_data_<date>.csv` | 预测数据 CSV |
| `output/capacity_forecast_report_<date>.md` | 容量风险预警报告 |

### CSV 字段
指标名称, 系统/业务线, 当前值, 预测值(4周后), 预测值(8周后), 增长率/周, 阈值, 预计到达阈值时间, 告警级别

### 图表要求
实线=历史数据，虚线=预测值，半透明带=置信区间，水平线=阈值，标注预计到达阈值的时间点。

### 报告章节
1. 预测概述和方法说明
2. 各指标预测趋势表
3. 容量耗尽时间线（按紧急程度排序）
4. 近期（4周内）高风险项
5. 中期（8周内）关注项
6. 扩容建议时间表
7. 图表引用

## 告警规则

- 预计 2 周内到达阈值 → 🔴 紧急（需立即扩容）
- 预计 4 周内到达阈值 → ⚠️ 告警（本周需启动扩容）
- 预计 8 周内到达阈值 → ⚡ 预警（需纳入扩容计划）
- 增长率异常加速（>2倍历史均值） → ⚠️ 趋势突变告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/trend_prediction_capacity_alert
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「预测未来8周的容量趋势，哪些指标会耗尽？」
- 「数据库使用率按现在的增长速度什么时候会满？」
- 「生成容量预警时间线，按紧急程度排序」
