# NLDB'16 Sentiment Analysis
This is the demo code for the Sentment Analysis talk at the 
[2016 NLDB Conference in Salford](http://www.salford.ac.uk/conferencing-at-salford/conference-management/current-conference/nldb-conference)

## Requirements
All scripts are written in python, therefore a functioning `python 2.7` environment is necessary. Dependencies are loaded via `pip`. If you do not have pip installed, [this guide](https://pip.pypa.io/en/stable/installing/) will provide detailed information.

Following packages are required:
 
 * matplotlib 1.4.3
 * nltk 3.1
 * numpy 1.9.2
 * scikit-learn 0.16.1
 * scipy 0.16.0b2
 * tqdm 3.7.1
 * facebook-sdk 0.4.0
 * requests 2.7.0
 

To make it easier for you, we have provided a [requirements.txt](requirements.txt) which can be installed by moving into the checked out directory and running `pip install -r /path/to/requirements.txt`.

## Analyze Facebook Pages
To analyze Facebook pages, run `python classify.py`.
As an example to pull all posts from the Austrian railway operator ÖBB and filter them by the keywords _flüchtling_, _krise_, _asyl_ from 1st of September until 30th of November following command is used:
`python classify.py unsereOEBB --access_token ABC...98AE --keywords flüchtling krise asyl --date_start 2015-09-01 --date_end 2015-11-30`

### Arguments
`--access_token` *REQUIRED* The access token is mandatory to make requests against the Facebook-API. A temporary access-token can be obtained here: [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)

`page` *REQUIRED* Facebook page id to import

`--date_start` The starting date to import posts from the page - format YYYY-MM-DD.

`--date_end` The ending date to import posts from the page - format YYYY-MM-DD

`--keywords` List of keywords separated by space. Only posts containing these keywords will be classified and plotted.
