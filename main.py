import os
import requests
from bs4 import BeautifulSoup as BS
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
    "https://ekaterinburg.drom.ru/toyota/corolla_axio/generation2/restyling2/bez-probega/?distance=500&minyear=2018&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/honda/vezel/generation1/restyling1/bez-probega/?minyear=2018&maxyear=2020&pts=2&damaged=2&unsold=1&distance=500",
    "https://ekaterinburg.drom.ru/toyota/corolla_fielder/generation3/restyling2/bez-probega/?minyear=2018&maxyear=2020&pts=2&damaged=2&unsold=1",
    "https://ekaterinburg.drom.ru/toyota/prius/generation3/bez-probega/?pts=2&damaged=2&unsold=1&distance=500",
    "https://ekaterinburg.drom.ru/toyota/prius_a/generation1/restyling1/bez-probega/?distance=500&minyear=2018&maxyear=2020&pts=2&damaged=2&unsold=1"
]


def write_append(data, file_name):
    for i in data:
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(f"{i}\n")


def lst_read_file(file):
    with open(file, encoding="utf-8") as file:
        return [i.strip() for i in file.readlines()]


def replace_url(url):
    return url.replace("/?", "/page1/?")


def checking_the_link_for_compliance_with_the_departure(link):
    response = requests.get(url=link)
    html = response.text
    soup = BS(html, 'lxml')
    check = soup.find("div", class_="edsrp6u2")
    check2 = soup.find("div", class_="e4ozpu0")
    if check or check2:
        return True
    return False


def check_history(his_data, new_data):
    res = []
    for h in his_data:
        if h in new_data:
            continue
        res.append(h)
    return res


def get_html(url):
    url = replace_url(url)
    response = requests.get(url)
    return response.text


def get_cnt_item(url):
    while True:
        soup = BS(get_html(url), "lxml")
        temp = soup.find("div", class_="css-1ksi09z eckkbc90")
        if temp:
            res = int(temp.text.split(" ")[0].strip())
            return res


def get_data(url):
    while True:
        data = []
        cnt = 0
        len_page = 20
        cnt_item = get_cnt_item(url)
        # print("cnt_item = ", cnt_item)
        cnt_page = 1
        soup = BS(get_html(url), "lxml")
        num = soup.find_all("div", class_="e15hqrm30")
        if num:
            cnt_page = int(num[-1].text.strip())
        while cnt < cnt_page:
            if cnt_item < 20:
                len_page = cnt_item
            items = soup.find_all("a", class_="css-xb5nz8 e1huvdhj1")
            for item in items[:len_page]:
                    name = item.get("href")
                    # print(name)
                    data.append(name)            
            cnt += 1
            cnt_item -= 20
            url = url.replace(f"page{cnt}", f"page{cnt + 1}")
        # print("len_data = ", len(data))
        if data:
            return data


def engine():
    news = []
    lst_res = []
    for url in URLS:
        for i in get_data(url):
            news.append(i)
    odls = lst_read_file("./old.txt")
    for old in odls:
        if old not in news and checking_the_link_for_compliance_with_the_departure(old):
            lst_res.append(old)
    if not os.path.exists('./history.txt'):
        open("./history.txt", "w").close()
    historys = lst_read_file("./history.txt")
    his_check = check_history(historys, news)
    open("./history.txt", "w").close()
    for i in lst_res:
        if i not in his_check:
            his_check.append(i)
            requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params=dict(chat_id=CHAT_ID,text=i, disable_web_page_preview=True))
    write_append(his_check, "history.txt")
    open("./old.txt", "w").close()
    write_append(news, "./old.txt")


def run():
    if os.path.exists('./old.txt'):
        engine()
    else:
        for url in URLS:
            data = get_data(url)
            write_append(data, "old.txt")


def main():
    try:
        run()
        print("[ + ]", datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
    except Exception as ex:
        print(f"[ - ] {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {ex}")


if __name__ == '__main__':
    main()
