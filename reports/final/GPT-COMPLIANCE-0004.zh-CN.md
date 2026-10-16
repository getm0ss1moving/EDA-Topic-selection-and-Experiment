# 第四批四轮迭代：选题与角色规范报告

本批 GPT-COMPLIANCE-0004 已完成 D04、D05 各四轮新增的完整 proposer → challenger → verifier 循环，八轮研究 PR 均已合并；24 份有效科学输出和八次新会话独立规范审计已冻结。停止检查确认两个方向均停在四轮，没有第五轮工作或新角色会话。当前获准实验的题目为零，正式联合弃用为零；两个后继题均保留为需要补证的研究假设。


| 方向 | 保留的前题 | 后继题 | 本批最终状态 |
|---|---|---|---|
| D04 物理设计 | EDA-0009：固定修复候选的付费观测/共享验证，三轮后暂停 | EDA-0012：共享位置可行性反馈驱动叶级时钟聚类 | 科学裁定 park；运行时在四轮上限停止 |
| D05 时序 | EDA-0010：候选完整输出共享，三轮后暂停 | EDA-0011：局部单元选择的候选相对时序证书 | 科学裁定 park；运行时在四轮上限停止 |

本批没有形成已经验证的优质组合型成果或结构型创新。它把两个后继方向收敛为更具体、可以被强基线否定的系统假设，并指出最先需要获得的证据：D04 的真实组相关合法域与需求，D05 的同信息 AA/精确缓存之外的有用差异。真实物理收益仍未知；缺少结果不被包装成成果，也不等于证明方向无价值。

冻结清单、逐轮回执及边界见 [完成记录](../../runs/GPT-COMPLIANCE-0004/completion.json)、[公开字节审计](../../runs/GPT-COMPLIANCE-0004/publication-audit.json) 和 [停止证明](../../runs/GPT-COMPLIANCE-0004/stop-check.json)。本批是有限任务调度，不是已认证的常驻无人值守服务。旧题、质疑、未定项及被隔离尝试均保留；新 ID 不覆盖旧记录。

## 每轮交付索引

以下均为新批次的完整 P/C/V 循环，编号按方向分别计算；后继题各完成一轮，不把旧题记录删除。P 为提出者、C 为质疑者、V 为科学核验、A 为另一个独立规范 auditor。

| 方向/轮 | 选题 | 科学裁定 | 冻结输出 | GitHub |
|---|---|---|---|---|
| D04/1 | EDA-0009 | revise | [P](../../runs/SUB-2e1f236a3f9a0f3f0b1c30016dc8ad8f2b235c94f980b0989b1d3e287588d85c/proposal.md) / [C](../../runs/SUB-8799913f1db1283e09646461628b8009a043423bf86ae40cb5a9c85eb7ec0042/challenges.md) / [V](../../runs/SUB-f70b504c01235e69199f322b0bbd1ddec249af0289ea0e1883b1132758ddb6bf/verification.md) / [A](../../runs/SUB-7e97f68607ffccc8e48853bfd2247e683998c8b4353be4e36eca19d4f14fd154/verification.md) | [PR #72](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/72) |
| D04/2 | EDA-0009 | revise | [P](../../runs/SUB-988d5b734de75037f4ca472fe6c9799a673f9538cd7b4053da26a004347406f8/proposal.md) / [C](../../runs/SUB-3090026e572d0cecae72323cca434d6748d78424acd61699d6ecfb2e8aad0f6b/challenges.md) / [V](../../runs/SUB-b69a8b5d5ff701c8a70bb5122fcfe70e9cf376634d0f50de420109f7e3b8d8a0/verification.md) / [A](../../runs/SUB-55cc0847368e9b869318025e7199ab71f69c0a03de9933db4418a279696fd97c/verification.md) | [PR #77](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/77) |
| D04/3 | EDA-0009 | park | [P](../../runs/SUB-2966cec6a631f48b998ddb78b67aba187e072ad1d9b4d3498aeebdb879a9f0cc/proposal.md) / [C](../../runs/SUB-83d9a23ab90f7ca974796e8ed39617078e1ee76f0abcab0f0746f6bab6c2278f/challenges.md) / [V](../../runs/SUB-047b42329a35771ca6788e18cc97583dedaf36526c13f12defa839e36c8b1ed0/verification.md) / [A](../../runs/SUB-38bbccd6fbce4ef1bd73982cdbcd3a66c264f9e076fd93819cb97aaa51cb7f46/verification.md) | [PR #79](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/79) |
| D04/4 | EDA-0012 | park | [P](../../runs/SUB-4cff54ad61aa12a294a808f36ba47524b43e6642cf97d8d49571572141c2a45f/proposal.md) / [C](../../runs/SUB-19f19b087b06fe9b61eb1d39a8bfacf1c5a73c0597c3f6ca95d51eadd40c72e5/challenges.md) / [V](../../runs/SUB-82b8167ca9b955b4087f667585378f4e53893e95a14fffdff461b7b0937b1659/verification.md) / [A](../../runs/SUB-fbeea4498bb08978f6df0a09380c9af648ef2ea947868621919273036fd09503/verification.md) | [PR #82](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/82) |
| D05/1 | EDA-0010 | revise | [P](../../runs/SUB-b4a0830fd75dd9263101adcdda8a60e7ed86f687e08723fe63c0f3e83046ffae/proposal.md) / [C](../../runs/SUB-1a4046d48852400f673bf14b891eeb70900fc985b29d11840149262bdfe13693/challenges.md) / [V](../../runs/SUB-c4ea36b9e62a68730c225ac73645a9b5d399bbd2142507a0212c0ef12fb9dd0c/verification.md) / [A](../../runs/SUB-7f1fa5d72cb3dbe99558c18a4edc83e596e157506a358070f449d2777b8ebc3b/verification.md) | [PR #71](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/71) |
| D05/2 | EDA-0010 | revise | [P](../../runs/SUB-017839376433acd2ef83e1cf06276f1d54e9af5740eb2561a0b9b928a404a6ae/proposal.md) / [C](../../runs/SUB-1745834c07cf7e42c0a3756f0da807ddba9a85495361276d8b9e21390cf2f1b0/challenges.md) / [V](../../runs/SUB-a8da4b6a1a7928ee94f15ee0ec17693629258c346fc2b559b406e2dca9fd3327/verification.md) / [A](../../runs/SUB-b64d239e50bb39771d2c3f838b8b5874c19a640fe6e897f1c9e5b10b004dbc93/verification.md) | [PR #73](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/73) |
| D05/3 | EDA-0010 | park | [P](../../runs/SUB-e59222b261fdda904cd66c5a892de454e5dbcbabf4b3fa142896b356fd1ce075/proposal.md) / [C](../../runs/SUB-d65e80f160a5b95d5338cbbede7dbefddeea23f506a1e7f2db70102f2d45167c/challenges.md) / [V](../../runs/SUB-77d7bb685bc812bcb6e3e2a5a357478f7f2a743ad0dcba6a249962e0b163af95/verification.md) / [A](../../runs/SUB-2872435ae5bc9d693c101e73fa71f0ba2a5c7c5381281741b4461cb9bd92ab17/verification.md) | [PR #76](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/76) |
| D05/4 | EDA-0011 | park | [P](../../runs/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/proposal.md) / [C](../../runs/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/challenges.md) / [V](../../runs/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.md) / [A](../../runs/SUB-798d896ad7a77ed584bf663fbed8b2cbc22d5127c3e4c9619a42cd49a69af124/verification.md) | [PR #78](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/78) |

本批提出者请求模型为 gpt-6.1-sol/high，质疑者为 gpt-6-astra/low，科学 verifier 与独立规范 auditor 为 gpt-6.1-sol/low。每个工作均从新会话、明确释放的输入开始；这不等于独立认证实际后端路由或强操作系统隔离。科学角色只通过冻结文件交换，协调者负责调度与发布，不代签科研同意。

## D05：从完整输出共享转向单元选择的相对证书

EDA-0010 已在第三轮被独立 verifier 判为 parked。它要求返回每个候选的完整端点向量，但现有需求证据主要对应标量候选选择；同时，已明确写出的索引、共享与维护操作可以移植到强传统基线，尚未证明额外系统收益。这个结论保留了研究假设，未证明所有相关方法都不可能有效。[第三轮核验](../../runs/SUB-77d7bb685bc812bcb6e3e2a5a357478f7f2a743ad0dcba6a249962e0b163af95/verification.md)

第四轮以新 ID EDA-0011 提出“面向局部单元选择的候选相对时序证书”。新题改变了输出合同，因此单独查重、单独定义方向，没有继承前题签名或认可。其真实决策是选出满足约束的单元候选；预测仅决定计算顺序和细化方式，最终正确性依赖经过验证的界与精确参考计算。[提案](../../runs/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/proposal.md)

设候选 c、已知可行的当前最佳候选 b 共享同一边界状态 z，比较差值 D_cb(z)=J(c,z)-J(b,z)。对当前真实状态构建可靠包围 Z，并保留共同上游、slew/load 影响的相关符号；候选特有的负载和下游影响必须独立处理。只有差值下界严格大于零、且 b 的可行性已经确认时，才淘汰 c。界重叠、平局、守卫未知或状态无法包围时，继续细化或调用精确参考 R。最终获胜者、约束、恢复状态和整轮参考检查仍需完整计费。

这可能节省候选的精确刷新工作，但 Z 的构造、完整依赖更新、负查询失效、区间划分和回退均有成本。若边界精确值已经便宜可得，直接缓存后精确打分可能更好。独立核验认可条件淘汰引理，同时指出它属于已有分支定界思想；当前基本差值表达与通用 affine arithmetic 移植对照重合，尚未建立有用的 EDA 专属差异。有限模型代码已公开，但 verifier 只检查了该轮代码，没有独立重跑其数值结果，更没有证明 STA 加速。[第四轮核验](../../runs/SUB-6a2f437f43fd9ee63a3de84bc3fe096a5da49e6da3e6f7074f95b7c3140c386f/verification.md)

可继续检验的 AI/agent 组合包括：统一成本预测器与分区专门预测器决定先细化哪一对、继续细分还是直接精确刷新；算法工作者分别返回输出项和上游项的可靠部分界与依赖标识，由确定性协调器合并。预测本身不提供证书。最小原型仍可使用非 LLM 的集中控制器；多 agent 只有在相同信息、工具调用、内存和通信计费下优于普通并行或单控制器时才有贡献。

后续最小任务顺序应依据已经核验的质疑修正，以下是协调者对既有裁定的整理，并非双方已经同意的实验授权：

1. 找到实际标量决策读者，说明更强完整刷新 R 相对现有快照/局部更新语义的质量或成本价值；完成最接近的 AA、候选剪枝、时序更新及赛题获胜方法对照。
2. 将原 T02 拆成“参考 R 与 recorder”和“最小可靠证书及同信息 AA 可执行实现”。两者均须先于证书正确性测试和构造成本 census；原计划把关键实现在 T06、却在 T03/T04 先测试，属于有效的依赖缺口。
3. 检验负载副作用、LUT 分区、max 分支、相关性、外向舍入、负查询、相等值但不同依赖、近似平局、非法候选、epoch 变更及恢复；任何错误证书立即停止正确性主张。
4. 在真实获配的合法数据与算力上，先做基线成本 census，再锁定工程上有意义的阈值、独立设计族划分和统计规则。
5. 同时比较缓存精确 R、同 DAG/同信息 AA 与分支定界、独立绝对界、精确边界缓存、普通集中/并行控制器；近似局部更新作为单独质量点。最后再判断是否值得加入学习器或多 agent。
6. 修订后的精确 tasklist 哈希获得 proposer/challenger 各自同意并经 verifier 检查后，才能进入对应的正式实验。当前双方均要求修订，资源与负责者尚未锁定。

判断：当前是值得做廉价区别检验的系统方法假设，组合型贡献和结构型创新均未确立。第四轮科学结论为 park，运行时已到四轮上限；没有实验准入、联合弃用或物理性能预测。详细原始任务表与质疑均保持英文、保持冻结。[原 tasklist](../../runs/SUB-2c26123b9b1c2d001f3615e1ad5087ac6444ac38a03cae6f9cfa57304e86de20/tasklist.md)、[质疑](../../runs/SUB-d7573b7cfdc55db5c5f659765501be34d4e33ea88cac5eabe8a7d118fa61d1be/challenges.md)、[完整轮次 PR #78](https://github.com/getm0ss1moving/EDA-Topic-selection-and-Experiment/pull/78)。

## D04 前题：固定修复候选间的付费观测与共享验证

EDA-0009 在同一不可变基点产生固定候选池，研究能否通过选择性获取局部检查上下文、预测残余共享工作，减少完成有效修复选择的总成本。当前定义已经区分付费公共缓存 K0、冷缓存与部分缓存；“共同工作”需要扣除已由 K0 覆盖的部分。相同信息、代价、动作和确定性 tie-break 的传统策略与提案策略被明确合并，未来差异只能来自有证据支持的表示或估计器及其完整成本。

三轮文本修订完成了这些定义层面的修复：补入 AiDRC 的任务对应基线；把单步信息收益启发式与允许联合观测的控制分开；修复任务表中预注册和 census 的先后关系；让所有方法具有相同 STOP/CONTINUE/full-report 动作。多个相关观测可能只有共同获取后才有价值，但扩大动作集也会增加规划成本，旧的动作数量上界不能直接沿用。

仍未解决的核心是“什么证据可以安全地提前排除候选，以及究竟省掉哪些实际工作”。公开源代码中的中间 marker 会被清理、修补、去重或经调用者/导出层过滤，因此瞬时 marker 不能直接当作最终失败证据。完整已结束 worker 的保留 marker 可能是较窄的证明边界，但尚未验证持久性、可取消粒度、已经在途的成本及恢复开销。原始支持界约束的是谓词工作，不是墙钟时间。

另外，受限纯键子问题与已有付费布尔求值、共享过滤排序存在重合。相关因子、联合预测或 agent 包装本身未建立新贡献；有用的物理系统差异、真实小候选池的需求频率和残余共享分布仍需要证据。第三轮 verifier 因此决定 park，并保留重新开启条件，未证明所有物理候选共享都无价值。[第三轮科学核验](../../runs/SUB-047b42329a35771ca6788e18cc97583dedaf36526c13f12defa839e36c8b1ed0/verification.md)

## D04 后继题：把共享合法位置反馈到叶级时钟分组

EDA-0012 的提案为“共享位置可行性反馈驱动的叶级时钟聚类”。它固定数据单元布局、时钟域、buffer master 和 buffer 数量，在局部叶级邻域内联合考虑 sink 分组、电气约束和完整 buffer footprint；独立核验已决定 park，保留重新开启条件；当前没有实验准入。[冻结提案](../../runs/SUB-4cff54ad61aa12a294a808f36ba47524b43e6642cf97d8d49571572141c2a45f/proposal.md)

它把一个候选表达成“sink 集合、占用 site 的完整 footprint、单元与电气有效性来源”。精确检查器同时检查 sink 覆盖和 footprint 不重叠，返回合法分配或当前有限选项域的冲突；冲突反馈给有界的重新分组过程。有限域无解只说明该次枚举没有解，不能声称真实物理问题无解。扩大域、改变占用或电气条件后，旧的 no-good/cut 需要重新验证或作废。预测器可排序候选或估计冲突代价；精确检查、合法化与最终 route/timing guard 仍负责正确性。

多 agent 的可选分工为分组、几何、电气分析工作者，由单一确定性仲裁器管理有版本的公共状态；不允许多个工作者并发改写同一设计数据库。统一预测器与专门预测器都要与普通集中控制器、同信息的整体求解及分解算法比较，计入标签、训练、推理、通信、重试、冲突缩减和回退成本。已有 CTS 阻塞感知、联合优化及 logic-based Benders 是必须面对的近邻，不以“增加 agent”或“组合已知算法”直接认定贡献。

独立 verifier 将三项质疑均判为 valid、阻止实验晋级：sink 重新分组究竟改变了真实电气合法域，还是仅改变了人为枚举窗口；是否存在区别于同信息传统控制器的具体估计器或有用实现；census、几何 observer、模型定义和精确任务同意的先后绑定是否足够。若每个组的合法位置域都相同、buffer master 和数量固定，而且仅看几何可行性，重新给 sink 分组不会改变能否放下这些 buffer。真实组相关电气约束可能打破这个条件，但需要明确证明适用关系，不能由小模型直接外推。[冻结质疑](../../runs/SUB-19f19b087b06fe9b61eb1d39a8bfacf1c5a73c0597c3f6ca95d51eadd40c72e5/challenges.md)

最终科学裁定为 park。八项准入门中，仅方向一致性通过；其余是尚未通过，不是已证明不可能。当前 proposer 的同意为 pending，challenger 为 revision_requested，没有双方实验 tasklist 共识。旧 EDA-0009 的全部负面结果仍保留，未把其暂停解释为对 EDA-0012 的支持。[独立核验](../../runs/SUB-82b8167ca9b955b4087f667585378f4e53893e95a14fffdff461b7b0937b1659/verification.md)、[原任务表](../../runs/SUB-4cff54ad61aa12a294a808f36ba47524b43e6642cf97d8d49571572141c2a45f/tasklist.md)

根据已核验质疑，后续任务至少需要如下顺序；这是裁定整理，尚未由 proposer 修订、双方签名或获配执行：

1. 先从真实电气与工程约束推导组相关位置域，给出每个被排除选项的原因。与同成本的原分组扩域、重新分配比较，加入共同域、宽松位置和无竞争负对照；先回答是否存在真实机制，避免制造紧约束来获得效果。
2. 在 census 前定义并验证 footprint observer、site/row/方向/padding/固定单元适配器和明确的布局阶段快照。用有限几何实例检查完整 footprint、坐标、遗漏选项、过时占用及域版本；observer 不能由点原点碰撞计数替代。
3. 冻结有限优化式、全局选项/迭代/工作上界、精确 oracle 和 native、联合分配、整体求解、普通 LBBD 等强基线。把估计器比较与控制器比较交叉设计；同状态、分数、动作和 tie-break 的控制器直接合并。
4. 核对赛题获胜实现、近邻论文与数据权利，锁定代表性合法 checkpoint、实际机器预算和完整命令。先做被授权的基线校准，再锁定工程阈值、独立设计族划分和统计规则；实际训练仍须等具体模型与标签生成流程被精确任务同意覆盖。
5. 若机制与需求仍成立，比较统一/专门预测器及冲突代价估计的完整成本。重新检查上层时钟插入及后续合法化后叶级 buffer 是否保持有效；最终 route、setup/hold、DRC、连接和回退均计入。一个错误证书即停止正确性主张。
6. 有用机制先于多 agent 包装。只有在同信息、工具、并行度、token 和重试预算下，才比较分组/几何/电气工作者与集中非 LLM 控制器；否则删除包装。修订后的任务表及其生成依赖必须重新取得双方同意和独立核验。

预测：总成本和 routed QoR 的改善方向仍未知，没有可信的加速倍数、WNS 改善幅度或成功概率。有限域可行性也不能证明 routed PPA 最优或工艺签核。当前适合保留为条件性研究假设，尚不能宣称优质组合型成果或结构型创新已经成立。

## 规范核查的含义与保留事项

八次独立审计覆盖 24 份有效科学输出，每份检查输入、隔离、写入、证据、主张、同意、资源、方向和发布九项规则，共 216 项：208 项在所给范围内未发现违规、3 项支持的偏差、5 项未定。被隔离尝试另有 27 项：24 项范围内未发现违规、1 项偏差、2 项未定，不混入有效四轮统计。详见 [英文逐角色矩阵](GPT-COMPLIANCE-0004.conduct.en.md) 与 [机器计数](../../runs/GPT-COMPLIANCE-0004/conduct-counts.json)。

本报告由协调者整理，科学裁定属于每轮独立 verifier；规范矩阵另由新会话的 protocol auditor 检查三个科学角色。核查材料为冻结输出、公共 JOB/prompt/PACKET 描述符及明确释放的事件元数据，没有读取角色私有对话或 scratch。矩阵中的“范围内未发现违规”不代表观察到了所有执行动作，也不证明操作系统隔离、实际后端模型路由或普遍科学新颖性。

目前需明确保留的事件包括：

- D04 第一轮 challenger/verifier 的证据访问级别或来源字段格式偏差。真实的来源访问限制有披露，审计未据此推断伪造或蓄意行为。
- 一次 D04 第二轮收集隔离。独立审计确认 verifier 登记的完整路径均属于原 JOB 授权路径，但不符合 canonical SUB ID 格式；另有 challenger 自有历史输出的归属映射未随该次审计提供，保留未定检查。原三份输出和审计完整保留，重跑三角色使用新身份、干净检查点，不计隔离尝试为有效一轮。[事件审计](../../runs/SUB-573df9c23c1928e04ad3ba0801e204c7a5e9136c546774e8db25a922e11348c0/verification.md)
- D04 第三轮 proposer 的平台筛查中断前输入、隔离和资源活动无法完整还原。该轮独立规范审计保留三项 unresolved，不推断发生了违规，也不作完整清白证明。[第三轮规范审计](../../runs/SUB-38bbccd6fbce4ef1bd73982cdbcd3a66c264f9e076fd93819cb97aaa51cb7f46/verification.md)
- D04 第四轮 verifier 在完成通用政策阅读前，先列出了本 JOB 内的文件名，审计记为非关键读取顺序偏差；没有据此推断读入其他角色私有内容。该轮 challenger 中断前的输入、隔离范围保留两项 unresolved，未由自述替代独立观察。[第四轮规范审计](../../runs/SUB-fbeea4498bb08978f6df0a09380c9af648ef2ea947868621919273036fd09503/verification.md)
- 平台筛查中断按原任务、原模型重试，记录在 backend-failures.json。筛查原因及未观察到的活动仍未知，没有更换提供商或降低防护。中断本身不构成科研失当结论。
- D05 第二轮 tasklist 同意状态的旧文字，以及第四轮证书实现先后顺序，分别作为研究缺陷保留。没有伪造 agree 签名。第四轮审计保留了需要科学鉴定的标记，报告引用原科学 verifier 的 OBJ-1402 裁定，未声称实际修复已完成。

前批次 GPT-COMPLIANCE-0003 的元数据范围核查仍有 15 个 unresolved 单元格，本批不追溯清零。两项 PR #67 历史科学指控在本批获得限定范围的独立核验：原始源码行号指控被 refuted；旧 4096 案例数值主张缺公开原始重放代码/输出的缺陷被认定 valid，并撤去该项经验支持。新检查不能反向认证旧执行，也没有从证据缺失推断蓄意伪造。[限定历史核验记录](../../runs/GPT-COMPLIANCE-0004/historical-review-resolution.json)

PR #79 的另一项历史行号指控也经过本轮独立核验并被 refuted：固定原始文件有 1452 行、哈希与旧记录一致，而工具渲染结果有 1388 行，两者采用不同计数。该裁定只确认所指原始字节和窄语义观察，没有证明历史运行、marker 持久性或取消正确性；旧冻结输出不改写，GitHub 原评论及其限定裁定保持可追溯。[历史行号裁定](../../runs/SUB-82b8167ca9b955b4087f667585378f4e53893e95a14fffdff461b7b0937b1659/verification.json)

协调者还修复了审计包误继承科学 verifier 专属 handover 的潜在边界问题（首个 live audit 前完成）、并行 PR 的会话注册表合并冲突，以及隔离审计缺少公开描述符映射的问题。后续 PR #80 又明确排除 protocol auditor 充任科学接受/弃用 verifier，并对科学 verifier 专属公开补充材料校验哈希与用途；PR #81 进一步拒绝“JOB 已登记材料但文件缺失”及未登记、空元数据等不完整配对。这些属于治理/传输修复，保持冻结科学输出字节不变。[边界修复](../../runs/GPT-COMPLIANCE-0004/audit-boundary-remediation.json)、[注册表冲突处理](../../runs/GPT-COMPLIANCE-0004/transport-reconciliations.json)、[描述符修复](../../runs/GPT-COMPLIANCE-0004/incident-descriptor-fix.json)

## 实验与资源边界

本批授权的是研究迭代。任务表中的诊断 CPU、内存、时长建议不等于真实资源分配；原型、数据/PDK 权利、执行者、精确 oracle 和工程阈值仍须按对应方案锁定。报告中的有限模型、代数检查和源码观察不提供物理 PPA、WNS/TNS、流程墙钟加速或制造签核保证。数值物理效果预测保持未校准/空值。

有价值的组合型系统仍然合格，但需在同需求、同信息、同工具与总成本条件下，对强传统方法和直接组合基线展示额外能力或收益。零方向漂移仅表示相对本题锚点保持一致，不证明创新。Parked 只暂停该题；正式联合弃用需要匹配签名与 verifier 检查，不能通过计数上限代替。

科研原件继续使用英文，原始题目、负面结果与签名不被新题覆盖。最终报告的人类复核按当前仓库开关为可选，独立科学 verifier 始终必需；没有以自动 CI 或协调者合并冒充科学通过。[实际人工复核开关](../../runs/GPT-COMPLIANCE-0004/human-review-policy.json)

公开审计从普通仓库克隆重新比对了 36 份冻结 release，其中 32 份为有效科学/规范输出、另 4 份属于保留的隔离尝试及其独立审计；有效工作的 32 份 JOB/prompt/PACKET 描述符也与运行时字节一致。139 项协调工具回归通过，结构校验、辅助脚本语法和差异检查通过。这些检查不替代科学判断。GitHub CLI 的 TLS 故障通过同一 PR 的 connector 传输恢复，未跳过确切 head 的检查。补充审查输入保留了原转义显示文本；当前回执另记真实 UTF-8 评论及哈希，程序解码核对内容一致，没有重写已冻结输入。PR #75 的可选清单兼容修复与当前清单一并随最终报告发布，其发布前 UI 状态保留在回执中。
