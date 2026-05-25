#!/usr/bin/env python3
"""图表工具 — matplotlib 通用配置和常用图表生成函数。

Usage:
    from scripts.chart_utils import setup_mpl, plot_time_series, plot_scatter_with_regression
    from scripts.chart_utils import plot_bar, plot_heatmap, plot_radar
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scripts.data_utils import get_output_dir, ensure_output_dirs


def setup_mpl():
    """初始化 matplotlib 中文字体配置，在所有图表生成前调用。"""
    plt.rcParams['font.sans-serif'] = [
        'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei',
        'Noto Sans CJK SC', 'SimHei', 'DejaVu Sans'
    ]
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['savefig.dpi'] = 150


# 标准颜色方案
COLORS = plt.cm.tab10.colors if hasattr(plt.cm, 'tab10') else ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']


def plot_time_series(series_dict, title, xlabel='周次', ylabel='',
                     threshold=None, threshold_label='', output_path=None,
                     figsize=(12, 6)):
    """生成多系列时间序列折线图。

    Args:
        series_dict: {label: [(x, y), ...]} 多个系列
        title: 图表标题
        xlabel, ylabel: 轴标签
        threshold: 可选，阈值线（水平虚线）
        threshold_label: 阈值线标签
        output_path: 输出 PNG 路径
        figsize: 图表尺寸
    """
    setup_mpl()
    fig, ax = plt.subplots(figsize=figsize)

    for i, (label, points) in enumerate(series_dict.items()):
        if not points:
            continue
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        color = COLORS[i % len(COLORS)]
        ax.plot(xs, ys, marker='o', color=color, label=label, linewidth=1.5, markersize=5)

    if threshold is not None:
        ax.axhline(y=threshold, color='red', linestyle='--', linewidth=1,
                   label=threshold_label or f'阈值={threshold}')

    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc='best')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=30)

    _, charts_dir = ensure_output_dirs()
    if output_path is None:
        output_path = os.path.join(charts_dir, f'time_series_{title}.png')

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_scatter_with_regression(x_vals, y_vals, labels=None, title='',
                                  xlabel='X', ylabel='Y', output_path=None,
                                  figsize=(10, 8)):
    """生成散点图 + 线性回归拟合线。

    Args:
        x_vals: list of lists, 每个子列表为一个系列
        y_vals: list of lists
        labels: 各系列标签
        title, xlabel, ylabel: 图表标注
        output_path: 输出路径

    Returns:
        (output_path, corr_results) — corr_results 包含各系列的 Pearson r 和 p 值
    """
    from scipy import stats as sp_stats
    setup_mpl()
    fig, ax = plt.subplots(figsize=figsize)
    corr_results = []

    for i in range(len(x_vals)):
        xs = np.array(x_vals[i], dtype=float)
        ys = np.array(y_vals[i], dtype=float)
        label = labels[i] if labels and i < len(labels) else f'Series {i+1}'
        color = COLORS[i % len(COLORS)]

        ax.scatter(xs, ys, color=color, label=label, s=30, alpha=0.7)

        if len(xs) >= 3:
            coeffs = np.polyfit(xs, ys, 1)
            line = np.poly1d(coeffs)
            x_line = np.linspace(xs.min(), xs.max(), 100)
            ax.plot(x_line, line(x_line), color=color, linewidth=1.5, linestyle='-')
            r, p = sp_stats.pearsonr(xs, ys)
            corr_results.append({'label': label, 'pearson_r': round(r, 3), 'p_value': round(p, 4)})

    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    _, charts_dir = ensure_output_dirs()
    if output_path is None:
        output_path = os.path.join(charts_dir, f'scatter_{title}.png')

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path, corr_results


def plot_bar(categories, values, title='', xlabel='', ylabel='',
             threshold=None, horizontal=True, output_path=None,
             figsize=(12, 6)):
    """生成条形图（默认横向）。

    Args:
        categories: 类别名列表
        values: 对应值列表
        title, xlabel, ylabel: 图表标注
        threshold: 可选阈值线
        horizontal: True=横向条形图, False=纵向
        output_path: 输出路径
    """
    setup_mpl()
    fig, ax = plt.subplots(figsize=figsize)

    idxs = range(len(categories))
    if horizontal:
        bars = ax.barh(idxs, values, color=COLORS[:len(categories)])
        ax.set_yticks(idxs)
        ax.set_yticklabels(categories, fontsize=9)
        if threshold is not None:
            ax.axvline(x=threshold, color='red', linestyle='--', linewidth=1)
    else:
        bars = ax.bar(idxs, values, color=COLORS[:len(categories)])
        ax.set_xticks(idxs)
        ax.set_xticklabels(categories, fontsize=9, rotation=30)
        if threshold is not None:
            ax.axhline(y=threshold, color='red', linestyle='--', linewidth=1)

    ax.set_title(title, fontsize=13, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, alpha=0.2, axis='x' if horizontal else 'y')

    _, charts_dir = ensure_output_dirs()
    if output_path is None:
        output_path = os.path.join(charts_dir, f'bar_{title}.png')

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_heatmap(matrix, row_labels, col_labels, title='相关性热力图',
                 cmap='RdBu_r', annot=True, output_path=None, figsize=(14, 12)):
    """生成相关性热力图。

    Args:
        matrix: 2D numpy array
        row_labels, col_labels: 行列标签
        title: 图表标题
        cmap: 颜色映射
        annot: 是否标注数值
        output_path: 输出路径
    """
    import seaborn as sns
    setup_mpl()
    fig, ax = plt.subplots(figsize=figsize)

    mask = np.triu(np.ones_like(matrix, dtype=bool), k=1)
    sns.heatmap(matrix, mask=mask, annot=annot, fmt='.2f',
                cmap=cmap, center=0,
                xticklabels=col_labels, yticklabels=row_labels,
                square=True, linewidths=0.5, ax=ax,
                cbar_kws={'shrink': 0.8})

    ax.set_title(title, fontsize=13, fontweight='bold', pad=15)

    _, charts_dir = ensure_output_dirs()
    if output_path is None:
        output_path = os.path.join(charts_dir, f'heatmap_{title}.png')

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path


def plot_radar(categories, values_dict, title='系统雷达图',
               output_path=None, figsize=(10, 10)):
    """生成雷达图（多系统对比）。

    Args:
        categories: 指标名列表（轴标签）
        values_dict: {系统名: [值, ...]}
        title: 图表标题
        output_path: 输出路径
    """
    setup_mpl()
    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # 闭合

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))

    for i, (label, values) in enumerate(values_dict.items()):
        vals = list(values) + [values[0]]  # 闭合
        color = COLORS[i % len(COLORS)]
        ax.fill(angles, vals, alpha=0.1, color=color)
        ax.plot(angles, vals, 'o-', linewidth=2, color=color, label=label, markersize=4)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)

    _, charts_dir = ensure_output_dirs()
    if output_path is None:
        output_path = os.path.join(charts_dir, f'radar_{title}.png')

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
