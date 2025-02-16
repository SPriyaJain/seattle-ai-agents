"""This script serves as a skeleton template for synchronous AgentQL scripts."""

import logging
import pandas as pd
import agentql
import math
from agentql.ext.playwright.sync_api import Page
from playwright.sync_api import sync_playwright

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main():
    # Load the CSV into a pandas DataFrame
    csv_file = "WASchools2.csv"
    df = pd.read_csv(csv_file, dtype=str)

    website_column = (
        "Website"
    )

    # Check if the new columns exists, if not, create them
    if "AcademicsLink" not in df.columns:
        df["AcademicsLink"] = None
    if "CourseCatalogLink" not in df.columns:
        df["CourseCatalogLink"] = None
    if "CurriculumLink" not in df.columns:
        df["CurriculumLink"] = None
    if "CTELink" not in df.columns:
        df["CTELink"] = None

    for index, row in df.iterrows():
      # if index < 15: # Index of previous run
          # continue
      
      school_website = row[website_column]
      if not school_website or (type(school_website) == float and math.isnan(school_website)):
          print("Website not found, continuing")
          continue
      
      print(f"{index}: Searching in {school_website}...")

      try:
        with sync_playwright() as p, p.chromium.launch(headless=False) as browser:
            # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
            page = agentql.wrap(browser.new_page())

            # Navigate to the desired URL
            page.goto(school_website)

            resp = get_response(page)
            df.at[index, "AcademicsLink"] = resp["navigation"]["academics_link"]
            df.at[index, "CourseCatalogLink"] = resp["navigation"]["course_catalog_link"]
            df.at[index, "CurriculumLink"] = resp["navigation"]["curriculum_link"]
            df.at[index, "CTELink"] = resp["navigation"]["career_and_technical_education_link"]
      except Exception as e:
          print(f"Error at index {index}: {e}")
          break
      finally:
          # Only 300 free credits, stop at 100 requests for now
          if index > 100:
              break
  
    df.to_csv("WASchools3.csv", index=False)
    print("Finished updating the academics links!")


def get_response(page: Page):
    query = """
      {
        navigation {
          academics_link(Link to Academics page)
          course_catalog_link(Link to Course Catalog page)
          curriculum_link(Link to Curriculum page)
          career_and_technical_education_link(Link to Career and Technical Education page)
        }
      }
    """

    response = page.query_data(query)

    # For more details on how to consume the response, refer to the documentation at https://docs.agentql.com/intro/main-concepts
    print(response)
    return response


if __name__ == "__main__":
    main()
