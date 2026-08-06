#!/usr/bin/env python
"""
FEALPy 线性求解器 —— 一键运行全部演示
======================================
按顺序运行所有 9 个求解器 + 综合对比。
每个 demo 独立运行，出错的不会阻塞后续程序。
"""
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEMOS = [
    ("01_spsolve",       "spsolve_demo.py"),
    ("02_cg",            "cg_demo.py"),
    ("03_minres",        "minres_demo.py"),
    ("04_gmres",         "gmres_demo.py"),
    ("05_lgmres",        "lgmres_demo.py"),
    ("06_bicg",          "bicg_demo.py"),
    ("07_bicgstab",      "bicgstab_demo.py"),
    ("08_jacobi",        "jacobi_demo.py"),
    ("09_gauss_seidel",  "gauss_seidel_demo.py"),
    ("10_comparison",    "comparison_demo.py"),
]

PYTHON = sys.executable

def main():
    print("=" * 62)
    print("  FEALPy 线性求解器 —— 一键运行全部演示")
    print("=" * 62)
    print()

    passed, failed = 0, 0
    for folder, script in DEMOS:
        path = os.path.join(BASE_DIR, folder, script)
        print(f"\n{'─' * 62}")
        print(f"  ▶ {folder}/{script}")
        print(f"{'─' * 62}")

        result = subprocess.run(
            [PYTHON, path],
            capture_output=True, text=True,
            encoding='utf-8', errors='replace',
            timeout=60,
            cwd=os.path.join(BASE_DIR, folder)
        )
        if result.returncode == 0:
            print(result.stdout)
            passed += 1
        else:
            print(result.stdout)
            print(f"  ✗ 错误:\n{result.stderr}")
            failed += 1

    print(f"\n{'=' * 62}")
    print(f"  完成: {passed} 通过, {failed} 失败 (共 {len(DEMOS)})")
    print(f"{'=' * 62}")


if __name__ == "__main__":
    main()
