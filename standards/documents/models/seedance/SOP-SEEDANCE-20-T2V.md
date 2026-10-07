---
id: "SOP-SEEDANCE-20-T2V"
type: "concept"
title: "Seedance 2.0 LAS T2V提示词准备SOP"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["SEEDANCE-BYTEPLUS-LAS", "SRC-INTERNAL-DESIGN"]
confidence: "medium"
review_status: "draft"
created: "2026-09-08"
updated: "2026-09-08"
privacy: "ai_allowed"
qms_level: 3
qms_kind: "sop"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# Seedance 2.0 LAS T2V提示词准备SOP

## 适用与输入
仅适用于Seedance 2.0、BytePlus LAS入口的T2V准备。本SOP为内部编制方法，依据该入口官方文档，不声称已取得官方sd2-pe完整Skill或完成API联调。输入需分镜、实际素材和声音目标。
## 步骤
1. 固定完整模型ID及版本，核对任务模式。从文字建立镜头主体、场景、动作起止和镜头运动。没有媒体时不引用不存在的编号。
2. 写清主体→可见动作→场景空间→摄影和视觉→声音意图，按时序描述，保留起止状态与必要对白。此顺序是内部工作方法，不声明为官方强制标题。
3. 准备素材映射表：文件ID/hash、媒体类型、角色用途、实际上传标识。引用只有在入口能解析时才进入最终稿；不要照搬H3的六段标签。
4. 按LAS当前对应模型行核对时长、媒体数量、尺寸和素材条件。旧版/其他平台限额不可代用；需要特定素材登记机制时按入口要求处理。
5. 生成独立提示词和请求准备记录；不把说明文字混入参数值。检查动作密度、声源、引用及切点，保留尚未核对字段。
## 输出和失败处理
输出可审提示词、素材映射和参数核对清单。缺素材、未知role或模型ID不一致时停止交接；时间不足时拆镜并保存角色/声音连续性。未实际提交时记录generation_executed:false。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
