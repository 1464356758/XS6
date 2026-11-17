# XS6 V6.3 新书部署记录

核查日期：2026-11-17（北京时间）。本文件记录部署事实与作者当前指令，不代替 book/state.json。

- 唯一写入目标：https://github.com/1464356758/XS6
- 实际默认分支：main。
- 部署基线 HEAD：81922d173a8e7ef554bee608d9c427f3983e49fa；消息为“按作者要求清空XS6仓库”。基线 tree 为 4b825dc642cb6eb9a060e54bf8d69288fbee4904；固定该提交查询 Contents 返回空数组。旧历史保留，不恢复旧作品。
- 输入包：作者随本次消息附加的 初始化系统包_V6.3.zip。通读 AGENTS.md、WORKFLOW.md、CRAFT.md，package-check 返回 version=6.3.0、package_ok、9 个受校验文件（连同清单本身共10个包文件）。
- 系统来源只读：https://github.com/1464356758/xiaoshuoV5/tree/main/system_templates/v6；核查来源 HEAD 为 c9d19aaa0d69874812369a627ab32125d122fc30。包中9个受校验文件的 Git blob 与来源对应文件一致；INIT_MANIFEST.json 为发行清单。未导入母版其他作品。
- 实际运行：python3 novel.py init --repository https://github.com/1464356758/XS6 --branch main --platform 纵横中文网。
- 本次新身份：53aad353-f0f1-4cee-8967-64a7c97f679b。init 仅运行一次；远端已存在该身份，后续必须恢复，不得再次生成。
- 初始化提交：4b36c726a9084b5613e59a7c61f27a6703dfbdde；tree=a3f201b851497b8e2bf531896aed065bf9b8a36f。以原tree增量创建，以基线HEAD为父提交，expected_sha校验、force=false。
- 回读证据：固定初始化提交的递归tree未截断，13个文件的Git blob逐项匹配本地；另直接回读 book/state.json、online/index.json，与本地逐字节一致。状态SHA-256为2b34de77a14ec33193a9dc941995b9e8b35e477da1c4f2d417da311830877f99，与索引引用一致。package-check、status、context、verify、index实际运行成功。
- 当前：平台纵横中文网；书名留空；WAITING_TOPIC；正文0章、无草稿。默认150章，每章5500—6500汉字，目标约6000汉字。

## 后续执行约定

作者只需选题和确认开始。本轮6个候选见 research/topics.md，均未选定；不调用configure抢先确立书名，不把候选方案写成已发生的剧情。

选定后创建book/plan.md，填写角色欲望、误判与两场不同交锋、世界边界、150章阶段路线、结局方向、前五章不同体验及近期安排。把实际阅读形成且适用的方法卡迁入plan，明确原创场景与不能搬用的内容；根据选题需要补读相关原文。再运行configure设置书名和平台。收到“开始写”才begin写首章，后续“下一章”完成一章。

每轮读→构思→写→改→存。冻结章及快照只读；保留未消解情绪、误解、未完成行动，分清读者和角色的知情。事实冲突改当前候选；转变缺依据补当前触发，不能捏造旧事。写前使用最相关的方法；写后凭正文证据定位表达、用笔、故事中最严重的问题，不以自评高分或文件检查证明好看。

同日不限章数，同请求重试接续原章，有草稿先续完；半章及完成正文时同步实际稿件。正文、简短编辑意见和章后记忆落盘；prose_check只定位重复候选，须回读裁决；assess绑定实际版本，freeze后verify、index，相关文件同批提交。回读固定提交的正文、记录、状态、索引并核对哈希后才能报告已冻结并保存。

不创建定时任务，不调用模型API，不自动发布、投稿或登记签约。模型自审如实标注为同上下文审读。笔名沿用作者已明确指定的“微晚”；尚未替作者创建或修改平台账号。
