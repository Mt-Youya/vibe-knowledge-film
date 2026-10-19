# vibe-knowledge-film

把选题或文案制作成**无旁白、字幕驱动的知识动画**。先核对事实，把概念变成能看懂的动作，再用 Canvas + JavaScript 绘制画面，由 Playwright 和 ffmpeg 渲染为 MP4。

An Agent Skill for subtitle-led educational films: source-backed scripts, storyboards, original Canvas animation, deterministic rendering, and synthesized audio.

[![skills.sh](https://skills.sh/b/Mt-Youya/vibe-knowledge-film)](https://skills.sh/Mt-Youya/vibe-knowledge-film)

## 安装

本仓库根目录就是一个完整 skill，包含 `SKILL.md`、参考资料、引擎和脚本；无需安装 npm 项目或连接付费视频服务。

通过 skills CLI 安装：

```bash
npx skills add Mt-Youya/vibe-knowledge-film --skill vibe-knowledge-film
```

也可以先克隆仓库，从本地安装：

```bash
npx skills add ./vibe-knowledge-film --skill vibe-knowledge-film
```

选择 Codex、Claude Code、Cursor 等目标 Agent；追加 `-g` 为全局安装。仅查看可发现的 skill，使用 `npx skills add Mt-Youya/vibe-knowledge-film --list`。安装命令来自 [skills CLI 官方文档](https://github.com/vercel-labs/skills)。

**skills.sh 是目录和安装入口，GitHub 是分发来源。** [官方 FAQ](https://skills.sh/docs/faq) 说明，用户通过 CLI 安装后，skill 会通过匿名安装统计自动进入目录和榜单；不需要另外上传 npm 包，也不能保证立刻出现。可安装、已推送和已被目录收录是不同状态。

## 使用

安装后在 Agent 中输入，例如：

```text
使用 vibe-knowledge-film，做一条 90 秒的无旁白知识短片，
给没有概率基础的人讲清“大数定律”。请直接完成事实表、
分镜、动画工程和视频，先做片段自查，再完成全片。
```

```text
使用 vibe-knowledge-film，把下面的文案改成可以画出来的字幕稿和分镜。
这次只需要文案和分镜，不渲染视频：……
```

默认 16:9、1920×1080、30fps。可从 **C 夜曲**（抽象概念、小实验）或 **B 寓言**（角色、行为机制）开始。内置引擎固定横屏；竖屏需要额外调整画布与版式。

完整制作交付 `facts.md`、`storyboard.md`、`film.js`、`index.html` 和 `renders/final.mp4`。它需要研究、绘图与视觉检查，耗时取决于内容复杂度、机器和片长。

## 渲染环境

只生成文案和分镜无需下列依赖。制作视频需要 **Python 3.10+**、**ffmpeg**、Python 包、Chromium 或 Chrome，以及开源字体。Node.js 仅用于运行 `npx skills` 安装器。

把 `SKILL_ROOT` 设置为安装后 `SKILL.md` 所在目录的绝对路径。在用户项目中创建虚拟环境，然后运行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r "$SKILL_ROOT/requirements.txt"
python3 -m playwright install chromium
python3 "$SKILL_ROOT/engine/get_fonts.py"
python3 "$SKILL_ROOT/scripts/check_environment.py"
```

ffmpeg 通过系统包管理器安装。字体首次会从 Google Fonts 下载数十 MB；未安装的 Chromium 也需要下载。默认使用 Playwright Chromium，缺失时尝试本机 Chrome，可用 `VK_BROWSER_CHANNEL` 显式指定。Windows、Linux 及离线配置见 [环境说明](references/setup.md)。

在 skill 目录之外创建工程；以下 `PROJECT` 代表实际输出目录：

```bash
python3 "$SKILL_ROOT/scripts/new_film.py" "$PROJECT" --world C
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --serve
```

新工程是空骨架，需要 Agent 按分镜实现画面。预览地址由命令输出。更多截图、片段、全片和声音命令见 [引擎文档](references/engine.md)。

## 样片

下面是原项目自选题练习的开头，各约 33 秒，用于展示两套外观，并非任意输入都能自动达到的质量保证。

**C 夜曲：《折叠》**

![蛋白质折叠样片](https://raw.githubusercontent.com/HeyChengC/vibe-knowledge-film/62d51508aad00003dc6209afa80c4b5dc540de59/examples/fold_C.gif)

**B 寓言：《鸽子的迷信》**

![鸽子的迷信样片](https://raw.githubusercontent.com/HeyChengC/vibe-knowledge-film/62d51508aad00003dc6209afa80c4b5dc540de59/examples/pigeon_B.gif)

工程和说明见 [examples](examples/README.md)。演示 GIF 引用原仓库的固定版本，不随 skill 安装；示例源码与静态截图保留在本仓库中。

## 项目结构与验证

| 路径 | 用途 |
|---|---|
| `SKILL.md` | Agent 入口、触发描述与制作流程 |
| `agents/openai.yaml` | Codex 展示信息和默认提示词 |
| `references/` | 按需读取的讲解设计、文案、外观和 API |
| `engine/` | 绘图、渲染、声音和字体下载 |
| `scripts/` | 初始化、环境检查、端到端渲染验证 |
| `examples/` | 样片、分镜与参考片研究 |

维护者可运行：

```bash
python3 -m unittest discover -s tests -v
npx skills add . --list
python3 scripts/check_environment.py
python3 scripts/smoke_test.py
```

最后一条会在临时目录中生成并解码 1.2 秒测试片，检查确定性、并行渲染、音效导出和 H.264/AAC 音视频流；需要完整渲染环境及随 ffmpeg 提供的 ffprobe。仓库包含同一流程的 GitHub Actions 检查。

## 来源与许可

本项目基于 [HeyChengC/vibe-knowledge-film](https://github.com/HeyChengC/vibe-knowledge-film)，保留其引擎、方法研究、示例和原许可；当前版本改进 skill 入口、安装说明与运行可靠性。

引擎、脚本和方法说明使用 [LICENSE](LICENSE) 中的 MIT 许可。该文件列出的参考片字幕与画面设计不在 MIT 授权范围内；`examples/stim_B`、`examples/info_C` 等材料用于学习对照，不应作为自己的作品发布。新片需原创，用户提供素材的权利与必要署名应保留。字体另遵循 `engine/fonts/OFL-*.txt`。
