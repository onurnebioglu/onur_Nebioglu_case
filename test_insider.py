from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

# ✅ WebDriver'ı başlat
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
actions = ActionChains(driver)

# ✅ Insider ana sayfasını aç
driver.get("https://useinsider.com/")
driver.maximize_window()
wait = WebDriverWait(driver, 50)

# ✅ Çerez (Cookie) banner'ını kapat
try:
    cookie_banner = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='cli-bar-message']")))
    cookie_banner.click()
    print("✅ Çerez uyarısı kapatıldı.")
except:
    print("ℹ️ Çerez uyarısı bulunamadı, devam ediliyor...")

# ✅ "Company" menüsünü aç
company_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Company')]")))
company_menu.click()
time.sleep(2)

# ✅ "Careers" seçeneğine tıkla
careers_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Careers')]")))
careers_button.click()
time.sleep(3)

# ✅ "Find Your Dream Job" butonuna tıkla
dream_job_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Find your dream job')]")))
dream_job_button.click()

# ✅ Sayfanın tam yüklenmesini bekle
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
print("✅ Sayfa tamamen yüklendi!")

# ✅ Dropdown açılmadan önce filtrelerin yüklendiğini kontrol et
location_option_xpath = "//*[@id='filter-by-location']/option[2]"
wait.until(EC.presence_of_element_located((By.XPATH, location_option_xpath)))
print("✅ Filtre seçenekleri yüklendi, dropdown açılıyor...")

# ✅ Location dropdown menüsünü aç ve İstanbul'u seç
location_xpath = "//*[@id='select2-filter-by-location-container']"
menu = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
menu.click()

while True:
    active_element = driver.switch_to.active_element
    time.sleep(1)
    active_element.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)
    active_element.send_keys(Keys.ENTER)
    time.sleep(2)

    title = driver.find_element(By.XPATH, location_xpath).get_attribute("title")
    if "Istanbul, Turkiye" in title:
        print("✅ 'Istanbul, Turkiye' başarıyla seçildi!")
        break
    else:
        print("❌ Yanlış seçim yapıldı, tekrar deniyoruz...")

# ✅ Department dropdown menüsünü aç ve "Quality Assurance" seç
department_xpath = "//*[@id='select2-filter-by-department-container']"
menu = wait.until(EC.element_to_be_clickable((By.XPATH, department_xpath)))
menu.click()

while True:
    active_element = driver.switch_to.active_element
    time.sleep(1)

    for _ in range(13):
        active_element.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)

    active_element.send_keys(Keys.ENTER)
    time.sleep(2)

    title = driver.find_element(By.XPATH, department_xpath).get_attribute("title")
    if "Quality Assurance" in title:
        print("✅ 'Quality Assurance' başarıyla seçildi!")
        break
    else:
        print("❌ Yanlış seçim yapıldı, tekrar deniyoruz...")

# ✅ Filtrelerin uygulanmasını bekle
print("⏳ Filtre uygulandıktan sonra bekleniyor...")
time.sleep(3)

# ✅ İş ilanlarının yüklenmesini 30 saniye bekle
print("⏳ İş ilanlarının yüklenmesini bekliyoruz...")
job_list_xpath = "//*[@id='jobs-list']/div[1]"

try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, job_list_xpath)))
    print("✅ Filtreleme tamamlandı, iş ilanları yüklendi!")
except:
    print("❌ Aradığınız iş ilanı bulunamadı! Tarayıcı açık kalacak.")

# ✅ Tüm ilanları kontrol et
job_index = 1
while True:
    try:
        job_xpath = f"//*[@id='jobs-list']/div[{job_index}]"
        job_element = driver.find_element(By.XPATH, job_xpath)

        qa_xpath = f"//*[@id='jobs-list']/div[{job_index}]/div/p"
        department_xpath = f"//*[@id='jobs-list']/div[{job_index}]/div/span"
        location_xpath = f"//*[@id='jobs-list']/div[{job_index}]/div/div"

        qa_text = driver.find_element(By.XPATH, qa_xpath).text
        department_text = driver.find_element(By.XPATH, department_xpath).text
        location_text = driver.find_element(By.XPATH, location_xpath).text

        print(f"🔎 {job_index}. İş: {qa_text} | {department_text} | {location_text}")

        if "Quality Assurance" in qa_text and "Quality Assurance" in department_text and "Istanbul, Turkiye" in location_text:
            print(f"✅ {job_index}. iş ilanı uygun, tıklanıyor!")

            actions.move_to_element(job_element).perform()
            time.sleep(2)

            view_role_xpath = f"//*[@id='jobs-list']/div[{job_index}]//a[contains(text(), 'View Role')]"
            view_role_button = wait.until(EC.element_to_be_clickable((By.XPATH, view_role_xpath)))

            driver.execute_script("arguments[0].click();", view_role_button)
            print("✅ 'View Role' butonuna tıklandı!")

            wait.until(EC.number_of_windows_to_be(2))
            driver.switch_to.window(driver.window_handles[1])

            assert "lever.co" in driver.current_url, "❌ Başvuru sayfası açılmadı!"
            print("✅ Başvuru sayfası başarıyla açıldı!")
            break
        else:
            print(f"❌ {job_index}. iş ilanı uygun değil, sonraki ilana bakılıyor...")
            job_index += 1

    except:
        print("❌ Aradığınız iş ilanı bulunamadı!")
        break

# ✅ Tarayıcıyı açık bırak
print("🚀 Tarayıcı açık bırakıldı, işlemi manuel kontrol edebilirsin.")
