# epicbot
- [Overview](#overview)
- [Installation](#installation)
- [Config](#config)
- [TODO](#todo)

<a name="overview"/>
## Overview
This repo contains the [scrapy](http://doc.scrapy.org/en/latest/)
web crawler that powers [epicloops.com](http://epicloops.com/). The goal of
[epicloops.com](http://epicloops.com/) is to use Creative Commons audio files
from the web as a source of loops and samples to be integrated into projects
built with [GarageBand](https://www.apple.com/mac/garageband/), [Logic](https://www.apple.com/logic-pro/),
[ProTools](http://www.avid.com/us/products/family/pro-tools/), etc. The sites
it is currently capable of crawling include:

- [soundclick.com](http://www.soundclick.com/)
- more to come...

The scrapy [pipeline](http://doc.scrapy.org/en/latest/topics/item-pipeline.html)
is used to ensure the file has a CC license, download the file and store it
on s3, gather data about the file from the [echonest api](http://the.echonest.com/),
persist this data to a database, and notify the samplers through sqs that the
file is ready to be split.

<a name="installation"/>
## Installation
1. Install `epiclib`:
```
git clone https://github.com/epicloops/epiclib.git
pip install -r ./epiclib/requirements.txt ./epiclib
```
2. Install `epicbot`:
```
# Make sure scrapy dependencies are installed. This may include libs such as:
#  - libxml2-dev
#  - libxslt1-dev
#  - libssl1.0.0

git clone https://github.com/epicloops/epicbot.git
pip install -r ./epicbot/requirements.txt ./epicbot
```

### Installation example:
For a rough working example of how to get this up and running see this saltstack
repo: [https://github.com/epicloops/epic-states/tree/qa](https://github.com/epicloops/epic-states)

<a name="config"/>
## Config
A json config file must be placed at `~/.epic/config`. Here is an example:
```
{
    "SQLALCHEMY_DATABASE_URI": "sqlite:////tmp/my_database.db",
    "AWS_ACCESS_KEY_ID": "XXXXXXXXXXXXXXXXXXXX",
    "AWS_SECRET_ACCESS_KEY": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "AWS_REGION": "us-east-1",
    "AWS_S3_BUCKET": "epic",
    "CRAWLERA_USER": "user",
    "CRAWLERA_PASS": "pass",
    "ECHONEST_API_KEY": "XXXXXXXXXXXXXXXXX"
}
```
**Note:** [crawlera](http://crawlera.com/) and [echonest](http://echonest.com/)
accounts are required and the aws credentials must have full access to the s3
bucket and sqs.

<a name="todo"/>
TODO
----
- Clean up and unify logging.
- Clean up config file parsing.
- Tests!!
- Docstrings!!
