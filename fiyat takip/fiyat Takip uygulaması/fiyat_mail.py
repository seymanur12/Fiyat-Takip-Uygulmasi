import requests
from bs4 import BeautifulSoup
import time
import smtplib

url1 ="https://www.trendyol.com/stradivarius/suni-kurklu-biker-ceket-p-51247165?boutiqueId=61&merchantId=150331"
def checkPrice(url , paramprice):
    headers = {'User-agent':''}
    page = requests.get(url ,  headers=headers)
    htmlPage = BeautifulSoup(page.content,'lxml')
    """ incele diyip etiketi seçiyoruz """
    productTitle = htmlPage.find("h1",class_ ="pr-new-br").getText()
    """ ucretini alalim """
    price = htmlPage.find("span", class_ ="prc-dsc").getText()
    """ img etiketinin class ini vercez"""
    image = htmlPage.find("img", class_="js-image-zoom__zoomed-area")
    """ işlem yapabilmek için int  ya da float a  çevircez"""
    """ işlem yapabilmek için TL ifadesini de kaldirmamiz gerek"""
    converstedPrice = float(price.replace(",",".").replace(" TL",""))
    """   price mevcut fiyatinda küçükse ürün fiyati düştü yazsin"""
    if(converstedPrice <= float(paramprice)):
     print("ürün fiyati düştü")
     sendMail(productTitle, url )
    else:
        print("ürün fiyati düşmedi")
        print(converstedPrice)



def sendMail(title,url ):
    """ kimden gideceği:""" 
    sender = 'örnek@gmail.com'
    receiver = 'örnek@gmail.com'  # alıcının mail adresi
   
    try:
        # SMTP sunucusuna bağlan
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        
        # TLS ile güvenli bağlantı kur
        server.starttls()
        server.login(sender, '')  # Burada ' ' içine e-posta hesabınızın şifresini yazmalısınız
        # E-posta konusunu oluştur
        subject = title + ' istediğin fiyata düştü'
        # E-posta içeriğini oluştur
        body = 'Bu linkten gidebilirsin: ' + url
        # E-posta içeriğini biçimlendir
        mailcontent = f"To:{receiver}\nFrom:{sender}\nSubject:{subject}\n\n{body}"
        # E-postayı gönder
        server.sendmail(sender, receiver, mailcontent)
        # Başarılı bir şekilde e-posta gönderildiğini belirt
        print('Mail gönderildi')
    except smtplib.SMTPException as e:
        # Eğer bir hata oluşursa hatayı yazdır
        print(e)
    finally:
        # Bağlantıyı kapat
        server.quit()


""" döngü oluşturcaz"""
while(True):
    checkPrice(url1,550)
    time.sleep(10 )


