# Go_marbel_test
# FastAPI Web Scraper API

## Overview

This FastAPI application provides an API endpoint to scrape reviews from web pages using Selenium WebDriver. The application utilizes GPT-based queries to dynamically extract CSS selectors for review elements.The llm was running locally on this server http://127.0.0.1:1234/v1/completions
and was accesible using /v1/completions endpoint.

## Features

- **Headless Web Scraping**: Uses Selenium WebDriver to scrape web pages without opening a browser window.
- **Dynamic CSS Selector Extraction**: Fetches CSS selectors dynamically using a local GPT-based service.
- **Error Handling**: Provides detailed error messages and HTTP exceptions for various failure points.
- **API Endpoint**: Exposes an endpoint `/api/reviews` for retrieving scraped reviews in JSON format.

## For local development and debugging, the server can be run with:

uvicorn LLM_v3:app --reload

hosted on http://127.0.0.1:8000

## Prerequisites

- Python 3.x
- FastAPI installed: `pip install fastapi`
- Selenium WebDriver (ChromeDriver) installed and accessible
- `httpx` installed: `pip install httpx`


