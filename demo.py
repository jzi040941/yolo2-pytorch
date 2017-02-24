import os
import cv2
import torch
import numpy as np

from darknet import Darknet19
import utils.image as im_utils
import utils.network as net_utils
import cfgs.config_voc as cfg


# hyper-parameters
npz_fname = 'models/yolo-voc.weights.npz'
# im_path = 'demo'
im_path = '/media/longc/Data/data/2DMOT2015/train/ADL-Rundle-3/img1/'

#---

net = Darknet19()
net.load_from_npz(npz_fname)

net.cuda()
net.eval()

im_fnames = sorted((fname for fname in os.listdir(im_path) if os.path.splitext(fname)[-1] == '.jpg'))
# im_fnames = ['person.jpg']
for fname in im_fnames:
    fname = os.path.join(im_path, fname)
    print('process: {}'.format(fname))

    im_data = np.asarray([im_utils.preprocess(fname, cfg)])
    im_data = net_utils.np_to_variable(im_data, is_cuda=True).permute(0, 3, 1, 2)
    net_out = net(im_data)

    np_netout = net_out.data.cpu().numpy()[0]
    im2show = im_utils.postprocess(np_netout, fname, cfg)
    cv2.imshow('test', im2show)
    cv2.waitKey(1)

