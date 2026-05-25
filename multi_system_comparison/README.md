# 多系统指标对比

## 概述

使用雷达图和条形图横向对比8条业务线在同一指标上的表现，输出系统综合排名。

## 输入

从巡检数据中提取可用率(%)、日均TPS、峰值TPS、平均交易时间(ms)、CPU/内存/磁盘使用率(%)。支持汇总大表 Excel（Sheet "1-交易性能"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/system_radar_<date>.png` | 系统雷达图 |
| `output/charts/system_bar_<date>.png` | 系统指标条形图 |
| `output/system_comparison_<date>.csv` | 系统对比 CSV |
| `output/system_comparison_report_<date>.md` | 系统对比报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/multi_system_comparison
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/multi_system_comparison/
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
