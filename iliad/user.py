from requests import Session
from lxml import html
import json

class User:

    url = "https://www.iliad.it/account/"
    toReplace = ('€', 'GB')

    def __init__(self, username, password):

        self.ident  = username
        self.passw  = password
        self.sess   = Session()
        self.load_xpaths()
        self.login()

    def login(self):
        
        data = {
            "login-ident": self.ident,
            "login-pwd": self.passw
        }

        res_login = self.sess.post(self.url, data)
        if not self.check_login(res_login):
            raise Exception("Login error. Check data")
        self.data = self.parse_data(res_login)
    
    def check_login(self, result):
        #error_xpath = "/html/body/div[1]/div[1]/div/div[1]/div"
        if "ID utente o password non corretto." in result.text:
            return False
        return True

    def load_xpaths(self):
        with open("iliad/xpaths.json", "r") as xpaths_json_file:
            self.xpaths = json.load(xpaths_json_file)

    def reload(self):
        res_reload = self.sess.get(self.url)
        self.data = self.parse_data(res_reload)
        return self.data.copy()
    
    def parse_data(self, result):
        ret = {}
        tree = html.fromstring(result.content)
        for key in self.xpaths:
            elem = tree.xpath(self.xpaths[key])[0]
            for r in self.toReplace:
                elem = elem.replace(r, '')
            elem = elem.replace(',', '.')
            elem = float(elem)
            ret[key] = elem
        return ret