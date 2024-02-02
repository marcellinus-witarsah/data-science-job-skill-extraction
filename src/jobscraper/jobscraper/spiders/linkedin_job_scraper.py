import scrapy
import time
from ..items import JobItem


class LinkedinJobScraperSpider(scrapy.Spider):
    name = "linkedin_jobs_spider"
    api_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BScientist&location=Indonesia&geoId=102478259&trk=public_jobs_jobs-search-bar_search-submit&start="

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(
            url=first_url,
            callback=self.parse,
            meta={"first_job_on_page": first_job_on_page},
        )

    def parse(self, response):
        first_job_on_page = response.meta["first_job_on_page"]
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("*****************************************")
        print(num_jobs_returned)

        for job in jobs:
            job_detail_url = job.css(".base-card__full-link::attr(href)").get(
                default="not-found"
            )
            job_title = job.css("h3.base-search-card__title::text").get(
                default="not-found"
            )
            job_listed = job.css("time::attr(datetime)").get(default="not-found")
            company_name = job.css("h4 a::text").get(default="not-found")
            company_location = job.css(".job-search-card__location::text").get(
                default="not-found"
            )
            yield response.follow(
                url=job_detail_url,
                callback=self.parse_jobs_page,
                meta={
                    "job_title": job_title,
                    "job_listed": job_listed,
                    "company_location": company_location,
                    "company_name": company_name,
                },
            )

        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            print("**********************************************************")
            print("MASUK")
            print("**********************************************************")
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={"first_job_on_page": first_job_on_page},
            )

    def parse_jobs_page(self, response):
        job_item = JobItem()
        job_item["job_title"] = response.meta["job_title"].strip()
        job_item["job_listed"] = response.meta["job_listed"].strip()
        job_item["company_name"] = response.meta["company_name"].strip()
        job_item["company_location"] = response.meta["company_location"].strip()
        job_item["job_description"] = response.css(".description__text ::text").getall()
        yield job_item
