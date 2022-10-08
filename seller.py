import requests
import time
import hashlib
from datetime import datetime, timedelta
import zoneinfo
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from requests.exceptions import ConnectTimeout, ReadTimeout


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
        except (ConnectTimeout, ReadTimeout):
            r = requests.post(f'https://api.digiseller.ru/api/seller-sells/v2?token={token}', headers=headers, json=json_data).json()
        print(r)
        for i in r['rows']:
            invoice_id = i['invoice_id']
            self.send_message(invoice_id, token)
            product = self.check_for_sheets(invoice_id, token)
            mail = i['email']
            date_pay = datetime.strptime(i['date_pay'], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
            self.send_to_sheets(invoice_id, mail, product, date_pay)

    def check_for_sheets(self, invoice_id, token):
        headers = {'Accept': 'application/json'}
        r = requests.get(f'https://api.digiseller.ru/api/purchase/info/{invoice_id}?token={token}', headers=headers).json()
        print(r)
        r = r['content']
        item_id = int(r['item_id'])
        with open('ids.txt', 'r', encoding='UTF-8') as file:
            ids = [int(i.strip()) for i in file.readlines()]
        if item_id in ids:
            return r["name"]
        r = r['options']
        if r[-1]['name'] == 'Where can I contact you?' or r[-1]['name'] == 'Где с вами можно связаться?':
            r = r[-2]
        else:
            r = r[-1]
        return f'{r["name"]} {r["user_data"]}'

    # ОТПРАВКА СООБЩЕНИЯ ( ЧТОБЫ ПЕРЕНЕСТИ НА НОВУЮ СТРОКУ ИСПОЛЬЗУЕТСЯ \n )
    def send_message(self, invoice_id, token):
        headers = {'Accept': "application/json",
                   'Content-Type': "application/json"}
        json_data = {
          "message": "Здравствуйте! Спасибо за покупку!\n"
                     "У нас есть ответы на возможные вопросы, которые у вас могут возникнуть:\n\n"
                     "🙍‍♂: Когда я получу свой товар? 📦\n"
                     "👔: Максимальное время получения товара может достигнуть 24 часа\n\n"
                     "🙍‍♂: Могу ли я ускорить получение товара? ⏳\n"
                     "👔: Да! Если вы указали данные от вашего аккаунта,"
                     " вы можете воспользоваться ботом в нашем телеграмм канале "
                     "(https://t.me/Sky_ShopBot) который ускорит вход в ваш аккаунт.\n"
                     "⚠ Бот не выдает товар, он ускоряет его получение на ваш аккаунт!\n\n"
                     "🙍‍♂: Я не пользуюсь телеграммам/я не оставлял данных для входа. Как я могу еще ускорить получение товара? ⏳\n"
                     "👔: Оставьте ссылки на ваши соц. сети, где я смогу с вами связаться. Или можете проверять данную переписку, чтобы не упустить важные сообщения\n\n"
                     "🙍‍♂: Как я пойму, что товар на аккаунте? 📦\n"
                     "👔: После завершения заказа я всегда оставляю сообщение в данном диалоге или пишу вам с соц. сеть, также вам на почту должны прийти сообщения (чеки), что вы успешно оплатили товар\n\n"
                     "🙍‍♂: Я вошел с помощью бота в телеграмме, что делать дальше?\n"
                     "👔: Вам нужно только ожидать. Если возникнут трудности или вопросы, я вам обязательно об этом сообщу. Напоминаю, время получение товара может достигнуть максимум 24 часа.\n\n"
                     "🙍‍♂: Примерно через сколько, я смогу получить свой товар?\n"
                     "👔: Если вы оплатили заказ в рабочее время магазина, вы с 95% вероятностью получите товар до конца дня.\n"
                     "Исключения: Непредвиденные обстоятельства, ограничения Microsoft, игнорирования сообщения от продавца 👔",
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
            range=f"Весь отчет 11.09.22 - 11.10.22!A:Z",
        ).execute()
        x = len(values['values']) + 1

        # Пример записи в файл
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {"range": f"Весь отчет 11.09.22 - 11.10.22!A{x}:D{x}",
                     "majorDimension": "ROWS",
                     "values": [[invoice_id, mail, product, date_pay]]}
                ]
            }
        ).execute()
