from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import httpx
import json
import time

app = FastAPI()

# Selenium WebDriver setup
def init_browser():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Set the path for ChromeDriver
    service = Service(r"C:\Users\Admin\AppData\Local\Google\Chrome SxS\Application\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# Function to fetch HTML content
def fetch_html(url):
    try:
        print(f"Fetching URL: {url}")
        driver = init_browser()
        print("we got the driver in it")
        driver.get(url)
        print(" ur L")
        time.sleep(2)  # Allow some time for the page to load
        html_content = driver.page_source
        driver.quit()
        print("HTML fetched successfully")
        return html_content
    except WebDriverException as e:
        print(f"Selenium error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching HTML: {str(e)}")

# Function to query Hermes for CSS selectors
def query_hermes(prompt, max_tokens=5000):
    url = "http://127.0.0.1:1234/v1/completions"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "hermes-3-llama-3.2-3b",
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    try:
        response = httpx.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "{}")
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error querying Hermes: {response.text}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying Hermes: {str(e)}")

def fetch_and_extract_reviews(page_url: str):
    try:
        print(f"Received URL: {page_url}")
        html_content = fetch_html(page_url)

        prompt = f"""
        Analyze the following HTML and identify the CSS selectors for:
        - Review Container
        - Review Title
        - Review Body
        - Review Rating
        - Reviewer Name
        - Next Page (if available)

        HTML:
        {html_content[:5000]}  # Limiting the prompt size
        """
        print("did we reach this point")
        css_selectors = json.loads(query_hermes(prompt))
        print("we did")
        driver = init_browser()
        driver.get(page_url)
        time.sleep(2)

        all_reviews = []

        
        while True:
            reviews = driver.find_elements(By.CSS_SELECTOR, css_selectors["review_container"])
            for review in reviews:
                try:
                    title = review.find_element(By.CSS_SELECTOR, css_selectors.get("review_title", "")).text
                except NoSuchElementException:
                    title = "N/A"

                try:
                    body = review.find_element(By.CSS_SELECTOR, css_selectors.get("review_body", "")).text
                except NoSuchElementException:
                    body = "N/A"

                try:
                    rating = review.find_element(By.CSS_SELECTOR, css_selectors.get("review_rating", "")).text
                except NoSuchElementException:
                    rating = "N/A"

                try:
                    reviewer = review.find_element(By.CSS_SELECTOR, css_selectors.get("reviewer_name", "")).text
                except NoSuchElementException:
                    reviewer = "N/A"

                all_reviews.append({
                    "title": title,
                    "body": body,
                    "rating": rating,
                    "reviewer": reviewer
                })

            # Check for pagination
            try:
                next_page = driver.find_element(By.CSS_SELECTOR, css_selectors.get("next_page", ""))
                next_page.click()
                time.sleep(2)  # Allow time for the next page to load
            except NoSuchElementException:
                break

        driver.quit()
        return json.dumps(all_reviews)
    except WebDriverException as e:
        print(f"Selenium error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting reviews: {str(e)}")

# API Endpoint to fetch reviews
@app.get("/api/reviews")
def get_reviews(page_url: str):
    try:
        reviews_json = fetch_and_extract_reviews(page_url)
        return {
            "message": "Reviews fetched successfully",
            "reviews": json.loads(reviews_json)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
