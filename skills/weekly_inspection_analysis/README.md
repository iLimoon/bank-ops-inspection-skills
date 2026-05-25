# 运维周报编排入口

## 概述

串联全部12个专项分析技能，协调数据提取、多维度分析和最终周报汇总，生成包含交易概览、资源容量、深度分析和异常汇总的完整运维周报。

## 输入

从巡检数据中提取汇总大表覆盖的所有指标。支持汇总大表 Excel（Sheet 全部 7 个 Sheet）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/report_<date>.md` | 运维周报（唯一入口，整合所有子报告内容） |
| `output/charts/charts/*.png` | 所有专项分析的 PNG 图表 |
| `output/*.csv` | 所有专项分析的 CSV 数据文件 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/weekly_inspection_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/weekly_inspection_analysis/
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
