# L3 Research And Reproduction Guide (EN/ZH)

## 1. Formal Problem Setup
### EN
- Objective: learn a conditional diffusion generator for ERP panorama video \(x_{1:N}\) given text prompt \(y\) and optional motion condition \(c\).
- Target behavior:
  - preserve text semantic alignment,
  - produce temporally coherent video frames,
  - satisfy panorama-specific continuity and motion distribution.
- Scope in this paper:
  - adaptation from pretrained SD/AnimateDiff-style backbone,
  - focus on controllable generation under panorama domain shift.

### ZH
- 目标：学习一个条件扩散生成器，在给定文本提示 \(y\) 与可选运动条件 \(c\) 时生成 ERP 全景视频 \(x_{1:N}\)。
- 期望行为：
  - 保持文本语义对齐，
  - 保持跨帧时序连贯，
  - 满足全景特有的连续性和运动分布约束。
- 本文范围：
  - 基于预训练 SD/AnimateDiff 路线进行适配，
  - 重点解决全景域偏移下的可控生成。

## 2. Notation And Data Representation
### EN
- \(x_{1:N}\): video clip with N frames.
- \(z_{1:N}\): latent representation encoded from \(x_{1:N}\) via pretrained VAE encoder.
- \(z_t\): noisy latent at diffusion step \(t\).
- \(y\): text prompt; encoded by CLIP text encoder.
- \(c\): motion condition tensor (paper uses panorama optical flow estimator).
- \(F_{360}(c)\): 360-Adapter output multi-scale features \(f_{360}^{1..4}\).
- ERP layout:
  - width:height ratio around 2:1 in image space,
  - wrap-around continuity required between left/right boundaries.

### ZH
- \(x_{1:N}\)：含 N 帧的视频片段。
- \(z_{1:N}\)：通过预训练 VAE 编码器从 \(x_{1:N}\) 得到的潜变量。
- \(z_t\)：扩散第 \(t\) 步的加噪潜变量。
- \(y\)：文本提示，由 CLIP 文本编码器编码。
- \(c\)：运动条件张量（文中使用全景光流估计器得到）。
- \(F_{360}(c)\)：360-Adapter 输出的多尺度特征 \(f_{360}^{1..4}\)。
- ERP 表示特点：
  - 图像空间宽高比约为 2:1，
  - 左右边界必须满足环绕连续性。

## 3. Objective/Formulation
### EN
- Base denoising objective (paper Eq. 6 form):
  - train denoiser \(\epsilon_\theta\) to predict diffusion noise from \((z_t, t, text, adapter\_features)\).
- Adapter-conditioned prediction:
  - \(f_{360}=F_{360}(c)\),
  - denoiser input includes \(f_{360}\) injected into U-Net encoder scales.
- Latitude-aware weighted loss (paper Eq. 9/10 concept):
  - reweight denoising error with latitude-dependent matrix \(W\),
  - assigns larger weights to lower/middle latitude regions with lower perceptual distortion.
- Missing details to note:
  - full symbolic derivation and all implementation constants for every loss variant are not exhaustively expanded in the main paper.

### ZH
- 基础去噪目标（对应论文 Eq. 6 形式）：
  - 训练去噪器 \(\epsilon_\theta\)，从 \((z_t, t, text, adapter\_features)\) 预测噪声。
- 适配器条件注入：
  - \(f_{360}=F_{360}(c)\)，
  - 去噪 U-Net 在编码器多尺度接收 \(f_{360}\)。
- 纬度感知加权损失（对应论文 Eq. 9/10 思路）：
  - 使用与纬度相关的权重矩阵 \(W\) 重加权去噪误差，
  - 对低/中纬度区域赋予更高权重以改善感知质量。
- 需明确的缺失项：
  - 主文未完整展开所有损失变体的全符号推导与全部实现常数细节。

## 4. Architecture And Information Flow
### EN
- Backbone:
  - SD v1.5 latent diffusion + AnimateDiff temporal modules as pretrained priors.
  - Most backbone weights are frozen during 360 adaptation.
- 360-Adapter structure:
  - condition tensor is downsampled via pixel unshuffle,
  - stacked adapter blocks with 2D conv + pseudo-3D residual operations,
  - first three blocks include downsampling to align with U-Net scale hierarchy.
- Feature injection:
  - adapter outputs multi-scale features \(f^1..f^4_{360}\),
  - each is additively fused into corresponding U-Net encoder feature map \(f^i_{enc}\).
- Enhancement path:
  - latent rotation and circular padding are applied for continuity handling in inference/training strategy.

### ZH
- 主干：
  - SD v1.5 潜空间扩散 + AnimateDiff 时序模块作为预训练先验，
  - 360 适配阶段大部分主干参数冻结。
- 360-Adapter 结构：
  - 条件张量先经 pixel unshuffle 下采样，
  - 由 2D 卷积 + pseudo-3D 残差结构组成多级适配块，
  - 前三级含下采样以对齐 U-Net 多尺度层级。
- 特征注入：
  - 适配器输出多尺度特征 \(f^1..f^4_{360}\)，
  - 与对应编码器特征 \(f^i_{enc}\) 做逐尺度相加融合。
- 增强路径：
  - 在训练/推理策略中引入潜变量旋转与圆周填充以处理连续性问题。

## 5. End-to-End Algorithm
### EN
- Training algorithm (high level):
  1. Sample panorama clip \(x_{1:N}\) and caption \(y\) from WEB360.
  2. Encode clip into latent \(z_{1:N}\), sample diffusion timestep \(t\), add noise -> \(z_t\).
  3. Estimate motion condition \(c\) (optical flow pipeline).
  4. With probability \(P\), replace \(c\) by zeros for condition-drop robustness.
  5. Compute adapter features \(f_{360}=F_{360}(c)\), inject into U-Net encoder.
  6. Predict noise and optimize weighted denoising objective (with latitude-aware weighting).
  7. Apply data-level random horizontal rotation augmentation for ERP consistency.
- Inference algorithm (high level):
  1. Initialize noise latent.
  2. For each denoising step, optionally rotate latent/condition by fixed angle.
  3. In late denoising half, enable circular padding to improve boundary continuity.
  4. Decode final latent via pretrained VAE decoder to panorama video.

### ZH
- 训练流程（高层）：
  1. 从 WEB360 采样全景片段 \(x_{1:N}\) 与描述 \(y\)。
  2. 编码为潜变量 \(z_{1:N}\)，采样时间步 \(t\)，加噪得到 \(z_t\)。
  3. 估计运动条件 \(c\)（光流流程）。
  4. 以概率 \(P\) 将 \(c\) 置零，提升无条件输入鲁棒性。
  5. 计算适配器特征 \(f_{360}=F_{360}(c)\)，注入 U-Net 编码器。
  6. 预测噪声并优化加权去噪目标（含纬度感知权重）。
  7. 训练阶段进行随机水平旋转增强，强化 ERP 连续性学习。
- 推理流程（高层）：
  1. 从随机噪声潜变量开始。
  2. 每步去噪时可对潜变量/条件执行固定角度旋转。
  3. 在后半程去噪启用圆周填充，改善边界连续性。
  4. 最终通过预训练 VAE 解码得到全景视频。

## 6. Training Recipe
### EN
- Data:
  - WEB360 with about 2,114 text-video pairs,
  - videos in ERP format, HD-level source clips, single-scene clipping process described in paper.
- Captioning:
  - BLIP on projected perspective views + GPT-assisted fusion (360 Text Fusion).
- Model setup:
  - base: Stable Diffusion v1.5 + Motion Module v14,
  - trainable component focus: 360-Adapter (backbone mostly frozen).
- Hyperparameters (reported):
  - resolution 512 x 1024,
  - frame length 16,
  - batch size 1,
  - learning rate 1e-5,
  - training steps 100k,
  - condition-drop probability \(P=0.2\),
  - beta schedule: start 0.00085, end 0.012.
- Compute note:
  - exact wall-clock and hardware profile are not fully enumerated in the main paper text.

### ZH
- 数据：
  - WEB360 约 2,114 对文-视频数据，
  - ERP 格式，论文描述了高质量片段筛选与单场景切分流程。
- 描述构建：
  - 对投影视角用 BLIP 描述，再通过 GPT 融合（360 Text Fusion）。
- 模型设置：
  - 基座：Stable Diffusion v1.5 + Motion Module v14，
  - 训练重点：360-Adapter（主干大多冻结）。
- 论文给出的超参数：
  - 分辨率 512 x 1024，
  - 帧长 16，
  - batch size 1，
  - 学习率 1e-5，
  - 训练 100k steps，
  - 条件丢弃概率 \(P=0.2\)，
  - beta 调度：start 0.00085，end 0.012。
- 算力说明：
  - 主文未完整给出详细硬件配置与总训练耗时。

## 7. Inference Recipe
### EN
- Inputs:
  - required: text prompt,
  - optional: motion condition map (optical flow-like control).
- Sampling:
  - DDIM with 25 steps,
  - text guidance scale 7.5.
- Continuity controls:
  - latent rotation angle set to \(\pi/2\),
  - circular padding enabled in late \(T/2\) denoising steps.
- Output:
  - panorama video decoded at 512 x 1024 in reported experiments,
  - optional downstream super-resolution if needed.

### ZH
- 输入：
  - 必选：文本提示，
  - 可选：运动条件图（类似光流控制）。
- 采样：
  - DDIM 25 步，
  - 文本引导系数 7.5。
- 连续性控制：
  - 潜变量旋转角为 \(\pi/2\)，
  - 在后 \(T/2\) 去噪阶段启用圆周填充。
- 输出：
  - 论文实验主要在 512 x 1024 分辨率，
  - 若业务需要可接后续超分模块。

## 8. Ablation Logic
### EN
- Hypothesis H1: Better caption granularity improves generation fidelity.
  - Test: remove 360 Text Fusion -> paper reports weaker semantic detail.
- Hypothesis H2: Temporal-aware pseudo-3D adapter operation improves frame stability.
  - Test: remove pseudo-3D layer -> reported flickering increases.
- Hypothesis H3: Latitude-aware loss improves panorama realism and clarity.
  - Test: remove latitude-aware weighting -> quality drops in FoV/clarity aspects.
- Interpretation:
  - gains are distributed across data quality, temporal modeling, and geometry-aware objective design.

### ZH
- 假设 H1：更细粒度描述能提升生成保真度。
  - 验证：去掉 360 Text Fusion -> 论文报告语义细节下降。
- 假设 H2：含时序建模的 pseudo-3D 适配层能提升跨帧稳定性。
  - 验证：去掉 pseudo-3D 层 -> 闪烁更明显。
- 假设 H3：纬度感知损失能提升全景真实感和清晰度。
  - 验证：去掉纬度加权 -> FoV/清晰度等方面下降。
- 解释：
  - 性能提升来自数据质量、时序建模、几何感知目标设计三方面协同。

## 9. Reproduction Checklist
### EN
- [ ] Lock environment and dependency versions (diffusion stack, CUDA, xformers if used).
- [ ] Verify backbone checkpoint parity (SD v1.5 + matching AnimateDiff motion module).
- [ ] Reconstruct WEB360 data pipeline (source selection, clip filtering, ERP formatting).
- [ ] Reproduce captioning pipeline (projection views + BLIP + fusion strategy).
- [ ] Confirm motion condition estimator is panorama-compatible and preprocessing is consistent.
- [ ] Implement adapter insertion at correct U-Net scales.
- [ ] Match loss weighting (including latitude-aware matrix definition).
- [ ] Match training schedule and condition-drop probability \(P=0.2\).
- [ ] Reproduce inference controls (DDIM steps, guidance scale, latent rotation, circular padding schedule).
- [ ] Evaluate with both generic video criteria and panorama-specific criteria.
- [ ] Compare against at least two baselines (native AnimateDiff, panorama LoRA variant).
- [ ] Record failure cases and classify by seam/content/motion category.

### ZH
- [ ] 锁定环境与依赖版本（diffusion 相关栈、CUDA、xformers 等）。
- [ ] 确认基座权重一致（SD v1.5 + 对应 AnimateDiff motion module）。
- [ ] 复现 WEB360 数据流程（来源筛选、片段切分、ERP 格式化）。
- [ ] 复现描述构建流程（多视角投影 + BLIP + 融合策略）。
- [ ] 确认运动条件估计器与全景输入兼容，且预处理一致。
- [ ] 在正确的 U-Net 尺度位置插入适配器。
- [ ] 对齐损失加权实现（含纬度权重矩阵定义）。
- [ ] 对齐训练日程与条件丢弃概率 \(P=0.2\)。
- [ ] 对齐推理控制（DDIM 步数、引导系数、旋转与圆周填充时序）。
- [ ] 同时用通用视频指标和全景专项指标评估。
- [ ] 至少与两个基线对比（原始 AnimateDiff、全景 LoRA 版本）。
- [ ] 记录失败案例，并按接缝/内容分布/运动模式分类。

## 10. Failure Modes And Debug Order
### EN
- Failure mode #1: severe left-right seam discontinuity.
  - Quick test: visualize first/last columns across frames and check temporal seam drift.
- Failure mode #2: strong flicker despite prompt alignment.
  - Quick test: disable/enable pseudo-3D branch and compare frame-to-frame optical consistency.
- Failure mode #3: panorama layout resembles narrow perspective video.
  - Quick test: inspect caption quality and data domain mix; verify WEB360 preprocessing.
- Recommended debug order:
  1. data and caption pipeline parity,
  2. adapter insertion correctness,
  3. loss weighting correctness,
  4. inference continuity controls (rotation + circular padding),
  5. baseline sanity comparison before long retraining.

### ZH
- 失败模式1：左右接缝严重不连续。
  - 快速排查：可视化每帧首尾列并检查接缝随时间漂移情况。
- 失败模式2：文本对齐尚可但跨帧闪烁明显。
  - 快速排查：对比关闭/开启 pseudo-3D 分支时的帧间一致性。
- 失败模式3：全景布局退化为普通窄视角视频。
  - 快速排查：检查描述质量与数据域分布，核对 WEB360 预处理一致性。
- 推荐调试顺序：
  1. 先对齐数据与描述流程，
  2. 再核查适配器插入位置与形状，
  3. 再核查损失加权实现，
  4. 再调试推理连续性控制（旋转 + 圆周填充），
  5. 最后与基线做 sanity check 再进入长时间重训。
