# 系统可用率分析

## 概述

监控各业务线的系统可用率，<99% 自动告警，生成可用率趋势图和异常事件列表。

## 输入

从巡检数据中提取系统可用率(%)。支持汇总大表 Excel（Sheet "1-交易性能"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/availability_trend_<date>.png` | 可用率趋势图 |
| `output/availability_<date>.csv` | 可用率数据 CSV |
| `output/availability_report_<date>.md` | 系统可用率分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/system_availability_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/system_availability_analysis/
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
