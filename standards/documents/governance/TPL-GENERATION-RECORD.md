---
id: "TPL-GENERATION-RECORD"
type: "concept"
title: "视频生成批次追溯记录模板"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["SRC-INTERNAL-DESIGN"]
confidence: "medium"
review_status: "draft"
created: "2026-09-08"
updated: "2026-09-08"
privacy: "ai_allowed"
qms_level: 4
qms_kind: "template"
qms_version: "1.0.0"
qms_status: "released"
qms_verification: "structural"
---

# 视频生成批次追溯记录模板

- 记录ID／项目集镜／创建时间／操作者：
- 用户需求、剧本、资产、分镜版本：
- 系列／版本／平台／模式／确切模型或任务ID：
- 所用手册、程序、SOP、模板的ID、版本和hash：
- 原始意图／最终提示词／供应商实际请求（去除密钥）：
- 素材文件ID/hash及引用职责：
- 随机种子（若提供）／扩写工具／工作流与权重版本：
- generation_executed：false（真实提交成功后另建记录填写结果）
- 接口响应、任务ID、状态／成片路径/hash：
- 检验记录／失败与修复／supersedes：

已保存记录不原地覆盖。修改新建记录并引用旧ID；API成功、结构通过和视听通过分别填写。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
