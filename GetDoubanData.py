import requests
from lxml import etree,html
from fake_useragent import UserAgent
import pandas as pd
import random
import  collections
import re
import openpyxl
url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4'
b=[]
for i in range(66):
    b.append(UserAgent().random)
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Mobile Safari/537.36 Edg/88.0.705.81'}
def Data(url):
    txt = requests.get(url,headers=headers).text
    tree = etree.HTML(txt)
    book_name = tree.xpath('''//li/div[2]/h2/a/text()''')
    c=[]
    for i in book_name:
        if len(i.split('\n')[2].strip()) > 0:
            c.append(i.split('\n')[2].strip())
    book_name=c
    #//*[@id="subject_list"]/ul/li[1]/div[2]/h2/a
    #//*[@id="subject_list"]/ul/li[2]/div[2]/h2/a
    #print(book_name)

    #作者、出版社、出版日期、定价
    #//*[@id="subject_list"]/ul/li[1]/div[2]/div[1]
    #//*[@id="subject_list"]/ul/li[2]/div[2]/div[1]
    all_informations = tree.xpath('''//li/div[2]/div[1]/text()''')
    c=[]
    for i in all_informations:
        c.append(i.split('\n')[3].strip())
    all_informations=c

    author = []
    publisher =[]
    book_put_on = []
    price = []
    for i in all_informations:
        count=collections.Counter(i)
        if count['/']>=4:
            author.append(i.split('/')[0]+' '+i.split('/')[1])
            publisher.append(i.split('/')[2].strip())
            book_put_on.append(i.split('/')[3].strip())
            price.append(i.split('/')[4].strip())
            continue
        author.append(i.split('/')[0].strip())
        publisher.append(i.split('/')[1].strip())
        book_put_on.append(i.split('/')[2].strip())
        try:
            price.append(i.split('/')[3].strip())
        except:
            price.append(0)
    print(author)
    print(publisher)
    print(book_put_on)
    print(price)
    #publisher = tree.xpath('''''')
    #book_put_on = tree.xpath('''''')
    #price = tree.xpath('''''')




    #评分、评论人数
    #//*[@id="subject_list"]/ul/li[1]/div[2]/div[2]/span[2]
    #//*[@id="subject_list"]/ul/li[2]/div[2]/div[2]/span[2]

    #//*[@id="subject_list"]/ul/li[1]/div[2]/div[2]/span[3]
    #//*[@id="subject_list"]/ul/li[2]/div[2]/div[2]/span[3]
    score = tree.xpath('''//li/div[2]/div[2]/span[2]/text()''')
    print(score)

    comment_num = tree.xpath('''//li/div[2]/div[2]/span[3]/text()''')
    c=[]
    for i in comment_num:
        c.append(i.split('\n')[1].strip())
    comment_num=c

    b=[]
    for i in comment_num:
        p1 = re.compile(r'[(](.*?)[)]', re.S) #最小匹配
        b.append(''.join(re.findall(p1, i)))
    comment_num=b

    df = pd.DataFrame([book_name,author,publisher,book_put_on,price,score,comment_num]).T
    df.columns=['book_name','author','publisher','book_put_on','price','score','comment_num']
    return df

df_all = pd.DataFrame()

for i in range(0,399,20):

    url1= url+"?start={}&type=T".format(i)
    if i==0:
        url1=url
    print(url1)
    df=Data(url1)
    # print("第{}页抓取完毕".format(int(i/20))+1)
    df_all=df_all.append(df,ignore_index=True)

name = '豆瓣小说综合前400'
df_all.to_excel(r"C:\Users\AidenPierce\Desktop\1.xlsx",index=False)