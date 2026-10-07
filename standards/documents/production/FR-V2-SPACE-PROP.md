---
id: "FR-V2-SPACE-PROP"
type: "concept"
title: "站位轴线与道具状态账本"
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
qms_facets: ["blocking.position", "props.state"]
---

# 站位轴线与道具状态账本

## 用法
对同一连续场景维护一份账本，每次镜头或道具事件新增记录，不覆盖前态。身体左右、世界方位和屏幕左右分栏。
## 可填写字段
- 场景ID、平面图版本、门桌窗等地标：____
- 镜头ID、摄影机位置、主要轴线、摄影机侧：____
- 角色ID、世界起点、朝向、屏幕位置、目光目标：____
- 路径、启动刺激、遮挡、停点、重心与下一动作：____
- 道具实例ID、尺寸材质、持有者、左右手、朝向：____
- 交接：递出部位、接收部位、共同接触、释放条件：____
- 事件后位置、开合、液位、损伤、污渍与残留：____
- 下镜继承、时间省略理由、有意越轴及交代方式：____
## 填写示范
杯P01在A右手，A在门侧，B坐桌边。A将杯柄朝B，B左手握柄后A松开；终态P01由B左手持有，杯口仍朝上。下一镜因反打使B移到屏幕左侧，世界位置不变。
## 判定
检查无接触换手、凭空复制、门桌位置漂移和无法通过的路线。用平面图复述人物和物件全过程；交接被省略时必须存在可理解的时间或声音线索。未观察实片时仅标状态设计闭合，不记为接触已实现。


## 2.0.1 审计修订

登记细项 blocking.space：位置、路径和世界空间交接；原 blocking.position 保留。
