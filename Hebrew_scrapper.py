import codecs
import pandas as pd
from bs4 import BeautifulSoup as bs
import os

path = os.getcwd()


def scrapper(file):
    name = []
    phone = []
    address = []
    info = bs(codecs.open(path+"\\data\\"+file, "r", "utf-8"), features="html.parser")
    k1 = info.find_all('div', attrs={'class': 'panel panel-info text-right'})
    for i in range(len(k1)):
        stri = str(k1[i].text)
        str3 = stri.replace('\n', '').replace('\t', '').replace('edit', '').replace('expand_less', ' ')
        if 'phone' in str3 and 'email' not in str3:
            phone.append(str3[str3.index('phone') + 5:str3.index('place')])
        if 'phone' in str3 and 'email' in str3:
            phone.append(str3[str3.index('phone') + 5:str3.index('email')])
        if 'phone' not in str3:
            phone.append("Not Found")
        if 'place' in str3:
            try:
                address.append(str3[str3.index('place') + 5:].replace("עדכן כרטיס", ''))
            except ValueError:
                address.append(str3[str3.index('place') + 5:])
        if 'place' not in str3:
            address.append('Not Found')

    try:
        for n in info.find_all('h3', attrs={'class': 'panel-title'}):
            nam = n.text.strip()
            if len(nam) == 0:
                n = "not found"
                name.append(n)
            else:
                name.append(nam)
    except ValueError:
        print(" element not found")
    data = [name, phone, address]
    df = pd.DataFrame(data, index=['name', 'phone', 'address'])
    tdf = df.T
    tdf.to_csv('dataada.csv', encoding='utf-8-sig', mode='a', index=False)
    print('ok')


if __name__ == "__main__":
    _, _, filenames = next(os.walk(path + "\\data"))
    for k in filenames:
        scrapper(k)
