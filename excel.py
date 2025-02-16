import random
import time

import pandas as pd
from googlesearch import search


# Function to perform Google search and get the first result
def get_school_website(school_name):
    query = f"{school_name}"  # Use school name to search
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


# Load the CSV into a pandas DataFrame
csv_file = "WASchools.csv"  # Replace with the path to your CSV file
df = pd.read_csv(csv_file)

# Check if there's a column for school names (adjust based on your CSV structure)
school_name_column = (
    "SchoolName"  # Replace with the actual column name for the school names
)

# Check if 'Website' column exists, if not, create it
if "Website" not in df.columns:
    df["Website"] = None  # Add the 'Website' column with initial value as None

# Fill in the "Website" column with the first Google search result for each school
for index, row in df.iterrows():
    school_name = row[school_name_column]
    print(f"{index}: Searching for {school_name}...")

    try:
        # Get the school website
        website = get_school_website(school_name)
    except Exception as e:
        print(f"{e}")
        print(f"Index: {index}, row: {row}")
        break

    # Store the result in the dataframe
    df.at[index, "Website"] = website
    print(website)

    # Pause to avoid making requests too quickly
    time.sleep(2 + random.uniform(0, 2))  # Adjust sleep time as necessary

# Save the updated DataFrame back to a CSV
df.to_csv("WASchools2.csv", index=False)
print("Finished updating the websites!")
