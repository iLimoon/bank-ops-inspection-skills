# 综合指标相关性热力图

## 概述

对所有运维指标进行Pearson/Spearman相关性分析，生成聚类热力图，识别核心瓶颈指标——改善这些指标可带来最大连锁优化效益。

## 输入

从巡检数据中提取交易量、TPS、可用率、CPU、内存、TIME-WAIT、目录使用率等全部数值指标。支持汇总大表 Excel（Sheet "1-交易性能" + "2-服务器资源"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/comprehensive_corr_heatmap_<date>.png` | 相关性热力图 |
| `output/comprehensive_corr_<date>.csv` | 相关性矩阵 CSV |
| `output/bottleneck_report_<date>.md` | 核心瓶颈指标报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/comprehensive_correlation_heatmap
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy, seaborn

## 目录结构

```
.claude/skills/comprehensive_correlation_heatmap/
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
