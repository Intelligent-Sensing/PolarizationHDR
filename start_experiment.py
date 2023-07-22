import numpy as np
import sys
import cv2
import glob
import os
from multi_exposure import save_reference
from ours import save_ours
from baseline_mertens import save_mertens
import subprocess
from natsort import natsorted

# Input arguments
data_dir = sys.argv[1]  # Get the input file directory
gt_angle = int(sys.argv[2])  # Angle (e.g. 135º) used to construct the gt
assert gt_angle in [0, 45, 90, 135], f"{gt_angle} is not a valid angle."
baseline_et = int(sys.argv[3])  # Exposure stack used to run baselines
out_dir = sys.argv[4]


# Parse exposure time and polarization angle from filename
def get_info(fname):
    i1 = fname.rfind("/")
    i2 = fname.rfind("_")
    i3 = fname.find(".raw")
    et = int(fname[i1 + 1 : i2])
    angle = int(fname[i2 + 1 : i3])
    return (fname, et, angle)


baseline_captures = []
gt_captures = []
mertens_captures = []

# Demosaic RAW images
fnames = natsorted(glob.glob(os.path.join(data_dir, "*.raw")))
for fname in fnames:
    imrows, imcols = 1024, 1224
    imsize = imrows * imcols
    with open(fname, "rb") as rawimage:
        fname, et, angle = get_info(fname)
        img = np.fromfile(rawimage, np.dtype("u1"), imsize).reshape((imrows, imcols))
        colour = cv2.cvtColor(img, cv2.COLOR_BAYER_BG2BGR)
        # Save the demosaiced image
        # np.save(fname.replace(".raw", ".npy"), colour)
        # cv2.imwrite(fname.replace(".raw", ".png"), colour)
        if et == baseline_et:
            baseline_captures.append(colour)
        if angle == gt_angle:
            gt_captures.append((colour, et, angle))
            mertens_captures.append(colour)

# Save ground truth and baseline results
gt_hdr = save_reference(gt_captures, out_dir)
ours_hdr = save_ours(baseline_captures, out_dir)
mertens_hdr = save_mertens(mertens_captures, out_dir, False)

# Generate HDR-VDP results
subprocess.call(
    [
        "bash",
        "hdrvdp3/compare.sh",
        "../../" + os.path.join(out_dir, "reference.png"),
        "../../" + os.path.join(out_dir, "ours.png"),
        "../../" + os.path.join(out_dir, "hdrvdp_ours.png"),
    ]
)
subprocess.call(
    [
        "bash",
        "hdrvdp3/compare.sh",
        "../../" + os.path.join(out_dir, "reference.png"),
        "../../" + os.path.join(out_dir, "mertens.png"),
        "../../" + os.path.join(out_dir, "hdrvdp_mertens.png"),
    ]
)
