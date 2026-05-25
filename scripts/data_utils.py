#!/usr/bin/env python3
"""数据工具 — 数据发现、解析和指标计算的共享函数。

Usage: from scripts.data_utils import safe_float, identify_biz, calc_wow, discover_data
"""

import os
import glob
from collections import OrderedDict

# 8 条业务线映射
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
    """从文件路径识别业务线名称。"""
    for keyword, biz_name in BIZ_MAP.items():
        if keyword in os.path.basename(filepath):
            return biz_name
    return None


def safe_float(value, default=None):
    """安全转换为 float，处理 '--'、'/'、'%'、千分位逗号等非标准值。"""
    if value is None:
        return default
    s = str(value).strip().replace('%', '').replace(',', '').replace('"', '')
    if s in ('', '--', '/', '-', 'None', 'nan', 'N/A'):
        return default
    try:
        return float(s)
    except ValueError:
        return default


def calc_wow(current, previous):
    """计算周环比变化(%)。current 和 previous 应为数值。"""
    if previous is None or previous == 0:
        return None
    if current is None:
        return None
    return round((current - previous) / previous * 100, 1)


def discover_data(data_dir=None):
    """自动发现数据目录和所有周数据。

    Returns:
        dict: {
            'data_dir': str,
            'week_dirs': {label: path},
            'weeks_sorted': [label, ...]
        }
    """
    if data_dir is None:
        # 从当前目录向上查找 data/raw_data/
        data_dir = os.environ.get('INSPECTION_DATA_DIR')
        if not data_dir:
            cur = os.getcwd()
            for _ in range(10):
                candidate = os.path.join(cur, 'data', 'raw_data')
                if os.path.isdir(candidate):
                    data_dir = candidate
                    break
                parent = os.path.dirname(cur)
                if parent == cur:
                    break
                cur = parent

    if not data_dir or not os.path.isdir(data_dir):
        raise FileNotFoundError(f"数据目录不存在: {data_dir}")

    week_dirs = {}
    for d in sorted(os.listdir(data_dir)):
        full = os.path.join(data_dir, d)
        if os.path.isdir(full) and '周' in d:
            week_dirs[d] = full

    return {
        'data_dir': data_dir,
        'week_dirs': week_dirs,
        'weeks_sorted': sorted(week_dirs.keys()),
    }


def get_output_dir():
    """获取输出目录，默认 ./output/。"""
    return os.environ.get('INSPECTION_OUTPUT_DIR', os.path.join(os.getcwd(), 'output'))


def ensure_output_dirs():
    """创建 output/ 和 output/charts/ 目录。"""
    base = get_output_dir()
    charts = os.path.join(base, 'charts')
    os.makedirs(charts, exist_ok=True)
    return base, charts


def detect_file_format(week_dir):
    """检测周目录中的数据格式。

    Returns:
        ('excel', path) 如果存在汇总大表
        ('docx', [paths]) 如果只有 DOCX 文件
    """
    xlsx_files = sorted(glob.glob(os.path.join(week_dir, '*巡检数据汇总*.*xl*')))
    if xlsx_files:
        return ('excel', xlsx_files[0])

    docx_files = sorted(glob.glob(os.path.join(week_dir, '*巡检报告*.docx')))
    docx_files.extend(sorted(glob.glob(os.path.join(week_dir, '*巡检周报*.docx'))))
    if docx_files:
        return ('docx', docx_files)

    return (None, None)
