---
id: "SOP-IMAGE-OPENAI-EDIT"
type: "concept"
title: "GPT Image 2 参考改图与局部修复SOP"
primary_domain: "图片和视频生成"
tags: ["图像适配", "质量管理"]
sources: ["IMG-OPENAI-MODEL-20260909", "IMG-OPENAI-GUIDE-20260909", "IMG-OPENAI-GENERATE-20260909", "IMG-OPENAI-EDIT-20260909"]
review_status: "draft"
created: "2026-09-09"
updated: "2026-09-09"
privacy: "ai_allowed"
qms_level: 3
qms_kind: "sop"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# GPT Image 2 参考改图与局部修复SOP

## 适用与输入
EDIT或INPAINT；必须实际读取输入图并登记SHA。指定基底图、身份参考、服装参考各自职责。INPAINT还需明确遮罩及待改区域，不能用“改图”一词猜测局部范围。

## 操作
1. 写“保留项/改动项”：保留脸型、发型、相机位置、背景地标；仅改变外套或指定局部。
2. 图片序号按请求顺序固定。优先使用最少必要参考；若脸和服装来自不同图，明确图1锁身份、图2仅供服装。
3. 遮罩应与基底图空间对齐，预览其透明区与受保护区；检查尺寸、通道和边缘。平台字段不同不能自动改名移植。
4. 用edits端点，省略input_fidelity。当前官方API另有JSON images引用结构；本地CLI可能使用multipart image，须查看实际客户端实现并记录协议，不能把二者字段混拼。

## 提示词例
“以图1为基底，保持角色脸型、发际线、手的位置与镜头构图；只将外套替换为图2的深蓝短夹克，保留原背景和光线方向。图2不提供身份或姿态。”

## 检验与修复
对照原图查看保护区域是否变化、边缘是否出现光晕、服饰遮挡关系是否正确。遮罩是引导而非逐像素保护承诺；保护区改变也应记缺陷。每轮仅修必要缺陷，先修身份再修装饰，保存父子输出关联。

## 输出
参考职责表、脱敏请求、实际输出及FR-IMAGE-INSPECTION。未上传或未响应时只保留准备状态。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。
