---
id: "SOP-H3-L2VA"
type: "concept"
title: "H3 L2VA提示词编写SOP"
primary_domain: "图片和视频生成"
tags: ["提示词", "质量管理"]
sources: ["H3-OFFICIAL-BASE", "SRC-INTERNAL-DESIGN"]
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

# H3 L2VA提示词编写SOP

## 适用与输入
适用于h3 / prompt-only / L2VA。输入冻结分镜、时长目标、声音计划及本模式所需素材。来源为官方写作指南，实际上传/API字段另行适配。
## 操作
需要已提供尾帧。前缀对齐Picture 1与结束时刻；从合理前态逐步收敛到尾帧构图和动作状态。不要把尾帧误当首帧，结尾不可在到达锚点后再启动新动作。


基础模式正文依次为integrated_multimodal_description、overall_soundscape、non_diegetic_music。叙述按播放顺序组织构图、主体、环境、动作、摄影与画内声音，后续切镜标记使用官方指南的时序格式。环境声与动作声区别于观众听到的配乐；没有音乐时明确写无配乐。各段镜头和总时长一致。
改写章节用英文，对白/歌词/可见文字保持原语言。先列镜头意图与素材职责，后编写最终文本。只说具体可观察动作，不用形容词堆叠代替动作或空间。引用标签和时间点在全文保持同义。帧对齐句沿用固定版本的base-en.txt，不凭记忆改标签或段序。

## 输出与检查
输出最终改写文本和独立参考映射。检查镜头可执行性、总时长、引用解析、素材职责、声源和首尾状态；检查未把写作章节当HTTP字段。素材未提供时给缺项清单，不能填写已完整引用。时长范围以当前固定指南为写作依据，平台是否接受必须单独核对。
## 常见失败及修复
身份漂移回查参考职责；动作跳变拆分动作路径；声音混乱明确说话人及画内/画外声；时间不够减少事件或拆段，保留不可删需求。

---
内部受控试运行文件；验证范围为规范整理和结构审查，未进行视频生成实测。
