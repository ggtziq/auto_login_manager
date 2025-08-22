# 使用說明 (Usage Guide)

本專案是一個基於 **SQLite** 與 **Selenium** 的自動化網站登入與帳密管理系統。  
⚠️ 注意：本專案目前僅支援 **Windows 系統**，因為：
- 使用 `cls` 指令清除終端機 (Linux/macOS 需改成 `clear`)。
- 預設 Chrome 路徑設定為 Windows 版本。

---

## 啟動方式
請先安裝相依套件：
```
pip install -r requirements.txt
```
執行主程式：
python main.py

## 主選單
啟動後會顯示以下選單：
```
網站登入系統01
---------------------
1. 登入網站
2. 進入帳密系統
3. 輸出 csv 檔案
0. 結束程式
---------------------
```
1. 登入網站
使用者輸入帳號或網站名稱後，自動從資料庫查詢對應的登入資訊，並透過 Selenium 自動登入網站。

2. 進入帳密系統
進入帳號密碼管理功能，可新增、查詢、修改或刪除帳號資訊。

3. 輸出 csv 檔案
將目前 SQLite 中所有帳號密碼資料匯出成 output.csv。

0. 結束程式
關閉程式並釋放資料庫連線。


## 帳密系統選單
進入 帳號、密碼管理系統 後，會看到以下選單：
```
帳號、密碼管理系統
---------------------
1. 新增帳號、密碼
2. 顯示帳號、密碼
3. 修改密碼
4. 刪除帳號、密碼
0. 結束程式
---------------------
```
1. 新增帳號、密碼
新增帳號資料（需輸入 XPath、網址等資訊）。

2. 顯示帳號、密碼
列出資料庫內所有帳號、密碼與網站名稱。

3. 修改密碼
可選擇修改帳號、密碼、XPath、網址等資訊。

4. 刪除帳號、密碼
提供刪除單筆或全部帳號的功能。

0. 結束程式
返回主選單。

## 資料匯出
選擇 3. 輸出 csv 檔案 時，會將所有帳號資料存成 output.csv，格式如下：
```
name,nameinput_path,passwd,passwdinput_path,action,webway,webname
testuser,//input[@id='username'],123456,//input[@id='password'],//button[@id='login'],https://example.com,ExampleSite
```
## 注意事項
1. 請確認已安裝 Google Chrome 與對應版本的 ChromeDriver。
2. 若 Chrome 安裝路徑不同，請修改程式中以下設定：
```
options.binary_location = r"../chrome-win64/chrome.exe"
```
3. 本程式主要適用於 Windows，若需在 Linux/macOS 使用，需手動修改調整 Chrome 路徑：
```
os.system("cls") 改成 os.system("clear")
```



