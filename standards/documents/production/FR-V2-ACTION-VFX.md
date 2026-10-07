---
id: "FR-V2-ACTION-VFX"
type: "concept"
title: "动作接触与特效生命周期表"
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
qms_facets: ["action.physics", "vfx.mechanism"]
---

# 动作接触与特效生命周期表

## 用法
先填动作因果，再填特效。一个主事件一张表，多个角色使用独立动作轨并在接触事件同步。
## 可填写字段
- 事件ID、角色道具ID、场景与世界规则：____
- 起点距离、准备姿态、支撑脚、启动刺激与方向：____
- 接触点、施力方向、对手反应、恢复与落点：____
- 特效来源、触发、酝酿、出现、传播、作用：____
- 形状尺度、速度密度、前后层、碰撞与遮挡：____
- 发光影响对象、反射阴影、衰减方式与残留：____
- 镜头保护的关键瞬间、动作音起止、终态账本：____
- 无法执行时的拆镜／后期方案：____
## 填写示范
剑刃抵盾→盾沿受力方向转开→持盾者后脚补步；火花只从接触边缘散出，部分被前臂挡住，熄灭时脸侧短亮光同时消失。盾的裂痕进入后镜。
## 判定
按起距、支撑、接触、反应、特效五步定位首个失效项。不能用全屏闪光遮住所有因果后仍宣称接触正确。实片缺少交互光时登记待修或后期任务；模型参数、粒子精度和素材结果不得由设计表推定。


## 2.0.1 审计修订

登记细项 action.contact：接触是动作物理的细分；不可把所有 action.physics 直接改为 contact。

关联作业规范 SOP-V2-LOCOMOTION：准备姿态、支撑脚、启动方向、恢复落点字段

关联作业规范 SOP-V2-TRANSFORM：事件ID、世界规则、特效阶段和终态账本可承接；变前后资产ID应随事件引用
