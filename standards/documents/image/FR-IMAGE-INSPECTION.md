---
id: "FR-IMAGE-INSPECTION"
type: "concept"
title: "图像资产逐项验收与返工记录模板"
primary_domain: "图片和视频生成"
tags: ["图像适配", "质量管理"]
sources: ["SRC-INTERNAL-DESIGN"]
review_status: "draft"
created: "2026-09-09"
updated: "2026-09-09"
privacy: "ai_allowed"
qms_level: 4
qms_kind: "template"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# 图像资产逐项验收与返工记录模板

## 追溯信息
job_id、asset_id、输出SHA、基线版本、检查日期与检查者：待填。每一项结果为pass/fail/not_applicable；不适用必须写原因，未观察为not_checked。

| 验收维度 | 观察证据 | 结果 | 缺陷与修复 |
|---|---|---|---|
| 身份：脸型、五官、发际线、年龄感 | 待填具体部位或局部坐标 | not_checked | 待填 |
| 三视图方向及同尺度、基线 | 待填各栏方向与差异 | not_checked | 待填 |
| 服饰道具的左右、数量、接缝、挂接点 | 待填 | not_checked | 待填 |
| 肢体、手部、遮挡与接触 | 待填 | not_checked | 待填 |
| 表情可见性与姿态：目光、肩颈、重心 | 待填 | not_checked | 待填 |
| 场景几何：门窗、地标、视角和轴线 | 待填 | not_checked | 待填 |
| 光向、材质、颜色与其他资产一致性 | 待填 | not_checked | 待填 |
| 改图保护区及边缘污染 | 对照输入图和遮罩 | not_checked | 待填 |
| 文字逐字比对、留白与分镜裁切适用性 | 待填 | not_checked | 待填 |
| 文件可解码、实测尺寸、格式和SHA | 待填 | not_checked | 待填 |

## 缺陷闭环
每条缺陷填写defect_id、严重度、预期/实见、定位证据、根因假设、修改动作、父输出SHA、新输出SHA、复验结论。关键身份/几何问题未关闭不可放行为视频参考；轻微装饰缺陷的例外须记录具体用途及授权，不写笼统“可用”。

## 交付
记录approved_for（角色参考/首帧/尾帧/场景/仅探索）、审批日期、已关闭缺陷与遗留项。一次预览不等于整组验收；逐图完成后才允许组图整体通过。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。
