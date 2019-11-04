import requests
import json
import db


def get_proxy():
    url = 'http://pubproxy.com/api/proxy?type=https'
    response = requests.get(url)
    json_proxy = json.loads(response.text)

    # Создаём словарь с данными о прокси
    proxy = dict.fromkeys(['ip', 'port'])
    proxy['ip'] = json_proxy['data'][0]['ip']
    proxy['port'] = json_proxy['data'][0]['port']
    return proxy


def write_proxy(proxy):
    connection, cursor = db.connect_to('enzymes.db')
    update_proxy = "UPDATE proxy SET ip=?, port=? WHERE id=0;"
    cursor.execute(update_proxy, (proxy['ip'], proxy['port']))
    connection.commit()


def read_proxy():
    connection, cursor = db.connect_to('enzymes.db')
    select_proxy = 'SELECT ip, port FROM proxy'
    cursor.execute(select_proxy)

    proxy_list = cursor.fetchall()
    ip, port = proxy_list[0]

    proxy = dict.fromkeys(['ip', 'port'])
    proxy['ip'] = ip
    proxy['port'] = port
    return proxy


def get_proxy_info():
    proxy = read_proxy()
    response = requests.get('http://free.ipwhois.io/json/{}?lang=ru'.format(proxy['ip'])).json()

    proxy_info = dict.fromkeys(['ip', 'country', 'city'])
    proxy_info['ip'] = response['ip']
    proxy_info['country'] = response['country']
    proxy_info['city'] = response['city']
    return proxy_info
