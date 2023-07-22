import numpy as np
import cv2
from utils import uniform_weights, normalize
import os

################
# FILE FORMAT #
################
# {data_dir}/{exposure time}_{angle}.npy
# e.g. indoor/10000_90µ.npy


def et_sort(my_tup):
    my_tup.sort(key=lambda x: x[1])
    return my_tup


def save_reference(captures, out_dir):
    print("Generating the ground truth result.")
    captures = et_sort(captures)

    img_list = []
    weights_batch = []
    exposure_list = []
    for i, capture in enumerate(captures):
        img, et, angle = capture

        if i == 0:
            margin = (30, 255)
        elif i == len(captures) - 1:
            margin = (0, 235)
        else:
            margin = (15, 235)
        weight = uniform_weights(img, margin[0], margin[1])

        img_list.append(img)
        weights_batch.append(weight)
        exposure_list.append(et * 1.8)

    img_list = np.stack(img_list)
    weights_batch = np.stack(weights_batch)
    exposure_list = np.array(exposure_list)

    ldr_scaled = [img_list[i] / exposure_list[i] for i in range(len(img_list))]

    epsilon = 1e-6
    hdr = np.sum(weights_batch * ldr_scaled, axis=0) / (
        np.sum(weights_batch, axis=0) + epsilon
    )

    tonemap = cv2.createTonemapReinhard(0.5, 3, 0.5, 0)
    hdr_tonemapped = tonemap.process(hdr.astype(np.float32))
    hdr_tonemapped = cv2.cvtColor(hdr_tonemapped, cv2.COLOR_BGR2RGB)
    hdr_tonemapped = normalize(hdr_tonemapped)
    hdr_tonemapped_8_bit = cv2.cvtColor((hdr_tonemapped * 255), cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(out_dir, "reference.png"), hdr_tonemapped_8_bit)
    return hdr_tonemapped_8_bit
