# L2 Master Guide (EN/ZH)

## 1. Task Setup And Evaluation Target / 任务设定与评估目标
### EN
- Task definition: Controllable text-guided **360 panorama video generation** in ERP format, with optional motion conditions.
- Input/Output:
  - input: text prompt (+ optional motion signal, e.g., optical flow),
  - output: multi-frame 360 video sequence with coherent spatiotemporal behavior.
- Evaluation target:
  - text alignment and visual quality,
  - frame consistency,
  - panorama-specific criteria: left-right continuity, panoramic content distribution, and panoramic motion pattern.

### ZH
- 任务定义：在 ERP 格式下进行可控的**文本引导 360 全景视频生成**，可选运动条件输入。
- 输入输出：
  - 输入：文本提示（可选运动信号，如光流），
  - 输出：时空连贯的 360 视频序列。
- 评估目标：
  - 文本对齐与视觉质量，
  - 跨帧一致性，
  - 全景特有指标：左右连续性、全景内容分布、全景运动模式。

## 2. Baseline Family And Failure Analysis / 基线家族与失败分析
### EN
- Representative baseline #1: native AnimateDiff on ERP-like outputs.
- Representative baseline #2: AnimateDiff + panorama LoRA (LatentLabs360 in the paper comparison).
- Observed failure reasons:
  - Standard T2V priors are learned from perspective videos; ERP has different content distribution and geometry.
  - Panorama motion trajectories are often curved and globally coupled, unlike local motion assumptions in standard settings.
  - ERP requires wrap-around boundary continuity; left/right edges represent neighboring regions on sphere.

### ZH
- 代表性基线1：直接使用 AnimateDiff 生成 ERP 风格输出。
- 代表性基线2：AnimateDiff + 全景 LoRA（文中对比的 LatentLabs360）。
- 失败原因分析：
  - 标准文生视频先验来自透视视频，ERP 的内容分布与几何结构不同。
  - 全景运动常呈曲线并带有全局耦合，和普通视频的局部运动假设不一致。
  - ERP 需要环绕连续，左右边界在球面上本应相邻。

## 3. Core Innovation And Positioning / 核心创新与方法定位
### EN
- Core innovation:
  - a lightweight **360-Adapter** to adapt pretrained T2V diffusion backbones,
  - **360 Enhancement Techniques** (latitude-aware loss + latent rotation + circular padding),
  - **WEB360** dataset with improved captions via 360 Text Fusion.
- Method-level novelty:
  - adaptation strategy targets panorama domain shift explicitly,
  - continuity handling is designed at both semantic/macroscopic and pixel/microscopic levels,
  - data annotation pipeline is tailored for panorama caption granularity.
- Engineering-only parts:
  - use of DDIM sampler and common CFG settings are mostly standard engineering choices.

### ZH
- 核心创新：
  - 轻量 **360-Adapter** 用于适配预训练文生视频扩散骨干，
  - **360 增强技术**（纬度感知损失 + 潜变量旋转 + 圆周填充），
  - 通过 360 Text Fusion 提升描述质量的 **WEB360** 数据集。
- 方法创新层面：
  - 适配策略明确针对全景域偏移，
  - 连续性处理同时覆盖语义级（宏观）和像素级（微观），
  - 数据标注流程针对全景描述粒度专门设计。
- 偏工程实现的部分：
  - DDIM 采样与常规 CFG 等设置主要属于常见工程选择。

## 4. Module-Level Pipeline / 模块级流程拆解
### EN
- Module A: Pretrained backbone
  - Stable Diffusion v1.5 + AnimateDiff motion priors (mostly frozen during adaptation).
- Module B: 360-Adapter
  - receives condition tensor (or zero-input with probability P during training),
  - extracts multi-scale features and injects them into U-Net encoder scales.
- Module C: 360 Enhancement
  - latitude-aware loss reweights denoising objective by latitude importance,
  - latent rotation encourages wrap-around consistency,
  - circular padding (late denoising half) improves seam-level continuity.
- Module D: Data and captioning
  - WEB360 dataset (~2,114 text-video pairs),
  - 360 Text Fusion: caption perspective projections then fuse to richer panorama caption.

### ZH
- 模块A：预训练骨干
  - Stable Diffusion v1.5 + AnimateDiff 运动先验（适配阶段大部分参数冻结）。
- 模块B：360-Adapter
  - 接收条件张量（训练时按概率 P 输入零条件），
  - 提取多尺度特征并注入 U-Net 编码器多层。
- 模块C：360 增强
  - 纬度感知损失按纬度重加权去噪目标，
  - 潜变量旋转增强环绕连续性，
  - 后半程圆周填充提升接缝像素连续性。
- 模块D：数据与描述
  - WEB360 数据集（约 2,114 对文-视频），
  - 360 Text Fusion：先多视角描述，再融合为更细粒度全景描述。

## 5. Design Rationale (Why Each Module Exists) / 设计动机（每个模块为何存在）
### EN
- Why 360-Adapter exists:
  - full finetuning is expensive and can damage pretrained priors,
  - adapter gives parameter-efficient domain adaptation.
- Why latitude-aware loss exists:
  - ERP distortion is not uniform; low/mid latitudes are often more visually critical, so weighted optimization can improve perceived quality.
- Why latent rotation + circular padding both exist:
  - latent rotation improves global semantic continuity,
  - circular padding improves local convolution boundary behavior; they address different scales of seam artifacts.
- Why WEB360 + 360TF exists:
  - data scarcity and weak captions were bottlenecks; better paired data improves text-grounded generation reliability.

### ZH
- 为什么需要 360-Adapter：
  - 全量微调开销大且可能破坏预训练先验，
  - 适配器提供参数高效的域适配能力。
- 为什么需要纬度感知损失：
  - ERP 畸变并不均匀，低/中纬度通常更关键，因此重加权优化有助于提升主观观感。
- 为什么同时要潜变量旋转和圆周填充：
  - 潜变量旋转改善全局语义连续性，
  - 圆周填充改善局部卷积边界行为；二者处理不同尺度的接缝问题。
- 为什么要 WEB360 + 360TF：
  - 数据缺乏与描述粗糙是核心瓶颈，更好的文-视频配对能提升文本驱动生成的可靠性。

## 6. Training And Inference Details / 训练与推理细节
### EN
- Backbone and settings (paper reported):
  - base: Stable Diffusion v1.5 + Motion Module v14,
  - resolution: 512 x 1024,
  - frames: 16,
  - batch size: 1,
  - total steps: 100k,
  - learning rate: 1e-5,
  - conditioning drop probability: P = 0.2.
- Diffusion schedule:
  - linear beta schedule similar to AnimateDiff,
  - beta_start = 0.00085, beta_end = 0.012.
- Inference:
  - DDIM, 25 sampling steps,
  - text guidance scale: 7.5,
  - latent rotation angle: pi/2,
  - supports text-only or text+motion generation.

### ZH
- 论文给出的主干与训练设置：
  - 基座：Stable Diffusion v1.5 + Motion Module v14，
  - 分辨率：512 x 1024，
  - 帧数：16，
  - batch size：1，
  - 总步数：100k，
  - 学习率：1e-5，
  - 条件丢弃概率：P = 0.2。
- 扩散调度：
  - 与 AnimateDiff 类似的线性 beta 调度，
  - beta_start = 0.00085，beta_end = 0.012。
- 推理配置：
  - DDIM，25 步采样，
  - 文本引导系数：7.5，
  - 潜变量旋转角：pi/2，
  - 支持仅文本或文本+运动条件生成。

## 7. Evidence Mapping (Claim -> Experiment) / 证据映射（结论 -> 实验）
### EN
- Claim 1: "Method improves panorama continuity and motion realism."
  - Evidence: Qualitative comparison figure (paper Fig. 6/7) and user-study panorama criteria (end continuity, content distribution, motion pattern).
- Claim 2: "Each proposed component contributes."
  - Evidence: Ablation study (paper Fig. 8) on 360TF, pseudo-3D layer, and latitude-aware loss.
- Claim 3: "Approach generalizes across personalized style models."
  - Evidence: Results shown with multiple personalized SD models (e.g., RealisticVision, Lyriel, ToonYou, RCNZ Cartoon).
- Weaker/limited evidence:
  - paper does not provide exhaustive compute-efficiency comparison against all alternatives.
  - statistical variance details for ablations are limited in the main text.

### ZH
- 结论1："方法能提升全景连续性和运动合理性。"
  - 证据：定性对比（文中 Fig. 6/7）以及用户研究中的全景指标（边界连续性、内容分布、运动模式）。
- 结论2："提出的各组件都有效。"
  - 证据：消融实验（文中 Fig. 8）验证 360TF、pseudo-3D 层与纬度感知损失。
- 结论3："方法可适配多种个性化风格模型。"
  - 证据：在多种个性化 SD 模型上的结果展示（如 RealisticVision、Lyriel、ToonYou、RCNZ Cartoon）。
- 证据较弱或有限的部分：
  - 论文没有给出覆盖所有对比方法的完整算力效率对比。
  - 主文中对消融统计方差等细节展开有限。

## 8. Transferability And Limits / 可迁移性与边界
### EN
- Transferability:
  - high potential for tasks that share ERP geometry and wrap-around continuity constraints,
  - adapter-based strategy is likely reusable in other panorama-conditioned generation pipelines.
- Required conditions:
  - access to panorama video data (or ability to build pseudo-paired data),
  - motion condition estimator compatible with panorama inputs.
- Known limits:
  - quality depends on data coverage and caption granularity,
  - high-resolution generation still constrained by base model and memory budget,
  - exact behavior under distribution shift (e.g., rare motion patterns) is not fully quantified.

### ZH
- 可迁移性：
  - 对共享 ERP 几何与环绕连续性约束的任务有较高迁移潜力，
  - 基于适配器的策略也可迁移到其他全景条件生成流程。
- 必要条件：
  - 需要可用的全景视频数据（或可构建近似配对数据），
  - 需要与全景输入兼容的运动条件估计器。
- 已知限制：
  - 效果依赖数据覆盖度和描述粒度，
  - 高分辨率生成仍受基座模型能力和显存预算限制，
  - 在分布偏移场景（如稀有运动模式）下的行为量化仍不充分。
