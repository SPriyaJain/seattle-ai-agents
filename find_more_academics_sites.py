import random
import time

import pandas as pd
from googlesearch import search


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



csv_file = "WASchools4.csv"
df = pd.read_csv(csv_file)

academics_link_column = "AcademicsLink"
course_catalog_link_column = "CourseCatalogLink"
curriculum_link_column = "CurriculumLink"
career_and_technical_education_link_column = "CTELink"

for index, row in df.iterrows():
    school_name = row["SchoolName"]
    print(f"{index}: Searching for {school_name}...")

    try:
        if pd.isna(row[academics_link_column]):
            dimension = "academics"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, academics_link_column] = website
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            print("Academics site already found")

        if pd.isna(row[course_catalog_link_column]):
            dimension = "course catalog"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, course_catalog_link_column] = website
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            print("Course catalog site already found")

        if pd.isna(row[curriculum_link_column]):
            dimension = "curriculum"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, curriculum_link_column] = website
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            print("Curriculum site already found")

        if pd.isna(row[career_and_technical_education_link_column]):
            dimension = "career and technical education"
            website = get_more_sites(school_name, dimension)
            # Store the result in the dataframe
            df.at[index, career_and_technical_education_link_column] = website
            # Pause to avoid making requests too quickly
            time.sleep(2 + random.uniform(0, 2))
        else:
            print("CTE site already found")

    except Exception as e:
        print(f"{e}")
        print(f"Index: {index}, school name: {school_name}")
        break

    # Save the updated DataFrame back to a CSV each time
    df.to_csv("WASchools5.csv", index=False)


print("Finished updating the websites!")
