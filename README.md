OpenWPM-Mobile [![Build Status](https://travis-ci.org/sensor-js/OpenWPM_mobile.svg?branch=master)](https://travis-ci.org/sensor-js/OpenWPM_mobile)
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

Make sure to point to the newly generated feature file (```features.csv```) from the previous step (step 1).
