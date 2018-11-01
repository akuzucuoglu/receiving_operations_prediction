# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 22:58:12 2018

@author: Ahmet
"""

#Data Preprocessing

#2. Bir buçuk yıldan geç gelen veriler bozuk olarak varsayılmıştır. 
dataset.drop(dataset[dataset["TOPLAM_SURE_OLUSTURMA_RECEIVE"]>=540].index, inplace=True)
dataset.drop(dataset[dataset["TOPLAM_SURE_OLUSTURMA_RECEIVE"]<=0].index, inplace=True)
dataset.drop(dataset[dataset["TOPLAM_SURE_OLUSTURMA_RECEIVE"].isnull()].index, inplace=True)


#3. Bozuk veri düzeltmece Yurtiçi / Yurtdışı
dataset["YURT_ICI_DISI"]=dataset.YURT_ICI_DISI.replace('Yurt dýþý','Yurt dışı')
dataset["YURT_ICI_DISI"]=dataset.YURT_ICI_DISI.replace('Yurt Ýçi','Yurt içi')
dataset["YURT_ICI_DISI"]=dataset.YURT_ICI_DISI.replace('YURTIÇI ÖDEME','Yurt içi')

#4. fill na columns for CITY, fill with COUNTRTY 
g=dataset[dataset["CITY"].isnull()]
dataset["CITY"].fillna(dataset["COUNTRY"], inplace=True)

#5. fill na with loc conditionally, TRolan boş kayıtlqrı dön Yurt içi yaz
yurt_ici_tr_nan_values = (dataset["COUNTRY"]=="TR") & (dataset["YURT_ICI_DISI"].isnull())
nulls=dataset[yurt_ici_tr_nan_values]
dataset.loc[yurt_ici_tr_nan_values,"YURT_ICI_DISI" ]="Yurt içi"

#6. fill na with loc conditionally, TRolmayan boş kayıtlqrı dön Yurt dışı yaz
yurt_ici_non_tr_nan_values = (dataset["COUNTRY"]!="TR") & (dataset["YURT_ICI_DISI"].isnull())
nulls=dataset[yurt_ici_non_tr_nan_values]
dataset.loc[yurt_ici_non_tr_nan_values,"YURT_ICI_DISI" ]="Yurt dışı"

#7. min receive date boş olanları datadan atıyoruz.
dataset.drop(dataset[dataset["MIN_RECEIVE_DATE"].isnull()].index, inplace=True)
dataset.drop(dataset[dataset["MIN_DELIVER_DATE"].isnull()].index, inplace=True)
dataset.drop(dataset[dataset["KALITE_PROV"].isnull()].index, inplace=True)

#8. gereksinim tarihi boş olanları datadan atıyoruz.
dataset.drop(dataset[dataset["GEREKSINIM_TARIHI"].isnull()].index, inplace=True)

#URETIM TASARIM değeri boş olanları Kalite Provisyonuna göre belirliyoruz.
ut_nan_gt_values= (dataset["KALITE_PROV"].str.contains("GT")) & (dataset["URETIM_TASARIM"].isnull())
dataset.loc[ut_nan_gt_values,"URETIM_TASARIM" ]="T"
#sip_satir_kalem bos olanları GY olarak atıyoruz Gider Yatırım
ut_nan_gy_values= (dataset["SIP_SATIR_KALEM"] == "KALEMSÝZ") & (dataset["URETIM_TASARIM"].isnull())
dataset.loc[ut_nan_gy_values,"URETIM_TASARIM" ]="GY"
#kalanları Ü olarak atıyoruz.!!!
dataset.loc[dataset["URETIM_TASARIM"].isnull(),"URETIM_TASARIM" ]="Ü"

#VENDOR TYPE doldurmaca, Dağıtıcı olanlar Dağıtıcı dieğrleri Üretici olarak belirlenir.
#yeni kolon oluştur.
dataset["DAGITICI_MI"] =""

#vendor_tpe_bos_olanlar
#öncelikle boş kayıtlar DIGER olarak belirlenir.
dataset.loc[dataset["VENDOR_TYPE"].isnull(),"VENDOR_TYPE" ]="DIGER"

dagitici_mi = (dataset["VENDOR_TYPE"].str.contains("DAGITICI"))
dataset.loc[dagitici_mi,"DAGITICI_MI" ]="Y"
dataset.loc[dataset["DAGITICI_MI"]=="","DAGITICI_MI"]="N"

#bozuk veri düzeltmece CITY (Ankara olanlar için)
dataset["CITY"]=dataset.CITY.replace('YEN?MAHALLE','ANKARA')
dataset["CITY"]=dataset.CITY.replace('KAHRAMAN KAZAN','ANKARA')

#ANKARA_MI yeni kolonu oluştur. CITY at.
dataset["ANKARA_MI"] =""
dataset.loc[(dataset["CITY"].str.contains("ANKARA")),"ANKARA_MI" ]=1
dataset.loc[dataset["ANKARA_MI"]=="","ANKARA_MI"]=0
dataset.pop("CITY")

#ITEM_CATEGORY kolonu 
#regexp example
import re
dataset["ITEM_NAME_CAT"] = dataset["SIP_SATIR_KALEM"].apply(lambda x: re.search('\D+',x).group() if re.search('\D+',x) else np.nan )
dataset["ITEM_NAME_CAT"]
dataset["ITEM_NAME_CAT"].value_counts()
dataset["ITEM_NAME_CAT"].describe


#ITEM_NAME_CAT_NEW: Bu kolonda AD1010 için AD kodu oluşturularak kalemler gruplanır.
#Bir kalem grubundan 500'den az veri varsa veya kategorisi boş olan veriler varsa bunlara DIGER kodu verilir.
count_of_item_Cat =  pd.DataFrame( columns=["ITEM_NAME_CAT","COUNT"])
count_of_item_Cat["COUNT"] = dataset['ITEM_NAME_CAT'].value_counts()
count_of_item_Cat["ITEM_NAME_CAT"]= dataset['ITEM_NAME_CAT'].value_counts().index
count_of_kucuk_item_Cat = count_of_item_Cat[count_of_item_Cat["COUNT"]<500]
dataset["ITEM_NAME_CAT_NEW"] = dataset["ITEM_NAME_CAT"]

for deger in count_of_kucuk_item_Cat["ITEM_NAME_CAT"]:
    dataset.loc[dataset["ITEM_NAME_CAT"] == deger,"ITEM_NAME_CAT_NEW" ]="DIGER"
    
dataset.loc[dataset["ITEM_NAME_CAT_NEW"].isnull(),"ITEM_NAME_CAT_NEW" ]="DIGER"

dataset.pop("ITEM_NAME_CAT")

##Satınalmacıların 300'den az satın alması varsa 1000000 ID'sinde gruplanır.
count_of_satinalmaci =  pd.DataFrame( columns=["SATINALMACI_ID","COUNT"])
count_of_satinalmaci["COUNT"] = dataset['SATINALMACI_ID'].value_counts()
count_of_satinalmaci["SATINALMACI_ID"]= dataset['SATINALMACI_ID'].value_counts().index
count_kucuk_satinalmaci = count_of_satinalmaci[count_of_satinalmaci["COUNT"]<300]
dataset["SATINALMACI_ID_NEW"] = dataset["SATINALMACI_ID"]

for deger in count_kucuk_satinalmaci["SATINALMACI_ID"]:
    dataset.loc[dataset["SATINALMACI_ID"] == deger,"SATINALMACI_ID_NEW" ]="1000000"

dataset.pop("SATINALMACI_ID")

#KM_MI kolonu kalite provizyonlarına bakılarak oluşturulur.
dataset["KM_MI"] = dataset["KALITE_PROV"].apply(lambda x: 1 if re.search('(K)',x) else 0 )

#Bütçe tiplerinde gruplama yapılır. Verisi 500'den az olan bütçe tipleri diğer olarak gruplanır.
dataset.loc[dataset["BUTCE_TIPI"] == "GG483","BUTCE_TIPI" ]= "483"
dataset.loc[dataset["BUTCE_TIPI"].str.contains("GG"), "BUTCE_TIPI" ]= "GGDIGER"

count_of_butce_tipi =  pd.DataFrame( columns=["BUTCE_TIPI","COUNT"])
count_of_butce_tipi["COUNT"] = dataset['BUTCE_TIPI'].value_counts()
count_of_butce_tipi["BUTCE_TIPI"]= dataset['BUTCE_TIPI'].value_counts().index
count_of_butce_tipi_kucuk = count_of_butce_tipi[count_of_butce_tipi["COUNT"]<500]
dataset["BUTCE_TIPI_NEW"] = dataset["BUTCE_TIPI"]

for deger in count_of_butce_tipi_kucuk["BUTCE_TIPI"]:
    dataset.loc[dataset["BUTCE_TIPI"] == deger,"BUTCE_TIPI_NEW" ]="DIGER"

dataset.pop("BUTCE_TIPI")

#Proje 4 haneli olarak alınır. Verisi 200'den az olan projeler DIGER olarak gruplanır.
dataset["PROJE"]=dataset["PROJE"].str.slice(0,4)
count_of_proje =  pd.DataFrame( columns=["PROJE","COUNT"])
count_of_proje["COUNT"] = dataset['PROJE'].value_counts()
count_of_proje["PROJE"]= dataset['PROJE'].value_counts().index
count_of_proje_kucuk = count_of_proje[count_of_proje["COUNT"]<200]
dataset["PROJE_NEW"] = dataset["PROJE"]

for deger in count_of_proje_kucuk["PROJE"]:
    dataset.loc[dataset["PROJE"] == deger,"PROJE_NEW" ]="DIGER"


##Kullanılmayan kolonlar atılmaktadır.
dataset.pop ("ITEM_CATEGORY")
dataset.pop ("KALITE_PROV")
dataset.pop ("VENDOR_TYPE")
dataset.pop ("SIPARIS_NO")
dataset.pop ("SIP_SATIR_NO")
dataset.pop ("SIP_SEVK_NO")
dataset.pop ("SIP_SEVK_TESLIM_ALINAN")
dataset.pop ("SIP_SATIR_MIKTAR")
dataset.pop ("SIP_SEVK_KABUL")
dataset.pop ("SIP_SEVK_RET")
dataset.pop ("PLANLANAN_TESLIM_ALMA_TARIHI")
dataset.pop ("DELIVER_EKSI_PLANLANAN")
dataset.pop ("RECEIVE_EKSI_PLANLANAN")
dataset.pop ("MIN_RECEIVE_DATE")
dataset.pop ("GEREKSINIM_TARIHI")
dataset.pop ("SIP_ONAY_TARIHI")
dataset.pop ("SEVKIYAT_OLUSTURMA_TARIHI")
dataset.pop ("MIN_DELIVER_DATE")
dataset.pop ("SIP_SEVK_MIKTAR")
dataset.pop ("SIP_SEVK_UOM")
dataset.pop ("SIP_SATIR_KALEM")
dataset.pop ("TEDARIKCI")
dataset.pop ("ITEM_TYPE")
dataset.pop("PROJE")
dataset.pop("CEVRIM_MIKTAR")
dataset.pop("PRIMARY_UOM_CODE")
#Toplam Süreyi tahminlemeyi ayır. Kullanmadığın indep. variable'ları pop et. Kullanacağını bırak.
dataset.pop("TOPLAM_SURE_OLUSTURMA")
#y_dataset_tso_receive = numeric_dataset.pop("TOPLAM_SURE_OLUSTURMA_RECEIVE")
dataset.pop("DELIVER_EKSI_RECEIVE")
dataset.pop("RECEIVE_EKSI_GEREKSINIM")
dataset.pop("DELIVER_EKSI_GEREKSINIM")


#1. numerik alanlar stringe çevrildi
dataset["SATINALMACI_ID_NEW"]=dataset["SATINALMACI_ID_NEW"].astype('str')
dataset["PROJE_NEW"]=dataset["PROJE_NEW"].astype('str')
dataset["SEVKIYAT_OLUSTURMA_YIL"]=dataset["SEVKIYAT_OLUSTURMA_YIL"].astype('str')
dataset["SEVKIYAT_OLUSTURMA_YIL_AY"]=dataset["SEVKIYAT_OLUSTURMA_YIL_AY"].astype('str')
dataset["ANKARA_MI"]=dataset["ANKARA_MI"].astype('str')
dataset["KM_MI"]=dataset["KM_MI"].astype('str')


#Create a separate dataset to modify just one of them. Use copy().
numeric_dataset = dataset.copy()


#One Hot Encoding
char_cols = numeric_dataset.dtypes.pipe(lambda x: x[x == 'object']).index
label_mapping = {}

for c in char_cols:
    numeric_dataset[c], label_mapping[c] = pd.factorize(numeric_dataset[c])

numeric_dataset = pd.get_dummies(numeric_dataset,columns = char_cols, drop_first = True)

