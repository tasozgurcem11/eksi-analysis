# Collect and analyze eksi forum public entries

### Crawl eksi sozluk public entries 


***

### Contents

1. [Introduction](#introduction)
2. [Setup](#setup)
3. [Run](#run)
4. [Analysis](#analysis)
5. [Future Work](#future-work)


## Introduction

eksisozluk is a public forum that is used to discuss various topics. It's been active since 1999. At total there are
more than 140.000.000 entries. It's also ranked with the 19th most visited website in Turkey.

https://webrazzi.com/2020/05/12/turkiye-nin-en-cok-ziyaret-edilen-20-web-sitesi/

Goal of this project is to collect and analyze eksi forum public entries. The collected data will be used to analyze the
most popular topics and to find new topics. Postgresql is used to store the data.


## Setup

2 different crawling is used, in the latest version Python request library is active. To use with Selenium then, 
chrome driver should be downloaded and installed. 
https://chromedriver.chromium.org/downloads

Sample .env file that is required:
```
CRAWL_WEBSITE=https://eksisozluk.com  # Website to crawl
CONN_URI={POSTGRESQL_CONN_URI}  # PostgreSQL connection URI
```

Add if you want to use Selenium:
```
CUSTOM_CHROME_DRIVER_PATH={CHROMEDRIVER_PATH} 
DEFAULT_CHROME_DRIVER_PATH=/usr/local/bin/chromedriver 
```

## Run

Build and run container:

```
docker build -t eksi .
```

```
docker run -it --rm eksi
```

## Analysis

So SQL queries are used to analyze the data.

Return most popular topics with given date:
```
SELECT *
FROM eksi_daily -- enter table name to look at
WHERE created_on = '2022-07-25' -- enter date to look at
ORDER BY entry_record DESC  -- order by entry_record desc
```

Return most popular entries:
```
SELECT *  
FROM eksi_daily -- enter table name to look at
ORDER BY entry_record DESC -- order by entry_record descending
LIMIT 5; 
```


## Future Work

So in future, Telegram bot and email sender will be used to send daily/weekly/monthly analysis based on:
* most popular topics
* new topics
* occurrences of each topic
* most active days
* etc.

To learn more and to contribute, please email me at:
tasozgurcem@gmail.com


