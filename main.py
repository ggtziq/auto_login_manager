import sqlite3,os,time,csv,codecs,io,os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  #禁用自動化標籤使用
from selenium.webdriver.common.keys import Keys

class DBManager:
    def __init__(self, db_name='Sqlite01.sqlite'):
        """ 初始化資料庫連線，確保表格存在 """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """ 確保表格存在 """
        sqlstr = '''
        CREATE TABLE IF NOT EXISTS password (
            "name" TEXT PRIMARY KEY NOT NULL, 
            "nameinput_path" TEXT, 
            "passwd" TEXT,
            "passwdinput_path" TEXT,
            "action" TEXT,
            "webway" TEXT,
            "webname" TEXT
        )
        '''
        self.cursor.execute(sqlstr)
        self.conn.commit()

    @staticmethod
    def menu():
        os.system("cls")
        print("帳號、密碼管理系統")
        print("---------------------")
        print("1. 新增帳號、密碼")
        print("2. 顯示帳號、密碼")
        print("3. 修改密碼")
        print("4. 刪除帳號、密碼")
        print("0. 結束程式")
        print("---------------------")

    def input_data(self):
        """ 新增帳號資料 """
        name = input('請輸入您欲新增的帳號: ')
        self.cursor.execute("SELECT * FROM password WHERE name=?", (name,))
        if self.cursor.fetchone() is not None:
            print("帳號已存在，請使用其他帳號。")
            return
        
        nameinput = input('請輸入帳號輸入路徑 (XPath): ')
        passwd = input('請輸入密碼: ')
        passwdinput = input('請輸入密碼輸入路徑 (XPath): ')
        action = input('請輸入登入按鈕路徑 (XPath): ')
        webway = input('請輸入網址: ')
        webname = input('請輸入網站名稱: ')

        sqlstr = '''
        INSERT INTO password (name, nameinput_path, passwd, passwdinput_path, action, webway, webname) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(sqlstr, (name, nameinput, passwd, passwdinput, action, webway, webname))
        self.conn.commit()
        print('新增帳號完成')
        input('按任意鍵返回主選單')

    def disp_data(self):
        """ 顯示所有帳號和密碼 """
        cursor = self.conn.execute('SELECT * FROM password')
        print('帳號\t\t密碼\t\t網址名稱')
        print("================")
        for row in cursor:
            print('{}\t\t{}\t\t{}'.format(row[0], row[2], row[6]))
        input('按任意鍵返回主選單')
    def chang_data(self):
        while True:
            name = input('請輸入帳號 (輸入 q 離開): ')
            if name.lower() == 'q':
                break
            
            # 確認帳號是否存在
            cursor = self.conn.execute("SELECT * FROM password WHERE name=?", (name,))
            if cursor.fetchone() is None:
                print("帳號不存在，請重新輸入。")
                continue
            
            print("\n請選擇要修改的內容：")
            print("1. 修改密碼")
            print("2. 修改帳號輸入路徑")
            print("3. 修改密碼輸入路徑")
            print("4. 修改後續行為")
            print("5. 修改網址路徑")
            print("6. 修改網址名稱")
            print("0. 退出修改")

            choice = input("請輸入對應數字: ")

            field_map = {
                '1': ('passwd', '新密碼'),
                '2': ('nameinput_path', '新的帳號輸入路徑 (XPath)'),
                '3': ('passwdinput_path', '新的密碼輸入路徑 (XPath)'),
                '4': ('action', '新的後續行為'),
                '5': ('webway', '新的網址路徑'),
                '6': ('webname', '新的網址名稱')
            }

            if choice == '0':
                print("已退出修改。")
                break

            if choice in field_map:
                field, prompt = field_map[choice]
                new_value = input(f'請輸入{prompt}: ')
                
                # 執行 SQL 更新
                sqlstr = f"UPDATE password SET {field} = ? WHERE name = ?"
                self.conn.execute(sqlstr, (new_value, name))
                self.conn.commit()

                print(f'{field} 修改成功！')
            else:
                print("無效選擇，請重新輸入。")

    def delete_data(self):
        while True:
            print("\n選擇刪除方式：")
            print("1. 刪除單個帳號")
            print("2. 刪除所有帳號")
            print("0. 返回主選單")
            
            choice = input("請選擇 (1-3): ")

            if choice == '1':  # 刪除單一帳號
                while True:
                    name = input('請輸入要刪除的帳號 (Enter ==> 停止輸入): ')
                    if name == "":  # 如果按 Enter，則返回主選單
                        break
                    
                    # 查詢帳號是否存在
                    sqlstr = "SELECT * FROM password WHERE name = ?"
                    cursor = self.conn.execute(sqlstr, (name,))
                    row = cursor.fetchone()
                    
                    if row is None:
                        print('{} 帳號不存在 !'.format(name))
                        continue
                    
                    print('確定刪除 {} 的資料?'.format(name))
                    yn = input('(Y(確定刪除) / N(返回上一步))? ')
                    if yn.lower() == 'y':
                        sqlstr = "DELETE FROM password WHERE name = ?"
                        self.conn.execute(sqlstr, (name,))
                        self.conn.commit()
                        print('已刪除 {} 的帳號資料!'.format(name))
                        input('請按任意鍵返回主選單')
                        break
            
            elif choice == '2':  # 刪除所有帳號
                yn = input('確定要刪除所有帳號資料嗎？此操作無法恢復！(Y/N) ')
                if yn.lower() == 'y':
                    self.conn.execute("DELETE FROM password")  # 刪除所有資料
                    self.conn.commit()
                    print("已刪除所有帳號資料！")
                    input('請按任意鍵返回主選單')
                    break
            
            elif choice == '0':  # 返回主選單
                print("返回主選單。")
                break
            
            else:
                print("無效的選擇，請重新輸入。")
    def export_to_csv(self, csv_file='output.csv'):
        """ 將資料導出為 CSV 檔案 """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM password")  # 查詢資料
        rows = cursor.fetchall()

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([description[0] for description in cursor.description])  # 寫入標題
            writer.writerows(rows)  # 寫入資料

        print(f"資料已成功導出到 {csv_file}")            

class User:
    def __init__(self, name, nameinput_path, passwd, passwdinput_path, action, webway, webname):
        self.name = name
        self.nameinput_path = nameinput_path
        self.passwd = passwd
        self.passwdinput_path = passwdinput_path
        self.action = action
        self.webway = webway
        self.webname = webname

    def display_info(self):
        print(f"帳號: {self.name}, 網址名稱: {self.webname}")

class WebWork:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    @staticmethod
    def usermenu():
        os.system("cls")
        print("網站登入系統01")
        print("---------------------")
        print("1. 登入網站")
        print("2. 進入帳密系統")
        print("3. 輸出csv檔案")
        print("0. 結束程式")
        print("---------------------")

    def webwork(self, user):
        """ 自動登入網站 """
        options = Options()
        options.binary_location = r"../chrome-win64/chrome.exe"  #原本設定絕對路徑的C:\Users\user\Desktop\test\自動登入\chrome-win64\chrome.exe，改成相對路徑模組os的os.path.dirname(__file__)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自動化標籤
        driver = webdriver.Chrome(service=Service(), options=options)  #service用來設置chromedriver的執行環境，options包含前面設置的chrome選項
        driver.get(user.webway)
        driver.maximize_window()  #最大化
        driver.execute_script("document.body.style.zoom='1'")  #設置放大倍率
        #driver.fullscreen_window()  #全屏
        # 通過xpath查找元素
        time.sleep(1)
        driver.find_element(By.XPATH, user.nameinput_path).send_keys(user.name)
        driver.find_element(By.XPATH, user.passwdinput_path).send_keys(user.passwd)
        if bool(user.action) == False:
            return False
        else:
            driver.find_element(By.XPATH, user.action).send_keys(Keys.ENTER)
        #login_button = driver.find_element(By.XPATH, user.action).send_keys(Keys.ENTER)

    def login(self):
        """ 登入功能，讓使用者在多個帳號中選擇 """
        account = input('請輸入帳號或網站名稱: ')
        
        # 查詢符合條件的所有帳號資料
        self.db_manager.cursor.execute("SELECT * FROM password WHERE name=? OR webname=?", (account, account))
        rows = self.db_manager.cursor.fetchall()

        if not rows:
            print("未找到該帳號或網址名稱。")
            input('按任意鍵返回主選單')
            return

        # 如果只有一筆資料，直接使用
        if len(rows) == 1:
            user = User(*rows[0])
            print("\n找到符合的帳號，直接進行登入:")
            user.display_info()
        else:
            # 如果找到多筆，讓使用者選擇
            print("\n以下是該帳號/網站名稱對應的資料，請選擇:")
            print("編號\t帳號\t\t網站名稱\t\t網址")
            print("----------------------------------------------------")
            for idx, row in enumerate(rows, start=1):
                print(f"{idx}.\t{row[0]}\t\t{row[6]}\t\t{row[5]}")

            while True:
                try:
                    choice = int(input("請輸入對應的編號進行登入 (輸入 0 返回主選單): "))
                    if choice == 0:
                        return
                    if 1 <= choice <= len(rows):
                        user = User(*rows[choice - 1])  # 取得對應的帳號資料
                        break
                    else:
                        print("請輸入有效的編號！")
                except ValueError:
                    print("請輸入數字！")

        # 顯示選擇的帳號資訊
        use_data = input("是否使用該帳號登入? (y/n): ")
        if use_data.lower() == 'y':
            self.webwork(user)
        else:
            print("使用者資料未被選擇。")

        input('按任意鍵返回主選單')

if __name__ == "__main__":
    db_manager = DBManager()
    web = WebWork(db_manager)

    while True:
        WebWork.usermenu()
        choice = input('請輸入您的選擇: ')
        print()
        if choice == '1':
            web.login()
        elif choice == '2':
            while True:
                DBManager.menu()
                sub_choice = input('請輸入您的選擇: ')
                if sub_choice == '1':
                    db_manager.input_data()
                elif sub_choice == '2':
                    db_manager.disp_data()
                elif sub_choice == '3':
                    db_manager.chang_data()
                elif sub_choice == '4':
                    db_manager.delete_data()
                else:
                    break
        elif choice =='3':
            db_manager.export_to_csv('output.csv')
            time.sleep(3)
        else:
            break
    db_manager.conn.close()
    print('程式執行完畢')
