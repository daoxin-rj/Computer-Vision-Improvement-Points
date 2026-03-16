# L1 Beginner Guide (EN/ZH)

## 1. Background You Need First
### EN
- Domain context: This paper is about **text-to-video generation**, but the target is a special format: **360-degree panorama video** (usually stored as ERP, equirectangular projection).
- Real-world scenario: 360 videos are used in VR tourism, immersive education, virtual events, and digital content production.
- Why this task matters now: Capturing real 360 video is expensive (special camera rigs, data collection, post-processing), so generating it from text can reduce cost and increase content scale.

### ZH
- 领域背景：这篇论文属于**文生视频**方向，但目标不是普通视频，而是**360度全景视频**（通常用 ERP 等距矩形投影格式存储）。
- 真实应用场景：360 视频常用于 VR 旅游、沉浸式教育、虚拟活动和内容生产。
- 为什么这个问题现在重要：真实拍摄 360 视频成本很高（设备、采集、后期都贵），如果能从文本直接生成，就能显著降低成本并扩大内容规模。

## 2. Problem In One Sentence
### EN
- One-line problem: How to generate controllable, high-quality 360 panorama videos from text prompts (and optional motion guidance).
- Input/output in simple words: Input is a sentence (and optionally a motion hint such as optical flow), output is a coherent 360 video clip.

### ZH
- 一句话问题：如何根据文本提示（可选再加运动控制）生成可控且高质量的 360 全景视频。
- 通俗输入输出：输入是一句文本（可选运动提示，如光流），输出是一段连贯的全景视频。

## 3. Why Existing Methods Struggle
### EN
- Old way #1: Directly use normal text-to-video models (trained on perspective videos). Problem: they do not understand panorama geometry well.
- Old way #2: Add panorama image tricks only. Problem: still weak for temporal consistency and panorama-specific motion patterns in videos.
- What users observe when it fails:
  - narrow or incorrect field of view,
  - left-right seam artifacts (video edges do not connect),
  - unnatural motion trajectories in ERP format.

### ZH
- 旧方法1：直接用普通文生视频模型（主要在透视视频上训练）。问题：模型对全景几何理解不足。
- 旧方法2：只加一些全景图像层面的技巧。问题：对视频时序一致性和全景特有运动模式帮助有限。
- 失败时你会看到：
  - 视野不够宽或内容分布不合理，
  - 左右边界不连续（接缝明显），
  - 在 ERP 格式下运动轨迹不自然。

## 4. Method Walkthrough (Step-by-Step)
### EN
- Step 1: Start from strong pretrained models (Stable Diffusion + AnimateDiff style pipeline) instead of training everything from scratch.
- Step 2: Add a lightweight **360-Adapter** to inject panorama-related motion/condition features into multiple encoder scales of the denoising U-Net.
- Step 3: Build a panorama text-video dataset (**WEB360**, about 2,114 clips) because existing paired panorama video-text data is lacking.
- Step 4: Improve caption quality with **360 Text Fusion** (caption multiple projected views, then fuse with LLM-assisted summarization).
- Step 5: Apply **360 Enhancement Techniques**:
  - latitude-aware loss (focus more on visually critical low/mid latitude regions),
  - latent rotation (improve global left-right continuity),
  - circular padding in late denoising steps (improve pixel-level seam quality).
- Step 6: At inference, user can provide only text, or text + motion condition for controllable generation.

### ZH
- 第1步：从强大的预训练模型出发（Stable Diffusion + AnimateDiff 路线），而不是从零训练整套模型。
- 第2步：加入轻量 **360-Adapter**，把全景相关的运动/条件特征注入到去噪 U-Net 编码器的多尺度特征中。
- 第3步：构建全景文生视频数据集 **WEB360**（约 2,114 段视频），因为现有配对数据不足。
- 第4步：使用 **360 Text Fusion** 提高描述质量（先对多个视角做描述，再融合为更细粒度的全景描述）。
- 第5步：加入 **360 增强技术**：
  - 纬度感知损失（更关注低/中纬度关键区域），
  - 潜变量旋转（增强全局左右连续性），
  - 后半程圆周填充（改善像素级接缝质量）。
- 第6步：推理时用户可以只给文本，也可以给文本 + 运动条件实现可控生成。

## 5. Why This Design Makes Sense
### EN
- Design choice A (lightweight adapter): keeps pretrained generation priors, so training is cheaper and more stable than full retraining.
- Design choice B (panorama-aware losses/operations): directly targets panorama-specific pain points (ERP distortion + seam continuity), not generic video issues only.
- Design choice C (new dataset + better captions): without good paired data and detailed captions, the model cannot learn reliable text-to-panorama mapping.

### ZH
- 设计选择A（轻量适配器）：保留预训练模型的生成先验，相比全量重训更省算力、更稳定。
- 设计选择B（全景感知损失与操作）：直接对准全景特有痛点（ERP 畸变 + 边界连续性），不只是泛化的视频问题。
- 设计选择C（新数据集 + 更细描述）：没有高质量配对数据和细粒度描述，模型就学不到稳定的“文本 -> 全景视频”映射。

## 6. Mini Example Or Thought Experiment
### EN
- Example prompt: "A city under cloudy sky, with a car driving down the street."
- What standard T2V may do: generate a normal-view video with weak panorama structure; edge continuity is often poor.
- What 360DVD changes: adapter + enhancement modules push content toward panorama-friendly layout and motion, while keeping text alignment.
- Expected difference: better left-right continuity, broader scene coverage, and more plausible motion in ERP video space.

### ZH
- 示例提示词："A city under cloudy sky, with a car driving down the street."
- 普通文生视频可能表现：生成普通视角风格的视频，全景结构弱，边界连续性差。
- 360DVD 的改变：通过适配器和增强模块，让内容分布和运动更符合全景视频，同时保持文本对齐。
- 预期差异：左右连续性更好，场景覆盖更广，ERP 空间里的运动更合理。

## 7. Learning Path For This Week
### EN
- Day 1: Learn basics of diffusion and why AnimateDiff can extend T2I to T2V.
- Day 2-3: Read this paper in order: Abstract -> Introduction -> Method 3.3/3.4 -> Experiment 4.3/4.4.
- Day 4-5: Run a mini reproduction idea: compare baseline AnimateDiff output vs seam-enhanced output on one panorama prompt.
- Day 6: Inspect failure cases (seam artifacts, narrow FoV, motion mismatch) and map them to method modules.
- Day 7: Write your own 1-page summary with three columns: problem, design choice, observed gain.

### ZH
- 第1天：先补 diffusion 基础，并理解 AnimateDiff 如何把图像模型扩展到视频。
- 第2-3天：按顺序阅读：摘要 -> 引言 -> 方法 3.3/3.4 -> 实验 4.3/4.4。
- 第4-5天：做一个小对比实验：同一提示词下，比较基线 AnimateDiff 与带接缝增强策略的结果。
- 第6天：观察失败案例（接缝伪影、视野过窄、运动不合理），并对应到具体模块。
- 第7天：写一页自己的总结表：问题是什么、设计怎么改、效果提升在哪里。

## 8. Common Confusions And Self-Check Questions
### EN
- Confusion #1: "Is this just adding a new dataset?" Correction: No. Core changes include adapter design + panorama-specific enhancement + dataset/caption pipeline.
- Confusion #2: "If I train longer, baseline should solve it." Correction: Domain mismatch (geometry/motion/seam) is structural, not just training-time shortage.
- Self-check Q1: Can you explain why ERP left-right continuity is unique and why ordinary convolution padding can break it?
- Self-check Q2: Can you identify which module addresses global continuity and which addresses local/pixel-level continuity?

### ZH
- 误区1："这是不是只是多了个数据集？" 纠正：不是。核心还包括适配器结构、全景增强机制和描述构建流程。
- 误区2："只要把基线训练更久就能解决。" 纠正：全景的几何/运动/接缝问题是结构性错配，不只是训练时长不足。
- 自测问题1：你能解释 ERP 左右连续性为何是全景特有要求，以及普通卷积填充为什么会破坏它吗？
- 自测问题2：你能指出哪个模块主要解决全局连续性，哪个模块主要解决局部像素级连续性吗？
