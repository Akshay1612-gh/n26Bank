import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
data = []
base_url = "https://www.trustpilot.com/review/n26.com?page="

for page in range(1, 250):
    print(f"Scraping page {page}...")
    url = base_url + str(page)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all review containers
        review_divs = soup.find_all("div", {"class": "styles_cardWrapper__kOLEb styles_show__qAseP"})

        # Process each review
        for review in review_divs:
            try:
                customer_name = review.find("span", {
                    "class": "typography_heading-xs__osRhC typography_appearance-default__t8iAq"}).text.strip()
            except AttributeError:
                customer_name = ""

            try:
                customer_review = review.find("p", {
                    "class": "typography_body-l__v5JLj typography_appearance-default__t8iAq"}).text.strip()
            except AttributeError:
                customer_review = ""

            try:
                n26_response = review.find("p", {
                    "class": "typography_body-m__k2UI7 typography_appearance-default__t8iAq styles_message__l9HgT"}).text.strip()
            except AttributeError:
                n26_response = ""

            try:
                date_of_experience = review.find("div", {
                    "class": "typography_body-m__k2UI7 typography_appearance-subtle__PYOVM"}).text.strip()
            except AttributeError:
                date_of_experience = ""

            try:
                date_of_review_tag = review.find("time")  # General search for <time>
                date_of_review = date_of_review_tag["datetime"] if date_of_review_tag else ""
            except (AttributeError, TypeError):
                date_of_review = ""

            try:
                rating = review.find("img", {"alt": True})["alt"]
                rating_out_of_5 = rating.split()[1]  # Extract the rating number
            except (AttributeError, IndexError):
                rating_out_of_5 = ""

            # Extract Review Link
            try:
                review_link_tag = review.find("a", {"class": "link_internal__7XN06"})  # Adjust class based on structure
                review_link = "https://www.trustpilot.com" + review_link_tag["href"] if review_link_tag else ""
            except AttributeError:
                review_link = ""

            country = ""
            if review_link:
                try:
                    detailed_response = requests.get(review_link, headers=headers)
                    detailed_soup = BeautifulSoup(detailed_response.content, "html.parser")
                    country_tag = detailed_soup.find("div", {"class": "styles_consumerInfoExtra__kV_GB"})  # Adjust class
                    country = country_tag.text.strip() if country_tag else ""
                except Exception as e:
                    print(f"Failed to fetch country for {review_link}: {e}")


            data.append({
                "Customer Name": customer_name,
                "Customer Review": customer_review,
                "N26 Response": n26_response,
                "Date Of Experience": date_of_experience,
                "Date Of Review": date_of_review,
                "Rating Out Of 5": rating_out_of_5,
                "Country": country
            })

        print(f"Page {page} scraped successfully.")
    else:
        print(f"Failed to scrape page {page}. Status Code: {response.status_code}")
        break
    sleep(2)
df = pd.DataFrame(data)
df.to_csv("N26_Reviews.csv", index=False)
print("Scraping completed. Data saved to 'N26_Reviews.csv'.")

