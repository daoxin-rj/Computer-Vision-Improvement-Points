# L2 Master Version (EN/ZH)

## 1. Task Definition / 任务定义
### EN
- task setting: Reconstruct 3D face geometry from monocular images under in-the-wild conditions.
- evaluation protocol: Quantitative and qualitative comparison with existing 3D face reconstruction methods; paper also mentions a new benchmark focused on part overlap.

### ZH
- 任务设定：在真实场景单目图像下重建三维人脸几何。
- 评测协议：与现有 3D 人脸重建方法进行定量与定性对比，并引入关注部件重叠的新基准。

## 2. Baseline / 基线方法
### EN
- strongest baseline: 3DMM-based monocular reconstruction methods supervised by landmarks/silhouette rendering.
- baseline limitation: Sparse/inaccurate landmarks and renderer-based segmentation losses can be unstable and weak for extreme expressions.

### ZH
- 主要基线方法：基于 3DMM 的单目重建方法，常用关键点或轮廓渲染监督。
- 基线方法局限：关键点稀疏或不准，且基于渲染器的分割损失在极端表情下容易不稳定。

## 3. Core Innovation / 核心创新
### EN
- what is new: Part Re-projection Distance Loss (PRDL) based on segmentation-derived geometric distributions.
- why it is not just engineering tuning: PRDL changes the supervision formulation from pixel-silhouette rendering to anchor-based statistical distribution matching.

### ZH
- 核心新增点：基于分割几何分布的 Part Re-projection Distance Loss（PRDL）。
- 为什么不是仅工程调参：PRDL 将监督形式从像素轮廓渲染改为锚点统计分布匹配，属于机制层改动。

## 4. Method Modules / 方法模块拆解
### EN
- module_a: Convert facial part segmentation masks into 2D point sets.
- module_b: Reproject predicted 3D face geometry into image plane point sets.
- module_c: Compute anchor-based statistical distances between source and target sets to optimize reconstruction.

### ZH
- 模块A：将面部分割掩码转成二维点集。
- 模块B：将预测的三维人脸重投影到图像平面得到点集。
- 模块C：通过锚点统计距离比较源/目标点集并优化重建。

## 5. Why Effective / 为什么有效
### EN
- mechanism-level reasoning: Distribution-based geometric constraints provide smoother and clearer gradients, improving local component alignment under expression variation.

### ZH
- 机制层面的有效性解释：基于分布的几何约束可提供更平滑清晰的梯度，从而在表情变化下提升局部部件对齐。

## 6. Experimental Evidence / 实验证据
### EN
- main gains: The paper reports state-of-the-art reconstruction quality and better performance on expression-heavy cases.
- key ablations: PRDL is highlighted as the key contributor; full numerical tables are NOT_SPECIFIED in extracted text.
- boundary conditions: Performance depends on part segmentation reliability.

### ZH
- 主要收益：论文报告达到 SOTA 重建质量，并在强表情场景下更优。
- 关键消融结论：PRDL 被强调为关键收益来源，但完整数值表在当前抽取文本中为 NOT_SPECIFIED。
- 方法边界条件：方法性能依赖面部分割质量。

