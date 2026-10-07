---
name: ai-video-fullchain
description: 引导AI视频任务使用QMS、Wiki导航和RAG证据，为当前写作或生产步骤检索合适的Skill、SOP、模板和来源包。
metadata:
  version: "0.1.0-public"
---

# AI视频全链路开发

本技能指导模型使用质量体系、Wiki和RAG，而不是把所有资料一次性塞进上下文。适用于从剧本、角色、场景、道具、故事板、镜头提示词、模型编译、审核返修到归档的全链路提示词开发。

核心模式：用户任务 → QMS选阶段和facet → Wiki理解方法关系 → RAG取原文证据 → 加载必要Skill/SOP/模板 → 写出当前产物 → 按验收边界复核。

## 工作方式

1. 识别当前交付物：给大模型的流程指令、给图像模型的静帧提示词、给视频模型的时间化镜头提示词、审核清单或返修记录。只处理本轮需要的产物。
2. 用 `scripts/run.py wiki --task NAME` 查看任务导航。可用任务见 `wiki/index.json`：`script`、`adaptation`、`dialogue`、`storyboard`、`micro-performance`、`assets`、`video`、`review`。
3. 用 `context --task NAME --query TEXT --evidence-ids CSV` 或 `search` 缩小来源范围。检索命中只是候选；需要使用时必须 `get` 或 `pack` 读取正文，并保留 ID、SHA、采用方式和未采用原因。
4. 写作时把用户事实、受控规范、来源技法、模型元组和缺口分开。不要继承案例中的人物、品牌、镜头时长、平台参数或本地路径。
5. 完成后对照对应 Wiki 页和 QMS bundle 检查：叙事是否成立，资产是否可识别，14个工种是否覆盖到可观察层，模型字段是否真实，审核结论是否只覆盖已观察版本。

## 必读引用

- 需要全流程顺序时，读 [references/fullchain-workflow.md](references/fullchain-workflow.md)。
- 需要确定Skill组合时，用 `python scripts/run.py wiki --task NAME` 从已绑定仓库读取 `wiki/index.json` 和对应页面；不要依赖安装目录中的相对链接。
- 需要生产闭环和媒体审核时，调用 `$shortdrama-production-qa`；需要微表情和静默反应时，调用 `$shortdrama-micro-performance`。
