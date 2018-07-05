# Single-Shot Refinement Neural Network for Object Detection

[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)

By [Shifeng Zhang](http://www.cbsr.ia.ac.cn/users/sfzhang/), [Longyin Wen](http://www.cbsr.ia.ac.cn/users/lywen/), [Xiao Bian](https://sites.google.com/site/cvbian/), [Zhen Lei](http://www.cbsr.ia.ac.cn/users/zlei/), [Stan Z. Li](http://www.cbsr.ia.ac.cn/users/szli/).

### Introduction

We propose a novel single-shot based detector, called RefineDet, that achieves better accuracy than two-stage methods and maintains comparable efficiency of one-stage methods. You can use the code to train/evaluate the RefineDet method for object detection. For more details, please refer to our [paper](https://arxiv.org/pdf/1711.06897.pdf).

<p align="left">
<img src="https://github.com/sfzhang15/RefineDet/blob/master/refinedet_structure.jpg" alt="RefineDet Structure" width="777px">
</p>

| System | VOC2007 test *mAP* | **FPS** (Titan X) | Number of Boxes | Input resolution
|:-------|:-----:|:-------:|:-------:|:-------:|
| [Faster R-CNN (VGG16)](https://github.com/ShaoqingRen/faster_rcnn) | 73.2 | 7 | ~6000 | ~1000 x 600 |
| [YOLO (GoogLeNet)](http://pjreddie.com/darknet/yolo/) | 63.4 | 45 | 98 | 448 x 448 |
| [YOLOv2 (Darknet-19)](http://pjreddie.com/darknet/yolo/) | 78.6 | 40 | 1445 | 544 x 544 |
| [SSD300* (VGG16)](https://github.com/weiliu89/caffe/tree/ssd) | 77.2 | 46 | 8732 | 300 x 300 |
| [SSD512* (VGG16)](https://github.com/weiliu89/caffe/tree/ssd) | 79.8 | 19 | 24564 | 512 x 512 |
| RefineDet320 (VGG16) | 80.0 | 40 | 6375 | 320 x 320 |
| RefineDet512 (VGG16) | **81.8** | 24 | 16320 | 512 x 512 |


<p align="left">
<img src="https://github.com/sfzhang15/RefineDet/blob/master/refinedet_results.jpg" alt="RefineDet results on multiple datasets" width="770px">
</p>

_Note: RefineDet300+ and RefineDet512+ are evaluated with the multi-scale testing strategy.  The code of the multi-scale testing has also been released in this repository._

### Citing RefineDet

Please cite our paper in your publications if it helps your research:

    @inproceedings{zhang2018single,
      title = {Single-Shot Refinement Neural Network for Object Detection},
      author = {Zhang, Shifeng and Wen, Longyin and Bian, Xiao and Lei, Zhen and Li, Stan Z.},
      booktitle = {CVPR},
      year = {2018}
    }

### Contents
1. [Installation](#installation)
2. [Preparation](#preparation)
3. [Training](#training)
4. [Evaluation](#evaluation)
5. [Models](#models)

### Installation
1. Get the code. We will call the cloned directory as `$RefineDet_ROOT`.
  ```Shell
  git clone https://github.com/sfzhang15/RefineDet.git
  ```

2. Build the code. Please follow [Caffe instruction](http://caffe.berkeleyvision.org/installation.html) to install all necessary packages and build it.
  ```Shell
  cd $RefineDet_ROOT
  # Modify Makefile.config according to your Caffe installation.
  # Make sure to include $RefineDet_ROOT/python to your PYTHONPATH.
  cp Makefile.config.example Makefile.config
  make all -j && make py
  ```

### Preparation
1. Download [fully convolutional reduced (atrous) VGGNet](https://gist.github.com/weiliu89/2ed6e13bfd5b57cf81d6). By default, we assume the model is stored in `$RefineDet_ROOT/models/VGGNet/`.

2. Download [ResNet-101](https://github.com/KaimingHe/deep-residual-networks). By default, we assume the model is stored in `$RefineDet_ROOT/models/ResNet/`.

3. Follow the [data/VOC0712/README.md](https://github.com/sfzhang15/RefineDet/blob/master/data/VOC0712/README.md) to download VOC2007 and VOC2012 dataset and create the LMDB file for the VOC2007 training and testing.

4. Follow the [data/VOC0712Plus/README.md](https://github.com/sfzhang15/RefineDet/blob/master/data/VOC0712Plus/README.md) to download VOC2007 and VOC2012 dataset and create the LMDB file for the VOC2012 training and testing.

5. Follow the [data/coco/README.md](https://github.com/sfzhang15/RefineDet/blob/master/data/coco/README.md) to download MS COCO dataset and create the LMDB file for the COCO training and testing.

### Training
1. Train your model on PASCAL VOC.
  ```Shell
  # It will create model definition files and save snapshot models in:
  #   - $RefineDet_ROOT/models/VGGNet/VOC0712{Plus}/refinedet_vgg16_{size}x{size}/
  # and job file, log file, and the python script in:
  #   - $RefineDet_ROOT/jobs/VGGNet/VOC0712{Plus}/refinedet_vgg16_{size}x{size}/
  python examples/refinedet/VGG16_VOC2007_320.py
  python examples/refinedet/VGG16_VOC2007_512.py
  python examples/refinedet/VGG16_VOC2012_320.py
  python examples/refinedet/VGG16_VOC2012_512.py
  ```
  
2. Train your model on COCO.
  ```Shell
  # It will create model definition files and save snapshot models in:
  #   - $RefineDet_ROOT/models/{Network}/coco/refinedet_{network}_{size}x{size}/
  # and job file, log file, and the python script in:
  #   - $RefineDet_ROOT/jobs/{Network}/coco/refinedet_{network}_{size}x{size}/
  python examples/refinedet/VGG16_COCO_320.py
  python examples/refinedet/VGG16_COCO_512.py
  python examples/refinedet/ResNet101_COCO_320.py
  python examples/refinedet/ResNet101_COCO_512.py
  ```
  
3. Train your model form COOC to VOC (Based on VGG16).
  ```Shell
  # It will extract a VOC model from a pretrained COCO model.
  ipython notebook convert_model_320.ipynb
  ipython notebook convert_model_512.ipynb
  # It will create model definition files and save snapshot models in:
  #   - $RefineDet_ROOT/models/VGGNet/VOC0712{Plus}/refinedet_vgg16_{size}x{size}_ft/
  # and job file, log file, and the python script in:
  #   - $RefineDet_ROOT/jobs/VGGNet/VOC0712{Plus}/refinedet_vgg16_{size}x{size}_ft/
  python examples/refinedet/finetune_VGG16_VOC2007_320.py
  python examples/refinedet/finetune_VGG16_VOC2007_512.py
  python examples/refinedet/finetune_VGG16_VOC2012_320.py
  python examples/refinedet/finetune_VGG16_VOC2012_512.py
  ```

### Evaluation
1. Build the Cython modules.
  ```Shell
  cd $RefineDet_ROOT/test/lib
  make -j
  ```
  
2. Change the ‘self._devkit_path’ in [`test/lib/datasets/pascal_voc.py`](https://github.com/sfzhang15/RefineDet/blob/master/test/lib/datasets/pascal_voc.py) to yours.

3. Change the ‘self._data_path’ in [`test/lib/datasets/coco.py`](https://github.com/sfzhang15/RefineDet/blob/master/test/lib/datasets/coco.py) to yours.

4. Check out [`test/refinedet_demo.py`](https://github.com/sfzhang15/RefineDet/blob/master/test/refinedet_demo.py) on how to detect objects using the RefineDet model and how to plot detection results.
  ```Shell
  # For GPU users
  python test/refinedet_demo.py
  # For CPU users
  python test/refinedet_demo.py --gpu_id -1
  ```

5. Evaluate the trained models via [`test/refinedet_test.py`](https://github.com/sfzhang15/RefineDet/blob/master/test/refinedet_test.py).
  ```Shell
  # You can modify the parameters in refinedet_test.py for different types of evaluation:
  #  - single_scale: True is single scale testing, False is multi_scale_testing.
  #  - test_set: 'voc_2007_test', 'voc_2012_test', 'coco_2014_minival', 'coco_2015_test-dev'.
  #  - voc_path: where the trained voc caffemodel.
  #  - coco_path: where the trained voc caffemodel.
  # For 'voc_2007_test' and 'coco_2014_minival', it will directly output the mAP results.
  # For 'voc_2012_test' and 'coco_2015_test-dev', it will save the detections and you should submitted it to the evaluation server to get the mAP results.
  python test/refinedet_test.py
  ```

### Models
We have provided the models that are trained from different datasets. To help reproduce the results in [Table 1, Table 2, Table 4](https://arxiv.org/pdf/1711.06897.pdf), most models contain a pretrained `.caffemodel` file, many `.prototxt` files, and python scripts.

1. PASCAL VOC models (VGG-16):
   * 07+12: [RefineDet320](https://drive.google.com/open?id=1rj6ikGCJg_rOlt0gUCXkjHzPkjpvzxXV), [RefineDet512](https://drive.google.com/open?id=10Fwymi1HizebH3qnyZmecXRvtBc1HCop)
   * 07++12: [RefineDet320](https://drive.google.com/open?id=1d1T_tTImZynD88CoB0OF0rdFXgp4E_le), [RefineDet512](https://drive.google.com/open?id=1h9IrfBHKnO1tQq3PWmo0TLhQcx7lUHhj)
   * COCO: [RefineDet320](https://drive.google.com/open?id=1dl-eyCZgDv_UwxGb2c1Usaqq2u2u7sqz), [RefineDet512](https://drive.google.com/open?id=1vJ8CZlOocsF5cASr3k2Or1vQx-hTfxs6)
   * 07+12+COCO: [RefineDet320](https://drive.google.com/open?id=1c8umLHI-x68uxT7CcCirFPhykPkyYUzC), [RefineDet512](https://drive.google.com/open?id=1-d4w152HsEaYgWY7v4_6zqxxQIijlHjX)
   * 07++12+COCO: [RefineDet320](https://drive.google.com/open?id=1pti47J-oE7Os02vNvO0JIrQp3_FQR70v), [RefineDet512](https://drive.google.com/open?id=1ZwnO_F1Pqdg1xyNSa-0XPEuh7knel9L_)

2. COCO models:
   * trainval35k (VGG-16): [RefineDet320](https://drive.google.com/open?id=1BIVvkSQM8DarpeqOpjgPpDxUoFq9ZxKM), [RefineDet512](https://drive.google.com/open?id=16j7gmHvd82LSog52kBXUUYyLx26mOV_6)
   * trainval35k (ResNet101): [RefineDet320](https://drive.google.com/open?id=1yrCfPIyKNsD9aBnn5iooFoX414FzXvzH), [RefineDet512](https://drive.google.com/open?id=1KWdfrowNIJqJF0j-ZxkQpkbAcPPbwAS1)

_Note: If you can not download our pre-trained models through the above links, you can download them through [BaiduYun](http://pan.baidu.com/s/1gf8J7Yr)._
