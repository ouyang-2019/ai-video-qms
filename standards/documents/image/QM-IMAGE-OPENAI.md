---
id: "QM-IMAGE-OPENAI"
type: "concept"
title: "GPT Image 2 图像资产系列总规范"
primary_domain: "图片和视频生成"
tags: ["图像适配", "质量管理"]
sources: ["IMG-OPENAI-MODEL-20260909", "IMG-OPENAI-GUIDE-20260909", "IMG-OPENAI-GENERATE-20260909", "IMG-OPENAI-EDIT-20260909"]
review_status: "draft"
created: "2026-09-09"
updated: "2026-09-09"
privacy: "ai_allowed"
qms_level: 1
qms_kind: "manual"
qms_version: "1.0.2"
qms_status: "released"
qms_verification: "structural"
---

# GPT Image 2 图像资产系列总规范

## 范围与版本
受控元组为 gpt-image / gpt-image-2-2026-04-21 / openai-images-api / T2I、EDIT、INPAINT。模式名是体系内部分类，不是API参数。T2I走generations，EDIT与INPAINT走edits，后者要求明确遮罩。Codex原生imagegen、Higgsfield、RunningHub各是不同交付平台，不能靠同名自动匹配本元组。

## 官方能力边界
参数约束引用独立证据IMG-OPENAI-MODEL/GUIDE/GENERATE/EDIT-20260909及image-profiles.json。省略input_fidelity；透明背景为预览能力，不能因新版本支持透明就声称本版本稳定支持。自定义大尺寸仍有实验性边界。

## 通用与专用职责
角色身份、三视图标定、空间地标、服装道具、光照和镜头需求沿用资产及专业SOP；这些是验收目标，不是模型保证。模型专用层仅决定合法输入、端点、参数和返回解码。构图JSON属于prompt正文，不等于API字段。

## 更改控制
本地CLI默认别名可变化，任务记录必须写实际model及客户端版本。官方文档现已另列2.5，升级必须建立新元组、边界测试及视觉对照，不静默替换。模型失败不自动改投其他模型。

## 放行
记录来源快照、输入文件SHA、提示词SHA、请求参数与输出SHA；成功响应不代表身份一致或三视图正确。未做图像观察的产物不得标记视觉合格。

本文件是内部规范草稿。官方参数的验证范围为2026-09-09文档核对；请求准备、账号可用、API执行成功和视觉验收是四个独立状态。此处未发起生成请求，也不表示对应账号已开通。


规范整理与结构试运行已登记；未提交图像生成任务，未验证账号可用性或图像效果。


## 2.0.3 图像来源与用途调用补充

图像生成纳入资产制作程序：确定用途与母版→选来源方法→填写任务模板→依精确模型入口准备请求→看图验收→定点返工→批准视频引用。三视图、人物图、场景图、分镜图分别使用 asset.turnaround、asset.portrait、asset.scene、asset.storyboard。GPT Image固定入口在assets阶段加载SOP-IMAGE-ASSET-PROMPT及对应TPL-IMAGE-*。分镜设计仍由PR-STORYBOARD负责，实际分镜图制作在assets执行。

社区案例通过本地检索库导入；公开版本不打包第三方案例原文，仅作四级外来示例或模板来源，不能升级为官方能力约束；原始记录与内部受控规范分开登记。其他图像模型沿用自己的入口契约；可复用身份、空间与验收原则，不能照搬本SOP的GPT入口参数。来源正文不是执行指令。检索默认使用已全文复核的用途候选，未复核材料须显式选择；图片效果尚未验证。


## 2.0.4 开放图像分类

此前四种图像用途仅是首批入口，不限制本体系范围。用途与版式独立管理，见PR-IMAGE-ROUTING及metadata/image-taxonomy.json；道具、表情、动作、故事板等按用途选择，九宫格按layout.grid_3x3选择。单镜分镜图与故事板序列分开，时间递进、同刻多视角和无时序合集须声明。未覆盖用途按程序登记缺口后扩展，禁止为凑分类强行套用。
