# RoshpitCrawler

RoshpitCrawler是一個用來爬取[Roshpit Champions](https://www.roshpit.ca)道具、拍賣品資料與發送通知的爬蟲專案。

專案內有兩隻爬蟲
- CollectItemInfoSpider(只有首次需要執行一次)
取得所有道具資料並儲存到資料庫
- CollectAuctionInfoSpider(透過排程每幾分鐘執行一次)
取得拍賣品的資料並比對是否符合使用者想要購買的道具屬性，若符合則透過Line或者是E-mail做通知。

RoshpitCrawler需要搭配[RoshpitWishList](https://github.com/edensquall/RoshpitWishList)才能發揮完整的功能，使用者透過RoshpitWishList網站建立想要購買的道具清單與設定通知方式。


## 使用框架

- 爬蟲框架: [Scrapy](https://scrapy.org)
- ORM框架: [SQLAlchemy](https://www.sqlalchemy.org)

## 架構設計

- 3-Tier Architecture
- Repository Pattern
- Unit of Work Pattern

## 目錄結構
```
.
├── RoshpitCrawler
│   ├── RoshpitCrawler
│   │   ├── __init__.py										RoshpitCrawler的初始化
│   │   ├── items.py											Scrapy傳遞資料的物件
│   │   ├── middlewares.py								Scrapy中間件
│   │   ├── models												各種Model
│   │   ├── pipelines.py									Scrapy資料處理管線
│   │   ├── repositories									各種Repository
│   │   ├── services											各種Application Service
│   │   ├── settings.py										Scrapy設定
│   │   ├── spiders												Scrapy爬蟲
│   │   ├── unit_of_works									各種Unit of Work
│   │   └── utils													公用程式
│   ├── .env															各種環境變數 (須自行建立)
│   ├── run_collect_auction_info_sp.py		執行collect_auction_info爬蟲
│   ├── run_collect_item_info_sp.py				執行collect_item_info爬蟲
│   └── scrapy.cfg												Scrapy專案設定
├── requirements.txt											所有需要的套件
└── venv																	虛擬環境 (須自行建立)
```

## 需求

-	Python 3.7+
  https://www.python.org/downloads/
-	MySQL
  https://www.mysql.com


## 安裝與設定

- 建立虛擬環境
```
python3 -m venv venv
```
https://docs.python.org/zh-tw/3/tutorial/venv.html
- 啟動虛擬環境
- 使用pip安裝需要的套件
```
pip install -r requirements.txt
```
https://pip.pypa.io/en/stable/user_guide/#requirements-files2
- 在RoshpitCrawler/RoshpitCrawler目錄下建立.env檔案
.env檔案內容如下，此處變數將於settings.py被使用，請自行設定 = 後的內容
```
DATABASE_URL = [DATABASE_URL]

IMAGES_STORE = [IMAGES_STORE]

GCS_PROJECT_ID = [GCS_PROJECT_ID] (使用Google Cloud Storage才需要)
GAC_PATH = [GAC_PATH]							(使用Google Cloud Storage才需要)

MAIL_HOST = [MAIL_HOST]
MAIL_PORT = [MAIL_PORT]
MAIL_FROM = [MAIL_FROM]
MAIL_USER = [MAIL_USER]
MAIL_PASS = [MAIL_PASS]
```

## 執行

```
python3 run_collect_item_info_sp.py
python3 run_collect_auction_info_sp.py
```

## 相關連結

- Roshpit Champions: https://www.roshpit.ca
- RoshpitWishList: https://github.com/edensquall/RoshpitWishList
- Scrapy: https://scrapy.org