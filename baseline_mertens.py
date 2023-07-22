import cv2
import numpy as np
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"


def save_mertens(img_list, save_dir, tonemap=False):
    print("Generating the exposure fusion baseline result.")
    # Exposure fusion using Mertens
    merge_mertens = cv2.createMergeMertens(
        contrast_weight=0.0, saturation_weight=0.0, exposure_weight=1.0
    )
    res_mertens = merge_mertens.process(img_list)

    # Optional tone-mapping
    if tonemap:
        tonemap1 = cv2.createTonemapReinhard(1.5, 0, 0, 0)
        # hdr_tonemapped = tonemap.process(hdr.astype(np.float32))
        # tonemap1 = cv2.createTonemap(gamma=2.2)
        res_mertens = tonemap1.process(res_mertens.copy())
        # print(np.amin(res_mertens), np.amax(res_mertens))

    res_mertens_8bit = np.clip(res_mertens * 255, 0, 255).astype("uint8")
    cv2.imwrite(os.path.join(save_dir, "mertens.png"), res_mertens_8bit)
    return res_mertens_8bit


# if __name__ == "__main__":
#     input_dir = sys.argv[1]
#     src_contents = os.walk(input_dir)
#     fnames = next(src_contents)[2]
#     fnames = list(filter(lambda x: ".npy" in x, fnames))

#     # Read all 4 polarization images (1 channel)
#     image_files = sorted([os.path.join(input_dir, name) for name in fnames])
#     print(image_files)
#     img_list = np.asarray([np.load(fn) for fn in image_files])
#     print(img_list.shape, np.amin(img_list), np.amax(img_list))

#     output_path = sys.argv[2]
#     run_mertens(output_path, img_list, False)
