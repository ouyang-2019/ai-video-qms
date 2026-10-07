---
id: "SOP-IMAGE-SEEDREAM"
type: "concept"
title: "Seedream 4.5 文生图、参考图与组图SOP"
primary_domain: "图片和视频生成"
tags: ["图像适配", "质量管理"]
sources: ["IMG-SEEDREAM-ARK-20260909"]
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

# Seedream 4.5 文生图、参考图与组图SOP

## 适用与输入
仅BytePlus ModelArk固定4.5元组。T2I无参考图；EDIT有参考图且单图输出；BATCH明确目标张数及每张职责，可有或无参考图。RunningHub同名模型需另建平台适配才能执行。

## 操作
写统一身份与风格基线，再逐张列镜头用途。场景参考图将门、窗、桌、关键道具位置明确固定；改变视角时说明相机从哪一侧观察，不同时重排场景。
参数model=seedream-4-5-251128，size选2K或4K；本SOP使用2K。单图sequential_image_generation=disabled；组图设auto并填写sequential_image_generation_options.max_images。参考图顺序与prompt中的图1、图2一致，数量同时满足参考上限及总图数约束。

## 提示词例
“生成一组3张同一客厅的场景设定图：第1张从南侧看北墙门窗；第2张从东侧看西侧书柜；第3张俯视平面布局。蓝沙发位于房间中心偏西，木桌在其东侧，北墙门在右、窗在左；材质、昼间光照和物件数量保持一致。”此例是设计要求，不能被记录为已生成成功。

## 检查
预检每张参考的格式、尺寸、体积；不要为4.5传5.0的PNG输出选项。真正执行后检查返回错误、实际数量、JPEG文件可解码性与每幅的空间关系。URL应在有效期内留存原文件及SHA。

## 返工与输出
空间漂移先固定一个合格主视图后改成参考编辑；张数不足则记录缺图并按缺项补生成，不伪造组图成功。输出逐图清单、参考映射、实际响应证据及四级验收表。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。
