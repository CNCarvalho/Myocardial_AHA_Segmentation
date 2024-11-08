# Myocardial_AHA_Segmentation
This is a Python tool to manually segment myocardial images according to the [American Heart Association (AHA) 16-segment model](https://doi.org/10.1161/hc0402.102975).

Tested and confirmed to work on:

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3124/)

[![Windows 10 64b](https://img.shields.io/badge/windows-10_64b-purple.svg)]()

## How to use

Load a `numpy.array` containing your myocardial image and a `numpy.array` containing the corresponding myocardial mask.
To initialize the main class, select the type of segmentation you want to perform: `basal`, `mid`, or `apical`.

    import numpy as np
    from AHA_segmentation import AHA_segmentation
  
    image = np.load(example_image.npy)
    mask = np.load('example_mask.npy')

    Segmentation_class = AHA_segmentation(image, mask, mode='basal')

This will create the main figure with the segmentation guidelines:

![Figure1](/assets/Figure1.png)

Call the `segment()` method and adjust the sliders until the guidelines are positioned correctly. The right ventricle should be positioned in the area defined by the rlines marked with a circle and a square.

    Segmentation_class.segment()

![Figure2](/assets/Figure2.png)

Call the `save_segment()` method to save. This will return a `numpy.array` mask whose values correspond to the AHA segment in each area.

    mask = Segmentation_class.save_segments()

![Figure4](/assets/Figure4.png)
