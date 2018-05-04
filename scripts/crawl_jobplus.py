import scrapy
class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = ['https://segmentfault.com/jobs/search?page=1']

    def parse(self, response):
        for job in response.css('div[class="company-list stream-list border-top"]'):
            yield{
                    'jobname': job.xpath('.//section/div/a/text()').extract_first().strip(),
                    'salary_up': job.xpath('.//section/div/div/strong/text()').re_first('-([a-zA-Z0-9]+)'),
                    'salary_down': job.xpath('.//section/div/div/strong/text()').re_first('([a-zA-Z0-9]+)-'),
                    'exper_need': job.xpath('.//section/div/div/text()').re_first('\/\s([\S]+)\s').strip(),
                    'work_address': job.xpath('.//section/div/span/text()').extract_first().strip(),
                    'job_need': job.xpath('.//section/div/div/text()').re_first('\/\s([\D]+)\s').strip(),
                    'job_description': job.xpath('.//section/div/a/text()').extract_first().strip()
                    }

