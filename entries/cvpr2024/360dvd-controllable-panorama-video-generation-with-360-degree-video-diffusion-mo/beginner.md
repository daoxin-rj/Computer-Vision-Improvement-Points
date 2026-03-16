# L1 Beginner Version (EN/ZH)

## 1. Problem
### EN
This paper tries to generate 360-degree panorama videos from text prompts, because real 360 video capture is expensive and hard to scale.

### ZH
这篇论文要解决的是：根据文本提示直接生成 360 度全景视频，因为真实全景视频拍摄成本高、难以规模化。

## 2. Why Old Methods Struggle
### EN
Regular text-to-video models are trained for normal perspective videos, not panoramic videos. They often fail on panoramic geometry and boundary continuity.

### ZH
常规文生视频模型主要面向普通视角视频，不是为全景视频设计，容易在全景几何和边界连续性上出错。

## 3. New Idea
### EN
The authors add a lightweight 360-Adapter and panorama-specific enhancement losses to a pretrained text-to-video diffusion model, then train on a new panorama video-text dataset (WEB360).

### ZH
作者在预训练文生视频扩散模型上加入轻量 360-Adapter 和全景专用增强损失，再用新的全景视频-文本数据集 WEB360 进行训练。

## 4. Why It May Work Better
### EN
It reuses strong pretrained generation ability, while adding only the extra components needed for panoramic structure and continuity.

### ZH
该方法保留了预训练模型的强生成能力，同时只增加解决全景结构与连续性问题所需的关键模块。

## 5. Analogy
### EN
It is like adapting a normal camera video editor to work with globe-style videos by adding a special panoramic correction plugin instead of rebuilding the whole editor.

### ZH
这就像给普通视频编辑器加一个“全景校正插件”，让它能处理地球仪式全景视频，而不是从零重做整个编辑器。

