#coding:utf-8
import re
import json
import requests

username = 'cephey'
password = 'QYEu7Qn3Noi6W7pG1uA8'


class RegruException(Exception):
    pass


class REGru(object):

    class Methods(object):
        CHECK_DOMAIN = 'domain/check'

    BASE_URL = 'https://api.reg.ru/api/regru2'

    def __init__(self, username=None, password=None):
        if username is None:
            raise Exception('username is required')
        if password is None:
            raise Exception('password is required')

        self.auth = 'username={}&password={}'.format(username, password)

    def request(self, url):
        resp = requests.get(url).json()
        if resp['result'] == 'success':
            return resp['answer']
        else:
            raise RegruException('lolo')

    def is_valid_hostname(hostname):
        if len(hostname) > 255:
            return False
        if hostname[~0] == ".":
            hostname = hostname[:-1]
        allowed = re.compile(r'[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63})*')
        return allowed.match(hostname)

    def check_domain(self, domains):
        """
        Возвращает имена переданных доменов и их доступность
        TODO: приводить строки к юникоду

        """
        data = None
        if isinstance(domains, list):
            data = [{'dname': name} for name in domains if name]
        if isinstance(domains, str):
            data = [{'dname': domains}, ]
        if data is None:
            raise Exception('domains must be string or list of string')

        domains = json.dumps({'domains': data})

        input_str = 'input_data={}&input_format={}'.format(domains, 'json')

        url = '{}/{}?{}&{}'.format(self.BASE_URL, self.Methods.CHECK_DOMAIN, self.auth, input_str)

        try:
            resp = self.request(url)
            return resp['domains']
        except Exception as e:
            print(e.__str__())


if __name__ == '__main__':
    ins = REGru(username, password)
    domains = [u"ya.ru", u"yayayayayaya.ru", u"xn--000.com", "", u"china.cn", u"ййй.me", u"wwww.ww", u"a.ru", u"qqйй.com"]
    resp = ins.check_domain(domains)
    for res in resp:
        print(res['dname'], res['result'])
