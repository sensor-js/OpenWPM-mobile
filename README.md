OpenWPM-Mobile [![Build Status](https://travis-ci.org/sensor-js/OpenWPM_mobile.svg?branch=master)](https://travis-ci.org/sensor-js/OpenWPM_mobile)
=======

OpenWPM-Mobile is a mobile web privacy measurement framework that is based on
OpenWPM.

## Installation

Run the following to install OpenWPM-Mobile.

```./install.sh```

To install the analysis related packages and files:

```install-analysis.sh```

## Emulating Android fonts

To ensure that your crawler is identifed as a mobile device (to the best effort possible) follow the instructions provided in [EmulatingAndroidFonts.md](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/EmulatingAndroidFonts.md) to install Android fonts on your crawler machines.


## Basic usage

Edit [`mobile_sensor_crawl.py`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/mobile_sensor_crawl.py) to change the crawl parameters, such as number of sites to crawl and the number of browsers to run in parallel.

Then start a crawl by running:

```python mobile_sensor_crawl.py```

## Running tests

The following will run all the tests:

```pytest test```

Run the following to run all tests except `test_crawl.py`, which simulates a small-scale crawl (slow).

```pytest test -m "not slow"```

## Data Analysis

1. To extract features for each script discovered in the crawl run the following command:

    ```python extract_features.py```

    Make sure to point to the correct database containing the crawl results inside [`extract_features.py`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/feature_extraction/extract_features.py#L813).

2. Once features are extracted you can generate clusters from the extracted features by using the [`Clustering_JS_scripts.ipynb`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/cluster_scripts/Clustering_JS_scripts.ipynb) ipyhton notebook script. 

    Make sure to point to the newly generated feature file (```features.csv```) from the step 1.
    
## Citation
If you use OpenWPM_Mobile in your research, please cite our CCS 2018 [`publication`](). You can use the following BibTeX.

```
@inproceedings{sensor-js-2018,
    author    = "Anupam Das and Gunes Acar and Nikita Borisov and Amogh Pradeep",
    title     = "{The Web's Sixth Sense: A Study of Scripts Accessing Smartphone Sensors}",
    booktitle = {Proceedings of ACM CCS 2018},
    year      = "2018",
}
```

## License
OpenWPM_Mobile is licensed under GNU GPLv3. Additional code has been included from ...
    
