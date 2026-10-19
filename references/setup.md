# 安装与运行环境

skill 的安装和视频渲染环境是两件事。只写文案、事实表或分镜时不需要 Python 第三方包；渲染时需要 Python 3.10+、Playwright 浏览器、ffmpeg 和字体。

所有资源相对于 `SKILL.md` 定位。下列 `SKILL_ROOT` 要替换为安装后的真实绝对路径，命令可从任意工作目录运行。不要从用户项目的当前目录寻找 `engine/`。

## 首次配置

建议在用户项目中创建虚拟环境，避免改变系统 Python；不要把虚拟环境放进待发布的 skill。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r "$SKILL_ROOT/requirements.txt"
python3 -m playwright install chromium
python3 "$SKILL_ROOT/engine/get_fonts.py"
python3 "$SKILL_ROOT/scripts/check_environment.py"
```

Windows PowerShell 用 `.venv\Scripts\Activate.ps1` 激活，设置路径时用 `$env:SKILL_ROOT`。其他 Python 命令相同。

ffmpeg 通过系统包管理器或 [ffmpeg 官方下载页](https://ffmpeg.org/download.html) 安装。Linux CI 若缺浏览器系统依赖，可使用 `python3 -m playwright install --with-deps chromium`；它可能需要管理员权限。

默认先启动 Playwright 安装的 Chromium；不存在时尝试本机 Chrome。可通过 `VK_BROWSER_CHANNEL=chrome` 指定 Chrome；指定后不会静默换浏览器。只有本机 Chrome 时可跳过 Chromium 下载。预览 `render.py --serve` 只需 Python 标准库和一个可手动打开的浏览器。

字体来自 Google Fonts，首次约需下载数十 MB，保存在 skill 的 `engine/fonts/`；许可证随仓库提供。`get_fonts.py --check` 只检查，不联网。下载失败会返回非零退出码，重跑会跳过已有字体。无法联网时可按脚本给出的链接手动下载到同一目录；不要用回退字体冒充已验证的视觉结果。

## 环境检查

```bash
python3 "$SKILL_ROOT/scripts/check_environment.py"
```

检查当前解释器版本、Python 包导入、ffmpeg 可执行性、浏览器能否启动及缺失字体。全部就绪返回 0，否则返回 1。使用同一个解释器安装依赖和运行渲染，不要混用全局 `pip`。

## 常见问题

| 现象 | 处理 |
|---|---|
| 找不到模块 | 用当前虚拟环境的 `python3 -m pip install -r ...` |
| 找不到 Chromium / Chrome | `python3 -m playwright install chromium`，或设置有效的 `VK_BROWSER_CHANNEL` |
| 字体报缺失 | 运行 `engine/get_fonts.py`，检查网络和 skill 目录的写权限 |
| 找不到 ffmpeg | 安装 ffmpeg 并让当前进程的 PATH 能找到它 |
| `--serve` 端口占用 | 关闭先前的预览进程；截图和渲染使用自动分配的本地端口 |
| 工程已存在 | 直接编辑；只有明确要重建时才使用 `new_film.py --force`，它会覆盖 `film.js` 与 `index.html` |

在无法配置依赖的环境里，先交付可编辑源文件与待执行命令，列明未渲染或未检查的范围。
