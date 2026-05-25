---
name: comprehensive_correlation_heatmap
description: 综合指标相关性热力图 — 对所有指标进行Pearson/Spearman相关性分析，生成聚类热力图，识别核心瓶颈指标。Use whenever the user wants to understand metric relationships, find bottleneck metrics, or generate a correlation heatmap. Trigger on keywords: 相关性, 热力图, 瓶颈指标, correlation, heatmap, 'which metrics are related', 指标关系.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 综合指标相关性热力图

## 概述

对所有运维指标进行全面的相关性分析，生成综合相关性矩阵和热力图，从全局视角识别关键指标之间的潜在关系和核心瓶颈指标。发现如「高TPS + 高CPU使用率 + 高TIME-WAIT」等性能瓶颈模式。

## 适用场景

- 全局了解各指标间的关联关系
- 识别「牵一发动全身」的核心瓶颈指标
- 发现隐藏的指标间依赖关系
- 为优化排期提供数据支撑（优先改善影响力最大的指标）

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

**Sheet**: "1-交易性能" + "2-服务器资源"
**关键列**: 整合以下指标：
- 交易指标（Sheet "1-交易性能"）：交易量、差错笔数、超时笔数、系统可用率、日均TPS、峰值TPS、平均交易时间
- 资源指标（Sheet "2-服务器资源"）：CPU平均负载、CPU使用率、内存使用率、TIME-WAIT数、运行主目录使用率
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

- 交易指标：Table 3, Table 4
- 存储指标：Table 3（应用文件使用空间、空闲率）
- 硬件指标：Table 5（CPU/内存/网络/磁盘）

## 分析流程

全局相关性分析帮助发现隐藏的指标依赖链，识别「牵一发动全身」的核心瓶颈指标——改善这些指标可以带来最大的连锁优化效益，避免头痛医头的碎片化优化。

### 步骤 1：数据整合
- 将所有指标整合为统一的宽表
- 处理缺失值（前向填充/均值填充）
- 标准化/归一化处理

### 步骤 2：相关性计算
- 计算所有指标两两之间的 Pearson 相关系数
- 计算 Spearman 秩相关系数
- 计算 p 值并标记显著性

### 步骤 3：热力图生成
- 使用 seaborn clustermap 生成聚类热力图
- 按相关性层次聚类排列指标顺序
- 自动将高度相关的指标归为一组

### 步骤 4：核心瓶颈指标识别
- 统计每个指标与其他指标的显著相关数量
- 识别「影响力中心」指标（与很多指标高度相关）
- 这些就是核心瓶颈指标：改善它们能带来最大连锁效益

### 步骤 5：生成输出
- 综合热力图 → `output/charts/comprehensive_corr_heatmap_<date>.png`
- 相关性矩阵 CSV → `output/comprehensive_corr_<date>.csv`
- 核心瓶颈指标报告 Markdown → `output/bottleneck_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/comprehensive_corr_heatmap_<date>.png` | 相关性热力图 |
| `output/comprehensive_corr_<date>.csv` | 相关性矩阵 CSV |
| `output/bottleneck_report_<date>.md` | 瓶颈指标报告 |

### CSV 字段
指标1, 指标2, Pearson_r, p_value, 显著性, Spearman_rho, 相关强度

### 图表要求
对称矩阵热力图，颜色映射 RdBu（红=正相关，蓝=负相关），单元格标注相关系数（|r| > 0.3 时显示），按层次聚类排列，标注显著性。

### 报告章节
1. 指标相关性全局概述
2. 高度相关指标组（|r| > 0.7）
3. 核心瓶颈指标识别（影响力排名 TOP 5）
4. 负相关关系分析
5. 业务含义解读
6. 优化建议
7. 图表引用

## 告警规则

- |r| > 0.7 且 p < 0.001 → 🔴 极强相关（高优先处理）
- |r| > 0.5 且 p < 0.01 → ⚠️ 强相关（需关注）
- 某个指标与 ≥5 个其他指标显著相关 → 🔴 核心瓶颈指标
- 指标组内平均 |r| > 0.6 → ⚠️ 该组指标之间存在系统性问题
- 负相关 r < -0.5 且涉及可用率 → 🔴 资源竞争告警

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/comprehensive_correlation_heatmap
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「生成所有指标的相关性热力图，找出核心瓶颈指标」
- 「哪些指标之间有强相关关系？」
- 「帮我分析一下TPS、CPU和交易时间之间的关联」
