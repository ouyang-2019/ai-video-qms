---
id: "FR-IMAGE-JOB"
type: "concept"
title: "图像任务与生成交接记录模板"
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

# 图像任务与生成交接记录模板

模板复制为实例后保留模板ID与版本。空值代表未记录；不能预填执行成功。

| 字段 | 实际值 |
|---|---|
| job_id / project_id / asset_id / asset_revision | 待填 |
| model / model_version / platform / mode | 待填 |
| SOP ID及版本 / official_evidence_ids | 待填 |
| 资产用途 / 角色或场景设计基线 | 待填 |
| 输入图片路径、SHA、顺序、职责 | 待填；T2I填写不适用原因 |
| mask路径、SHA、与基底对齐检查 | INPAINT必填 |
| 完整prompt / prompt_sha256 | 待填 |
| 参数原文 / 参数校验结果 / 客户端版本 | 待填 |
| 授权来源 / 预算上限 / 隐私范围 | 待填 |
| request_status | planned / request_prepared / executed / failed |
| 请求时间 / 服务请求ID / 脱敏响应文件 | 未执行留空 |
| 输出文件 / SHA / 实际格式尺寸 | 未执行留空 |
| visual_status / inspector / inspection_record | not_checked / pass / fail |
| 前版job_id / 缺陷ID / 本轮修改 | 首版填不适用 |

状态规则：只有参数校验通过可为request_prepared；只有真实服务响应和产物关联可为executed；只有完整逐图观察及验收记录可为pass。失败响应及拒绝也留存，不删除旧轮次。单纯找到历史图片文件只能记artifact_found。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。
