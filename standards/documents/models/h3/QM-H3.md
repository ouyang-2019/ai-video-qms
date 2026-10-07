---
id: "QM-H3"
type: "concept"
title: "MiniMax H3系列总规范"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["H3-OFFICIAL-SKILL", "SRC-INTERNAL-DESIGN"]
confidence: "medium"
review_status: "draft"
created: "2026-09-08"
updated: "2026-09-08"
privacy: "ai_allowed"
qms_level: 1
qms_kind: "manual"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# MiniMax H3系列总规范

本系列以官方h3-prompt-writing固定采集版本为提示词改写依据。共用故事、资产内容、动作和声画意图；专用部分为五种模式、字段顺序、参考标签、帧对齐和英文改写正文。对白、歌词及画面文字保留原语言。首尾帧倾向连续单镜头属于建议，不改成模型禁止多镜头。
本版规范入口名prompt-only，表示只编制提示词；不具备已验证的API transport。改写章节不是HTTP字段。请求时长、上传限制和参数需实际入口文档及联调，不能套用社区或其他海螺版本。
基础模式与全参考各有格式；不得把Seedance的@图或Wan云端角色标签直接搬入H3。引用必须对应真实已提供资产；缺图/音/视频时列缺项，不伪称已观察。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
