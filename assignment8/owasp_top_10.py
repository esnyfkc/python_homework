from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd


driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install())
)

driver.get("https://owasp.org/Top10/")

links = driver.find_elements(By.XPATH, "//ol/li/a")

print("Number of vulnerabilities:", len(links))

results = []

for link in links:
    title = link.text
    href = link.get_attribute("href")

    vulnerability = {
        "Title": title,
        "Link": href
    }

    results.append(vulnerability)

print(results)

df = pd.DataFrame(results)

df.to_csv("owasp_top_10.csv", index=False)

driver.quit()