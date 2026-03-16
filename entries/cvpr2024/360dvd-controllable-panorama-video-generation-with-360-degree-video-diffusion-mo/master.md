# L2 Master Version (EN/ZH)

## 1. Task Definition
### EN
- task setting: Text-guided controllable 360 panorama video generation.
- evaluation protocol: The paper reports comparative experiments for quality and effectiveness; exact metric details are NOT_SPECIFIED in the extracted abstract text.

### ZH
- 任务设定：文本引导、可控的 360 全景视频生成。
- 评测协议：论文给出了效果对比与有效性实验，但从当前抽取的摘要文本中无法获得完整指标细节（NOT_SPECIFIED）。

## 2. Baseline
### EN
- strongest baseline: Pretrained standard text-to-video diffusion methods.
- baseline limitation: Domain mismatch between perspective videos and equirectangular panorama videos causes degraded quality and motion/content inconsistency.

### ZH
- 主要基线方法：预训练的标准文生视频扩散方法。
- 基线方法局限：普通透视视频域与等距矩形全景视频域存在偏差，导致质量下降和内容/运动不一致。

## 3. Core Innovation
### EN
- what is new: A 360-Adapter plus 360 enhancement techniques and a new captioned dataset (WEB360) for panorama adaptation.
- why it is not just engineering tuning: The method explicitly models panorama-specific geometry and continuity issues instead of only retuning generic hyperparameters.

### ZH
- 核心新增点：提出 360-Adapter、360 增强策略，并构建新的带文本标注全景数据集 WEB360 用于适配。
- 为什么不是仅工程调参：方法显式建模全景几何与边界连续性问题，而不只是对通用参数做微调。

## 4. Method Modules
### EN
- module_a: Lightweight 360-Adapter on top of pretrained T2V diffusion model.
- module_b: 360 enhancement mechanisms, including latitude-aware loss and boundary continuity handling.
- module_c: WEB360 panorama video-text dataset and caption fusion strategy for training.

### ZH
- 模块A：在预训练文生视频扩散模型上叠加轻量 360-Adapter。
- 模块B：360 增强机制，包括纬度感知损失与边界连续性处理。
- 模块C：用于训练的 WEB360 全景视频-文本数据与文本融合策略。

## 5. Why Effective
### EN
- mechanism-level reasoning: Parameter-efficient adaptation preserves pretrained generative priors while injecting panorama-specific inductive bias for ERP geometry.

### ZH
- 机制层面的有效性解释：参数高效适配保留了预训练先验，同时为 ERP 几何注入了全景特定归纳偏置。

## 6. Experimental Evidence
### EN
- main gains: The paper claims superior panorama video generation quality and effectiveness versus prior T2V approaches.
- key ablations: Adapter and panorama-specific components are reported as important, but full numeric ablations are NOT_SPECIFIED in available extracted text.
- boundary conditions: Performance likely depends on panorama data quality and coverage.

### ZH
- 主要收益：论文声称相较既有文生视频方法在全景生成质量和有效性上更优。
- 关键消融结论：文中强调适配器与全景专用组件有效，但完整数值消融在当前抽取文本中为 NOT_SPECIFIED。
- 方法边界条件：效果很可能依赖全景数据质量与覆盖范围。

