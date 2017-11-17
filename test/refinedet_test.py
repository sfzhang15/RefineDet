import _init_paths
from fast_rcnn.test import single_scale_test_net, multi_scale_test_net_320, multi_scale_test_net_512
from fast_rcnn.config import cfg, cfg_from_file, cfg_from_list
from datasets.factory import get_imdb
import caffe
import os

if __name__ == '__main__':
    GPU_ID = 0
    single_scale = True # True: sinle scale test;  False: multi scale test
    test_set = 'voc_2007_test' # 'voc_2007_test' or 'voc_2012_test' or 'coco_2014_minival' or 'coco_2015_test-dev'
    voc_path = 'models/VGGNet/VOC0712/refinedet_vgg16_320x320/'
    coco_path = 'models/VGGNet/coco/refinedet_vgg16_320x320/'

    cfg.single_scale_test = single_scale
    if 'voc' in test_set:
        path = voc_path
    else:
        path = coco_path

    if '320' in path:
    	input_size = 320
    else:
    	input_size = 512

    caffe.set_mode_gpu()
    caffe.set_device(GPU_ID)

    imdb = get_imdb(test_set)
    imdb.competition_mode(False)

    if 'coco' in test_set:
        if single_scale is True:
            prototxt = path + 'single_test_deploy.prototxt'
        else:
            prototxt = path + 'multi_test_deploy.prototxt'
        f = open(prototxt, 'r')
        for line in f:
            if 'confidence_threshold' in line:
                line = line[:-1]
                cfg.confidence_threshold = float(line.split(' ')[-1])
    else:
        prototxt = path + 'deploy.prototxt'
    models = os.listdir(path)

    mAP = {}
    for model in models:
        if model.find('caffemodel') == -1:
            continue
        caffemodel = path + model
        net = caffe.Net(prototxt, caffemodel, caffe.TEST)
        net.name = os.path.splitext(os.path.basename(model))[0]
        cfg.net_name = net.name
        try:
        	iter = int(net.name.split('_')[-1])
        except:
            iter = 000000
        if single_scale is True:
            single_scale_test_net(net, imdb, targe_size=input_size)
        else:
            if input_size == 320:
                multi_scale_test_net_320(net, imdb)
            else:
                multi_scale_test_net_512(net, imdb)
        mAP[iter] = cfg.mAP

    keys = mAP.keys()
    keys.sort()
    templine = []
    print("#########################################################################################################")
    print("#########################################################################################################")
    if 'voc' in test_set:
        for key in keys:
            value = mAP.get(key)
            print("%d\t%.4f"%(key, value))
            templine.append("%d\t%.4f\n"%(key, value))
        with open(path+'mAP.txt', 'w+') as f:
            f.writelines(templine)
    elif 'coco' in test_set:
        print("Iter\tAP@0.5:0.95\tAP@0.5\tAP@0.75\tAP@S\tAP@M\tAP@L\tAR@1\tAR@10\tAR@100\tAR@S\tAR@M\tAR@L")
        templine.append("Iter\tAP@0.5:0.95\tAP@0.5\tAP@0.75\tAP@S\tAP@M\tAP@L\tAR@1\tAR@10\tAR@100\tAR@S\tAR@M\tAR@L\n")
        for key in keys:
            value = mAP.get(key) * 100
            print("%d\t    %.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f"
                            %(key,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11]))
            templine.append("%d\t    %.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n"
                            %(key,value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7],value[8],value[9],value[10],value[11]))
        with open(path+'mAP.txt', 'w+') as f:
            f.writelines(templine)
    print("#########################################################################################################")
    print("#########################################################################################################")