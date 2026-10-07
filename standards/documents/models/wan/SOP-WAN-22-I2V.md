---
id: "SOP-WAN-22-I2V"
type: "concept"
title: "Wan 2.2 open-source I2V准备SOP"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["WAN-OPEN-2.2", "SRC-INTERNAL-DESIGN"]
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

# Wan 2.2 open-source I2V准备SOP

## 适用与输入
仅适用于本文件登记版本、部署入口与I2V任务的提示词/请求准备，不能推广整个Wan系列。输入冻结镜头意图、时长目标、真实参考和部署信息。
## 步骤
1. 选择明确的I2V任务变体并提供首图。重点写动作和运镜，从图中状态发展；size语义按本地任务代码核对，不套云端resolution字段。
2. 共用镜头描述包含主体、动作、环境、镜头及风格，图像已有信息不重复矛盾改写。明确必要声画意图，未经对应任务核实的音频能力列为缺口。
3. 记录参考职责、顺序、文件hash和实际模型/任务名；固定代码/权重或云端模型/地域。使用提示词扩写时保存前后文本，检查新增事实。
4. 在具体部署文档中核对输入格式、数量、时长和请求参数。本SOP不提供未联调的执行命令，不将提示词推荐当硬性API契约。
5. 输出最终文字稿与独立请求准备表，逐项检查动作起止、空间、引用解析、未知字段。将格式检查和实际生成验收分开记录。
## 异常
不支持的任务变体停止路由；来源和当前部署不符则重新核对。随机生成失败不能只堆叠负面形容词，应回查素材、动作和模式后最小修复。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
