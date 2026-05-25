# 数据发现策略

所有分析技能共享的数据定位和格式检测逻辑。

## 1. 定位数据目录

从当前工作目录开始，向上查找 `data/raw_data/` 目录。也可通过环境变量 `INSPECTION_DATA_DIR` 显式指定数据根目录。

```bash
# 示例：显式指定
export INSPECTION_DATA_DIR=/path/to/data/raw_data/
```

## 2. 识别周目录

扫描数据目录下所有子目录，识别名称包含「周」的目录作为周次数据目录（如 `3月第1周`、`5月第3周`）。

```python
import os
week_dirs = sorted([
    d for d in os.listdir(data_dir)
    if os.path.isdir(os.path.join(data_dir, d)) and '周' in d
])
```

## 3. 检测数据格式（优先级从高到低）

在每个周目录中：

1. 查找 `*巡检数据汇总*.xlsx` → 如果存在，使用汇总大表（优先）
2. 查找 `*巡检报告*.docx`、`*巡检周报*.docx` → 如果不存在 Excel，回退使用单系统巡检报告

**汇总大表优先的原因**：7 个 Sheet 覆盖全部 8 条业务线的所有指标，一次解析替代逐份 DOCX 提取，数据一致性和完整性更好。

```python
import glob
summary = sorted(glob.glob(os.path.join(week_dir, '*巡检数据汇总*.*xl*')))
if summary:
    # 优先使用汇总大表
    fpath = summary[0]
else:
    # 回退 DOCX
    docx_files = sorted(glob.glob(os.path.join(week_dir, '*.docx')))
```

## 4. 业务线识别

从文件名关键词或 Excel 内容中识别 8 条业务线：

| 文件关键词 | 业务线 | 说明 |
|-----------|--------|------|
| ESB系统 | ESB系统 | 企业服务总线 |
| 银联无卡 | 银联无卡 | 银联无卡快捷支付 |
| 银联支付清算 | 银联前置 | 银联支付清算系统 |
| 超级网银 | 超级网银 | 统一支付(超级网银) |
| 人民银行大小额 | 人行大小额 | 统一支付(人民银行大小额支付系统) |
| 农信银 | 农信银 | 统一支付(农信银二代支付系统) |
| 核心系统 | 核心系统 | 银行核心系统 |
| 校园一卡通 | 校园一卡通 | 校园一卡通系统 |

```python
from collections import OrderedDict
BIZ_MAP = OrderedDict([
    ('银联无卡', '银联无卡'),
    ('银联支付清算', '银联前置'),
    ('超级网银', '超级网银'),
    ('人民银行大小额', '人行大小额'),
    ('农信银', '农信银'),
    ('核心系统', '核心系统'),
    ('ESB系统', 'ESB系统'),
    ('校园一卡通', '校园一卡通'),
])

def identify_biz(filepath):
    """从文件路径识别业务线名称"""
    for keyword, biz_name in BIZ_MAP.items():
        if keyword in filepath:
            return biz_name
    return None
```

## 5. 输出路径

默认输出到 `./output/`（相对于当前工作目录），可通过环境变量 `INSPECTION_OUTPUT_DIR` 覆盖。图表统一输出到 `./output/charts/`。

```bash
export INSPECTION_OUTPUT_DIR=/path/to/output/
```

## 汇总大表 Sheet 速查

| Sheet | 行数 | 内容 | 关联技能 |
|-------|------|------|---------|
| "1-交易性能" | 8 | 交易量/TPS/可用率/空闲率 | transaction, error_timeout, availability, storage, comparison |
| "2-服务器资源" | 16 | CPU/内存/目录使用率 | server_resource, correlation, pca, trend |
| "3-数据库巡检" | 86 | 数据库容量/表空间/xlog | database_capacity, trend |
| "4-依赖系统" | 18 | 外部依赖TPS/设计值 | dependency_performance |
| "5-变更与事件" | 20 | 变更记录/事件记录 | change_event |
| "6-第三方服务商摘要" | 4 | 服务商周报摘要 | weekly_inspection |
| "0-本周概览" | - | 使用说明 | - |
