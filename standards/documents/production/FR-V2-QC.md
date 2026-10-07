---
id: "FR-V2-QC"
type: "concept"
title: "逐镜验收与缺陷纠正记录"
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
qms_facets: ["quality.review", "continuity.state"]
---

# 逐镜验收与缺陷纠正记录

## 用法
一条缺陷一条记录，修前、修后与复验分别保留。模板不是验收报告；无实际素材时仅填写纸面检查结果。
## 可填写字段
- 记录ID、项目镜号、实际文件、提示词／资产／模型版本：____
- 检查层：剧本／文本／资产／视频／成片：____
- 目标与依据、实际现象、预期状态、时间区间：____
- 严重性：阻断／明显／轻微；理由：____
- 首个失效环节、原因假设、最小修改、修前路径：____
- 修后版本路径、同条件对照、原缺陷是否消失：____
- 前后镜身份、道具、方向、声桥和节奏复验：____
- 结论、未决项、接受例外、证据与检查人：____
## 填写示范
镜头4：杯子在B接触前悬浮，明显影响交接理解。修改共同接触与释放条件；复验接触全过程，并确认镜头5仍由B左手持杯。若尚未重生成，结论写“待复验”，不能填“已修复”。
## 判定
关闭记录必须有实际修后观察，且无新增相关缺陷；允许接受的瑕疵写清影响和理由。真实生成成功次数与尝试次数共同统计，纸面评分不得加入成功率。缺陷修复与素材发布各自留痕。


## 2.0.1 审计修订

登记细项 quality.inspect：检验和复核概念有交叠，不全局替换 quality.review。
