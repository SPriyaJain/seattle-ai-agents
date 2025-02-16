import random
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from googlesearch import search

# Set up Selenium WebDriver
options = Options()
options.add_argument('--headless')  # To run in headless mode (without opening browser window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Load your CSV file into a pandas DataFrame
csv_file = "WASchools4.csv"
df = pd.read_csv(csv_file)

if "OffersEducation" not in df.columns:
    df["OffersEducation"] = None

# Define the link columns
academics_link_column = "AcademicsLink"
course_catalog_link_column = "CourseCatalogLink"
curriculum_link_column = "CurriculumLink"
career_and_technical_education_link_column = "CTELink"

def get_more_sites(school_name, dimension):
    query = f"{school_name} {dimension}"
    # try:
    # Perform the Google search, return only the first result
    results = list(search(query, num_results=3))
    if results:
        if not results[0].startswith("/search?num="):
            return results[0]
        return results[1]
    else:
        return None  # Return None if no results found
    # except Exception as e:
    #     print(f"Error searching for {school_name}: {e}")
    #     return None

for index, row in df.iterrows():
    school_name = row["SchoolName"]
    print(f"{index}: Searching for {school_name}...")
    links = []

    try:
        if pd.isna(row[academics_link_column]):
            dimension = "academics"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, academics_link_column] = website
            links.append(website)
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            links.append(row[academics_link_column])
            print("Academics site already found")

        if pd.isna(row[course_catalog_link_column]):
            dimension = "course catalog"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, course_catalog_link_column] = website
            links.append(website)
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            links.append(row[course_catalog_link_column])
            print("Course catalog site already found")

        if pd.isna(row[curriculum_link_column]):
            dimension = "curriculum"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, curriculum_link_column] = website
            links.append(curriculum_link_column)
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            links.append(row[curriculum_link_column])
            print("Curriculum site already found")

        if pd.isna(row[career_and_technical_education_link_column]) and row["GradeCategory"] in ["Middle School", "High School", "PK-12", "K-12"]:
            dimension = "career and technical education"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, career_and_technical_education_link_column] = website
            links.append(website)
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            links.append(row[career_and_technical_education_link_column])
            print("CTE site already found or n/a")

    except Exception as e:
        print(f"{e}")
        print(f"Index: {index}, school name: {school_name}")
        break

    # Define the list of keywords to search for
    keywords = ["business", "accounting", "finance", "financial", "economics"]

    # === FILL IN FINANCIAL LITERACY INFO ===
    try:
        if not pd.isna(row["OffersEducation"]) and row["OffersEducation"] == "Found":
            continue

        # Initialize the OffersEducation value as "NotFound"
        offers_education = "NotFound"

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
        # Save to the CSV after each row
        df.to_csv("WASchools6.csv", index=False)
    except Exception as e:
        print(f"Error at index {index}: {e}")
        break

# Close the WebDriver session after processing
driver.quit()

# Save the updated DataFrame to a new CSV file
df.to_csv("WASchools6.csv", index=False)
