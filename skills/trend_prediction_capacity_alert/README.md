# 趋势预测与容量预警

## 概述

使用线性回归+指数平滑对关键指标进行时间序列预测，估算未来4-8周趋势和容量耗尽时间，按紧急程度排序生成扩容建议。

## 输入

从巡检数据中提取空间空闲率、目录使用率、CPU使用率、内存使用率、数据库使用率。支持汇总大表 Excel（Sheet "1-交易性能" + "2-服务器资源" + "3-数据库巡检"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/forecast_trend_<date>.png` | 预测趋势图 |
| `output/charts/capacity_timeline_<date>.png` | 容量预警时间线 |
| `output/forecast_data_<date>.csv` | 预测数据 CSV |
| `output/capacity_forecast_report_<date>.md` | 容量风险预警报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/trend_prediction_capacity_alert
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy, scikit-learn

## 目录结构

```
.claude/skills/trend_prediction_capacity_alert/
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
