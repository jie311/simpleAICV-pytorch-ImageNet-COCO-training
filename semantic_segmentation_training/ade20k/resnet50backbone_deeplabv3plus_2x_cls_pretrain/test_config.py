import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

from tools.path import ADE20Kdataset_path

from simpleAICV.semantic_segmentation import models
from simpleAICV.semantic_segmentation import losses
from simpleAICV.semantic_segmentation.datasets.ade20kdataset import ADE20KSemanticSegmentation
from simpleAICV.semantic_segmentation.common import Resize, RandomCrop, RandomHorizontalFlip, PhotoMetricDistortion, Normalize, SemanticSegmentationCollater, load_state_dict

import torch
import torchvision.transforms as transforms


class config:
    network = 'resnet50backbone_deeplabv3plus'
    # not include background class(class index: ignore index)
    input_image_size = 512
    num_classes = 150
    reduce_zero_label = True
    ignore_index = 255

    backbone_pretrained_path = ''
    model = models.__dict__[network](**{
        'backbone_pretrained_path': backbone_pretrained_path,
        'num_classes': num_classes,
    })

    # load pretrained model or not
    trained_model_path = '/root/code/SimpleAICV-ImageNet-CIFAR-COCO-VOC-training/semantic_segmentation_training/ade20k/resnet50backbone_deeplabv3plus_2x_cls_pretrain/checkpoints/resnet50backbone_deeplabv3plus-metric34.132.pth'
    load_state_dict(trained_model_path,
                    model,
                    loading_new_input_size_position_encoding_weight=False)

    test_criterion = losses.__dict__['CELoss'](**{
        'ignore_index': ignore_index,
    })

    test_dataset = ADE20KSemanticSegmentation(
        ADE20Kdataset_path,
        image_sets='validation',
        reduce_zero_label=reduce_zero_label,
        transform=transforms.Compose([
            Resize(image_scale=(input_image_size, input_image_size),
                   multi_scale=False,
                   multi_scale_range=(0.5, 2.0)),
            Normalize(),
        ]))
    test_collater = SemanticSegmentationCollater(divisor=32,
                                                 ignore_index=ignore_index)

    seed = 0
    # batch_size is total size
    batch_size = 32
    # num_workers is total workers
    num_workers = 16