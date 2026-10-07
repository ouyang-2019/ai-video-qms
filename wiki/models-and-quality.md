# 版本模型适配

模型适配必须使用完整元组：模型族、版本、平台、模式。只写“H3”“Seedance”或“Wan”不足以证明字段、参考图能力、时长或平台参数可用。

## 视频模型

- H3：读 `QM-H3`、`PR-H3` 和对应 `SOP-H3-*` / `TPL-H3-*`。公开版的 prompt-only 模式是文本模板，不是任何第三方平台API字段。
- Seedance：读 `QM-SEEDANCE`、`PR-SEEDANCE` 和对应2.0/2.5、T2V/I2V/REF模板。BytePlus平台规则不自动适用于其他入口。
- Wan：区分开源与云平台。读 `QM-WAN`、`PR-WAN-OPEN` 或 `PR-WAN-CLOUD`，再选2.2、2.6、3.0及T2V/I2V/REF/EDIT/EXTEND模板。

## 图像模型

图像合同属于 `assets` 阶段。GPT Image和Seedream的端点、编辑能力、输入格式和验收记录互不替代。图片生成结果没有经过视觉审核前，不能称为最高质量或默认推荐。

## 验收边界

`released` 表示公开版结构和内容经过内部整理，不表示真实API已执行或画面质量已通过。模型编译通过、平台下载成功、人工视听通过和交付通过是四个不同结论。
