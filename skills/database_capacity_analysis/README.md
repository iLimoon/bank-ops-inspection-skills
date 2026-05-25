# 数据库容量分析

## 概述

监控43个数据库系统的存储容量、表空间使用率、连接数和备份状态，识别容量紧张和性能瓶颈，输出高风险数据库列表。

## 输入

从巡检数据中提取数据库占用空间(GB)、使用率(%)、表空间使用率、pg_xlog数量、备份状态、最大请求数。支持汇总大表 Excel（Sheet "3-数据库巡检"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/db_usage_trend_<date>.png` | 数据库使用率趋势图 |
| `output/charts/tablespace_growth_<date>.png` | 表空间增长排行图 |
| `output/db_capacity_alert_<date>.csv` | 高风险数据库 CSV |
| `output/db_capacity_report_<date>.md` | 数据库容量分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/database_capacity_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/database_capacity_analysis/
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
