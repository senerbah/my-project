import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver'ı başlat
driver = webdriver.Chrome()  # ChromeDriver'ı PATH'de olduğundan emin ol
site_url = "https://tim.org.tr/tr/ihracat-rakamlari"

# Web sitesine git
driver.get(site_url)

# Verileri kaydetmek için klasör oluştur
output_folder = "TİM_Datasets"
os.makedirs(output_folder, exist_ok=True)

try:
    # Sayfa tamamen yüklenene kadar bekle
    wait = WebDriverWait(driver, 20)

    # Yıl ve ayların bulunduğu tüm xn-report-item elementlerini bul
    report_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "xn-report-item")))

    for item in report_items:
        # Her xn-report-item içinde bağlantıları bul
        links = item.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            try:
                # Her bir bağlantıyı işleme al
                file_url = link.get_attribute("href")
                file_name = file_url.split("/")[-1].split("?")[0]  # URL'den dosya ismini al
                file_path = os.path.join(output_folder, file_name)

                # Dosyayı indir
                print(f"{file_name} indiriliyor...")
                response = requests.get(file_url, stream=True)

                # Eğer dosya başarılı şekilde indirildiyse
                if response.status_code == 200:
                    with open(file_path, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"Dosya kaydedildi: {file_path}")
                else:
                    print(f"Dosya indirilemedi: {file_url} - HTTP Hatası: {response.status_code}")
            
            except Exception as e:
                print(f"Bir hata oluştu: {e}")
finally:
    # Tarayıcıyı kapat
    driver.quit()
    print("Tarayıcı kapatıldı.")
