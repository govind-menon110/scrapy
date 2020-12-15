import scrapy


class Spider275(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pgno = 1
        self.start_urls = ['https://www.1mg.com/drugs-therapeutic-classes/drug-class-275?page=' + str(self.pgno)]

    name = 'Spider275'
    allowed_domains = ['1mg.com']

    def parse(self, response):
        Medicines = {}
        if response.xpath(
                '//div[@class="style__product-card___1gbex style__card___3eL67 style__raised___3MFEA style__white-bg___10nDR style__overflow-hidden___2maTX"]'):
            Medicines["Names List"] = response.css(".style__space-between___2mbvn div:nth-child(1)::text").extract()
            Medicines["Prescription"] = response.css(".style__font-12px___2ru_e span::text").extract()
            Medicines["Type of Sell"] = response.css(".style__font-12px___2ru_e .style__padding-bottom-5px___2NrDR:nth-child(1)::text").extract()
            Medicines["Manufacturer"] = response.css(".style__padding-bottom-5px___2NrDR+ .style__padding-bottom-5px___2NrDR::text").extract()
            Medicines["Salt"] = response.css(".style__product-content___5PFBW::text").extract()
            Medicines["Cost"] = response.css(".style__space-between___2mbvn div+ div::text").extract()
            Medicines["Therapeutic Class"] = response.css(".style__drug-list-heading___niild::text").extract()
            Medicines["Image Link"] = response.css(".style__card-image___1oz_4 img").extract()
            yield Medicines
            self.pgno += 1
            next_page_url = 'https://www.1mg.com/drugs-therapeutic-classes/drug-class-275?page=' + str(self.pgno)
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            pass

