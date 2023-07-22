import numpy as np
import os
from utils import uniform_weights, normalize
import cv2
import matplotlib.pyplot as plt
import copy


def exp_sort(my_tup):
    my_tup.sort(key=lambda x: np.average(x))
    return my_tup


def exposure_ratio(img1_tuple, img2_tuple):
    img1, margin1 = img1_tuple
    img2, margin2 = img2_tuple
    mask1 = uniform_weights(img1, margin1[0], margin1[1])
    mask2 = uniform_weights(img2, margin2[0], margin2[1])

    ratio = (img1 / img2) * (mask1 * mask2)

    ratio_masked = ratio[(mask1 * mask2) == 1]
    ratio_masked = ratio_masked[~np.isinf(ratio_masked)]
    ratio_masked = ratio_masked[~np.isnan(ratio_masked)]
    counts, bins = np.histogram(
        ratio_masked.flatten(),
        bins=200,
        range=None,
        weights=None,
        density=None,
    )
    ratio_mode = bins[counts.argmax()]

    visualize = False
    if visualize:
        ratio_temp = copy.copy(ratio[..., 0])
        ratio_temp[(mask1[..., 0] * mask2[..., 0]) == 0] = 0
        ratio_temp[np.isinf(ratio_temp)] = 0
        ratio_temp[np.isnan(ratio_temp)] = 0
        ratio_temp = normalize(ratio_temp)
        plt.imshow(((ratio_temp) * 255).astype(int))
        plt.title("I_45 / I_135")
        plt.colorbar()
        # plt.savefig("scratch/division.pdf", format="pdf", bbox_inches="tight");
        plt.show()
        plt.stairs(counts, bins)
        plt.title("Histogram")
        # plt.savefig("scratch/histogram.pdf", format="pdf", bbox_inches="tight");
        plt.show()

    return ratio_mode


def save_ours(img_list, out_dir):
    print("Generating our result.")
    # img_list = [np.load(fname) for fname in fnames]
    img_list = exp_sort(img_list)

    brightest_img = img_list[-1]
    brightest_margin = (0, 235)
    weights_batch = []
    exposure_list = []
    for i, img in enumerate(img_list):
        if i == 0:
            margin = (30, 255)
        elif i == len(img_list) - 1:
            margin = brightest_margin
        else:
            margin = (15, 235)
        weight = uniform_weights(img, margin[0], margin[1])
        weights_batch.append(weight)
        ratio = exposure_ratio((img, margin), (brightest_img, brightest_margin))
        exposure_list.append(ratio)
    weights_batch = np.array(weights_batch)

    epsilon = 1e-6
    ldr_scaled = [img_list[i] / exposure_list[i] for i in range(len(img_list))]
    hdr = np.sum(weights_batch * ldr_scaled, axis=0) / (
        np.sum(weights_batch, axis=0) + epsilon
    )
    tonemap = cv2.createTonemapReinhard(0.5, 3, 0.5, 0)
    hdr_tonemapped = tonemap.process(hdr.astype(np.float32))
    hdr_tonemapped = cv2.cvtColor(hdr_tonemapped, cv2.COLOR_BGR2RGB)
    hdr_tonemapped = normalize(hdr_tonemapped)
    hdr_tonemapped_8_bit = cv2.cvtColor((hdr_tonemapped * 255), cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(out_dir, "ours.png"), hdr_tonemapped_8_bit)
    return hdr_tonemapped_8_bit
