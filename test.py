import time

import pandas as pd
from googlesearch import search


# Function to perform Google search and get the first result
def get_school_website(school_name):
    query = f"{school_name}"  # Use school name to search
    try:
        print(query)
        # Perform the Google search, return only the first result
        results = list(
            search(query, num_results=10)
        )  # num_results limits the results to 1
        if results:
            print(results)
            return results[0]  # Return the first result's URL
        else:
            return None  # Return None if no results found
    except Exception as e:
        print(f"Error searching for {school_name}: {e}")
        return None


get_school_website("East Valley Middle School")
