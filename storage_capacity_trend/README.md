# 存储容量趋势分析

## 概述

分析应用存储空间的周变化趋势，计算空闲率，提前发现容量瓶颈，输出趋势图和容量预警列表。

## 输入

从巡检数据中提取应用文件使用空间、应用空间空闲率(%)。支持汇总大表 Excel（Sheet "1-交易性能"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/storage_trend_<date>.png` | 存储容量趋势图 |
| `output/charts/storage_free_rate_<date>.png` | 空闲率变化图 |
| `output/storage_<date>.csv` | 存储容量数据 CSV |
| `output/storage_report_<date>.md` | 存储容量分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/storage_capacity_trend
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/storage_capacity_trend/
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
