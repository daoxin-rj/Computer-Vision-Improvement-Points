# L1 Beginner Version (EN/ZH)

## 1. Problem / 问题定义
### EN
The paper tries to rebuild a 3D face from one 2D image, especially when the person has difficult or extreme expressions.

### ZH
论文要解决的是：从单张 2D 图像重建 3D 人脸，特别是在表情夸张或困难情况下也能重建准确。

## 2. Why Old Methods Struggle / 旧方法为何困难
### EN
Many methods rely on sparse landmarks or silhouette rendering losses, which can be unstable and miss fine facial part geometry.

### ZH
很多方法依赖稀疏关键点或轮廓渲染损失，这些监督不够稳定，且容易忽略细粒度的面部部件几何。

## 3. New Idea / 新方法核心想法
### EN
The authors use facial part segmentation as geometric guidance and design PRDL, a point-distribution distance loss after reprojecting the 3D face back to 2D.

### ZH
作者把面部分割信息作为几何引导，提出 PRDL：将 3D 人脸重投影到 2D 后，用点集分布距离来监督重建。

## 4. Why It May Work Better / 为什么可能更有效
### EN
This supervision gives cleaner optimization signals and better local alignment for eyes, mouth, eyebrows, and other facial components.

### ZH
这种监督信号更清晰，能更好约束眼睛、嘴巴、眉毛等局部部件的对齐与形状。

## 5. Analogy / 直观类比
### EN
Instead of checking only the outer face outline, it checks many key regions inside the face map, like aligning multiple neighborhoods instead of just city borders.

### ZH
它不只检查人脸外轮廓，而是检查脸内多个关键区域，就像不是只看城市边界，而是把多个街区都对齐。

