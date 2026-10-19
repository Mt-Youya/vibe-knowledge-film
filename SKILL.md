---
name: vibe-knowledge-film
description: >-
  Create subtitle-led educational films with original Canvas animation, storyboards,
  deterministic frame rendering, and synthesized audio. Use for Vibe 知识大赏、无旁白科普短片、
  字幕驱动的知识动画，或把选题/文案做成代码生成的视频；也可修改已有此类工程。
  Defaults to 16:9 horizontal video. Not intended for talking-head or voiceover production.
license: SEE LICENSE
---

# Vibe 知识短片

把知识做成可见的因果过程：观众读一句字幕，同时看屏上的东西执行这句话里的动作。
交付可编辑工程、事实来源、分镜和视频；用户只要文案、分镜或片段时，交付到其指定范围。

## 默认与边界

- 默认无旁白、1920×1080、30fps、16:9；完整选题通常 2–5 分钟。用户指定的时长、外观和交付范围优先。引擎固定横屏；竖屏需要调整引擎和版式，不能只改导出参数。
- 使用已有上下文和项目约定。只补问会影响内容或交付的缺失信息，其余说明假设后继续。用户要求完整制作时，分镜和 30 秒样片是内部检查点，不默认停下来等待确认；明确要求审核时才等待。
- 写原创内容；参考片用于研究表达方法。不要复制其中的字幕、构图或署名；保留用户素材的必要署名和授权要求。权利范围见 [LICENSE](LICENSE)。
- 缺少渲染条件时仍可完成事实表、文案、分镜和代码，明确报告缺少的依赖和未验证的部分。空骨架或静帧不能当作已完成的视频。

## 先定位资源与运行环境

本文件所在目录是 **skill 根目录**，不是用户的工作目录。下面的 `SKILL_ROOT` 代表该目录的绝对路径，`PROJECT` 代表用户项目中的输出目录；执行时替换为实际路径。不要假定安装在某个 Agent 的固定目录。

1. 查看目标项目和已有修改；新工程放在用户项目中，不放在 skill 目录。
2. 先运行 `python3 "$SKILL_ROOT/scripts/check_environment.py"`。它检查 Python 包、ffmpeg、浏览器启动和字体，缺项时返回非零状态并给出修复提示。安装步骤见 [references/setup.md](references/setup.md)。
3. 只写文案或分镜时无需安装渲染依赖。制作视频时，先补齐依赖再进入渲染。

## 制作流程

### 1. 定论点、核事实、找形象

先写一句话论点、目标观众和要讲清的概念。把上屏的事实、数字、适用条件及可核对来源记入 `facts.md`；优先查原始论文、官方材料或用户提供的可靠资料。未经核对的参考片文案不能直接当作事实来源；查不到的内容应删去、替换或明确标注不确定。

读 [references/visualization.md](references/visualization.md) 的第二至六节：六种画法、何时不画、找形象、分镜格式。需要对照案例时再读第一、七节。

为每个概念选可识别的主体、动作和尺度。具体事物应有能认出的外形；数学中的点、线、坐标可以直接使用，但应明确它们表示什么。提问、命名、结论可以留白，不需要硬凑新画面或固定比例。

### 2. 同时写字幕和分镜

读 [references/script.md](references/script.md)。在 `storyboard.md` 中一行一镜，至少记录：

| 时间 | 字幕 | 主体和动作 | 屏上标注 / 来源 | 观众理解的变化 | 声音 |
|---|---|---|---|---|---|

字幕说“移走一半”，画面就要真的移走一半。数字来自真实计算，示意比例和假说必须标明。遮住字幕后，应仍能识别主体及其变化；只读字幕，应能理解连续的论证。

让一组道具或尺度贯穿全片，先例子后命名；在需要阅读、思考的地方停留。参考资料里的句长、镜数、留白比例是经验起点，按实际阅读速度调整。

选外观时读 [references/worlds.md](references/worlds.md)：行为故事常用 **B 寓言**，抽象机制常用 **C 夜曲**。可以按用户要求调整，不必把不相干的选题塞进同一套装置。

### 3. 建工程，做难镜头和开头片段

读 [references/engine.md](references/engine.md) 的命令与 API。使用空骨架，按本片分镜写画面；通用字幕、绘图工具可以复用，示例中的具体作品设计不直接搬用。

```bash
python3 "$SKILL_ROOT/scripts/new_film.py" "$PROJECT" --world C
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --stills 5.9 18.1
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --motion 8.2 10.6
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --sheet 16
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --clip 0 30 head
```

`--world` 可用 B 或 C。已有工程直接修改，不重新初始化覆盖；时长不足 30 秒时用实际片长。
先实现最难的一镜，检查它是否真的解释了概念，再扩展到开头片段和全片。看原尺寸静帧和转场序列，按 [references/visualization.md](references/visualization.md) 第八节修正具体问题；改完重截相同时刻，检查到达可读、可辨认、因果清晰的标准，不凑固定返工轮数。

### 4. 完成画面与声音

每帧仅由时间 `t` 决定；用固定随机种子，模拟预先计算或按时间求值，避免 `Math.random()`、实时时钟和跨帧累积状态。字幕统一放在画面最外层，留净底部约 80%–95% 的区域。先抽帧、再渲片段、最后渲全片。

```bash
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --det
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --jobs 4
python3 "$SKILL_ROOT/engine/render.py" "$PROJECT" --events
python3 "$SKILL_ROOT/engine/audio.py" "$PROJECT"
```

根据机器资源选择 `--jobs`，单路可省略。声音事件在 `film.js` 里用 `fr.sfx` 登记；无背景音乐时可合成音效与底音，有用户提供且可用的配乐时用 `audio.py --bgm` 混合。没有 BGM 不必阻塞交付，说明实际音轨内容。

### 5. 验证与交付

- 内容：对照 `facts.md` 核对数字、条件和来源；分镜中的关键因果在画面上成立，模拟量与字幕一致。
- 视觉：查看关键镜头静帧、字幕最长句和各转场序列；主体可辨认、字幕可读、颜色含义一致，无意外遮挡。
- 技术：`--det` 成功；视频可解码，尺寸、帧率、时长、音视频流符合要求；听取音轨检查削波、突变与音画时刻。
- 交付：链接 `storyboard.md`、`facts.md`、`film.js` 及 `renders/final.mp4`，简述检查范围。`raw.mp4` 是无声中间产物；未完整观看或试听的部分如实说明，不以命令成功代替内容验收。

## 按需参考

- [references/setup.md](references/setup.md)：首次安装、依赖、浏览器和字体故障。
- [references/engine.md](references/engine.md)：确定性绘图、字幕、音效 API 和渲染命令。
- [references/visual-grammar.md](references/visual-grammar.md)：版式、转场和动作手感速查。
- [references/analysis.md](references/analysis.md)：原项目对四条参考片的观察，非独立核验后的事实来源。
- [references/prompts.md](references/prompts.md)：需要向其他工具提供 brief 或诊断作品时使用；其中的示例审批步骤不覆盖当前用户指令。
- [examples/README.md](examples/README.md)：样片和引擎调用示例，含原创练习及明确标注的参考片研究。
