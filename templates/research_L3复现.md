# L3 Research And Reproduction Guide (EN/ZH)

## 1. Formal Problem Setup
### EN
- formal objective:
- optimization target:
- assumptions and scope:

### ZH
- 形式化目标：
- 优化目标：
- 假设与范围：

## 2. Notation And Data Representation
### EN
- key symbols:
- data tensor/layout conventions:
- condition/control representation:

### ZH
- 关键符号：
- 数据张量/维度约定：
- 条件或控制信号表示：

## 3. Objective/Formulation
### EN
- core equations/objective terms:
- regularization or auxiliary loss:
- if missing, state exact missing details:

### ZH
- 核心公式/目标项：
- 正则项或辅助损失：
- 若缺失，请明确写出缺失内容：

## 4. Architecture And Information Flow
### EN
- backbone and frozen/trainable parts:
- module insertion points:
- feature flow from input to output:

### ZH
- 主干结构及冻结/可训练部分：
- 模块插入位置：
- 从输入到输出的特征流：

## 5. End-to-End Algorithm
### EN
- training algorithm step-by-step:
- inference algorithm step-by-step:
- pseudocode-level summary:

### ZH
- 训练算法逐步流程：
- 推理算法逐步流程：
- 伪代码级摘要：

## 6. Training Recipe
### EN
- dataset split and filtering:
- preprocessing pipeline:
- optimizer/scheduler/batch/steps:
- important hyperparameters:
- compute budget:

### ZH
- 数据集划分与筛选：
- 预处理流程：
- 优化器/调度/批大小/训练步数：
- 关键超参数：
- 训练算力预算：

## 7. Inference Recipe
### EN
- required inputs:
- sampling or decoding settings:
- controllable knobs and default values:
- runtime/memory observations:

### ZH
- 必要输入：
- 采样或解码设置：
- 可控参数及默认值：
- 运行时与显存观察：

## 8. Ablation Logic
### EN
- component-to-hypothesis mapping:
- key ablation findings:
- interpretation of negative results:

### ZH
- 组件与假设的对应关系：
- 关键消融结论：
- 负结果的解释：

## 9. Reproduction Checklist
### EN
- [ ] environment and dependency lock
- [ ] data source availability and license check
- [ ] preprocessing parity with paper/code
- [ ] architecture parity
- [ ] loss-term parity
- [ ] optimizer and schedule parity
- [ ] random seed and evaluation protocol parity
- [ ] qualitative and quantitative sanity checks

### ZH
- [ ] 环境与依赖版本锁定
- [ ] 数据来源可用性与许可检查
- [ ] 预处理流程与论文/代码一致
- [ ] 模型结构一致性
- [ ] 损失函数项一致性
- [ ] 优化器与调度一致性
- [ ] 随机种子与评测协议一致性
- [ ] 定性和定量结果的基本校验

## 10. Failure Modes And Debug Order
### EN
- top failure mode #1 and quick test:
- top failure mode #2 and quick test:
- top failure mode #3 and quick test:
- recommended debug order:

### ZH
- 主要失败模式1与快速排查：
- 主要失败模式2与快速排查：
- 主要失败模式3与快速排查：
- 推荐调试顺序：
