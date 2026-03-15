#!/usr/bin/env python3
"""
从 monoZ.pdf（arXiv:1701.05379 Fig 5, CMS-PAS-EXO-16-010）提取 MET bin edges。

方法 1：若已安装 PyMuPDF (fitz)，将 PDF 渲染为图像并检测直方图阶梯边缘。
方法 2：否则使用论文/分析中采用的 CMS-EXO-16-010 官方 bin edges。
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MONOZ_PDF = SCRIPT_DIR / "monoZ.pdf"

# 论文 plot_figures.py 中使用的 CMS-PAS-EXO-16-010 bin edges（与 monoZ 图一致）
CMS_EXO_16_010_BIN_EDGES = [100, 150, 200, 250, 300, 400, 500, 600, 900, 1200]


def extract_from_image() -> list[float] | None:
    """用 PyMuPDF 渲染 PDF 并尝试从图像中检测 bin 边缘。"""
    try:
        import fitz  # PyMuPDF
        import numpy as np
    except ImportError:
        return None

    if not MONOZ_PDF.exists():
        print(f"文件不存在: {MONOZ_PDF}", file=sys.stderr)
        return None

    doc = fitz.open(MONOZ_PDF)
    page = doc[0]
    # 2x 缩放以便更清晰检测边缘
    mat = fitz.Matrix(2, 2)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    doc.close()

    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if img.shape[2] >= 3:
        gray = img[:, :, :3].mean(axis=2).astype(np.float64)
    else:
        gray = img.squeeze().astype(np.float64)

    h, w = gray.shape
    # 取图中偏上的水平带（主图区域，避开标题和 ratio panel）
    y0, y1 = int(h * 0.25), int(h * 0.55)
    row = gray[y0:y1, :].mean(axis=0)

    # 平滑后求梯度，阶梯上升沿为负梯度
    kernel = np.ones(5) / 5
    row_smooth = np.convolve(row, kernel, mode="same")
    grad = -np.gradient(row_smooth)
    # 只保留明显峰（bin 左边缘）
    thresh = max(grad.min(), grad.max() * 0.3) if grad.max() > 0 else 0
    peaks = []
    for i in range(1, len(grad) - 1):
        if grad[i] > thresh and grad[i] >= grad[i - 1] and grad[i] >= grad[i + 1]:
            peaks.append(i)

    if len(peaks) < 5:
        return None

    # 按 x 排序并去近邻，保留约 9 个 bin 边界（10 个边）
    peaks = sorted(set(peaks))
    merged = [peaks[0]]
    for p in peaks[1:]:
        if p - merged[-1] >= w / 30:
            merged.append(p)
    if len(merged) < 8:
        merged = peaks[:10]  # fallback

    # 映射像素 x -> E_T (GeV)。图中轴范围约 80–1200 GeV
    x_min_px, x_max_px = merged[0], merged[-1] if len(merged) > 1 else w
    et_min, et_max = 80.0, 1200.0
    edges_geV = [
        round(et_min + (x - x_min_px) / max(x_max_px - x_min_px, 1) * (et_max - et_min), 1)
        for x in merged
    ]
    # 确保首尾
    edges_geV = [et_min] + [e for e in edges_geV[1:-1] if et_min < e < et_max] + [et_max]
    return edges_geV if len(edges_geV) >= 5 else None


def main() -> None:
    print("monoZ.pdf 对应: arXiv:1701.05379 (Brivio et al.), CMS-PAS-EXO-16-010 选择")
    print("横轴: E_T^miss [GeV], 纵轴: # Events / GeV")
    print()

    edges = extract_from_image()
    if edges is not None and len(edges) >= 5:
        print("从 PDF 图像检测到的 bin edges (GeV):")
        print(edges)
        print()
        print("(若与下方参考不一致，请以 CMS 官方为准)")
        print()

    print("采用的 bin edges (CMS-PAS-EXO-16-010, 与 plot_figures.py 一致) [GeV]:")
    print(CMS_EXO_16_010_BIN_EDGES)
    print()
    print("NumPy 格式:")
    print("bin_edges = np.array(" + repr(CMS_EXO_16_010_BIN_EDGES) + ", dtype=float)")
    print()
    print("Bin 宽度 (GeV):", [CMS_EXO_16_010_BIN_EDGES[i + 1] - CMS_EXO_16_010_BIN_EDGES[i] for i in range(len(CMS_EXO_16_010_BIN_EDGES) - 1)])


if __name__ == "__main__":
    main()
