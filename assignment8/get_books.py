from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pandas as pd
import json

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install())
)

driver.get(
    "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
)
# Task 2
book_entries = driver.find_elements(
    By.CSS_SELECTOR,
    "li.cp-search-result-item"
)

print("Number of books:", len(book_entries))

results = []
for book in book_entries:
    title_element = book.find_element(By.CSS_SELECTOR, "span.title-content")
    title = title_element.text
# Task 3
    author_elements = book.find_elements(By.CSS_SELECTOR, "a.author-link")

    authors = []
    for author in author_elements:
        authors.append(author.text)

    author_text = "; ".join(authors)
    format_div = book.find_element(By.CSS_SELECTOR, "div.cp-format-info")
    format_year_element = format_div.find_element(
        By.CSS_SELECTOR,
        "span.display-info-primary"
    )
    format_year = format_year_element.text
    book_data = {
    "Title": title,
    "Author": author_text,
    "Format-Year": format_year
    }

    results.append(book_data)

    print("Title:", title)
    print("Author:", author_text)
    print("Format-Year:", format_year)
    print()

df = pd.DataFrame(results)
print(df)

df.to_csv("get_books.csv", index=False)

with open("get_books.json", "w") as json_file:
    json.dump(results, json_file, indent=4)

driver.quit()