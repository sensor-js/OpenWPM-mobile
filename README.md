OpenWPM-Mobile [![Build Status](https://travis-ci.org/sensor-js/OpenWPM-mobile.svg?branch=master)](https://travis-ci.org/sensor-js/OpenWPM-mobile)
=======

OpenWPM-Mobile is a mobile web privacy measurement framework that is based on
OpenWPM.

## Installation

Run the following to install OpenWPM-Mobile.

```./install.sh```

To install the analysis related packages and files:

```install-analysis.sh```


## Basic usage

Edit [`mobile_sensor_crawl.py`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/mobile_sensor_crawl.py) to change the crawl parameters, such as number of sites to crawl and the number of browsers to run in parallel.

Then start a crawl by running:

```python mobile_sensor_crawl.py```


## Imitating Mobile Browser
OpenWPM-Mobile takes several steps to realistically imitate Firefox for Android.

This involves overriding navigator object’s user agent, platform,
appVersion and appCodeName strings; matching the screen resolution,
screen dimensions, pixel depth, color depth; enabling touch
status; removing plugins and supported MIME types that may indicate a desktop browser.

OpenWPM-Mobile also uses the preferences used to configure Firefox
for Android such as hiding the scroll bars and disabling popup windows.
We relied on the values provided in the [`mobile.js`](https://dxr.mozilla.org/mozilla-esr45/source/mobile/android/app/mobile.js) script found in the Firefox for Android source code repository.

When running crawls with OpenWPM-Mobile we installed 
Android fonts on our crawler machines to mitigate font-based
fingerprinting. You may follow the instructions provided in
[EmulatingAndroidFonts.md](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/EmulatingAndroidFonts.md)
to install Android fonts on your crawler machines.

## Running tests

The following will run all the tests:

```pytest test```

If you don't want to run the (slow) crawling test `test_crawl.py` execute the following:

```pytest test -m "not slow"```

## Data Analysis

1. To extract features for each script discovered in the crawl run the following command:

    ```python extract_features.py```

    Make sure to point to the correct database containing the crawl results inside [`extract_features.py`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/feature_extraction/extract_features.py#L813).

2. Once features are extracted you can generate clusters from the extracted features by using the [`Clustering_JS_scripts.ipynb`](https://github.com/sensor-js/OpenWPM_mobile/blob/mobile_sensors/cluster_scripts/Clustering_JS_scripts.ipynb) Jupyter notebook.

    Make sure to point to the newly generated feature file (```features.csv```) from the step 1.
    
## Citation
If you use OpenWPM_Mobile in your research, please cite our CCS 2018 [`paper`](). You can use the following BibTeX.

```
@inproceedings{sensor-js-2018,
    author    = "Anupam Das and Gunes Acar and Nikita Borisov and Amogh Pradeep",
    title     = "{The Web's Sixth Sense: A Study of Scripts Accessing Smartphone Sensors}",
    booktitle = {Proceedings of ACM CCS 2018},
    year      = "2018",
}
```

## License

OpenWPM-Mobile is licensed under GNU GPLv3. Additional code has been included from
[OpenWPM](https://github.com/citp/OpenWPM) (which OpenWPM-Mobile is based on),
[FourthParty](https://github.com/fourthparty/fourthparty) and
[Privacy Badger](https://github.com/EFForg/privacybadgerfirefox), all of which
are licensed GPLv3+.
    
