
#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


#############################################
# PROJE GÖREVLERİ
#############################################

#############################################
# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################

import pandas as pd

#§ Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.

df= pd.read_csv('persona.csv')


def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?

df['SOURCE'].unique()

#Soru 3: Kaç unique PRICE vardır?

df['PRICE'].unique()

#§ Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df['PRICE'].value_counts()

#Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df['COUNTRY'].value_counts()

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby('COUNTRY').agg({'PRICE':'sum'})
df.groupby('COUNTRY')['PRICE'].sum()
# Soru 7: SOURCE türlerine göre satış sayıları nedir?


df['SOURCE'].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby('COUNTRY')['PRICE'].mean()

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby('SOURCE')['PRICE'].mean()

# § Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(['COUNTRY','SOURCE'])['PRICE'].mean()

# Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?

df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'})

# Görev 3: Çıktıyı PRICE’a göre sıralayınız.

agg_df=df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'}).sort_values(by='PRICE',ascending=False)

# Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.

df.sort_values(by='PRICE',ascending=False)

agg_df=agg_df.reset_index()
agg_df.head()


# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

bins=[0,18,23,30,40,agg_df['AGE'].max()]
agg_labels=['0_18','19_23','24_30','31_40','41_'+str(agg_df['AGE'].max())]

agg_df['age_cat']=pd.cut(agg_df['AGE'],bins,labels=agg_labels)

# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.

agg_df.values
[row[0].upper()+'_'+row[1].upper()+'_'+row[2].upper()+'_'+row[5].upper() for row in agg_df.values]

agg_df['customers_level_based']= [row[0].upper()+'_'+row[1].upper()+'_'+row[2].upper()+'_'+row[5].upper() for row in agg_df.values]

agg_df= agg_df[['customers_level_based','PRICE']]

agg_df.columns=['customers_level_based', 'PRICE']

agg_df['customers_level_based'].value_counts()

agg_df.groupby('customers_level_based').agg({'PRICE':'mean'})

# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.


agg_df['SEGMENT']= pd.qcut(agg_df['PRICE'], 4, labels=['D','C','B','A'])
agg_df.head()

agg_df.groupby('SEGMENT').agg({'PRICE':['mean','max','sum','count']})



#Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.

new_user='TUR_ANDROID_FEMALE_31_40'
agg_df[agg_df['customers_level_based']==new_user]
new_user_1='FRA_IOS_FEMALE_31_40'
agg_df[agg_df['customers_level_based']==new_user_1]
