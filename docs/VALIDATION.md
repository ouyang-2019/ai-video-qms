# 0.1.0公开版验证记录

日期：2026-10-07。以下是代码、文件控制与调用结构验证，不是生成模型或媒体质量验收。

- Node测试：23项全部通过，含精确模型隔离、文件/元数据哈希、隐私依赖、预算、不可覆盖记录与路径/junction边界。
- Python测试：34项，33项通过，1项在本机因Windows符号链接权限跳过；Node的junction逃逸检查通过。覆盖RAG全文/中文检索、正文变更、最新隐私、CRLF字节SHA、Wiki全部8任务、用途/版式语义、设计包及完整Skill在中文/空格路径下安装和调用。
- doctor：143份受控文件、8个模型入口、24条来源元数据，来源库空白初始状态通过。
- check_public：目录、JSON/Python语法、链接、Wiki/Skill路由、自动主机路径与凭据模式检查通过。发布还对Git暂存内容做同类检查。
- 独立只读审查发现的get/pack换行SHA及直接工具写入边界问题已修复并复核；正式规范全部使用LF分发换行，哈希以确切UTF-8文件字节为准。

所有Skill、原创方法示例和受控文件按仓库版本固定；本地导入资料保持单独的审批、隐私和SHA记录。上述测试没有运行外来脚本、生成付费图像/视频、审看真实产物、逐条确认全部第三方方法或证明平台实时能力。模型配置是有日期的规范快照。

复现：

```bash
node --test tests/qms.test.js
python -B -X utf8 -m unittest discover -s tests -p "test_*.py"
python -B -X utf8 tools/qms.py doctor
python -B -X utf8 tools/check_public.py --tracked
```

跨平台CI结果以本仓库对应提交的GitHub Actions为准，不能用本机测试代替远端运行记录。
