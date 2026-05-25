# 服务器资源分析

## 概述

监控CPU负载、内存使用率、TIME-WAIT连接数、网卡错误、运行主目录使用率，识别高负载节点和资源瓶颈。

## 输入

从巡检数据中提取CPU平均/最大负载、内存使用率(%)、TIME-WAIT数、网卡错误数、运行主目录使用率(%)。支持汇总大表 Excel（Sheet "2-服务器资源"）和 DOCX 巡检报告两种格式。数据发现策略详见 `references/data-discovery.md`，解析工具见 `scripts/excel_parser.py`。

## 输出

| `output/charts/cpu_mem_trend_<date>.png` | CPU与内存趋势图 |
| `output/charts/server_resource_<date>.png` | 服务器资源总览图 |
| `output/server_resource_<date>.csv` | 服务器资源 CSV |
| `output/server_resource_report_<date>.md` | 服务器资源分析报告 |

## 运行方式

在 Claude Code 中直接描述需求即可自动触发此技能，也可显式调用：

```
/server_resource_analysis
```

触发关键词已内置于技能 definition 中，说出自然语言需求即可。

## 依赖

matplotlib, openpyxl, python-docx, numpy, scipy

## 目录结构

```
.claude/skills/server_resource_analysis/
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
