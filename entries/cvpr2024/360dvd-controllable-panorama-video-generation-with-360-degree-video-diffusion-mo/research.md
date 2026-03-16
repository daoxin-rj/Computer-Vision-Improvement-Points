# L3 Research And Reproduction Version (EN/ZH)

## 1. Problem Formulation
### EN
- formal objective: Learn a conditional generative model for 360 panorama videos given text prompts and motion conditions.
- assumptions: A pretrained T2V diffusion backbone exists and can be adapted with lightweight modules.

### ZH
- 形式化目标：学习在文本提示与运动条件下生成 360 全景视频的条件生成模型。
- 假设条件：存在可用的预训练文生视频扩散骨干，且可通过轻量模块适配。

## 2. Key Notation
### EN
- notation list: NOT_SPECIFIED in extracted text.

### ZH
- 关键符号列表：当前抽取文本中为 NOT_SPECIFIED。

## 3. Core Formulation
### EN
- equations or objective terms: Includes panorama-aware optimization with latitude-aware loss and continuity-related enhancement terms.
- if missing, state: PAPER_DOES_NOT_PROVIDE_DETAIL

### ZH
- 核心公式或目标项：包含全景感知优化，涉及纬度感知损失与连续性增强相关项。
- 若缺失请标注：PAPER_DOES_NOT_PROVIDE_DETAIL

## 4. Reasoning Or Derivation
### EN
- derivation chain: Standard T2V priors fail on ERP panorama geometry; add adapter and geometric losses to close domain and projection mismatch.
- design rationale: Parameter-efficient adaptation is preferred over full retraining for stability and cost.

### ZH
- 推导链条：标准文生视频先验无法直接处理 ERP 全景几何；通过适配器与几何损失缓解域偏差和投影失配。
- 设计动机：相比全量重训，参数高效适配更稳定、成本更低。

## 5. Algorithm Or Pipeline
### EN
- step-by-step pipeline:
  1) Initialize from pretrained T2V diffusion model.
  2) Insert trainable 360-Adapter and 360 enhancement training terms.
  3) Train on WEB360 panorama video-text pairs with motion conditioning.
  4) Generate controllable 360 videos at inference.

### ZH
- 分步骤算法或流程：
  1) 从预训练文生视频扩散模型初始化。
  2) 插入可训练 360-Adapter 与 360 增强训练项。
  3) 在 WEB360 全景视频-文本数据上结合运动条件训练。
  4) 推理阶段生成可控 360 全景视频。

## 6. Training Strategy
### EN
- data setup: WEB360 panorama video-text dataset.
- optimization: Adapter-based fine-tuning with panorama-aware losses.
- hyperparameters: NOT_SPECIFIED in extracted text.
- if missing, state: NOT_SPECIFIED

### ZH
- 数据配置：WEB360 全景视频-文本数据集。
- 优化策略：基于适配器的微调，并加入全景感知损失。
- 超参数：当前抽取文本中为 NOT_SPECIFIED。
- 若缺失请标注：NOT_SPECIFIED

## 7. Inference Strategy
### EN
- inference-time logic: Condition generation on text prompt and motion control signals.
- compute cost: NOT_SPECIFIED in extracted text.

### ZH
- 推理流程：在文本提示与运动控制信号条件下进行生成。
- 计算开销：当前抽取文本中为 NOT_SPECIFIED。

## 8. Ablation-Relevant Insights
### EN
- what components matter most: 360-Adapter, ERP boundary enhancement, and latitude-aware loss are central to reducing panorama artifacts.

### ZH
- 哪些组件最关键：360-Adapter、ERP 边界增强与纬度感知损失是减少全景伪影的关键。

## 9. Reproduction Risks
### EN
- ambiguous details: Exact architecture dimensions and complete objective weights are PAPER_DOES_NOT_PROVIDE_DETAIL from current extraction.
- implementation pitfalls: Incorrect ERP boundary handling can cause seam artifacts.
- external dependency risks: Reproducibility depends on access to WEB360 and preprocessing consistency.

### ZH
- 语义不清或缺失细节：从当前抽取内容看，精确结构维度与完整损失权重属于 PAPER_DOES_NOT_PROVIDE_DETAIL。
- 实现陷阱：ERP 边界处理不当会产生明显拼接缝伪影。
- 外部依赖风险：复现依赖 WEB360 可用性与一致的数据预处理流程。

