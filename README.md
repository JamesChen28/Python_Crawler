
# Python_Crawler
搜尋PTT看版標題含特定關鍵字之文章，將搜尋到的內容產出一份csv檔。
例如：Steam版標題含「限免」之文章。

## Ver 1.0.1
**使用說明**：
將參數調整在pttCrawler_config.json，執行pttCrawler_Steam_LimitedFree.py，即可完成PTT特定看板標題關鍵字搜尋，並產出csv檔。

### Parameter Description
* **board**：PTT看版名稱
* **keyword**：標題關鍵字
* **previousPage**：欲往前幾頁搜尋

### Output Description
* **網址**：PTT特定標題關鍵字文章的網址
* **標題**：含有特定關鍵字的標題
* **日期**：文章發佈日期
