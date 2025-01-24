import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_and_save_companies():
    driver = webdriver.Chrome()
    driver.get("https://www.distributorcentral.com/p/supplier-list")

    # Wait for company elements to load
    wait = WebDriverWait(driver, 10)
    companies = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".supplier-list-item .supplier-name")
        )
    )

    # Extract company names
    company_names = [company.text for company in companies]

    driver.quit()

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"distributor_companies_{timestamp}.csv"

    # Save to CSV
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name"])  # Header
        writer.writerows([[name] for name in company_names])

    return filename, len(company_names)


if __name__ == "__main__":
    filename, count = scrape_and_save_companies()
    print(f"Successfully scraped {count} companies")
    print(f"Data saved to: {filename}")
