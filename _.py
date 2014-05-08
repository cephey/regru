#coding:utf-8
import json
import requests

from settings import username, password

import logging
logger = logging.getLogger(__name__)


class RegRuAPI(object):

    # API methods
    CHECK_DOMAIN = 'domain/check'
    # end API methods

    BASE_URL = 'https://api.reg.ru/api/regru2'

    def __init__(self, username=None, password=None):
        if username is None:
            raise Exception('username is required')
        if password is None:
            raise Exception('password is required')

        self.auth = 'username={}&password={}'.format(username, password)

    def request(self, url):
        """
        Запрос в REG.RU API

        """
        try:
            response = requests.get(url).json()
        except Exception as e:
            logger.error(e.__str__())
            return None

        if response['result'] == 'success':
            return response['answer']
        else:
            logger.error(response)
            return None

    def build_url(self, method, data):
        """
        Собираю URL

        """
        return '{}/{}?{}&{}'.format(self.BASE_URL, method, self.auth, data)

    def check_domain(self, domains):
        """
        domains: list_of_string or string

        Проверка доступности доменов
        Возвращает имена переданных доменов и их доступность

        Возвращать словарь вида:
        {
            u'yayayayayaya.ru': {'error_code': None,                            'result': u'Available'},
            u'china.cn':        {'error_code': u'TLD_DISABLED',                 'result': u'error'},
            u'ййй.me':          {'error_code': u'DOMAIN_BAD_NAME',              'result': u'error'},
            u'ya.ru':           {'error_code': u'DOMAIN_ALREADY_EXISTS',        'result': u'error'},
            u'a.ru':            {'error_code': u'DOMAIN_INVALID_LENGTH',        'result': u'error'},
            u'qqйй.com':        {'error_code': u'HAVE_MIXED_CODETABLES',        'result': u'error'}
            u'':                {'error_code': u'INVALID_DOMAIN_NAME_FORMAT',   'result': u'error'},
            u'xn--000.com':     {'error_code': u'INVALID_DOMAIN_NAME_PUNYCODE', 'result': u'error'},
        }

        """
        if isinstance(domains, str):
            domains = [domains, ]

        data = []
        if isinstance(domains, list):
            # убираю повторяющиеся имена
            domains = set(domains)

            for domain in domains:
                print('-', domain, '-')
                # domain = domain.decode('utf-8')
                data.append({'dname': domain})

        domains_str = json.dumps({'domains': data})
        input_str = 'input_data={}&input_format={}'.format(domains_str, 'json')

        url = self.build_url(self.CHECK_DOMAIN, input_str)

        response = self.request(url)

        result = {}
        if response:
            for domain in response['domains']:
                key = domain['dname'].encode('utf-8')
                result[key] = {'result': domain['result'], 'error_code': domain.pop('error_code', None)}
            return result

        return None


def check_available():
    """
    Проверка доступности доменов

    """
    domains = ["ya.ru", "yayayayayaya.ru", "xn--000.com", "", "china.cn", "ййй.me", "a.ru", "qqйй.com"]

    api = RegRuAPI(username, password)

    resp = api.check_domain(domains)

    if resp:
        for domain in domains:
            if resp[domain]['result'] == 'error':
                print(domain, resp[domain]['error_code'])
            else:
                print(domain, resp[domain]['result'])
    else:
        print(u'Ошибка сервиса')


if __name__ == '__main__':
    check_available()
