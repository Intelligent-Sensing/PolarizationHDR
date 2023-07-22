---
layout: default
---

A simple yet effective approach for turning a polarization camera into a snapshot HDR camera.

This project was selected for a poster and demo at [ICCP 2023](https://iccp2023.iccp-conference.org).

[![secret_sauce.png](/assets/img/secret_sauce.png)](/assets/img/secret_sauce.png)


# Abstract

High dynamic range (HDR) images are important for a range of tasks, from navigation to consumer photography. 
Accordingly, a host of specialized HDR sensors have been developed, the most successful of which are based on capturing variable per-pixel exposures. In essence, these methods capture an entire exposure bracket sequence at once in a single shot. This paper presents a straightforward but highly effective approach for turning an off-the-shelf polarization camera into a high-performance HDR camera. By placing a linear polarizer in front of the polarization camera, we are able to simultaneously capture four images with varied exposures, which are determined by the orientation of the polarizer. We develop an outlier-robust and self-calibrating algorithm to reconstruct an HDR image (at a single polarity) from these measurements. Finally, we demonstrate the efficacy of our approach with extensive real-world experiments.

# Method

The intensity of light observed through two polarizers $$I$$ is linearly dependent on the cosine squared of the angle $$\theta$$ between the polarizers. In other words, as the polarizers’ angles become more orthogonal, they transmit less of the incident light $$I_0$$ (and vice-versa).

$$ I(\theta) = I_0\text{cos}^2(\theta) $$

Fusing together the 4 images captured by the polarization camera, we obtain an HDR image $$H$$.
Similar to classical HDR methods, we use a weighted sum to merge the images where the weights $$w_i$$ are determined by the exposure time of each image. 

$$ H = \frac{\sum(w_i\circ I(\theta_i)) }{ \sum w_i} $$

However, our method uses one exposure setting to simultaneously capture all 4 images, so exposure time we cannot use exposure time to determine $$w_i$$. Instead, we estimate the relative brightness of each image and use those values as the weights. 
Relative brightness $$B$$ for an image is defined as the mode of the image's pixel values scaled by a factor of $$\frac{1}{\text{brightest image}}$$.

$$ B_i = \text{mode}\left(\frac{I(\theta_i)}{I(\theta_{\text{brightest}})}\right) $$


[![histogram.png](/assets/img/histogram.png)](/assets/img/histogram.png)


# Results

We reconstruct HDR images of a diverse set of natural scenes from snapshots taken with a polarization camera.


[![results.png](/assets/img/results.png)](/assets/img/results.png)