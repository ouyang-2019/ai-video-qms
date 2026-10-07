---
id: "SOP-H3-REF2VA"
type: "concept"
title: "H3 Ref2VA提示词编写SOP"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["H3-OFFICIAL-REF", "SRC-INTERNAL-DESIGN"]
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

# H3 Ref2VA提示词编写SOP

## 适用与输入
适用于h3 / prompt-only / Ref2VA。输入冻结分镜、时长目标、声音计划及本模式所需素材。来源为官方写作指南，实际上传/API字段另行适配。
## 操作
输入可为图、视频、音频组合。先辨认每项真实素材以及要保留/改变的属性；Subject是内容单元，Picture是画面锚点，Video是视频与时序，Audio是音频职责。分别说明身份、动作、空间或声音来源，不将全部素材写成相同“参考”。视频有音轨不代表自动引用声音。

正文依次为subject_definitions、summary、retention_analysis、detailed_description、overall_soundscape、non_diegetic_music。定义引用内容及角色，摘要说明目标，保留分析逐项说明保留、迁移或修改，详细描述按时间排列声画。章节写英文，原对白/歌词/场景文字保留。引用标签全段一致；说话人使用官方指南约定。
## 输出与检查
输出最终改写文本和独立参考映射。检查镜头可执行性、总时长、引用解析、素材职责、声源和首尾状态；检查未把写作章节当HTTP字段。素材未提供时给缺项清单，不能填写已完整引用。时长范围以当前固定指南为写作依据，平台是否接受必须单独核对。
## 常见失败及修复
身份漂移回查参考职责；动作跳变拆分动作路径；声音混乱明确说话人及画内/画外声；时间不够减少事件或拆段，保留不可删需求。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
