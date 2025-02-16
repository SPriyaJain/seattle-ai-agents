import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver
options = Options()
options.add_argument('--headless')  # To run in headless mode (without opening browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load your CSV file into a pandas DataFrame
csv_file = "WASchools3.csv"
df = pd.read_csv(csv_file)

# Define the link columns
academics_link_column = "AcademicsLink"
course_catalog_link_column = "CourseCatalogLink"
curriculum_link_column = "CurriculumLink"
career_and_technical_education_link_column = "CTELink"

# Define the list of keywords to search for
keywords = ["business", "accounting", "finance", "financial", "economics"]

# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    try:
        print(f"At index {index}")
        print(row["Website"])
        # Initialize the OffersEducation value as "NotFound"
        offers_education = "NotFound"

        # List of links to check
        links = [
            row[academics_link_column],
            row[course_catalog_link_column],
            row[curriculum_link_column],
            row[career_and_technical_education_link_column]
        ]

        # If all links are empty, write "NoData"
        if all(pd.isna(link) for link in links):
            print("NoData")
            print(links)
            df.at[index, "OffersEducation"] = "NoData"
            continue  # Skip to the next row if there is no data

        # Iterate over each link and check for the keywords
        for link in links:
            if pd.notna(link):  # If the link is not blank
                driver.get(link)
                html = driver.page_source

                # Check if any of the keywords appear in the HTML
                if any(keyword.lower() in html.lower() for keyword in keywords):
                    offers_education = "Found"
                    break  # If found, no need to check further links

        # Assign the result to the 'OffersEducation' column
        df.at[index, "OffersEducation"] = offers_education
        print(offers_education)
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

# Close the WebDriver session after processing
driver.quit()

# Save the updated DataFrame to a new CSV file
df.to_csv("WASchools4.csv", index=False)
