# 变更与事件关联分析

## 概述

将变更/事件时间线与指标波动叠加，量化变更对系统行为的影响程度，输出事件影响报告。

## 输入

从巡检数据中提取类型、变更/事件描述、影响系统、影响程度、各性能指标。支持汇总大表 Excel（Sheet "5-变更与事件"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/change_event_overlay_<date>.png` | 变更事件叠加指标图 |
| `output/change_event_impact_<date>.csv` | 变更事件影响 CSV |
| `output/change_event_report_<date>.md` | 变更与事件关联报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/change_event_correlation
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/change_event_correlation/
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
