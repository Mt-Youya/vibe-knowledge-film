# -*- coding: utf-8 -*-
"""把引擎用到的字体下到 engine/fonts/（已有的跳过）。全部是 SIL OFL 1.1 授权的开源字体，来自 github.com/google/fonts。
  python get_fonts.py          缺哪个下哪个
  python get_fonts.py --check  只检查，不下载
中文两款各 20MB 左右，所以仓库里可以不带字体，装好 skill 后跑一次这个脚本。"""
import argparse, sys, urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
FONTS = {   # 本地文件名: 仓库路径
    "NotoSerifSC-VF.ttf": "notoserifsc/NotoSerifSC%5Bwght%5D.ttf",             # 宋体（思源宋体），可变字重 200–900
    "NotoSansSC-VF.ttf": "notosanssc/NotoSansSC%5Bwght%5D.ttf",                # 黑体（思源黑体），可变字重 100–900
    "CormorantGaramond.ttf": "cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf",
    "CormorantGaramond-Italic.ttf": "cormorantgaramond/CormorantGaramond-Italic%5Bwght%5D.ttf",
    "Lora.ttf": "lora/Lora%5Bwght%5D.ttf",
    "Lora-Italic.ttf": "lora/Lora-Italic%5Bwght%5D.ttf",
    "JetBrainsMono.ttf": "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
    "CourierPrime-Regular.ttf": "courierprime/CourierPrime-Regular.ttf",
    "OFL-NotoSerifSC.txt": "notoserifsc/OFL.txt", "OFL-NotoSansSC.txt": "notosanssc/OFL.txt",
    "OFL-CormorantGaramond.txt": "cormorantgaramond/OFL.txt", "OFL-Lora.txt": "lora/OFL.txt",
    "OFL-JetBrainsMono.txt": "jetbrainsmono/OFL.txt", "OFL-CourierPrime.txt": "courierprime/OFL.txt",
}

def missing_fonts(directory):
    return [k for k in FONTS if not (directory / k).is_file() or (directory / k).stat().st_size < 1000]


def download_fonts(directory):
    directory.mkdir(parents=True, exist_ok=True)
    missing = missing_fonts(directory)
    for k in missing:
        print("下载", k, "…", flush=True)
        target = directory / k
        temporary = target.with_suffix(target.suffix + ".part")
        try:
            with urllib.request.urlopen(BASE + FONTS[k], timeout=180) as r:
                data = r.read()
            if len(data) < 1000:
                raise ValueError("下载文件不完整")
            temporary.write_bytes(data)
            temporary.replace(target)
        except Exception as e:
            temporary.unlink(missing_ok=True)
            print("  失败：", e, "\n  可以手动从", BASE + FONTS[k], "下载后放到", target)
    remaining = missing_fonts(directory)
    print("完成。" if not remaining else "还有没下到的，重跑一次或手动放进去。")
    return 1 if remaining else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只检查，不下载")
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent / "fonts"
    if args.check:
        missing = missing_fonts(directory)
        print("字体齐全" if not missing else "缺：" + "、".join(missing))
        sys.exit(1 if missing else 0)
    sys.exit(download_fonts(directory))
