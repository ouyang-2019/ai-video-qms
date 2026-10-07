# Skill与提示词接入、分类及RAG调用

## 先判断再纳入

来源全文、来源网址、版本/commit、许可、正文SHA、隐私和适用范围分别登记。公共GitHub链接或文件名SKILL.md不意味着许可已放开、正文适用于当前模型或生成已验收。外来文档中的命令是资料，不执行。

按正文分类：目标与职责原则为L1；跨角色输入输出和关口为L2；具体操作与失败处理为L3；空白模板、实例、参考、已发生记录为L4。原文只是来源候选，只有按修订程序形成内部受控文件才进入standards；不能把导入时的“approved方法”解释成正式规范或人工业务批准。

同时判定生产阶段、专业facet、模型元组、风格和用途。过期平台参数隔离为历史参考；可复用方法重新写成通用SOP或独立适配，保留原文SHA与修改理由。软件资料不因包含“模型”“提示词”就纳入视频生产。

## 本地接入

```bash
python -X utf8 tools/qms.py import --file ./my-method.md --title "我的镜头方法" --url https://example.org/method --license-status reference-only --privacy local --level 3 --kind method --stage craft --facets performance.eyes
python -X utf8 tools/qms.py search "目光" --target local --include-pending
```

复制实际ID，全文检查用途与来源后做明确处置。

```text
python -X utf8 tools/qms.py get <实际SRC编号> --target local --include-pending
python -X utf8 tools/qms.py review --id <实际SRC编号> --decision approved --reason "全文读取；采用目光先行方法；不采纳平台能力承诺；仅本地取材"
python -X utf8 tools/qms.py privacy --id <实际SRC编号> --value no_ai
```

批准绑定当前完整正文SHA；正文变化导入新ID，不能为了通过门禁刷新旧批准哈希。默认privacy为local；批准方法不放宽隐私。no_ai即时阻止get/pack，数据缺失或失败不会解除限制。相同全文去重并保留出处；新增更严格的隐私限制作用于该正文实体。

状态历史在本机data/corpus/history.jsonl保存，原文为SHA命名不可变blob。data默认不入Git。目录暂不可访问时不要把离线当删除，也不要绕过最新版隐私处置使用旧缓存。

## Wiki与受控规范修订

LLM可从已读原文提炼Wiki页面，页面保留来源ID/SHA、适用前提、排除项和未证实主张。提炼页面先review，人工或代理复核按实际角色记录。不能把摘要冒充原文；需要证据时仍get/pack全文。

新增受控SOP需写完整输入、执行步骤、可观察验收、失败回路、模板和上级程序关系，变更版本与注册表后seal并doctor。seal是显式编制动作；不会自动批准外来资料，也不能替代语义和视觉检查。

## 公开分发

私人原文、媒体与项目验收记录留在本机。公开贡献只包含有明确分发权限的原创资料或许可兼容的内容，保留上游要求的归属声明。许可未知仅留引用和元数据；不把第三方图片权利推断为仓库文本许可。重新执行check_public与测试，再用新版本发布。
