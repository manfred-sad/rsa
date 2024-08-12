import requests
import time
import logging
import json
from datetime import datetime
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler
import cloudscraper


# куки и токен берем из браузера. Адрес эндпоинта мог поменяться, надо проверять.
url = "https://myroadsafety.rsa.ie/api/v1/Availability/All/cfdda22c-4401-ef11-af89-005056b9b50c/0fed074d-c2d6-e811-a2c0-005056823b22"
cookie = "__cf_bm=r0_L_OAiDz3W0m7biolPZNb8dzehNZ.HXnPD3nf2JDg-1723469635-1.0.1.1-lFxaQ.VnklKUomUix.lWy1XtspsPcXQn3btHfEiH7JAyR1HUidzDfBglHstdztaGsjV7WSD3kJyXkeFbv2Z5uQ; _gid=GA1.2.1357798824.1723469641; _scid=b173c5db-db87-4cb7-9924-83c8af5cdad6; _ScCbts=%5B%5D; _fbp=fb.1.1723469642389.840757089414599047; _tt_enable_cookie=1; _ttp=qGWFm59jN6S-7Edo-B8NEq2Rtl5; _scid_r=b173c5db-db87-4cb7-9924-83c8af5cdad6; _ga=GA1.1.2123417257.1723469641; _ga_J53N6LXN3P=GS1.1.1723469642.1.1.1723469683.0.0.0; OptanonAlertBoxClosed=2024-08-12T13:42:12.869Z; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZWdtckB5YW5kZXgucnUiLCJ1bmlxdWVfbmFtZSI6Ik9MRUciLCJmYW1pbHlfbmFtZSI6IlNJTU9OT1YiLCJzdWIiOiIyODJlMWJjNi0yYjg5LWVlMTEtYWY4Ni0wMDUwNTZiOWI1MGMiLCJwcHNuIjoiOTcwMDg3MUFBIiwiMmZhYXV0aCI6InRydWUiLCJteWdvdiI6InRydWUiLCJteWdvdnRva2VuIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaMjVwYm1kclpYa3ViWGxuYjNacFpDNTJNU0lzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNNak0wTnpFNU56WXNJbTVpWmlJNk1UY3lNelEzTURFM05pd2lkbVZ5SWpvaU1TNHdJaXdpYVhOeklqb2lhSFIwY0hNNkx5OWhZMk52ZFc1MExtMTVaMjkyYVdRdWFXVXZaVEU1TjJWaE9XVXRNREpsTlMwMFkySTJMVGsyWWpJdE5UVTNNV05rTmpRMU56VTBMM1l5TGpBdklpd2ljM1ZpSWpvaWFqVTNTa0ZsUW1obmR6QjBNelZTYmtoU2NsZGxlVTFOVHpSVkwwUjBUR1JTVFV4RWRIZFRka2t3UVQwaUxDSmhkV1FpT2lKa05XWTVaamhtWmkxbE9UQTFMVFJrT0RFdE9UZzRZaTFoWVdJMU1XWXpPRGN5T1RNaUxDSnBZWFFpT2pFM01qTTBOekF4TnpZc0ltRjFkR2hmZEdsdFpTSTZNVGN5TXpRM01ERTNOaXdpWlcxaGFXd2lPaUp2YkdWbmJYSkFlV0Z1WkdWNExuSjFJaXdpYjJsa0lqb2lZVEJoTWpRMU5XWXRPV1F6WXkwME9XVm1MVGt6TnpJdFl6azJaVGs0TVdRM09USmlJaXdpVUhWaWJHbGpVMlZ5ZG1salpVNTFiV0psY2lJNklqazNNREE0TnpGQlFTSXNJa0pwY25Sb1JHRjBaU0k2SWpJd0x6QXlMekU1T0RVaUxDSk1ZWE4wU205MWNtNWxlU0k2SWt4dloybHVJaXdpWjJsMlpXNU9ZVzFsSWpvaVQyeGxaeUlzSW5OMWNtNWhiV1VpT2lKVGFXMXZibTkySWl3aWJXOWlhV3hsSWpvaU16VXpPRE14T1RJeE1UWTBJaXdpUkZOUVQyNXNhVzVsVEdWMlpXd2lPaUl5SWl3aVJGTlFUMjVzYVc1bFRHVjJaV3hUZEdGMGFXTWlPaUl5SWl3aVEzVnpkRzl0WlhKSlpDSTZJakV4TlRVM09UTTVJaXdpUVdOalpYQjBaV1JRY21sMllXTjVWR1Z5YlhNaU9uUnlkV1VzSWtGalkyVndkR1ZrVUhKcGRtRmplVlJsY20xelZtVnljMmx2Yms1MWJXSmxjaUk2SWpjaUxDSlRUVk15UmtGRmJtRmliR1ZrSWpwMGNuVmxMQ0pVYjNSd01rWkJSVzVoWW14bFpDSTZabUZzYzJVc0lrRmpZMlZ3ZEdWa1VISnBkbUZqZVZSbGNtMXpSR0YwWlZScGJXVWlPakUyTmpZNU5EZzNNakVzSWxOcmFYQkZibUZpYkdVeVJrRlFjbTl0Y0hRaU9pSlpaWE1pTENKMGNuVnpkRVp5WVcxbGQyOXlhMUJ2YkdsamVTSTZJa0l5UTE4eFFWOXphV2R1YVc0dFZqVXRURWxXUlNJc0lrTnZjbkpsYkdGMGFXOXVTV1FpT2lJNE16QmlOV0ptWXkwMVlXUTRMVFF4TWprdFlUbGxaQzB4Tmpjd05qYzRZelUzWXpZaWZRLmJiQlZMMGE0ZllFZTJTemJjNjhpU1g1TmhlWW1qa2V0RWt5dkNyV1lGMGxBZ2g1QUVrakFMOVBLNXRkZTBURlF5TFFKdVFqOE5VSGpKS3dYai1wUDZQdTZ5b1FRQjZfNmxneGFMalRSeWVxOGNVRktMb3gzQVRLcXZfWFdpYXVsQmc5dGNybUtlc1owUWxwNlpMWC03ck10aEh1MXI1anl3SFdkLUN5MWZib3ZEeGZlVmJ3YUFNLUxIeEk0Y3ZDY0JieFBjcFRFNERValdDY2o1aDRULWNETlNxMUJOM1ZCTlV1NDNlTUVFRGJnbzBZeWRlTFNUOHJHZ3kzeDFoNXlsMHJiRGprekNaekRuSTVTYkhjUXAxYUUtQjYzRDdodzkyY2JNVWo1a2lfWHZ4S0tIYVRtT1FUb3pwMWpOb0U1R2tmYVIyNkVjZFBXMzQyU0xKaWxMZyIsIm5iZiI6MTcyMzQ3MDE3NywiZXhwIjoxNzIzNDc3Mzc3LCJpYXQiOjE3MjM0NzAxNzcsImlzcyI6Im15cm9hZHNhZmV0eS5yc2EuaWUiLCJhdWQiOiJteXJvYWRzYWZldHkucnNhLmllIn0.blvOKJmpu6t3Gj9gvI4UzLVdiG8RmBWxdf0YBV13LO8; QueueITAccepted-SDFrts345E-V3_bsprodfeb=EventId%3Dbsprodfeb%26QueueId%3D205c9b78-e116-4b60-86fb-67abed8faae6%26RedirectType%3Dqueue%26IssueTime%3D1723470179%26Hash%3D8115d2fdc95a4c1e12dbe109b2c9da5ee3e770265d8ce75f84fe349a867e4a86; OptanonConsent=isIABGlobal=false&datestamp=Mon+Aug+12+2024+14%3A43%3A00+GMT%2B0100+(%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.15.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0&AwaitingReconsent=false&geolocation=IE%3BL"
Bearer = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZWdtckB5YW5kZXgucnUiLCJ1bmlxdWVfbmFtZSI6Ik9MRUciLCJmYW1pbHlfbmFtZSI6IlNJTU9OT1YiLCJzdWIiOiIyODJlMWJjNi0yYjg5LWVlMTEtYWY4Ni0wMDUwNTZiOWI1MGMiLCJwcHNuIjoiOTcwMDg3MUFBIiwiMmZhYXV0aCI6InRydWUiLCJteWdvdiI6InRydWUiLCJteWdvdnRva2VuIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaMjVwYm1kclpYa3ViWGxuYjNacFpDNTJNU0lzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNNak0wTnpFNU56WXNJbTVpWmlJNk1UY3lNelEzTURFM05pd2lkbVZ5SWpvaU1TNHdJaXdpYVhOeklqb2lhSFIwY0hNNkx5OWhZMk52ZFc1MExtMTVaMjkyYVdRdWFXVXZaVEU1TjJWaE9XVXRNREpsTlMwMFkySTJMVGsyWWpJdE5UVTNNV05rTmpRMU56VTBMM1l5TGpBdklpd2ljM1ZpSWpvaWFqVTNTa0ZsUW1obmR6QjBNelZTYmtoU2NsZGxlVTFOVHpSVkwwUjBUR1JTVFV4RWRIZFRka2t3UVQwaUxDSmhkV1FpT2lKa05XWTVaamhtWmkxbE9UQTFMVFJrT0RFdE9UZzRZaTFoWVdJMU1XWXpPRGN5T1RNaUxDSnBZWFFpT2pFM01qTTBOekF4TnpZc0ltRjFkR2hmZEdsdFpTSTZNVGN5TXpRM01ERTNOaXdpWlcxaGFXd2lPaUp2YkdWbmJYSkFlV0Z1WkdWNExuSjFJaXdpYjJsa0lqb2lZVEJoTWpRMU5XWXRPV1F6WXkwME9XVm1MVGt6TnpJdFl6azJaVGs0TVdRM09USmlJaXdpVUhWaWJHbGpVMlZ5ZG1salpVNTFiV0psY2lJNklqazNNREE0TnpGQlFTSXNJa0pwY25Sb1JHRjBaU0k2SWpJd0x6QXlMekU1T0RVaUxDSk1ZWE4wU205MWNtNWxlU0k2SWt4dloybHVJaXdpWjJsMlpXNU9ZVzFsSWpvaVQyeGxaeUlzSW5OMWNtNWhiV1VpT2lKVGFXMXZibTkySWl3aWJXOWlhV3hsSWpvaU16VXpPRE14T1RJeE1UWTBJaXdpUkZOUVQyNXNhVzVsVEdWMlpXd2lPaUl5SWl3aVJGTlFUMjVzYVc1bFRHVjJaV3hUZEdGMGFXTWlPaUl5SWl3aVEzVnpkRzl0WlhKSlpDSTZJakV4TlRVM09UTTVJaXdpUVdOalpYQjBaV1JRY21sMllXTjVWR1Z5YlhNaU9uUnlkV1VzSWtGalkyVndkR1ZrVUhKcGRtRmplVlJsY20xelZtVnljMmx2Yms1MWJXSmxjaUk2SWpjaUxDSlRUVk15UmtGRmJtRmliR1ZrSWpwMGNuVmxMQ0pVYjNSd01rWkJSVzVoWW14bFpDSTZabUZzYzJVc0lrRmpZMlZ3ZEdWa1VISnBkbUZqZVZSbGNtMXpSR0YwWlZScGJXVWlPakUyTmpZNU5EZzNNakVzSWxOcmFYQkZibUZpYkdVeVJrRlFjbTl0Y0hRaU9pSlpaWE1pTENKMGNuVnpkRVp5WVcxbGQyOXlhMUJ2YkdsamVTSTZJa0l5UTE4eFFWOXphV2R1YVc0dFZqVXRURWxXUlNJc0lrTnZjbkpsYkdGMGFXOXVTV1FpT2lJNE16QmlOV0ptWXkwMVlXUTRMVFF4TWprdFlUbGxaQzB4Tmpjd05qYzRZelUzWXpZaWZRLmJiQlZMMGE0ZllFZTJTemJjNjhpU1g1TmhlWW1qa2V0RWt5dkNyV1lGMGxBZ2g1QUVrakFMOVBLNXRkZTBURlF5TFFKdVFqOE5VSGpKS3dYai1wUDZQdTZ5b1FRQjZfNmxneGFMalRSeWVxOGNVRktMb3gzQVRLcXZfWFdpYXVsQmc5dGNybUtlc1owUWxwNlpMWC03ck10aEh1MXI1anl3SFdkLUN5MWZib3ZEeGZlVmJ3YUFNLUxIeEk0Y3ZDY0JieFBjcFRFNERValdDY2o1aDRULWNETlNxMUJOM1ZCTlV1NDNlTUVFRGJnbzBZeWRlTFNUOHJHZ3kzeDFoNXlsMHJiRGprekNaekRuSTVTYkhjUXAxYUUtQjYzRDdodzkyY2JNVWo1a2lfWHZ4S0tIYVRtT1FUb3pwMWpOb0U1R2tmYVIyNkVjZFBXMzQyU0xKaWxMZyIsIm5iZiI6MTcyMzQ3MDE3NywiZXhwIjoxNzIzNDc3Mzc3LCJpYXQiOjE3MjM0NzAxNzcsImlzcyI6Im15cm9hZHNhZmV0eS5yc2EuaWUiLCJhdWQiOiJteXJvYWRzYWZldHkucnNhLmllIn0.blvOKJmpu6t3Gj9gvI4UzLVdiG8RmBWxdf0YBV13LO8"


def log(log_file='rsa.log'):
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = TimedRotatingFileHandler(
        log_file, 
        when='midnight', 
        interval=1,  
        backupCount=5,  
        encoding='utf-8',  
        delay=False, 
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Форматтер для консоли
    console_formatter = ColoredFormatter(
        '%(log_color)s%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':    'cyan',  
            'INFO':     'green',  
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'bold_red,bg_white',
            'asctime':  'green',  
            'levelname': 'green'   
        }
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

logger = log()

i = 1

def send_telegram_message(message, logger):
    chat_id = "" 
    bot_token = ""
    current_time = datetime.now()
    try:
        message_send = requests.Session()
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            'chat_id': chat_id,
            'parse_mode': 'html',
            'text': message,
            'disable_web_page_preview': True ,
            'is_automatic_forward':	True
        }
        res = message_send.post(url, params=params)

        if res.status_code == 200:
            response_data = res.json()
            message_id = response_data['result']['message_id']
            logger.info(f"message_id: {message_id}")
            logger.info(f"Telegram message sent successfully. Status {res.status_code}.")
            time.sleep(1)
        else:
            logger.error(f"Failed to send Telegram message. Status {res.status_code}. Text: {res.text}")
    except Exception as e:
        logger.error("Error sending Telegram message: ", exc_info=True)

def read_previous_data(filename='previous_data.json'):
    data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                record = json.loads(line.strip())
                data.append((record['name'], datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')))
    except FileNotFoundError:
        logger.error("File not found. Starting with an empty list.")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
    except Exception as e:
        logger.error(f"Error reading previous data: {str(e)}")
    return data

def append_data(data, filename='previous_data.json'):
    with open(filename, 'a') as file:
        for name, date in data:
            record = {
                'name': name,
                'date': date.strftime('%Y-%m-%d %H:%M:%S')
            }
            file.write(json.dumps(record) + '\n')

def compare_and_log(current_data, previous_data):
    new_entries = []
    for name, date in current_data:
        # Проверяем, есть ли текущий элемент в предыдущих данных
        if (name, date) not in previous_data:
            new_entries.append((name, date))
            logger.info(f"New slot found: Location: {name}, Next available date: {date.strftime('%Y-%m-%d %H:%M')}")
            message = f"New slot found. Location: <b>{name}</b>, Date: <b>{date.strftime('%Y-%m-%d %H:%M')}</b>"
            send_telegram_message(message, logger)
            append_data(new_entries)  # Добавляем только новые записи в файл
    return new_entries

previous_data = read_previous_data()

headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Authorization": Bearer,
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Cookie": cookie,
            "Host": "myroadsafety.rsa.ie",
            "Pragma": "no-cache",
            "Referer": "https://myroadsafety.rsa.ie/portal/booking/new/e5bbe47a-3f94-e911-a2be-0050568fd8e0/d2dc5f8c-2506-ea11-a2c3-0050568fd8e0",
            "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36",
            }

while True:
    logger.info(f"Try #{i}")
    scraper = cloudscraper.create_scraper()
    rsa = scraper.get(url, headers=headers, timeout=20)
    if rsa.status_code == 200:
        
        logger.info("Data fetched successfully.")
        data = rsa.json()
        #logger.info(data)

        valid_dates = []
        for record in data:
            next_availability = record.get('nextAvailability', '0001-01-01T00:00:00Z')
            if next_availability != "0001-01-01T00:00:00Z":
                center_name = record.get('name', 'Unknown Center')  # Имя тестового центра
                logger.debug(f"Next availability for {center_name}: {next_availability}")
                date = datetime.strptime(next_availability, '%Y-%m-%dT%H:%M:%SZ')
                valid_dates.append((record['name'], date))

        previous_data = read_previous_data()
        new_entries = compare_and_log(valid_dates, previous_data)
        if new_entries:
            previous_data.extend(new_entries) 

    else:
        logger.error(f"Failed to fetch data. Status code: {rsa.status_code}, text: {rsa.text}")

    i += 1
    logger.info("Sleep for 2 min")
    time.sleep(120)