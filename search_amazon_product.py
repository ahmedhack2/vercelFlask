import requests
from bs4 import BeautifulSoup
import time




# function that take product name and search on amazon
def newsearch_amazon(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

        # Send a GET request to the provided URL with headers
        response = requests.get(url, headers=headers)
        
        # Retry logic for 503 error
        max_retries = 150
        retries = 0
        while response.status_code == 503 and retries < max_retries:
            print('503 error - Retrying...')
            time.sleep(2)  # Wait for 2 seconds before retrying
            response = requests.get(url, headers=headers)
            retries += 1
        
        # If still getting 503 error after retries, return None
        if response.status_code == 503:
            print('503 error - Max retries reached. Service unavailable.')
            return None
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the product containers on the page
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        # Initialize a list to store the results
        results = []
        
        # Iterate over each product container
        for container in product_containers:
            # Extract the product title
            title_element = container.find('h2')
            title = title_element.text.strip()
            
            # Extract the product price
            price_element = container.find('span', {'class': 'a-offscreen'})
            price = price_element.text.strip() if price_element else 'Not available'
            
            # Extract the product rating
            rating_element = container.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.strip() if rating_element else 'Not rated'
            
            # Extract the product link
            link_element = container.find('a', {'class': 'a-link-normal'})
            link = 'https://www.amazon.com' + link_element['href'] if link_element else 'Link not available'
            
            # Create a dictionary of product details
            product = {
                'title': title,
                'price': price,
                'rating': rating,
                'link': link
            }
            
            # Add the product details to the results list
            results.append(product)
        
        # Return the results
        return results
    
    except requests.exceptions.RequestException as e:
        print('An error occurred:', e)
        return None