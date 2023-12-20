import requests
from bs4 import BeautifulSoup

def scrape(url):
    try:
        # Make a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the entry title element and check if it exists before accessing its text content
        entry_title_element = soup.find('h1', class_='entry-title')
        recipe_name = entry_title_element.text.strip() if entry_title_element else "Recipe Title Not Available"

        # Extract other information based on the provided HTML structure
        ingredient_list = [ingredient.text.strip() for ingredient in soup.find_all('li', class_='wprm-recipe-ingredient')]

        # Find the Total Time element and check if it exists before accessing its next sibling
        total_time_label = soup.find('span', class_='wprm-recipe-details-label', text='Total Time:')
        total_time = total_time_label.find_next('span', class_='wprm-recipe-details').text.strip() if total_time_label else "Not available"

        # Find the Servings element and check if it exists before accessing its next sibling
        servings_label = soup.find('span', class_='wprm-recipe-details-label', text='Servings:')
        servings = servings_label.find_next('span', class_='wprm-recipe-details').text.strip() if servings_label else "Not available"

        # Find the main content div and check if it exists before accessing its text content
        main_content_div = soup.find('div', class_='entry-content')
        main_content = main_content_div.get_text(separator='\n').strip() if main_content_div else "Main content not available"

        # # Print the extracted information
        # print("Recipe Name:", recipe_name)
        # print("Ingredients:", ingredient_list)
        # print("Total Time:", total_time)
        # print("Servings:", servings)
        # print("Description:", main_content)

        return {
            "recipe_name": recipe_name,
            "ingredients": ingredient_list,
            "total_time": total_time,
            "servings": servings,
            "description": main_content
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")

"""Websites with successfuls:
    url = "https://www.indianhealthyrecipes.com/"
    url ="https://www.vidhyashomecooking.com/"
"""
url = "https://www.vidhyashomecooking.com/panchmel-dal-rajasthani-panchratna-dal/"
out = scrape(url)
print("\n".join([str(out[key]) for key in out]))