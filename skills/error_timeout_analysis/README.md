# 差错与超时分析

## 概述

监控各业务线的差错和超时情况，计算差错率和超时率，识别异常高峰周，生成折线图和分析报告。

## 输入

从巡检数据中提取差错笔数、超时笔数、交易量(笔)。支持汇总大表 Excel（Sheet "1-交易性能"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/error_timeout_trend_<date>.png` | 差错率与超时率趋势图 |
| `output/error_timeout_<date>.csv` | 差错与超时数据 CSV |
| `output/error_timeout_report_<date>.md` | 差错与超时分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/error_timeout_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/error_timeout_analysis/
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
