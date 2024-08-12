import requests
import time
import logging
import json
from datetime import datetime
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


# куки и токен берем из браузера. Адрес эндпоинта мог поменяться, надо проверять.
url = "https://myroadsafety.rsa.ie/api/v1/Availability/All/cfdda22c-4401-ef11-af89-005056b9b50c/0fed074d-c2d6-e811-a2c0-005056823b22"
cookie = "OptanonAlertBoxClosed=2024-03-29T09:21:51.346Z; _scid=634929f8-6587-46f4-85b7-d3ae960d5ec2; _tt_enable_cookie=1; _ttp=SrhtBn33tCIar-LqTfODh12cdRE; _fbp=fb.1.1711704329662.763139638; _ga=GA1.2.643024384.1711704328; _scid_r=634929f8-6587-46f4-85b7-d3ae960d5ec2; _ga_J53N6LXN3P=GS1.1.1713993927.2.1.1713993949.0.0.0; token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZWdtckB5YW5kZXgucnUiLCJ1bmlxdWVfbmFtZSI6Ik9MRUciLCJmYW1pbHlfbmFtZSI6IlNJTU9OT1YiLCJzdWIiOiIyODJlMWJjNi0yYjg5LWVlMTEtYWY4Ni0wMDUwNTZiOWI1MGMiLCJwcHNuIjoiOTcwMDg3MUFBIiwiMmZhYXV0aCI6InRydWUiLCJteWdvdiI6InRydWUiLCJteWdvdnRva2VuIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaMjVwYm1kclpYa3ViWGxuYjNacFpDNTJNU0lzSW5SNWNDSTZJa3BYVkNKOS5leUoyWlhJaU9pSXhMakFpTENKcGMzTWlPaUpvZEhSd2N6b3ZMMkZqWTI5MWJuUXViWGxuYjNacFpDNXBaUzlsTVRrM1pXRTVaUzB3TW1VMUxUUmpZall0T1RaaU1pMDFOVGN4WTJRMk5EVTNOVFF2ZGpJdU1DOGlMQ0p6ZFdJaU9pSnFOVGRLUVdWQ2FHZDNNSFF6TlZKdVNGSnlWMlY1VFUxUE5GVXZSSFJNWkZKTlRFUjBkMU4yU1RCQlBTSXNJbUYxWkNJNkltUTFaamxtT0dabUxXVTVNRFV0TkdRNE1TMDVPRGhpTFdGaFlqVXhaak00TnpJNU15SXNJbVY0Y0NJNk1UY3hOelE1TURrNE5pd2lhV0YwSWpveE56RTNORGc1TVRnMkxDSmhkWFJvWDNScGJXVWlPakUzTVRjME9Ea3hPRFlzSW1WdFlXbHNJam9pYjJ4bFoyMXlRSGxoYm1SbGVDNXlkU0lzSW05cFpDSTZJbUV3WVRJME5UVm1MVGxrTTJNdE5EbGxaaTA1TXpjeUxXTTVObVU1T0RGa056a3lZaUlzSWxCMVlteHBZMU5sY25acFkyVk9kVzFpWlhJaU9pSTVOekF3T0RjeFFVRWlMQ0pDYVhKMGFFUmhkR1VpT2lJeU1DOHdNaTh4T1RnMUlpd2lUR0Z6ZEVwdmRYSnVaWGtpT2lKTWIyZHBiaUlzSW1kcGRtVnVUbUZ0WlNJNklrOXNaV2NpTENKemRYSnVZVzFsSWpvaVUybHRiMjV2ZGlJc0ltMXZZbWxzWlNJNklqTTFNemd6TVRreU1URTJOQ0lzSWtSVFVFOXViR2x1WlV4bGRtVnNJam9pTWlJc0lrUlRVRTl1YkdsdVpVeGxkbVZzVTNSaGRHbGpJam9pTWlJc0lrTjFjM1J2YldWeVNXUWlPaUl4TVRVMU56a3pPU0lzSWtGalkyVndkR1ZrVUhKcGRtRmplVlJsY20xeklqcDBjblZsTENKQlkyTmxjSFJsWkZCeWFYWmhZM2xVWlhKdGMxWmxjbk5wYjI1T2RXMWlaWElpT2lJM0lpd2lVMDFUTWtaQlJXNWhZbXhsWkNJNmRISjFaU3dpUVdOalpYQjBaV1JRY21sMllXTjVWR1Z5YlhORVlYUmxWR2x0WlNJNk1UWTJOamswT0RjeU1Td2lVMnRwY0VWdVlXSnNaVEpHUVZCeWIyMXdkQ0k2SWxsbGN5SXNJblJ5ZFhOMFJuSmhiV1YzYjNKclVHOXNhV041SWpvaVFqSkRYekZCWDNOcFoyNXBiaTFXTlMxTVNWWkZJaXdpUTI5eWNtVnNZWFJwYjI1SlpDSTZJakJoWkRoaVlUQXlMV0l4WldZdE5HRmpZUzFpWVRBMExUWTRPR05tTUdWa01XSmtZeUlzSW01aVppSTZNVGN4TnpRNE9URTRObjAuRU1mY3hWZWRYWGluN0FWcy1UelFEa092cTJPanNhT1ZfQ2Z0dWZBWVBGMHJOM0Nic0RndVBqd2RPUkl5RlhPaURDeTYxdVFzQ0RhbE0wSWc3Vno3d2VMOEdXNzJTcldnYnFtdkZLX1dqTUIyX2xCZE1qNUVvSUZwMXVlVmk5eDRranJLcWY5N0s1RHpDa1YyMlVJRmFhQi10MV90aEtwOUFDUHFZM21WMkl5T2cxZVotb1pkZVFfZnZ0MUdRSEVQWGlRbS1WTGMwWVJHM3lGTHlpZXdYVm5ZOGVSWmhkVWVXS3BaWjl6QjlfM3k0aElTQlplSEZFSjd5QmJyLUFPVkpfT2VLM3phUzJSakRNS2hQTExOQlA1VFhXVXdXZUFPZGNTYUJZUGhBUUp3YnhuWGlkVVVTR3hIZ3ozVUxrMlJMRzlnTlVJYm01SkVoazk1WU5BQXd3IiwibmJmIjoxNzE3NDg5MTg2LCJleHAiOjE3MTc0OTYzODYsImlhdCI6MTcxNzQ4OTE4NiwiaXNzIjoibXlyb2Fkc2FmZXR5LnJzYS5pZSIsImF1ZCI6Im15cm9hZHNhZmV0eS5yc2EuaWUifQ.CEgFQ-Ph-Qb6oo5XDHvNFj2_ga3dGSbry-8XeLA_8no; QueueITAccepted-SDFrts345E-V3_bsprodfeb=EventId%3Dbsprodfeb%26QueueId%3Ddc7fa33e-233a-47f4-b1fd-b9eab0f97d7a%26RedirectType%3Dsafetynet%26IssueTime%3D1717489187%26Hash%3D28368cc536f110a99208a6c559b0544af9ee1bdd9a503d0b8763f21f364cb5a1; OptanonConsent=isIABGlobal=false&datestamp=Tue+Jun+04+2024+09%3A19%3A46+GMT%2B0100+(%D0%92%D0%B5%D0%BB%D0%B8%D0%BA%D0%BE%D0%B1%D1%80%D0%B8%D1%82%D0%B0%D0%BD%D0%B8%D1%8F%2C+%D0%BB%D0%B5%D1%82%D0%BD%D0%B5%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=6.15.0&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1&geolocation=IE%3BL&AwaitingReconsent=false"
Bearer = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Im9sZWdtckB5YW5kZXgucnUiLCJ1bmlxdWVfbmFtZSI6Ik9MRUciLCJmYW1pbHlfbmFtZSI6IlNJTU9OT1YiLCJzdWIiOiIyODJlMWJjNi0yYjg5LWVlMTEtYWY4Ni0wMDUwNTZiOWI1MGMiLCJwcHNuIjoiOTcwMDg3MUFBIiwiMmZhYXV0aCI6InRydWUiLCJteWdvdiI6InRydWUiLCJteWdvdnRva2VuIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaMjVwYm1kclpYa3ViWGxuYjNacFpDNTJNU0lzSW5SNWNDSTZJa3BYVkNKOS5leUoyWlhJaU9pSXhMakFpTENKcGMzTWlPaUpvZEhSd2N6b3ZMMkZqWTI5MWJuUXViWGxuYjNacFpDNXBaUzlsTVRrM1pXRTVaUzB3TW1VMUxUUmpZall0T1RaaU1pMDFOVGN4WTJRMk5EVTNOVFF2ZGpJdU1DOGlMQ0p6ZFdJaU9pSnFOVGRLUVdWQ2FHZDNNSFF6TlZKdVNGSnlWMlY1VFUxUE5GVXZSSFJNWkZKTlRFUjBkMU4yU1RCQlBTSXNJbUYxWkNJNkltUTFaamxtT0dabUxXVTVNRFV0TkdRNE1TMDVPRGhpTFdGaFlqVXhaak00TnpJNU15SXNJbVY0Y0NJNk1UY3hOelE1TURrNE5pd2lhV0YwSWpveE56RTNORGc1TVRnMkxDSmhkWFJvWDNScGJXVWlPakUzTVRjME9Ea3hPRFlzSW1WdFlXbHNJam9pYjJ4bFoyMXlRSGxoYm1SbGVDNXlkU0lzSW05cFpDSTZJbUV3WVRJME5UVm1MVGxrTTJNdE5EbGxaaTA1TXpjeUxXTTVObVU1T0RGa056a3lZaUlzSWxCMVlteHBZMU5sY25acFkyVk9kVzFpWlhJaU9pSTVOekF3T0RjeFFVRWlMQ0pDYVhKMGFFUmhkR1VpT2lJeU1DOHdNaTh4T1RnMUlpd2lUR0Z6ZEVwdmRYSnVaWGtpT2lKTWIyZHBiaUlzSW1kcGRtVnVUbUZ0WlNJNklrOXNaV2NpTENKemRYSnVZVzFsSWpvaVUybHRiMjV2ZGlJc0ltMXZZbWxzWlNJNklqTTFNemd6TVRreU1URTJOQ0lzSWtSVFVFOXViR2x1WlV4bGRtVnNJam9pTWlJc0lrUlRVRTl1YkdsdVpVeGxkbVZzVTNSaGRHbGpJam9pTWlJc0lrTjFjM1J2YldWeVNXUWlPaUl4TVRVMU56a3pPU0lzSWtGalkyVndkR1ZrVUhKcGRtRmplVlJsY20xeklqcDBjblZsTENKQlkyTmxjSFJsWkZCeWFYWmhZM2xVWlhKdGMxWmxjbk5wYjI1T2RXMWlaWElpT2lJM0lpd2lVMDFUTWtaQlJXNWhZbXhsWkNJNmRISjFaU3dpUVdOalpYQjBaV1JRY21sMllXTjVWR1Z5YlhORVlYUmxWR2x0WlNJNk1UWTJOamswT0RjeU1Td2lVMnRwY0VWdVlXSnNaVEpHUVZCeWIyMXdkQ0k2SWxsbGN5SXNJblJ5ZFhOMFJuSmhiV1YzYjNKclVHOXNhV041SWpvaVFqSkRYekZCWDNOcFoyNXBiaTFXTlMxTVNWWkZJaXdpUTI5eWNtVnNZWFJwYjI1SlpDSTZJakJoWkRoaVlUQXlMV0l4WldZdE5HRmpZUzFpWVRBMExUWTRPR05tTUdWa01XSmtZeUlzSW01aVppSTZNVGN4TnpRNE9URTRObjAuRU1mY3hWZWRYWGluN0FWcy1UelFEa092cTJPanNhT1ZfQ2Z0dWZBWVBGMHJOM0Nic0RndVBqd2RPUkl5RlhPaURDeTYxdVFzQ0RhbE0wSWc3Vno3d2VMOEdXNzJTcldnYnFtdkZLX1dqTUIyX2xCZE1qNUVvSUZwMXVlVmk5eDRranJLcWY5N0s1RHpDa1YyMlVJRmFhQi10MV90aEtwOUFDUHFZM21WMkl5T2cxZVotb1pkZVFfZnZ0MUdRSEVQWGlRbS1WTGMwWVJHM3lGTHlpZXdYVm5ZOGVSWmhkVWVXS3BaWjl6QjlfM3k0aElTQlplSEZFSjd5QmJyLUFPVkpfT2VLM3phUzJSakRNS2hQTExOQlA1VFhXVXdXZUFPZGNTYUJZUGhBUUp3YnhuWGlkVVVTR3hIZ3ozVUxrMlJMRzlnTlVJYm01SkVoazk1WU5BQXd3IiwibmJmIjoxNzE3NDg5MTg2LCJleHAiOjE3MTc0OTYzODYsImlhdCI6MTcxNzQ4OTE4NiwiaXNzIjoibXlyb2Fkc2FmZXR5LnJzYS5pZSIsImF1ZCI6Im15cm9hZHNhZmV0eS5yc2EuaWUifQ.CEgFQ-Ph-Qb6oo5XDHvNFj2_ga3dGSbry-8XeLA_8no"


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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            }

while True:
    logger.info(f"Try #{i}")
    rsa = requests.get(url, headers=headers, timeout=20)
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
        logger.error(f"Failed to fetch data. Status code: {rsa.status_code}")

    i += 1
    logger.info("Sleep for 2 min")
    time.sleep(120)