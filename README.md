# Snapshot HDR Imaging with a Polarization Camera
> Mingyang Xie*, Matthew Chan*, Christopher Metzler

Code for paper "Snapshot HDR Imaging with a Polarization Camera" by Mingyang Xie, Matthew Chan, and Christopher Metzler.

**UPDATE**: We've released an accompanying [project page](https://intelligent-sensing.github.io/polarization-hdr/) for this paper.

## Installation

Run the following commands to install the required packages.
```bash
conda create -n polarization-hdr python=3.9
conda activate polarization-hdr
pip install -r requirements.txt
```

**NOTE**: Matlab/2019b or newer is required to compute HDR-VDP metrics.

## Dataset
We provide the dataset used in our paper. Please download the dataset from [here](https://drive.google.com/drive/folders/1rN8B11976k9330NZEGnEkuDfvFG0rdz5?usp=sharing) and unzip it. 

RAW images follow the naming convention `<exposure_time>_<polarization_angle>.raw`. For example, `1000_0.raw` is a RAW image captured with an exposure time of 1000 µs and a polarization angle of 0 degrees. 

(Note: Some files are prefixed with `up-`. These images were captured without the additional linear polarizer attached.)

## Usage

Place the dataset (or your own dataset) in the folder `DATA_DIR/SCENE_NAME` and set up an output directory `OUT_DIR`.

Run the following command to generate ground truth, ExposureFusion, and our HDR reconstructions.
```bash
python start_experiment.py DATA_DIR/SCENE_NAME GT_ANGLE BASELINE_EXPOSURE_TIME OUT_DIR
```
Arguments:
- Specify the directory `DATA_DIR/SCENE_NAME` containing RAW images.
- Specify which polarization angle `GT_ANGLE` to reconstruct the ground truth HDR image with (valid options are [0, 45, 90, 135]).
- Specify which exposure time `BASELINE_EXPOSURE_TIME` to use for the our method and the ExposureFusion baseline. The value provided must match the <exposure_time> of an image in `DATA_DIR/SCENE_NAME`
- Specify the directory `OUT_DIR` to dump the HDR results to.

### Example

The following command will generate HDR images for the helicopter scene. The ground truth HDR image will be reconstructed using 135º polarization images. Our method and the ExposureFusion baseline will be reconstructed using the 61222 µs exposure time images. 
```bash
python start_experiment.py data/window 135 357046 out/window
```