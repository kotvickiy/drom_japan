#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import os
from config import TOKEN, CHAT_ID
from datetime import datetime


URLS = [
    "https://ekaterinburg.drom.ru/toyota/aqua/generation1/restyling2/bez-probega/?distance=500&minyear=2018&fueltype=5&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/nissan/note/generation2/restyling1/bez-probega/?distance=500&minyear=2018&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/toyota/vitz/generation3/restyling2/bez-probega/?distance=500&minyear=2018&fueltype=1&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/honda/freed/generation2/restyling0/bez-probega/?distance=500&minyear=2018&fueltype=1&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/toyota/sienta/generation2/restyling1/bez-probega/?distance=500&minyear=2018&fueltype=1&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/honda/stepwgn/generation5/restyling1/bez-probega/?minyear=2018&pts=2&damaged=2&unsold=1&distance=500",
    "https://ekaterinburg.drom.ru/toyota/noah/generation3/restyling1/bez-probega/?minyear=2018&pts=2&damaged=2&unsold=1&distance=500",
    "https://ekaterinburg.drom.ru/toyota/voxy/generation3/restyling1/bez-probega/?distance=500&minyear=2018&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/toyota/esquire/generation1/restyling1/bez-probega/?distance=500&minyear=2018&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/toyota/corolla_axio/generation2/restyling2/bez-probega/?distance=500&minyear=2018&pts=2&damaged=2&unsold=1"
]


class DromJapan:
    def __init__(self):
        self.html = ""
        self.soup = ""


    @staticmethod
    def write_append(data, file_name):
        for i in data:
            with open(file_name, "a", encoding="utf-8") as file:
                file.write(f"{i}\n")
    

    @staticmethod
    def lst_read_file(file):
        with open(file, encoding="utf-8") as file:
            return [i.strip() for i in file.readlines()]
    

    @staticmethod
    def replace_url(url):
        return url.replace("/?", "/page1/?")
    

    @staticmethod
    def checking_the_link_for_compliance_with_the_departure(link):
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        check = soup.find("div", class_="edsrp6u2")
        if check:
            return True
        return False


    def get_html(self, url):
        responce = requests.get(url)
        self.html = responce.text
    

    def get_soup(self):
        self.soup = BeautifulSoup(self.html, "lxml")
    

    def get_cnt_item(self):
        temp = self.soup.find("div", class_="css-1ksi09z eckkbc90")
        if temp:
            return int(temp.text.split(" ")[0].strip())
        return 0
    

    def get_data(self, url):
        url = self.replace_url(url)
        data = []
        cnt = 0
        lenPage = 20
        cnt_item = self.get_cnt_item()
        # print(cnt_item)
        cnt_page = 1
        num = self.soup.find_all("div", class_="e15hqrm30")
        if num:
            cnt_page = int(num[-1].text.strip())
        while cnt < cnt_page:
            # print(url)
            if cnt_item < 20:
                lenPage = cnt_item
            responce = requests.get(url)
            soup = BeautifulSoup(responce.text, "lxml")
            items = soup.find_all("a", class_="css-xb5nz8 e1huvdhj1")
            for item in items[:lenPage]:
                name = item.get("href")
                data.append(name)            
            cnt += 1
            cnt_item -= 20
            url = url.replace(f"page{cnt}", f"page{cnt + 1}")
        return data
        
    
    def engine(self):
        news = []
        data_news = []
        lst_res = []
        his_res = []
        for url in URLS:
            self.get_html(url)
            self.get_soup()
            self.get_cnt_item()
            for i in self.get_data(url):
                news.append(i)
        odls = self.lst_read_file("./old.txt")
        for new in news:
            if new not in odls:
                data_news.append(new)
        self.write_append(data_news, "./old.txt")
        for old in odls:
            if old not in news and self.checking_the_link_for_compliance_with_the_departure(old):
                # print(old)
                lst_res.append(old)
        if not os.path.exists('./history.txt'):
            open("./history.txt", "w").close()
        historys = self.lst_read_file("./history.txt")
        for i in lst_res:
            if i not in historys:
                his_res.append(i)
                requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params=dict(chat_id=CHAT_ID,text=i, disable_web_page_preview=True))
        self.write_append(his_res, "history.txt")
        open("./old.txt", "w").close()
        self.write_append(news, "./old.txt")      
    

    def run(self):
        if os.path.exists('./old.txt'):
            self.engine()
        else:
            for url in URLS:
                self.get_html(url)
                self.get_soup()
                self.get_cnt_item()
                data = self.get_data(url)
                self.write_append(data, "old.txt")


def main():
    try:
        dj = DromJapan()
        dj.run()
        print("[ + ]", datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    except Exception as ex:
        print(f"[ - ] {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {ex}")


if __name__ == '__main__':
    main()
