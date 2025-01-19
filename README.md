# Go_marbel_test
# FastAPI Web Scraper API

## Overview

This FastAPI application provides an API endpoint to scrape reviews from web pages using Selenium WebDriver. The application utilizes GPT-based queries to dynamically extract CSS selectors for review elements.

## Features

- **Headless Web Scraping**: Uses Selenium WebDriver to scrape web pages without opening a browser window.
- **Dynamic CSS Selector Extraction**: Fetches CSS selectors dynamically using a local GPT-based service.
- **Error Handling**: Provides detailed error messages and HTTP exceptions for various failure points.
- **API Endpoint**: Exposes an endpoint `/api/reviews` for retrieving scraped reviews in JSON format.

## Prerequisites

- Python 3.x
- FastAPI installed: `pip install fastapi`
- Selenium WebDriver (ChromeDriver) installed and accessible
- `httpx` installed: `pip install httpx`


