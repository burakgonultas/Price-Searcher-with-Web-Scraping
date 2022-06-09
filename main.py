# Burak Gönültaş - 2022 

# Kütüphanelerin import'u  
# Requests ve Beautifulsoup kütüphanelerinin altı çiziliyse ve çalışmıyorsa doğru interpreter'i seçtiğinizden emin olun. 
# Kullanılan interpreter'a pip install komutuyla kütüphaneler eklenmiş olmalı.

# Mail yollama işleminin çalışabilmesi için 272. satırdaki işlemleri yapınız!
import requests
from bs4 import BeautifulSoup
import smtplib
import time

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

# Çekilecek verilere ait linkler. Linkler ile ilgili hata mesajı alındığında ilgili link'in kırık olup olmadığını kontrol edin. 
CarrefoursaDomatesLink = 'https://www.carrefoursa.com/domates-pazar-kg-p-30013008'
AmaDomatesLink = 'https://www.amazon.com.tr/dp/B08XXVWYTY?ref_=cm_sw_r_cp_ud_dp_ADBRX523VM0HZG8XBTYV'
OrganikDomatesLink = 'https://www.organikciyizbiz.com/organik-domates-beef-organik-ufuklar'

CarrefoursaDeterjanLink = 'https://www.carrefoursa.com/fairy-platinum-72-yikama-bulasik-makinesi-deterjani-kapsulu-limon-kokulu-p-30033017'
AmaDeterjanLink = 'https://www.amazon.com.tr/dp/B07MG11RK6?ref_=cm_sw_r_cp_ud_dp_XT09JPW7VXT5AWDEAQDR'
HepsiburadaDeterjanLink = 'https://www.hepsiburada.com/fairy-platinum-bulasik-makinesi-deterjani-tableti-kapsulu-limon-kokulu-72-yikama-p-HBV0000011YPT'

CarrefoursaTuvaletKLink = 'https://www.carrefoursa.com/solo-tuvalet-kagidi-32-li-p-30085678'
AmaTuvaletKLink = 'https://www.amazon.com.tr/dp/B07VCNGDPJ?ref_=cm_sw_r_cp_ud_dp_T1Q0AZ048EFQRRDMW3BB'
HepsiburadaTuvaletKLink = 'https://www.hepsiburada.com/solo-tuvalet-kagidi-32-li-p-HBCV000007EFWO'


# Fiyat takibini sağlayan ana fonksiyon
def Fiyat_Takip():

    # Sonuçları mail atabilmek için çekilen verilerin içerisinde bulunan Türkçe harflerden kurtulmak zorundayız. Bunu yapabilmek için bir sözlük (dictionary) oluşturduk.
    TR_to_ENG = {'ğ': 'g', 'Ğ': 'G', 'ç': 'c', 'Ç': 'C', 'ş': 's', 'Ş': 'S', 'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ı': 'i', 'İ': 'I'}

    # Carrefoursa Domates
    
    # İlgili linkteki verileri requests ile çekiyoruz, beautiful'un html.parser özelliği ile parçalanabilir hâle getiriyoruz.
    CarDomSayfa = requests.get(CarrefoursaDomatesLink, headers = headers)
    CarDomIcerik =  BeautifulSoup(CarDomSayfa.content,'html.parser')

    # İçeriğimizi BeautifulSoup içeriğinden String hale geçiriyoruz. Bu sayede içerisinde gezip Türkçe harfleri tespit edip değiştirebiliyoruz.
    CarDomIcerik = str(CarDomIcerik)
    for key, value in TR_to_ENG.items():
        CarDomIcerik = CarDomIcerik.replace(key, value)
    CarDomIcerik =  BeautifulSoup(CarDomIcerik,'html.parser')
    
    # İlgili linkten ürünün adını çekiyoruz
    CarDomName=CarDomIcerik.find("div",{"class":"name"}).find("h1").text
    print(CarDomName)

    # İlgili linkten ürünün fiyatını çekiyoruz. Fiyatı rakipleri ile kıyaslayabilmek için replace komutuyla "," işaretini "." işaretiyle değiştiriyor, değişkeni float'a çeviriyoruz
    CarDomFiyat=float(CarDomIcerik.find("span",{"class":"item-price js-variant-price"}).get_text()[:5].replace(',','.'))
    print(CarDomFiyat)


    
    #Amazon Domates

    AmaDomSayfa = requests.get(AmaDomatesLink, headers = headers)
    AmaDomIcerik =  BeautifulSoup(AmaDomSayfa.content,'html.parser')

    AmaDomIcerik = str(AmaDomIcerik)
    for key, value in TR_to_ENG.items():
        AmaDomIcerik = AmaDomIcerik.replace(key, value)
    AmaDomIcerik =  BeautifulSoup(AmaDomIcerik,'html.parser')

    AmaDomName=AmaDomIcerik.find("span",{"id":"productTitle"}).text.strip()
    print(AmaDomName)

    AmaDomFiyat1=AmaDomIcerik.find("div",{"class":"a-section a-spacing-none aok-align-center"})
    AmaDomFiyat=float(AmaDomFiyat1.find("span","a-offscreen").get_text().replace(',','.')[:5])
    print(AmaDomFiyat)


    # Organikçiyizbiz Domates

    OrgDomSayfa = requests.get(OrganikDomatesLink, headers = headers)
    OrgDomIcerik =  BeautifulSoup(OrgDomSayfa.content,'html.parser')

    OrgDomIcerik = str(OrgDomIcerik)
    for key, value in TR_to_ENG.items():
        OrgDomIcerik = OrgDomIcerik.replace(key, value)
    OrgDomIcerik =  BeautifulSoup(OrgDomIcerik,'html.parser')

    OrgDomName=OrgDomIcerik.find("div",{"class":"col-sm-4 pull-right"}).find("h1").text
    print(OrgDomName)

    OrgDomFiyat=float(OrgDomIcerik.find("span",{"style":"color: #94C82C; font-weight: 500; font-size: 27px;"}).getText().replace(',','.')[:4])
    print(OrgDomFiyat)


    # Domates Kıyaslama
    # if else ile elde ettiğimiz fiyatları birbiriyle kıyaslıyoruz. En uygun fiyatlı olanı messageDom değişkenine atıyoruz. Bu sayede E-mail atacağımız fonksiyonu kullanabileceğiz.

    if CarDomFiyat <= AmaDomFiyat and CarDomFiyat <= OrgDomFiyat:
        #Cardomfiyat en küçükse:
        messageDom="En uygun fiyatli domates: \n"+"Market: CarrefourSA \n"+"Talep edilen: "+str(CarDomName)+"\n"+"Fiyat: "+str(CarDomFiyat)+" TL"+"\nLink: "+str(CarrefoursaDomatesLink)
        print(messageDom)
        
    elif AmaDomFiyat <= CarDomFiyat and AmaDomFiyat <= OrgDomFiyat:
        #Amazon fiyat en küçükse:
        messageDom="En uygun fiyatli domates:\n"+"Market: Amazon \n"+"Talep edilen: "+str(OrgDomName)+"\n"+"Fiyat: "+str(OrgDomFiyat)+" TL"+"\nLink: "+str(OrganikDomatesLink)
        print(messageDom)
        

    else:
        #Organik fiyat en küçükse:
        messageDom="En uygun fiyatli domates:\n"+"Market: Organikciyizbiz \n"+"Talep edilen: "+str(OrgDomName)+"\n"+"Fiyat: "+str(OrgDomFiyat)+" TL"+"\nLink: "+str(OrganikDomatesLink)
        
        print(messageDom)

    

    #Carrefoursa Bulaşık Makinesi Deterjanı (Kapsül)
    
    CarDeterSayfa = requests.get(CarrefoursaDeterjanLink, headers = headers)
    CarDeterIcerik =  BeautifulSoup(CarDeterSayfa.content,'html.parser')

    CarDeterIcerik = str(CarDeterIcerik)
    for key, value in TR_to_ENG.items():
        CarDeterIcerik = CarDeterIcerik.replace(key, value)
    CarDeterIcerik =  BeautifulSoup(CarDeterIcerik,'html.parser')

    CarDeterName=CarDeterIcerik.find("div",{"class":"name"}).find("h1").text
    print(CarDeterName)

    CarDeterFiyat=float(CarDeterIcerik.find("span",{"class":"item-price js-variant-price"}).get_text().replace(',','.')[:6])
    print(CarDeterFiyat)
    

    #Amazon Bulaşık Makinesi Deterjanı (Kapsül)
    
    AmaDeterSayfa = requests.get(AmaDeterjanLink, headers = headers)
    AmaDeterIcerik =  BeautifulSoup(AmaDeterSayfa.content,'html.parser')

    AmaDeterIcerik = str(AmaDeterIcerik)
    for key, value in TR_to_ENG.items():
        AmaDeterIcerik = AmaDeterIcerik.replace(key, value)
    AmaDeterIcerik =  BeautifulSoup(AmaDeterIcerik,'html.parser')

    AmaDeterName=AmaDeterIcerik.find("span",{"id":"productTitle"}).text.strip()
    print(AmaDeterName)
    
    AmaDeterFiyat1=AmaDeterIcerik.find("div",{"class":"a-section a-spacing-none aok-align-center"})
    AmaDeterFiyat=float(AmaDeterFiyat1.find("span","a-offscreen").get_text().replace(',','.')[:6])
    print(AmaDeterFiyat)
    

    # Hepsiburada Bulaşık Makinesi Deterjanı (Kapsül)
    
    HepsiDeterSayfa = requests.get(HepsiburadaDeterjanLink, headers = headers)
    HepsiDeterIcerik =  BeautifulSoup(HepsiDeterSayfa.content,'html.parser')

    HepsiDeterIcerik = str(HepsiDeterIcerik)
    for key, value in TR_to_ENG.items():
        HepsiDeterIcerik = HepsiDeterIcerik.replace(key, value)
    HepsiDeterIcerik =  BeautifulSoup(HepsiDeterIcerik,'html.parser')

    HepsiDeterName=HepsiDeterIcerik.find("h1",{"id":"product-name"}).text.strip()
    print(HepsiDeterName)

    HepsiDeterFiyat1=float(HepsiDeterIcerik.find("span",{"data-bind":"markupText:'currentPriceBeforePoint'"}).getText())
    HepsiDeterFiyat2=float(HepsiDeterIcerik.find("span",{"data-bind":"markupText:'currentPriceAfterPoint'"}).getText())
    HepsiDeterNokta=HepsiDeterFiyat2/100
    HepsiDeterFiyat=HepsiDeterFiyat1+HepsiDeterNokta
    print(HepsiDeterFiyat)
    
    # Deterjan Kıyaslama

    if CarDeterFiyat <= AmaDeterFiyat and CarDeterFiyat <= HepsiDeterFiyat:
        #CarrefourSA en küçükse:
        messageDeter="En uygun fiyatli deterjan: \n"+"Market: CarrefourSA \n"+"Talep edilen: "+str(CarDeterName)+"\n"+"Fiyat: "+str(CarDeterFiyat)+" TL"+"\nLink: "+str(CarrefoursaDeterjanLink)
        print(messageDeter)
        
    elif AmaDeterFiyat <= CarDeterFiyat and AmaDeterFiyat <= HepsiDeterFiyat:
        #Amazon fiyat en küçükse:
        messageDeter="En uygun fiyatli deterjan:\n"+"Market: Amazon \n"+"Talep edilen: "+str(AmaDeterName)+"\n"+"Fiyat: "+str(AmaDeterFiyat)+" TL"+"\nLink: "+str(AmaDeterjanLink)
        
        print(messageDeter)
        

    else:
        #Hepsiburada fiyat en küçükse:
        messageDeter="En uygun fiyatli deterjan:\n"+"Market: Hepsiburada \n"+"Talep edilen: "+str(HepsiDeterName)+"\n"+"Fiyat: "+str(HepsiDeterFiyat)+" TL"+"\nLink: "+str(HepsiburadaDeterjanLink)
        
        print(messageDeter)

    
    
    #Carrefoursa Tuvalet Kağıdı

    CarTKSayfa = requests.get(CarrefoursaTuvaletKLink, headers = headers)
    CarTKIcerik =  BeautifulSoup(CarTKSayfa.content,'html.parser')

    CarTKIcerik = str(CarTKIcerik)
    for key, value in TR_to_ENG.items():
        CarTKIcerik = CarTKIcerik.replace(key, value)
    CarTKIcerik =  BeautifulSoup(CarTKIcerik,'html.parser')

    CarTKName=CarTKIcerik.find("div",{"class":"name"}).find("h1").text
    print(CarTKName)

    CarTKFiyat=float(CarTKIcerik.find("span",{"class":"item-price js-variant-price"}).get_text().replace(',','.')[:6])
    print(CarTKFiyat)


    #Amazon Tuvalet Kağıdı
   
    AmaTKSayfa = requests.get(AmaTuvaletKLink, headers = headers)
    AmaTKIcerik =  BeautifulSoup(AmaTKSayfa.content,'html.parser')

    AmaTKIcerik = str(AmaTKIcerik)
    for key, value in TR_to_ENG.items():
        AmaTKIcerik = AmaTKIcerik.replace(key, value)
    AmaTKIcerik =  BeautifulSoup(AmaTKIcerik,'html.parser')

    AmaTKName=AmaTKIcerik.find("span",{"id":"productTitle"}).text.strip()
    print(AmaTKName)
    
    AmaTKFiyat1=AmaTKIcerik.find("div",{"class":"a-section a-spacing-none aok-align-center"})
    AmaTKFiyat=float(AmaTKFiyat1.find("span","a-offscreen").get_text().replace(',','.')[:6])
    print(AmaTKFiyat)

    # Hepsiburada Tuvalet Kağıdı
   
    HepsiTKSayfa = requests.get(HepsiburadaTuvaletKLink, headers = headers)
    HepsiTKIcerik =  BeautifulSoup(HepsiTKSayfa.content,'html.parser')

    HepsiTKIcerik = str(HepsiTKIcerik)
    for key, value in TR_to_ENG.items():
        HepsiTKIcerik = HepsiTKIcerik.replace(key, value)
    HepsiTKIcerik =  BeautifulSoup(HepsiTKIcerik,'html.parser')

    HepsiTKName=HepsiTKIcerik.find("h1",{"id":"product-name"}).text.strip()
    print(HepsiTKName)

    HepsiTKFiyat1=float(HepsiTKIcerik.find("span",{"data-bind":"markupText:'currentPriceBeforePoint'"}).getText())
    HepsiTKFiyat2=float(HepsiTKIcerik.find("span",{"data-bind":"markupText:'currentPriceAfterPoint'"}).getText())
    HepsiTKNokta=HepsiTKFiyat2/100
    HepsiTKFiyat=HepsiTKFiyat1+HepsiTKNokta
    print(HepsiTKFiyat)

    # Tuvalet Kağıdı Kıyaslama

    if CarTKFiyat <= AmaTKFiyat and CarTKFiyat <= HepsiTKFiyat:
        #CarrefourSA en küçükse:
        messageTK="En uygun fiyatli Tuvalet Kagidi: \n"+"Market: CarrefourSA \n"+"Talep edilen: "+str(CarTKName)+"\n"+"Fiyat: "+str(CarTKFiyat)+" TL"+"\nLink: "+str(CarrefoursaTuvaletKLink)
        print(messageTK)
        
    elif AmaTKFiyat <= CarTKFiyat and AmaTKFiyat <= HepsiTKFiyat:
        #Amazon fiyat en küçükse:
        messageTK="En uygun fiyatli Tuvalet Kagidi:\n"+"Market: Amazon \n"+"Talep edilen: "+str(AmaTKName)+"\n"+"Fiyat: "+str(AmaTKFiyat)+" TL"+"\nLink: "+str(AmaTuvaletKLink)
        
        print(messageTK)
        

    else:
        #Hepsiburada fiyat en küçükse:
        messageTK="En uygun fiyatli Tuvalet Kagidi:\n"+"Market: Hepsiburada \n"+"Talep edilen: "+str(HepsiTKName)+"\n"+"Fiyat: "+str(HepsiTKFiyat)+" TL"+"\nLink: "+str(HepsiburadaTuvaletKLink)
        
        print(messageTK)

    # Elde ettiğimiz değerleri mail_yolla fonksiyonuna yolluyoruz.
    mail_yolla(messageDom,messageDeter,messageTK)
    
# E Posta yollama 
    
def mail_yolla(messageDom,messageDeter,messageTK):

    # Klasik SMTP komutlarıyla elde ettiğimiz verileri mail olarak yolluyoruz. Detaylı bilgi: https://docs.python.org/3/library/smtplib.html

    # sender değişkenine mail'i yollacak adresi, receiver'a mail'i alacak adresi yazınız.
    # server.login işlemine sender mail'inden alınan "uygulama şifresi" izninin anahtar'ını yazınız.
    # Detaylı bilgi için: https://support.google.com/accounts/answer/185833?hl=tr
    sender ="mail_gönderen@gmail.com"
    receiver = "mail_alan@gmail.com"
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(sender,"mail_gönderen'in şifresi buraya gelmeli.")
        subject = "Haftalik sepetiniz"
        body = messageDom + "\n\n"+messageDeter+ "\n\n"+messageTK
        mailContent= f"To:{receiver} \n From:{sender} \n Subject: {subject} \n\n {body}"

        server.sendmail(sender,receiver,mailContent)
        print("Mail Gonderildi!")
    except smtplib.SMTPException as e:
        print(e)
    finally:
        server.quit()

# Programımızın belirli aralıklarla mail atabilmesi için TIME kütüphanesi kullanarak bir zamanlayıcı oluşturuyoruz. 
# Oluşturduğumuz zamanlayıcının devamlı çalışmasını sağlamak için sonsuz while döngüsünün altına yazıyoruz.
while(1):
    Fiyat_Takip()
    time.sleep(60*60)
    

    # Kodumu incelediğiniz için teşekkürler. Soru ve önerileriniz için: https://www.linkedin.com/in/burakgonultas/
