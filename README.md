# 运维巡检分析技能包

银行运维周报生成系统的全套 Claude Code 技能集，覆盖交易性能、服务器资源、数据库容量、依赖系统、变更事件关联等维度的自动分析。

## 快速开始

### 方式A：npx skills 安装（推荐）

```bash
npx skills add iLimoon/bank-ops-inspection-skills
```

### 方式B：git clone + 复制

```bash
git clone https://github.com/iLimoon/bank-ops-inspection-skills.git
cp -r bank-ops-inspection-skills/change_event_correlation/ \
      bank-ops-inspection-skills/comprehensive_correlation_heatmap/ \
      ... \
      bank-ops-inspection-skills/references/ \
      bank-ops-inspection-skills/scripts/ \
      /path/to/项目/.claude/skills/
# 注意：不需要复制 README.md
```

### 方式C：下载 tar.gz

从 GitHub Releases 下载 `claude-skills-pack.tar.gz`，解压后按方式B复制。

## 前置条件

- **Claude Code**（支持 skill 机制）
- **Python 3.7+**

依赖会在首次使用时自动安装（`pip install`），也可预先安装：

```bash
pip install matplotlib numpy openpyxl python-docx scipy -q
```

## 数据准备

技能会自动发现数据，推荐按以下方式组织原始数据：

```
项目根目录/
├── data/raw_data/
│   ├── 3月第1周/
│   │   ├── 巡检数据汇总_2026W10.xlsx    # 汇总大表（优先）
│   │   ├── ESB系统_运维中心应用巡检报告(...).docx
│   │   └── ...
│   ├── 3月第2周/
│   └── ...
└── output/                              # 分析输出目录（自动创建）
```

### 两种数据源

| 优先级 | 格式 | 文件名 | 说明 |
|--------|------|--------|------|
| 优先 | `.xlsx` | `*巡检数据汇总*.xlsx` | 汇总大表，7个Sheet，覆盖全部8条业务线 |
| 回退 | `.docx` | `*巡检报告*.docx` | 单系统巡检报告，每条业务线一份 |

### 环境变量（可选）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `INSPECTION_DATA_DIR` | 数据根目录 | 自动向上查找 `data/raw_data/` |
| `INSPECTION_OUTPUT_DIR` | 输出目录 | `./output/` |

## 技能清单（13 个）

### 基础分析（7 个）

| 技能 | 调用命令 | 可触发的自然语言 |
|------|---------|-----------------|
| 交易性能综合分析 | `/transaction_performance_analysis` | 交易量、TPS、交易时间、环比变化、性能瓶颈 |
| 差错与超时分析 | `/error_timeout_analysis` | 差错率、超时率、异常周、业务异常 |
| 系统可用率分析 | `/system_availability_analysis` | 可用率、availability、SLA、downtime |
| 存储容量趋势分析 | `/storage_capacity_trend` | 存储容量、磁盘空间、空闲率、容量瓶颈 |
| 服务器资源分析 | `/server_resource_analysis` | CPU、内存、TIME-WAIT、高负载、服务器 |
| 数据库容量分析 | `/database_capacity_analysis` | 数据库、database、表空间、pg_xlog、备份 |
| 依赖系统性能分析 | `/dependency_performance_analysis` | 依赖系统、超设计值、外部依赖TPS |

### 深度分析（5 个）

| 技能 | 调用命令 | 可触发的自然语言 |
|------|---------|-----------------|
| 变更与事件关联分析 | `/change_event_correlation` | 变更影响、事件分析、生产事件 |
| 多系统指标对比 | `/multi_system_comparison` | 系统对比、雷达图、横向对比、排名 |
| 综合指标相关性热力图 | `/comprehensive_correlation_heatmap` | 相关性、热力图、瓶颈指标、指标关系 |
| 主成分分析与聚类 | `/pca_cluster_analysis` | PCA、聚类、主成分、异常模式、系统分组 |
| 趋势预测与容量预警 | `/trend_prediction_capacity_alert` | 预测、forecast、趋势预测、容量预警、扩容 |

### 编排入口（1 个）

| 技能 | 调用命令 | 可触发的自然语言 |
|------|---------|-----------------|
| 运维周报编排入口 | `/weekly_inspection_analysis` | 周报、巡检、运维报告、总报告、全面分析 |

## 共享资源

所有技能共用以下资源，无需重复实现：

### 数据发现 (`references/data-discovery.md`)

统一的数据定位策略：目录扫描、格式检测（Excel优先/DOCX回退）、8条业务线识别映射、输出路径配置。

### 工具脚本 (`scripts/`)

| 脚本 | 说明 |
|------|------|
| `data_utils.py` | 数据发现（`discover_data`）、安全解析（`safe_float`）、业务线识别（`identify_biz`）、环比计算（`calc_wow`） |
| `excel_parser.py` | 汇总大表解析（`parse_summary_xlsx`）、业务线行提取（`get_biz_rows`）、时间序列提取（`extract_metric_series`） |
| `chart_utils.py` | 中文字体配置（`setup_mpl`）、时间序列图、散点回归图、条形图、热力图、雷达图 |

## 支持的 8 条业务线

| 文件关键词 | 业务线 | 说明 |
|-----------|--------|------|
| ESB系统 | ESB系统 | 企业服务总线 |
| 银联无卡 | 银联无卡 | 银联无卡快捷支付 |
| 银联支付清算 | 银联前置 | 银联支付清算系统 |
| 超级网银 | 超级网银 | 统一支付(超级网银) |
| 人民银行大小额 | 人行大小额 | 大小额支付系统 |
| 农信银 | 农信银 | 农信银二代支付 |
| 核心系统 | 核心系统 | 银行核心系统 |
| 校园一卡通 | 校园一卡通 | 校园一卡通系统 |

## 输出结构

```
output/
├── report_{日期}.md                        # 总报告（唯一入口）
├── transaction_performance_report_*.md     # 交易性能综合分析
├── error_timeout_report_*.md               # 差错与超时分析
├── availability_report_*.md                # 系统可用率分析
├── storage_report_*.md                     # 存储容量分析
├── server_resource_report_*.md             # 服务器资源分析
├── db_capacity_report_*.md                 # 数据库容量分析
├── dependency_report_*.md                  # 依赖系统分析
├── change_event_report_*.md                # 变更事件关联分析
├── system_comparison_report_*.md           # 多系统对比
├── bottleneck_report_*.md                  # 瓶颈分析
├── pca_cluster_report_*.md                 # PCA聚类分析
├── capacity_forecast_report_*.md           # 趋势预测
├── charts/                                 # 所有 PNG 图表
└── *.csv                                   # 指标/告警/预测数据
```

## 告警规则摘要

| 级别 | 触发条件 |
|------|---------|
| 🔴 紧急 | 磁盘/CPU/内存 > 90%、可用率 < 99%、依赖超设计值100%、2周内容量耗尽 |
| ⚠️ 告警 | 磁盘/CPU/内存 > 80%、可用率 < 99.5%、依赖超设计值80%、4周内耗尽 |
| ⚡ 预警 | 差错率 > 1%、超时率 > 0.5%、8周内耗尽、趋势突变 |

## 目录结构

```
bank-ops-inspection-skills/
├── README.md                            # 本文件
├── references/
│   └── data-discovery.md               # 共享数据发现策略
├── scripts/
│   ├── data_utils.py                   # 数据工具：发现、解析、计算
│   ├── excel_parser.py                 # Excel 汇总大表解析
│   └── chart_utils.py                  # 图表工具：6种常用图表
├── transaction_performance_analysis/   # 交易性能综合分析
│   ├── SKILL.md                         # Claude Code 技能定义
│   ├── README.md                        # 用户文档
│   └── requirements.txt                 # Python 依赖
├── error_timeout_analysis/              # 差错与超时分析
├── system_availability_analysis/        # 系统可用率分析
├── storage_capacity_trend/              # 存储容量趋势分析
├── server_resource_analysis/            # 服务器资源分析
├── database_capacity_analysis/          # 数据库容量分析
├── dependency_performance_analysis/     # 依赖系统性能分析
├── change_event_correlation/            # 变更与事件关联分析
├── comprehensive_correlation_heatmap/   # 综合指标相关性热力图
├── multi_system_comparison/             # 多系统指标对比
├── pca_cluster_analysis/                # 主成分分析与聚类
├── trend_prediction_capacity_alert/     # 趋势预测与容量预警
└── weekly_inspection_analysis/          # 运维周报编排入口
```

## 适配到其他项目

技能包内置了数据自发现机制，适配新项目只需：

1. **数据目录**: 按上述结构组织原始数据，或设置 `INSPECTION_DATA_DIR` 环境变量
2. **业务线**: 修改 `references/data-discovery.md` 中的业务线识别表和 `scripts/data_utils.py` 中的 `BIZ_MAP`
3. **阈值**: 按你的运维规范修改各 SKILL.md `## 告警规则` 章节
4. **数据列名**: 修改各 SKILL.md `## 数据提取` 章节中的 Sheet 名和关键列名，以及 `scripts/excel_parser.py` 中的列映射

## 依赖项

| 包 | 版本 | 说明 | 哪些技能需要 |
|----|------|------|------------|
| matplotlib | >=3.5.3 | 图表生成 | 全部 |
| numpy | >=1.21.6 | 数值计算 | 全部 |
| openpyxl | >=3.1.3 | Excel 解析 | 全部 |
| python-docx | >=0.8.11 | DOCX 解析 | 全部 |
| scipy | >=1.7.0 | 统计分析 | 全部 |
| scikit-learn | >=1.0.2 | PCA/聚类/线性回归 | pca_cluster, trend_prediction |
| seaborn | >=0.12.2 | 热力图 | correlation_heatmap, pca_cluster |
