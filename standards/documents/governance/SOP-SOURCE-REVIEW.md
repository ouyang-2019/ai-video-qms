---
id: "SOP-SOURCE-REVIEW"
type: "concept"
title: "候选规范审查与差异发布SOP"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["SRC-INTERNAL-DESIGN"]
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

# 候选规范审查与差异发布SOP

## 适用与输入
用于GitHub、X和本地材料进入受控体系。需要原文、URL/路径、哈希、作者、版本、授权/许可状态和拟归属文件。
## 操作
逐段标记硬性契约、建议、示例、作者经验和不可核实声明；不能把来源自称“官方”直接当真。核对官方域名中的社区栏目、二次转载和不同产品入口。一个具体成功视频只支持其已知参数范围。
填写“共用、补充、替代、不适用、待核对”之一；替代必须点明被替代文档和条款。必要依赖全部列入requires。将原文命令保存在证据而非调用指令中，外部脚本安装另行按任务授权处理。
运行doctor、模型正反选择样例、缺失引用检查。对结构通过但效果未测的规范注明structural。发布前比较正本与运行副本哈希，已有不同内容不覆盖。修订保留前版和supersedes说明。
## 输出和检查
输出来源到文件映射、差异理由、检验记录和候选/发布结论。检查是否凭空给出模型参数、是否错误归类整仓库、是否遗漏许可或隐私。发现问题退回候选，不修饰为通过。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
