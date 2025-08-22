# auto_login_manager
一個使用 **SQLite** + **Selenium** 製作的自動化網站登入工具。  
支援帳號密碼管理、網站登入、自動輸出帳號資料成 CSV。

## 功能特色
- 帳號密碼管理 (新增、修改、刪除、查詢)
- 自動登入指定網站
- 資料匯出 CSV
- 多帳號支援

## 環境需求
- Python 3.9+
- Google Chrome + ChromeDriver
- 需求套件: `pip install -r requirements.txt`

## 使用方式
python main.py

⚠️ 注意
本專案目前僅支援 Windows 環境，因為：
- 使用 `cls` 清除螢幕。
- 預設 Chrome 路徑為 Windows 版本。
若要在 Linux/macOS 執行，需自行修改上述部分。
