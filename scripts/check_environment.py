#!/usr/bin/env python3
"""Check render dependencies without installing or downloading anything."""
import importlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    issues = []
    if sys.version_info < (3, 10):
        issues.append("需要 Python 3.10+")
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    for module, package in (("playwright.sync_api", "playwright"), ("numpy", "numpy"),
                            ("scipy.signal", "scipy"), ("PIL.Image", "Pillow")):
        try:
            importlib.import_module(module)
            print(f"OK: {package}")
        except ImportError as exc:
            issues.append(f"{package} 无法导入: {exc}")
    if shutil.which("ffmpeg"):
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode:
            issues.append("ffmpeg 无法执行")
        else:
            print("OK: " + result.stdout.splitlines()[0])
    else:
        issues.append("PATH 中没有 ffmpeg；请先通过系统包管理器安装")
    sys.path.insert(0, str(ROOT / "engine"))
    from get_fonts import missing_fonts
    missing = missing_fonts(ROOT / "engine/fonts")
    if missing:
        issues.append("缺少字体: " + ", ".join(missing))
    else:
        print("OK: fonts")
    try:
        from playwright.sync_api import sync_playwright
        from render import launch_browser
        with sync_playwright() as playwright:
            browser = launch_browser(playwright)
            print(f"OK: browser {browser.version}")
            browser.close()
    except Exception as exc:
        issues.append(f"浏览器不可用: {exc}")
    if issues:
        print("\n需要处理：")
        for issue in issues:
            print(f"- {issue}")
        print(f'\nPython 包: "{sys.executable}" -m pip install -r "{ROOT / "requirements.txt"}"')
        print(f'浏览器: "{sys.executable}" -m playwright install chromium')
        print(f'字体: "{sys.executable}" "{ROOT / "engine/get_fonts.py"}"')
        return 1
    print("\n渲染环境就绪。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
