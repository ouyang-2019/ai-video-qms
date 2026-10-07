---
id: "FR-V2-AUDIO-EDIT"
type: "concept"
title: "对白语气声音与剪辑时间表"
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
qms_facets: ["audio.voice", "audio.sfx", "audio.music", "edit.rhythm"]
---

# 对白语气声音与剪辑时间表

## 用法
使用同一项目时间线登记声画事件；对白、拟音、环境和音乐分轨，最后检查组合。生成原声与后期添加分别记录。
## 可填写字段
- 记录ID、镜头ID、时间线版本、台词版本：____
- 说话者、听者、固定声线、语言、准确台词：____
- 起声、重音词、停顿原因、语速变化、句尾：____
- 呼吸区间、口型可见性、头部动作、实读时长：____
- 拟音声源、材质、事件起止、画内外、远近遮挡：____
- 环境底声、音乐目的、进入发展退出、对白避让：____
- 切点目的、动作承接、声桥、转场含义：____
- 真实音轨与素材来源、试听结果、未决事项：____
## 填写示范
“钥匙”两字略重，停一下后轻声说“留给你”；钥匙碰木桌的短声对应接触，窗外雨声跨切不断。切到听者停止翻页的手，音乐暂不进入。
## 判定
先检台词可懂和说话者，再检接触时序、空间与跨切，最后检配乐层次。没有试听只能标设计完成。台词超时优先删改或拆镜；拒绝用全局加速、反复开头音乐或不明震撼音效掩盖结构问题。


## 2.0.1 审计修订

登记细项 audio.prosody：韵律是声线SOP的一部分，不等同所有 audio.voice。

登记细项 audio.foley：拟音是音效子类，audio.sfx 包括其他音效，不能等同。
