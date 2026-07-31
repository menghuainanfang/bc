# 模拟测试样例

## 模拟论文：简化版 Transformer 论文摘要

以下是一个模拟的英文论文摘要，用于测试 Skill 的 6 步工作流程是否能正常触发和执行。

---

### 模拟论文输入（文本形式，实际使用时为 PDF）

**Title:** "Gated Attention Networks for Efficient Long-Range Sequence Modeling"

**Abstract:**
We propose Gated Attention Networks (GANet), a novel architecture that combines the self-attention mechanism with gating mechanisms inspired by Long Short-Term Memory (LSTM) networks. While standard self-attention achieves strong performance on sequence modeling tasks, its quadratic complexity with respect to sequence length limits its applicability to long sequences. GANet addresses this limitation by introducing a learnable gating function that dynamically prunes attention weights, reducing the effective number of token interactions. Experiments on Long Range Arena (LRA) benchmark show that GANet achieves 20% faster inference than standard self-attention while maintaining comparable accuracy. On sequences of length 4096, GANet reduces memory consumption by 35% compared to the vanilla Transformer.

**Key Terms:** self-attention, gating mechanism, LSTM, Long Range Arena, attention pruning

---

### 预期 Skill 输出结构

如果 Skill 正确执行，应输出包含以下 6 个步骤的 Markdown 文档：

1. **📄 论文信息卡片** — 提取标题、作者、会议、核心问题与贡献
2. **🏗️ 论文逻辑骨架** — 问题→动机→方法→实验→结论
3. **📖 术语类比词典** — self-attention、gating mechanism、LSTM、LRA 等的类比例子
4. **🆕 新知识检测与讲解** — 标记 LRA benchmark、attention pruning 等新知
5. **🗺️ 分段阅读路线图** — 两遍阅读法的逐节引导问题
6. **📁 知识归档建议** — 可复用方法论、写作模板、参考文献链

### 关键验收项

| 验收项 | 要求 |
|--------|------|
| 不编造实验数据 | ✅ 只能引用论文中已有的数据（20% faster, 35% reduction） |
| 不伪造公式 | ✅ 不自行写出数学推导 |
| 不编造结论 | ✅ 不添加"该方法可推广到XX领域"等未声明的扩展 |
| 术语类比准确 | ✅ gate mechanism 类比 LSTM 的门控，self-attention 类比加权求和 |
| 新知标记完整 | ✅ LRA benchmark 如超出本科知识范围应被标记 |

---

> ⚠️ 提醒：这是一个模拟样例。实际使用时，请替换为你自己的真实 PDF 论文，并观察 Skill 的 6 步输出是否符合预期。
