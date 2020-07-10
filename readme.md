# AII Scrapy

This is a scrapy project to crawl aii-alliance.org. 

## For the first run

1. Delete the `aii_items.db` and it will be created automatically.
2. Change the `FILES_STORE` setting in `**settings.py**`
3. Execute the `run.sh` to start the 6 spiders, all crawled items will be saved into aii_items.db and files will be stored into `FILES_STORE` location.



## For the later update

1. After the first running, just need to execute the `run.sh` periodically to update new contents.

