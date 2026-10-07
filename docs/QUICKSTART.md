# 安装与第一个镜头

## 环境和兼容

使用 Python 3.10+ 与 Node 20+。命令统一从仓库根运行；Windows 可用 `python -X utf8` 避免终端编码差异，Linux/macOS 若命令名为 `python3` 则相应替换。程序只用标准库，不需要 npm install、pip install、API Key 或生图平台账号。

Codex 与 Claude 安装完整 Skill 文件夹后仍需连接本仓库的工具和规范。其他大模型通过能读文件并执行本地命令的宿主使用相同文档；只有聊天能力的宿主可手动读取 bundle，但不能声称已自动调用工具。本次验证了文件格式、安装定位和工具调用，没有执行每种宿主/模型的在线能力测试。

## 路径与安装

```bash
python -X utf8 tools/install_skills.py --target ../my-video-project/.agents/skills
```

Claude 可将目标换成 `.claude/skills`。仓库源码没有嵌入安装者绝对路径；安装副本的 `.runtime.json` 保存实际仓库根，仅用于本机，禁止提交。若已有同名技能，先选一个新的目标目录进行评估，再由使用者决定迁移，不覆盖运行中的版本。

安装后 `scripts/run.py` 按环境变量 `AI_VIDEO_QMS_HOME`、本技能 `.runtime.json`、源码祖先的仓库标记查找运行时。它调用 `tools/qms.py --root <repo>`。不要把 Node CLI 的 `--root` 混为同一参数：Node 的根是 `standards/`，Python 工作台的根是整个仓库。

## 杯子停顿样例

样例用匿名角色 A，只有原创设计，没有实际参考图片、演员或生成视频。

```bash
python -X utf8 tools/qms.py doctor
python -X utf8 tools/qms.py seed-demo
python -X utf8 tools/qms.py wiki --task micro-performance
python -X utf8 tools/qms.py search "杯子 停顿"
```

复制搜索结果实际 `SRC-...`，先全文读取，再组包。不要照抄一个并不存在的来源 ID。

```text
python -X utf8 tools/qms.py get <实际SRC编号>
python -X utf8 tools/qms.py context --task micro-performance --evidence-ids <实际SRC编号>
```

```bash
python -X utf8 tools/qms.py shot-check --plan examples/cup-pause/shot-plan.json
python -X utf8 tools/qms.py shot-bundle --plan examples/cup-pause/shot-plan.json --out data/cup-pause-bundle.md
```

设计卡中 writing/camera/editing/continuity 必须有设计；其他工种填设计和可观察通过条件，或具体的不适用理由。人物表演按时间列 body/gaze/face/breath，不能只写“紧张”。

助手读包后输出目标模型提示词、参考职责、参数栏和验收清单；没有实际生成前保留 `generation_executed=false`。实际运行平台与付款需另行授权；本仓库没有替用户提交生成的功能。

## 资产路由

```bash
python -X utf8 tools/qms.py image-route --purpose prop --layout exploded --semantics same_time_multiview
python -X utf8 tools/qms.py image-route --purpose storyboard_sequence --layout grid_3x3 --semantics temporal_sequence
python -X utf8 tools/qms.py select --stage assets --model gpt-image --version gpt-image-2-2026-04-21 --platform openai-images-api --mode T2I --facets asset.turnaround,layout.three_view
```

image-route未给模型时只返回设计规范与适配待定状态；要编译执行契约需明确完整模型元组。用途不是版式。九宫格不自动代表九个连续镜头；人物表情板通常为 independent_collection。先明确每格表示时间、同刻视角还是独立合集，再按用途看图验收。

## 常见错误

- `No exact released model profile`：运行 profiles，选完整模型/版本/平台/模式；未知平台登记缺口，不换名硬套。
- `budget exceeded`：拆任务或镜头批次，不能以截断规范正文解决。
- `pending/local/no_ai`：读当前处置记录，保持限制；不能为了出包直接放行或刷新批准 SHA。
- `source hash drift`：保留原版本，重导入变更后的完整正文并重新复核。
- 输出已存在：选择新记录文件名，保留旧证据，不覆盖已发生的失败或通过记录。
