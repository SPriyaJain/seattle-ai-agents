import time

from typing import Any, List, Optional

import requests
from bs4 import BeautifulSoup

from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class NestedModel1(BaseModel):
    name: str
    website: str


class ExtractSchema(BaseModel):
    schools: list[NestedModel1]


fire_app = FirecrawlApp(api_key="fc-ddbe096f8ab5484493ecb8d8b7c80674")

url = "https://en.wikipedia.org/wiki/List_of_school_districts_in_Washington"
wiki_url_prefix = "https://en.wikipedia.org/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


# Example of extracting links to the school district pages
districts = []
# Structure:
"""
{
    "district_name": str,
    "has_link": bool,
    "wiki_link": str,
    "website": str,
    "schools": [{
        "name": str,
        "website": str
    }]
}
"""
for link in soup.find_all("a", href=True):
    if "School_District" in link["href"]:  # Look for school district links
        if "redlink=1" in link["href"]:
            districts.append({"district_name": link["title"], "has_link": False})
        else:
            districts.append(
                {
                    "district_name": link["title"],
                    "has_link": True,
                    "wiki_link": wiki_url_prefix + link["href"],
                    "schools": [],
                }
            )

# for i in districts:
# print(i["href"], i["title"])

# print(districts)


# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for dist in districts:
    if dist["has_link"]:
        driver.get(dist["wiki_link"])

        # Allow time for the page to load
        time.sleep(0.2)

        # Find all elements with the class "external text"
        elements = driver.find_elements(By.CSS_SELECTOR, ".external.text")

        # Loop through the elements and print their text or other attributes
        for element in elements:
            if "www." in element.text:
                dist_website = element.text
                dist["website"] = dist_website

                # FIRECRAWL
                data = fire_app.extract(
                    [dist_website + "/*"],
                    {
                        "prompt": "Extract a list of schools and their corresponding websites.",
                        "schema": ExtractSchema.model_json_schema(),
                    },
                )
                if data["success"]:
                    dist["schools"] = data["data"]["schools"]
                    for school in dist["schools"]:
                        


driver.quit()

print(districts)
