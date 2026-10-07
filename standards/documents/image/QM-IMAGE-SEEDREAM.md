---
id: "QM-IMAGE-SEEDREAM"
type: "concept"
title: "Seedream 4.5 BytePlus 图像资产系列总规范"
primary_domain: "图片和视频生成"
tags: ["图像适配", "质量管理"]
sources: ["IMG-SEEDREAM-ARK-20260909"]
review_status: "draft"
created: "2026-09-09"
updated: "2026-09-09"
privacy: "ai_allowed"
qms_level: 1
qms_kind: "manual"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# Seedream 4.5 BytePlus 图像资产系列总规范

## 范围与平台
受控元组为 seedream / seedream-4-5-251128 / byteplus-modelark / T2I、EDIT、BATCH。本地RunningHub存在seedream-v4.5及v5端点，但这不能证明BytePlus账号可用，也不能证明其字段兼容。本规范可用于请求准备；账号与客户端接入状态单独登记。

## 官方边界
参数见IMG-SEEDREAM-ARK-20260909与image-profiles.json。单图和组图由sequential_image_generation区分，BATCH不是多次独立请求的别名。4.5输出JPEG，不继承5.0的PNG选项；组图数量是上限意图，收到数量须实测核对。

## 参考职责
逐图说明身份、服装、场景或构图职责，避免多个参考同时争夺角色身份。图片序号必须与实际输入顺序一致。参考一致性和组图连贯性是需验证的能力，不能将官方营销描述写成每次必定成功。

## 不可移植与变更
不沿用Seedance视频参数，不把RunningHub端点名替换成BytePlus model字段。版本升级、平台迁移、输入类型或输出格式变化都建立独立试验；不做无声回退。URL仅作临时交付地址，实际执行后应及时留存文件及校验值。

## 放行
PR-IMAGE-CONTRACT约束发布前的预检、实际响应、逐图验收和返工。若当前只有提示词，不填写task_id、输出SHA或视觉通过。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。
