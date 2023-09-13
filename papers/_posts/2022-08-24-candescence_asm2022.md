---
layout: paper
title: "A Deep Learning Approach to Capture the Essence of Candida albicans Morphologies"
image: /assets/images/papers/candescence_asm2022.jpg
authors: Van Bettauer, Anna Carolina Borges Pereira Costa, Raha P Omran, Samira Massahi, Eftyhios Kirbizakis, Shawn Simpson, Vanessa Dumeaux, Chris Law, Malcolm Whiteway, Michael T Hallett.
ref: Bettauer et al. 2022. Microb Spectrum
journal: "Microbiology Spectrum (2022)"
pdf: /assets/pdfs/papers/candescence_asm2022.pdf
doi: 10.1128/spectrum.01472-22
abbrev: "Microb Spectrum (2022)"
pub_year: 2022
---

<br />
<div data-badge-popover="right" data-badge-type="donut" data-hide-no-mentions="true" class="altmetric-embed"></div>

# Abstract

We present deep learning-based approaches for exploring the complex array of morphologies exhibited by the opportunistic human pathogen Candida albicans. Our system, entitled Candescence, automatically detects C. albicans cells from differential image contrast microscopy and labels each detected cell with one of nine morphologies. This ranges from yeast white and opaque forms to hyphal and pseudohyphal filamentous morphologies. The software is based upon a fully convolutional one-stage (FCOS) object detector, a deep learning technique that uses an extensive set of images that we manually annotated with the location and morphology of each cell. We developed a novel cumulative curriculum-based learning strategy that stratifies our images by difficulty from simple yeast forms to complex filamentous architectures. Candescence achieves very good performance (~85% recall; 81% precision) on this difficult learning set, where some images contain hundreds of cells with substantial intermixing between the predicted classes. To capture the essence of each C. albicans morphology and how they intermix, we used a second technique from deep learning entitled generative adversarial networks. The resultant models allow us to identify and explore technical variables, developmental trajectories, and morphological switches. Importantly, the model allows us to quantitatively capture morphological plasticity observed with genetically modified strains or strains grown in different media and environments. We envision Candescence as a community meeting point for quantitative explorations of C. albicans morphology.
**Importance:** The fungus Candida albicans can “shape shift” between 12 morphologies in response to environmental variables. The cytoprotective capacity provided by this polymorphism makes C. albicans a formidable pathogen to treat clinically. Microscopy images of C. albicans colonies can contain hundreds of cells in different morphological states. Manual annotation of images can be difficult, especially as a result of densely packed and filamentous colonies and of technical artifacts from the microscopy itself. Manual annotation is inherently subjective, depending on the experience and opinion of annotators. Here, we built a deep learning approach entitled Candescence to parse images in an automated, quantitative, and objective fashion: each cell in an image is located and labeled with its morphology. Candescence effectively replaces simple rules based on visual phenotypes (size, shape, and shading) with neural circuitry capable of capturing subtle but salient features in images that may be too complex for human annotators.