import requests
import smtplib
from bs4 import BeautifulSoup
import time
# Her bir ürünün bilgilerini içeren bir sözlük listesi
urunler = [
    {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-2023-gps-44mm-starlight-aluminium-case-with-starlight-sport-band-s-m-p-HBCV00004XGWD2',
       'fiyat_siniri': 8000
    },
    {
        'url':'https://www.hepsiburada.com/apple-watch-seri-9-gps-45mm-gece-yarisi-aluminyum-kasa-spor-kordon-m-l-mr9a3tu-a-p-HBCV00004XGXFK',      
        'fiyat_siniri': 7000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-2023-gps-44mm-starlight-aluminium-case-with-starlight-sport-band-m-l-p-HBCV00004XGWD4',
        'fiyat_siniri': 7000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-seri-9-gps-41mm-gece-yarisi-aluminyum-kasa-spor-kordon-s-m-mr8w3tu-a-p-HBCV00004XGXEU',
        'fiyat_siniri': 7000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-seri-9-gps-45mm-gece-yarisi-aluminyum-kasa-spor-loop-mr9c3tu-a-p-HBCV00004XGXFM',
        'fiyat_siniri': 1000
    },
        {
        'url':  'https://www.hepsiburada.com/apple-watch-seri-9-gps-41mm-gumus-rengi-aluminyum-kasa-spor-kordon-s-m-mr903tu-a-p-HBCV00004XGXF0',
        'fiyat_siniri': 1000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-2023-gps-40mm-silver-aluminium-case-with-storm-blue-sport-band-s-m-p-HBCV00004XGWCW' ,
        'fiyat_siniri': 4000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-2023-gps-44mm-midnight-aluminium-case-with-midnight-sport-loop-pm-HBC00004XGWDB',
        'fiyat_siniri': 4000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-2023-gps-44mm-starlight-aluminium-case-with-starlight-sport-loop-pm-HBC00004XGWD5',
        'fiyat_siniri': 1000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-seri-9-gps-45mm-pembe-aluminyum-kasa-spor-kordon-s-m-mr9g3tu-a-p-HBCV00004XGXFU',
        'fiyat_siniri': 1000
    },
        {
        'url': 'https://www.hepsiburada.com/apple-watch-se-2-nesil-gps-44mm-silver-aluminium-case-with-white-sport-band-regular-mnjx3tu-a-p-HBCV00002Y4TJK',
        'fiyat_siniri': 2000
    },

    # Diğer ürünleri ekleyebilirsiniz
]

headers = {'user-agent': ''}


def fiyat_kontrollerini_yap():
    for urun in urunler:
        try:
            sayfa = requests.get(urun['url'], headers=headers)
            sayfa.raise_for_status()  # İstek başarılı mı kontrol et
            soup = BeautifulSoup(sayfa.content, 'html.parser')
            baslik = soup.find(id='product-name').get_text().strip()
            baslik = baslik[0:22]
            print(baslik)
            fiyat_elementi = soup.find('span', {'data-bind': "markupText:'currentPriceBeforePoint'"}).get_text()
            fiyat = float(fiyat_elementi) #! fiyat 
            print(fiyat)
            #! Fiyat sınırının altındaysa
            if fiyat < urun['fiyat_siniri']:
                mail_gonder(baslik, urun['url'])
        except Exception as hata:
            print("urun için beklenmeyen bir hata oluştu:",hata)

# E-posta gönderme fonksiyonu
def mail_gonder(baslik, urun_url):
    gonderen = 'örnek@gmail.com'
    alici = 'örnek@gmail.com'
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gonderen, 'fhxz wzgz ghqg fbhm')  # Buraya e-posta hesabınızın şifresini yazmalısınız
        konu = baslik + 'İNDİRİM VAR'
        icerik ="Fiyat düştü! \n Bu linkten gidebilirsin:"+ urun_url

   
        mail_icerigi = icerik
        server.sendmail(gonderen, alici, mail_icerigi)
        print("Mail gönderildi "+baslik)
    except Exception as hata:
        print("Beklenmeyen bir hata oluştu: "+hata)
    finally:
        server.quit()

while True:
    fiyat_kontrollerini_yap()
    time.sleep(60 * 60)
