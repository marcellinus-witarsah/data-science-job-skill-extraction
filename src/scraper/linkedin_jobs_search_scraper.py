import time
import pandas as pd
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""
python src/scraper/linkedin_jobs_search_scraper.py --job-title "Data Scientist" --job-location "United States" --n-jobs 25 --filepath data/raw/test.csv
"""


def main():
    # input from command line
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
    print(len(jobs))
    for i, job in enumerate(jobs):
        try:
            print(i, end="\r")
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
            job_title_element = soup.find("h2", {"class": "top-card-layout__title"})
            if job_title_element is None:
                job_titles.append("Not Found")
            else:
                job_titles.append(job_title_element.text.strip())

            job_post_element = soup.find("span", {"class": "posted-time-ago__text"})
            if job_post_element is None:
                job_posts.append("Not Found")
            else:
                job_posts.append(job_post_element.text.strip())

            job_description_element = soup.find(
                "div", {"class": "show-more-less-html__markup relative overflow-hidden"}
            )
            if job_description_element is None:
                job_descriptions.append("Not Found")
            else:
                job_descriptions.append(job_description_element.text.strip())

            job_function = soup.select(
                "ul.description__job-criteria-list > li:nth-child(3) > span"
            )
            if job_function is None:
                job_functions.append("Not Found")
            else:
                job_functions.append(job_function[0].text.strip())

            job_industry = soup.select(
                "ul.description__job-criteria-list > li:nth-child(4) > span"
            )
            if job_industry is None:
                job_industries.append("Not Found")
            else:
                job_industries.append(job_industry[0].text.strip())
            print(
                f"{i}: {job_title_element.text.strip()}, {job_post_element.text.strip()}, {job_description_element.text.strip()}, {job_function[0].text.strip()}, {job_industry[0].text.strip()}"
            )
        except Exception as e:
            print(f"At iteration {i} with error of {e}")

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


if __name__ == "__main__":
    main()
