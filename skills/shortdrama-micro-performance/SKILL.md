---
name: shortdrama-micro-performance
description: 在公开版AI视频QMS下，为短剧镜头设计可观察的微表情、静默反应、视线、呼吸、肢体语言、对白节奏和情绪节拍。
metadata:
  version: "0.1.0-public"
---

# 情境驱动微表演

本技能把抽象情绪改写成镜头可见的身体、眼神、面部、呼吸、动作和余韵。它适用于微表情、静默反应、倾听镜、家庭Q版、固定半身互动、对白中的潜台词，以及表演审核。

## 设计方法

1. 先保留已批准身份、服装、比例、机位、光线、道具和对白。表演只服务当前镜头目标，不改写剧情事实。
2. 写清角色此刻目标、阻碍、收到的信息和初始基线。反应不能早于刺激发生。
3. 按“触发 → 第一反应 → 眼神神态 → 呼吸/身体 → 台词或无对白 → 余韵”组织。步骤可以重叠，但因果不能跳。
4. 每个行为写成可观察信号：视线落点、眼睑/眉/嘴角幅度、头颈和肩背支撑、手部接触、重心、呼吸节奏、停顿位置。不要只写“悲伤、开心、震惊”。
5. 给出时间窗口，避开台词口型冲突。说话者、听者、画外声、旁白和声线分别标注。
6. 风格适配：Q版保留可读的大形变和节奏，不添加写实皱纹血管；固定半身不擅自推镜，手部表达也要写起势、接触和终态。
7. 审核时只评估已观察版本；候选配方未经实片验证只能标 `media_validation: not_run`。

## 运行辅助

```bash
python scripts/run.py bundle --stage craft --facets performance.microexpression,performance.eyes,performance.breath --target remote
python scripts/run.py context --task micro-performance --query "强忍委屈的静默反应" --evidence-ids SRC-xxxx
```

## 必读引用

- 需要写镜头表演时，读 [references/micro-performance.md](references/micro-performance.md)。
- 需要完整生产上下文时，调用 `$shortdrama-production-qa`。
