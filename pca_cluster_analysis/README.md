# 主成分分析与聚类

## 概述

使用PCA降维和K-means聚类，将数十个指标压缩为2-3个主成分（资源维、性能维、稳定维），发现系统模式组，识别异常模式系统。

## 输入

从巡检数据中提取全部数值型运维指标（构建系统×指标矩阵）。支持汇总大表 Excel（Sheet "1-交易性能" + "2-服务器资源"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/pca_analysis_<date>.png` | PCA碎石图与载荷图 |
| `output/charts/system_cluster_<date>.png` | 系统聚类图 |
| `output/pca_cluster_result_<date>.csv` | 聚类结果 CSV |
| `output/pca_cluster_report_<date>.md` | PCA聚类分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/pca_cluster_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy, scikit-learn, seaborn

## 目录结构

```
.claude/skills/pca_cluster_analysis/
├── SKILL.md         # 技能定义（系统使用）
├── README.md        # 本文件（用户文档）
└── requirements.txt # Python 依赖

共享资源（所有技能共用）：
.claude/skills/
├── references/
│   └── data-discovery.md    # 数据发现策略
└── scripts/
    ├── data_utils.py         # 数据工具：发现、解析、计算
    ├── excel_parser.py       # Excel 汇总大表解析
    └── chart_utils.py        # 图表工具：6种常用图表
```
