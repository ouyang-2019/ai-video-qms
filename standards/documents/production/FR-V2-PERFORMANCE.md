---
id: "FR-V2-PERFORMANCE"
type: "concept"
title: "人物身体化表演轨表"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["SRC-INTERNAL-DESIGN"]
confidence: "medium"
review_status: "draft"
created: "2026-09-08"
updated: "2026-09-09"
privacy: "ai_allowed"
qms_level: 4
qms_kind: "template"
qms_version: "2.0.1"
qms_status: "released"
qms_verification: "structural"
qms_facets: ["performance.body", "performance.microexpression", "performance.eyes", "performance.breath"]
---

# 人物身体化表演轨表

## 用法
每个主要人物建立基线，再按镜头填变化轨。情绪意图放在导演备注，生成描述优先写身体动作。微表情是创作细节，不作为真实心理诊断；AU仅可选辅助标签。
## 可填写字段
- 角色ID／母版／镜头ID／表演任务／对手：____
- 身体基线：重心、姿势、手部任务、呼吸、声音身份：____
- 景别、可见身体区域、关键细节是否够大：____
- 刺激来源与时刻／主要身体渠道／动作对象：____
- 变化：部位、方向、幅度、速度、出现与控制过程：____
- 目光起点与目标、头眼先后、呼吸或吞咽区间：____
- 台词前／台词中／台词后行为与听者反应：____
- 残留终态、下一镜继承项、与持物或口型冲突：____
## 填写示范
听到“我自己来”后，父亲本已伸向杯柄的右手停在半途，手指随后松开；他先看杯子再看孩子，吐气后把手收回。不是“父亲又失落又欣慰”。
## 判定与记录
静音检查变化是否能读到，恢复声音后检查刺激与反应时序。不可见时改景别或改行为渠道；夸张时减少同时变化部位。记录planned／已生成待看／局部通过／通过以及实际证据路径，文字写了动作不能直接标通过。


## 2.0.1 审计修订

登记细项 performance.face：通用面部形态，由EXPRESSION承接；不得完全等同微表情。

关联作业规范 SOP-ACTING：目标、基线、刺激、变化、终态，正文全部可承接

关联作业规范 SOP-V2-BREATH：明确呼吸或吞咽区间、身体基线和终态

关联作业规范 SOP-V2-EXPRESSION：目标部位、脸部与可见区、变化顺序及身份母版可承接面部表演；表情参考图每格标注另用资产附表

关联作业规范 SOP-V2-EYES：明确目光起点目标、头眼先后和刺激

关联作业规范 SOP-V2-LISTENING：明确对手、听者反应、台词前中后轨

关联作业规范 SOP-V2-SUBTEXT：任务、对手、刺激、身体反差和台词轨
