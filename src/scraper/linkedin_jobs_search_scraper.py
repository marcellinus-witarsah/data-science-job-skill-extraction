"""
Author: Marcellinus Aditya Witarsah
Description: Used for scraping Linked In jobs search page.
Command:
python src/scraper/linkedin_jobs_search_scraper.py --job-title "Data Scientist" --job-location "United States" --n-jobs 25 --filepath data/raw/test.csv
"""

import time
import pandas as pd
import argparse
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def html_element_handler(element):
    if len(element) == 0:
        return "Not Found"
    else:
        return element[0].text.strip()


def main():
    # Input from CLI
    parser = argparse.ArgumentParser(
        prog="Linked In Jobs Search Scraper",
        description="Scrape Job Title, Job Description, and Job Posted at The Search Job Site",
    )

    parser.add_argument(
        "--job-title", required=True, type=str, help="Job title for scraping"
    )
    parser.add_argument(
        "--job-location", required=True, type=str, help="Job location for scraping"
    )
    parser.add_argument(
        "--n-jobs", required=True, type=int, help="Total jobs for scraping"
    )
    parser.add_argument("--filepath", type=str, help="Path to the file to be saved")

    args = parser.parse_args()
    job_title = args.job_title
    job_location = args.job_location
    n_jobs = args.n_jobs
    filepath = args.filepath

    # Add Logger
    logger = logging.getLogger(__name__)

    # Open the LinkedIn
    driver = webdriver.Chrome()

    # Navigate to Jobs Page
    try:
        page_num = 0
        url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={job_location}&start={page_num}"
        driver.get(url)
        driver.maximize_window()
    except Exception as e:
        print(e)

    # Scroll the page until reach the certain amount of jobs to be scraped
    while True:
        total_jobs = len(
            driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
        )

        # Break loop uf reach certain amount
        if total_jobs >= n_jobs:
            break

        # Perform scrolling activity
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        try:
            # Click if there's "See more jobs" button element
            next = driver.find_element(
                By.XPATH, "//button[@aria-label='See more jobs']"
            )
            next.click()
            time.sleep(1)
        except:
            pass

    # Collect li element containing the jobs
    jobs = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")
    job_titles = []
    job_posts = []
    job_descriptions = []
    job_functions = []
    job_industries = []
    logger.info(f"Total jobs = {len(jobs)} jobs.")
    for i, job in enumerate(jobs):
        try:
            logger.info(f"{i} iteration")
            job.click()
            time.sleep(3)

            see_more_button = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//button[@aria-label="Show more, visually expands previously read content above"]',
                    )
                )
            )
            see_more_button.click()
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Get html elements
            job_title_element = soup.select("h2.top-card-layout__title")
            job_post_element = soup.select("span.posted-time-ago__text")
            job_description_element = soup.select("div.show-more-less-html__markup")
            job_function_element = soup.select(
                "ul.description__job-criteria-list > li:nth-child(3) > span"
            )
            job_industry_element = soup.select(
                "ul.description__job-criteria-list > li:nth-child(4) > span"
            )
            # Extract content and append to the list
            job_titles.append(html_element_handler(job_title_element))
            job_posts.append(html_element_handler(job_post_element))
            job_functions.append(html_element_handler(job_function_element))
            job_industries.append(html_element_handler(job_industry_element))
            job_descriptions.append(str(job_description_element[0]))
        except Exception as e:
            logger.warning(f"At iteration {i} with error of {e}")

    # Save it in form of Pandas DataFrame
    pd.DataFrame(
        {
            "job_title": job_titles,
            "job_post": job_posts,
            "job_description": job_descriptions,
            "job_function": job_functions,
            "job_industry": job_industries,
        }
    ).to_csv(filepath, index=False)
    logger.info("Finished Scraping.")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
