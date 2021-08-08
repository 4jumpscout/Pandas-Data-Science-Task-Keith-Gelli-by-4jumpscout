import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from itertools import combinations
from collections import Counter

ocak=pd.read_csv("Sales_January_2019.csv")
subat=pd.read_csv("Sales_February_2019.csv")
mart=pd.read_csv("Sales_March_2019.csv")
nisan=pd.read_csv("Sales_April_2019.csv")
mayis=pd.read_csv("Sales_May_2019.csv")
haziran=pd.read_csv("Sales_June_2019.csv")
temmuz=pd.read_csv("Sales_July_2019.csv")
agustos=pd.read_csv("Sales_August_2019.csv")
eylül=pd.read_csv("Sales_September_2019.csv")
ekim=pd.read_csv("Sales_October_2019.csv")
kasım=pd.read_csv("Sales_November_2019.csv")
aralık=pd.read_csv("Sales_December_2019.csv")

hepsi=pd.concat([ocak,subat,mart,nisan,mayis,haziran,temmuz,agustos,eylül,ekim,kasım,aralık])
hepsi.dropna(inplace=True)
### Tüm verileri tek bir DataFrame'de topladık ve boş değerleri sildik

hepsi=hepsi[hepsi["Order ID"].str[0:2]!="Or"]
### Tekrarlanan başlıkları kaldırarak düzenli bir hale getirdik

hepsi["Aylar"]=hepsi["Order Date"].str[0:2]
### Aylar adında yeni bir başlık açtık ve veriyi çeşitlendirdik



hepsi["Aylar"]=hepsi["Aylar"].astype(int)
hepsi["Order ID"]=pd.to_numeric(hepsi["Order ID"])
hepsi["Quantity Ordered"]=pd.to_numeric(hepsi["Quantity Ordered"])
hepsi["Price Each"]=pd.to_numeric(hepsi["Price Each"])
hepsi["Order Date"]=pd.to_datetime(hepsi["Order Date"])
hepsi["Purchase Address"]=hepsi["Purchase Address"].astype(str)
### Verilerin tipleri ayarlandı

hepsi["Satışlar"]=hepsi["Quantity Ordered"]*hepsi["Price Each"]
### Satışlar adında yeni bir sutün açıp siparişten kazanılan toplam tutar yazıldı



### Soru 1- Hangi ay satış için en iyisi? Bu ayda ne kadar kazanılmış?
def soru_1():
    soru_1=hepsi.groupby(["Aylar"]).sum()
    aylar=["Ocak","Subat","Mart","Nisan","Mayıs","Haziran","Temmuz","Agustos","Eylül","Ekim","Kasım","Aralık"]

    plt.title("Aylara göre kazanç grafiği")
    plt.xlabel("Aylar")
    plt.ylabel("Kazanç")
    plt.bar(aylar,soru_1["Satışlar"])
    return plt.show()



### Soru 2- En çok hangi şehire ürün satılmış
def soru_2():
    hepsi["Şehirler"]=hepsi["Purchase Address"].apply(lambda x: x.split(",")[1])
    hepsi["Şehirler"]=hepsi["Şehirler"].astype(str)
    soru_2=hepsi.groupby(["Şehirler"]).sum()
    şehir=hepsi["Şehirler"].unique()
    şehir.sort()

    plt.title("Şehirlere göre kazanç grafiği")
    plt.xlabel("Şehirler")
    plt.ylabel("Kazanç")
    plt.bar(şehir,soru_2["Satışlar"])
    return plt.show()



### Soru 3- Ne zaman reklam verirsek ürün satışlarımız maksimuma ulaşabilir?
def soru_3():
    hepsi["Saat"]=hepsi["Order Date"].dt.hour
    soru_3=hepsi.groupby(["Saat"]).sum()

    plt.title("Saatlere göre kazanç miktarı")
    plt.ylabel("Kazanç")
    plt.xlabel("Saat")
    saat=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    plt.bar(saat,soru_3["Satışlar"])
    return plt.show()


### Soru 4- Hangi ürünler en çok beraber satılmış?
def soru_4():
    soru_4 = hepsi[hepsi['Order ID'].duplicated(keep=False)]
    soru_4['Grup Hali'] = soru_4.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
    soru_4 = soru_4[['Order ID', 'Grup Hali']].drop_duplicates()

    count = Counter()

    for row in soru_4['Grup Hali']:
        row_list = row.split(',')
        count.update(Counter(combinations(row_list, 2)))

    for key,value in count.most_common(10):
        return print(key, value)


### Soru 5- En çok hangi ürün satılmış
def soru_5():
    soru_5=hepsi.groupby(["Product"]).sum()
    ürünler=hepsi["Product"].unique()
    ürünler.sort()
    figure(figsize=(10,8), dpi=50)

    plt.title("Ürünlerin satış adetleri")
    plt.xlabel("Ürünler")
    plt.ylabel("Adet")
    plt.bar(ürünler,soru_5["Quantity Ordered"])
    return plt.show()
print("Soru 1- Hangi ay satış için en iyisi? Bu ayda ne kadar kazanılmış?\n Soru 2-En çok hangi şehire ürün satılmış\n Soru 3-Ne zaman reklam verirsek ürün satışlarımız maksimuma ulaşabilir?\n Soru 4-Hangi ürünler en çok beraber satılmış?\n Soru 5-En çok hangi ürün satılmış")
x=int(input("Kaçıncı soruyu görmek istersiniz"))
while True:
    if x==1:
        soru_1()
        break
    elif x==2:
        soru_2()
        break
    elif x==3:
        soru_3()
        break
    elif x==4:
        print(soru_4())
        break
    elif x==5:
        soru_5()
        break
    else:
        print("hatalı kodlama yaptınız. Tekrar deneyiniz.")
        x = int(input("Kaçıncı soruyu görmek istersiniz"))
        continue
