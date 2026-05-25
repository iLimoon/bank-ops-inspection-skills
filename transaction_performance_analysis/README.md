# 交易性能综合分析

## 概述

统一分析各业务线的交易量、TPS 和交易时间指标，包括趋势分析、环比变化检测、TPS-延迟关联分析和高峰低谷识别。

## 输入

从巡检数据中提取交易量(笔)、日均TPS、峰值TPS、平均交易时间(ms)。支持汇总大表 Excel（Sheet "1-交易性能"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/volume_trend_<date>.png` | 交易量趋势图 |
| `output/charts/tps_trend_<date>.png` | TPS与交易时间趋势图 |
| `output/charts/tps_latency_scatter_<date>.png` | TPS-交易时间散点图 |
| `output/transaction_performance_<date>.csv` | 交易性能数据 CSV |
| `output/transaction_performance_report_<date>.md` | 交易性能分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/transaction_performance_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/transaction_performance_analysis/
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
