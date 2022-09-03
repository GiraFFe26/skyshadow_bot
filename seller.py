import requests
import time
import hashlib
from datetime import datetime, timedelta
import zoneinfo
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from requests.exceptions import ConnectTimeout


class digiseller_api:
    def __init__(self):
        self.API = '' #api-key
        self.SELLER_ID = int('') #id продавца

    # ПОЛУЧЕНИЕ ТОКЕНА
    def get_token(self):
        timestamp = str(int(time.time()))
        sign = hashlib.sha256((self.API + timestamp).encode('UTF-8')).hexdigest()
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        json_data = {
            "seller_id": self.SELLER_ID,
            "timestamp": timestamp,
            "sign": sign
        }
        r = requests.post('https://api.digiseller.ru/api/apilogin', headers=headers, json=json_data).json()
        return r['token']

    def get_product_info(self, unique_code, token):
        headers = {'Accept': 'application/json'}
        r = requests.get(f'https://api.digiseller.ru/api/purchases/unique-code/{unique_code}?token={token}', headers=headers).json()
        if r['retdesc'] == 'отсутствует или неверно задан параметр unique_code' or r['retdesc'] == 'не найден unique_code':
            return r['retdesc']
        if r["unique_code_state"]["options"] == 1:
            status = 'уникальный код не проверен'
        elif r["unique_code_state"]["options"] == 2:
            status = 'товар доставлен, доставка не подтверждена и не опровергнута'
        elif r["unique_code_state"]["options"] == 3:
            status = 'товар доставлен, доставка подтверждена'
        elif r["unique_code_state"]["options"] == 4:
            status = 'товар доставлен, но отвергнут'
        elif r["unique_code_state"]["options"] == 5:
            status = 'уникальный код проверен, товар не доставлен'
        return f'Ваш товар: {r["name_invoice"].replace("?", "")}\nСостояние сделки: {status}'

    def get_sales(self, token):
        headers = {'Content-Type': "application/json",
                   'Accept': "application/json"}
        offset = datetime.now(zoneinfo.ZoneInfo("Europe/Moscow"))
        offset = datetime.strftime(offset, "%Y-%m-%d %H:%M:%S")
        json_data = {
                  "date_start": str(datetime.strptime(offset, "%Y-%m-%d %H:%M:%S") - timedelta(minutes=3)),
                  "date_finish": str(offset),
                  "returned": 0,
                  "page": 1,
                  "rows": 10
                }
        try:
            r = requests.post(f'https://api.digiseller.ru/api/seller-sells/v2?token={token}', headers=headers, json=json_data).json()
        except ConnectTimeout:
            r = requests.post(f'https://api.digiseller.ru/api/seller-sells/v2?token={token}', headers=headers, json=json_data).json()
        print(r)
        for i in r['rows']:
            invoice_id = i['invoice_id']
            self.send_message(invoice_id, token)
            product = self.get_product_info(invoice_id, token)
            mail = i['email']
            date_pay = datetime.strptime(i['date_pay'], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
            self.send_to_sheets(invoice_id, mail, product, date_pay)

    def get_product_info(self, invoice_id, token):
        headers = {'Accept': 'application/json'}
        r = requests.get(f'https://api.digiseller.ru/api/purchase/info/{invoice_id}?token={token}', headers=headers).json()['content']['options'][-2]
        return f'{r["name"]} {r["user_data"]}'

    # ОТПРАВКА СООБЩЕНИЯ ( ЧТОБЫ ПЕРЕНЕСТИ НА НОВУЮ СТРОКУ ИСПОЛЬЗУЕТСЯ \n )
    def send_message(self, invoice_id, token):
        headers = {'Accept': "application/json",
                   'Content-Type': "application/json"}
        json_data = {
          "message": "Здравствуйте! Спасибо за покупку!\nВы можете ускорить получение товара, если воспользуетесь"
                     " нашим ботом в телеграмме!\nhttps://t.me/Sky_ShopBot\n\n⚠ Внимание! Этот бот не выдает товар! Он "
                     "просто позволяет быстрее зайти на ваш аккаунт!\n[Автоматическое сообщение]",
          "files": [
            {
              "newid": "",
              "name": "",
              "type": ""
            },
          ]
        }
        requests.post(f'https://api.digiseller.ru/api/debates/v2/?token={token}&id_i={invoice_id}', headers=headers,
                      json=json_data)

    def send_to_sheets(self, invoice_id, mail, product, date_pay):
        # Файл, полученный в Google Developer Console
        CREDENTIALS_FILE = 'creds.json'
        # ID Google Sheets документа (можно взять из его URL)
        spreadsheet_id = ''
        # Авторизуемся и получаем service — экземпляр доступа к API
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        values = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"Весь отчет (10-11)!A:Z",
        ).execute()
        x = len(values['values']) + 1

        # Пример записи в файл
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"Весь отчет (10-11)!A{x}:D{x}",
                     "majorDimension": "ROWS",
                     "values": [[invoice_id, mail, product, date_pay]]}
                ]
            }
        ).execute()
