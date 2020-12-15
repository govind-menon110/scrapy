import json
import scrapy
import os.path


class finalspider2(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        f = open(os.path.dirname(__file__) + '/../isthisall.json')
        spidey = json.load(f)[0]
        self.urllist = []
        self.pgno = {}
        for i in spidey.values():
            val = -1
            for p in range(0, 4):
                val = i.find('-', (val + 1))
            self.pgno[i[(val + 1):]] = int(1)
            self.urllist.append("https://1mg.com" + i + "?page=" + str(self.pgno[i[(val + 1):]]))
        self.start_urls = self.urllist

    name = 'finalspider2'
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
            current_url = response.request.url
            posq = current_url.find('?')
            pos_ = -1
            for p in range(0, 4):
                pos_ = current_url.find('-', (pos_ + 1))
            self.pgno[current_url[(pos_ + 1):posq]] += 1
            next_page_url = 'https://www.1mg.com/drugs-therapeutic-classes/drug-class-' + str(current_url[(pos_ + 1):posq]) + '?page=' + str(self.pgno[current_url[(pos_ + 1):posq]])
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            pass
