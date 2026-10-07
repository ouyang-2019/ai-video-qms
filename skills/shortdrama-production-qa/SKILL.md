---
name: shortdrama-production-qa
description: 使用公开版AI视频QMS管理短剧从剧本、资产、计时分镜、模型交接、视听审核、最小返修到归档记录的生产闭环。
metadata:
  version: "0.1.0-public"
---

# 短剧制作与审核闭环

本技能把短剧/漫剧制作拆成可追溯的质量流程。它不绑定任何私人项目、角色、工作流ID或付费平台；公开版只负责文本设计、上下文组装、结构检查、审核方法和交接记录。

## 制作顺序

1. 冻结目标：项目名、集/段/镜号、剧本版本、交付时长、画幅、预算、允许改动、模型元组和已批准资产。
2. 剧本先成立：故事动机、选择、冲突、后果、笑点/情绪兑现和对白归属通过后，再进入分镜或生成提示词。
3. 资产先批准：角色、服装、道具、场景、站位、声音身份分别记录。参考图要写清职责和不可继承内容。
4. 按时间编排：每镜写起始状态、动作窗口、对白/呼吸/接触、结束状态和下一镜承接。
5. 14工种可观察设计：编剧导演、表演/微表情、站位、道具、服装、环境、摄影、灯光、动作、特效、语音、声音、剪辑、连续性都要有设计或明确不适用理由。写作、摄影、剪辑、连续性必须显式设计。
6. 模型编译：用 `scripts/run.py bundle` 按模型元组加载模板。H3、Seedance、Wan和图像端点各自独立，不互相猜字段。
7. 生成交接和QA：公开版只生成交接包；真实媒体通过后才能记录平台执行和视听验收。
8. 最小修复与归档：缺陷版、候选、返修、母版和交付版分开保存；没有新输出和复测，失败项不能改成通过。

## 运行辅助

```bash
python scripts/run.py shot-check --plan shot-plan.json
python scripts/run.py shot-bundle --plan shot-plan.json --out build/shot-bundle --max-chars 240000
python scripts/run.py bundle --stage review --facets performance.microexpression,continuity.state --target remote
```

## 必读引用

- 设计生产镜头时，读 [references/production-loop.md](references/production-loop.md)。
- 微表情、倾听、静默反应或固定半身互动，调用 `$shortdrama-micro-performance`。
- 需要跨阶段查找规范和来源，调用 `$ai-video-fullchain`；只选规范和模板时调用 `$ai-video-qms`。
