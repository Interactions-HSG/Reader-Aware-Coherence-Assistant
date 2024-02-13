#GoycwKdjBJ7oPPSnBIOV498hMHCivpiU6BjQ5YbZ
#47299473(simon) 35278460(danai) 2191982532(jeremy)

import requests
import json
import os

API_KEY_GOOGLE_SCHOLAR = json.load(open('config.json'))["GOOGLE_SCHOLAR_API_KEY"]


def retrieve_and_merge_abstracts(api_key, author_id):
    # Define the Semantic Scholar API endpoint for author's detailed papers
    api_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"

    # Define the API parameters to specify the fields you want
    params = {
        "fields": "abstract",
        "limit": 100  # Limit to the most recent 100 papers (adjust as needed)
    }

    # Set up the request headers with the API key
    headers = {
        "x-api-key": api_key
    }

    try:
        # Make the API request to retrieve abstracts of the author's papers
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            # Parse the API response to extract paper abstracts
            data = response.json()
            papers = data.get("data", [])

            # Create a list to store abstracts
            abstracts = []

            # Save abstracts to the list
            for i, paper in enumerate(papers):
                abstract = paper.get("abstract")
                if abstract:
                    abstracts.append(f"Abstract {i+1}:\n{abstract}\n\n")

            # Merge abstracts into a single text file
            merged_abstracts_filename = "scientist_abstracts.txt"
            with open(merged_abstracts_filename, "w", encoding="utf-8") as merged_file:
                merged_file.writelines(abstracts)

            print("Abstracts retrieved and merged successfully.")

        else:
            print(f"Error: Unable to fetch papers. Status Code: {response.status_code}")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def my_fetch(author_id):
    # Define the Semantic Scholar API endpoint for author's detailed papers
    api_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"

    # Define the API parameters to specify the fields you want
    params = {
        "fields": "abstract",
        "limit": 100  # Limit to the most recent 100 papers (adjust as needed)
    }

    # Set up the request headers with the API key
    headers = {
        "x-api-key": API_KEY_GOOGLE_SCHOLAR
    }

    try:
        # Make the API request to retrieve abstracts of the author's papers
        response = requests.get(api_url, params=params, headers=headers)

        if response.status_code == 200:
            # Parse the API response to extract paper abstracts
            data = response.json()
            papers = data.get("data", [])

            # Create a list to store abstracts
            abstracts = []

            # Save abstracts to the list
            for i, paper in enumerate(papers):
                abstract = paper.get("abstract")
                if abstract:
                    abstracts.append(f"Abstract {i+1}:\n{abstract}\n\n")

            return '\n'.join(abstracts)
        else:
            return f"Error: Unable to fetch papers. Status Code: {response.status_code}"
    
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    # Example usage
    author_id = "2191982532"  # Replace with the actual author's ID

    # Retrieve and merge abstracts for the scientist's papers
    retrieve_and_merge_abstracts(API_KEY_GOOGLE_SCHOLAR, author_id)

if __name__ == '__main__': main()
