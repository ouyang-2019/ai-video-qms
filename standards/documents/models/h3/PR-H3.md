---
id: "PR-H3"
type: "concept"
title: "H3视频提示词准备与生成交接程序"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["H3-OFFICIAL-SKILL", "SRC-INTERNAL-DESIGN"]
confidence: "medium"
review_status: "draft"
created: "2026-09-08"
updated: "2026-09-08"
privacy: "ai_allowed"
qms_level: 2
qms_kind: "procedure"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# H3视频提示词准备与生成交接程序

## 输入与责任
输入为已审剧本/分镜、镜头中间描述、参考资产清单、时长目标及模型入口。适配者保证语义不失真，检查者核对模式和引用；提交者另行确认实际服务配置。
## 步骤
1. 确认输入齐备；未知版本、媒体缺失、未授权素材不继续伪造请求。
2. 选择T2VA/I2VA/FL2VA/L2VA/Ref2VA；基础与全参考用各自模板。检查英文改写正文与保留原语言的对白。
3. 从登记册选择对应SOP和模板，先列参考职责，再表达动作、镜头和声音；保留剧本事实及起止状态。
4. 验证时间锚点、引用一致性、字段及素材存在性。专用编译只负责准备文件，不代表API执行。
5. 输出改写稿、素材映射、参数待核对项和规范包哈希。实际生成后按PR-QC验收，保存任务ID、结果文件和偏差。
## 输出、交接与异常
输出包括提示词、请求准备表、缺项和检查记录。接收者能追溯需求、资产、规范及来源版本才可交接。超出能力时重新拆镜或换经过核对的profile，不能静默删需求。失败只修改定位到的环节并保留旧记录。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
