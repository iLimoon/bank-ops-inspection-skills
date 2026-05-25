---
name: pca_cluster_analysis
description: 主成分分析与聚类 — PCA降维+K-means聚类发现系统模式组，识别与任何组都不相似的异常模式系统。Use when user wants to find system patterns, 聚类, 主成分分析, or asks 'which systems are similar', 'are there any unusual systems', 异常检测. Trigger on keywords: PCA, 聚类, cluster, 主成分, 异常模式, 降维, 系统分组.
context: fork
agent: general-purpose
allowed-tools: "Bash(python *) Bash(pip *) Read Write"
---

# 主成分分析与聚类

## 概述

使用主成分分析(PCA)对所有运维指标进行降维，然后对系统进行聚类分析，发现指标模式相似的系统组，并识别与任何组都不相似的异常模式系统。主成分可被赋予业务含义（如 PC1=「资源消耗维度」、PC2=「性能维度」、PC3=「稳定性维度」）。

## 适用场景

- 发现指标行为模式相似的系统组
- 识别独特的异常模式系统（与其他系统都不同）
- 理解「哪些指标对系统差异贡献最大」
- 系统架构优化和资源分配决策

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
**关键列**: 合并两个 Sheet 的全部数值指标（交易量, TPS, 可用率, CPU, 内存, 目录使用率等），构建「系统×指标」多维特征矩阵。
**解析方式**: `openpyxl` 读取，按 「周次」 列筛选目标周。

### 方式B（回退）：从 DOCX 巡检报告提取

整合全部运维指标（同 comprehensive_correlation_heatmap 的指标范围）。

## 分析流程

PCA降维将数十个指标压缩为2-3个主成分（如资源维、性能维、稳定维），让系统间的差异一目了然。聚类帮助运维团队按模式管理而非逐系统排查。

### 步骤 1：数据矩阵构建
- 行 = 系统（或系统×周的组合）
- 列 = 所有数值型指标
- 处理缺失值
- 标准化（z-score normalization）

### 步骤 2：PCA 降维
- 计算各主成分的解释方差比例
- 生成碎石图确定保留的主成分数量（通常保留解释 80%+ 方差的前 N 个）
- 输出各指标在主成分上的载荷(loading)

### 步骤 3：载荷分析
- 识别每个主成分主要由哪些指标驱动
- 为主成分赋予业务含义

### 步骤 4：聚类分析
- 在 PCA 降维后的空间进行 K-means 聚类
- 使用肘部法则确定最优聚类数 K
- 可选：层次聚类并生成树状图

### 步骤 5：异常模式检测
- 计算每个系统到其所属聚类中心的距离
- 标记距离 > 2倍标准差的系统为「异常模式」
- 标记单独成类（n=1）的系统

### 步骤 6：生成输出
- PCA碎石图+载荷图 → `output/charts/pca_analysis_<date>.png`
- 系统聚类图（2D PCA空间） → `output/charts/system_cluster_<date>.png`
- 聚类结果 CSV → `output/pca_cluster_result_<date>.csv`
- 异常模式列表 Markdown → `output/pca_cluster_report_<date>.md`

## 输出产物

### 输出文件清单
| `output/charts/pca_analysis_<date>.png` | PCA碎石图+载荷图 |
| `output/charts/system_cluster_<date>.png` | 系统聚类图 |
| `output/pca_cluster_result_<date>.csv` | 聚类结果 CSV |
| `output/pca_cluster_report_<date>.md` | PCA聚类报告 |

### CSV 字段
系统名称, PC1, PC2, PC3, 聚类编号, 到聚类中心距离, 是否异常模式, 最近系统

### 图表要求
**碎石图**：柱状图 + 累积方差折线。**载荷图**：每个指标一个向量，展示对PC1/PC2的贡献。**聚类图**：散点图按聚类着色，标注聚类中心和异常模式系统，添加95%置信椭圆。

### 报告章节
1. PCA降维结果概述
2. 主成分载荷解读（各PC的业务含义）
3. 系统聚类结果
4. 各聚类特征描述
5. 异常模式系统清单
6. 图表引用

## 告警规则

- 到聚类中心距离 > 2σ → 🔴 异常模式告警（与同类系统显著不同）
- 到聚类中心距离 > 1.5σ → ⚠️ 偏离模式关注
- 系统单独成类（n=1） → 🔴 独特模式告警
- 主成分解释方差突然变化 → ⚠️ 指标结构突变（整体模式改变）
- 聚类间平均距离 > 3σ → ⚠️ 系统间差异过大

## 使用示例

### 调用方式

在 Claude Code 中使用：

```
/pca_cluster_analysis
```

### 自然语言触发

也可以直接用自然语言描述需求（系统自动匹配此技能）：

- 「对系统做PCA聚类分析，看看哪些系统模式相似」
- 「有没有和所有其他系统都不一样的异常系统？」
- 「哪些指标对系统之间的差异贡献最大？」
