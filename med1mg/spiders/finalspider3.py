#Scrapes all Info from Individual Medicines links given in check.json by MedicineSpideyLarge (Step 3)
import json
import scrapy
import os.path


class finalspider3(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        g = open(os.path.dirname(__file__) + '/../isthisall.json')
        f = open(os.path.dirname(__file__) + '/../check.json')
        spidey = json.load(f)
        urllist = []
        self.url_to_therapy = {}
        self.url_to_img = {}
        for i in spidey:
            links = i['Links']
            plink = i['Parent Link']
            img = i['Image Links']
            for j in links:
                listindex = links.index(j)
                self.url_to_therapy[j] = plink  ##Medicine['Therepeutic Class'] = get_key(self.url_to_therapy[j])
                self.url_to_img[j] = img[listindex]
                urllist.append("https://1mg.com" + j)
        self.start_urls = urllist
        self.referral = json.load(g)[0]

    name = 'finalspider3'
    allowed_domains = ['1mg.com']

    def get_key(self, val):
        for key, value in self.referral.items():
            if val == value:
                return key

    def parse(self, response):
        Medicines = {}
        Medicines["Name"] = response.css(".DrugHeader__title___1NKLq::text").extract()
        try:
            Medicines["Prescription"] = response.css(".DrugHeader__prescription-req___34WVy span::text").extract()
        except:
            Medicines["Prescription"] = "Not Necessary"
        Medicines["Type of Sell"] = response.css(".DrugPriceBox__quantity___2LGBX::text").extract()
        Medicines["Manufacturer"] = response.css(".DrugHeader__meta___B3BcU:nth-child(1) a::text").extract()
        Medicines["Salt"] = response.css(".saltInfo a::text").extract()
        Medicines["MRP"] = response.css(".DrugPriceBox__bestprice-slashed-price___2ANwD::text").extract()
        Medicines["Best Price"] = response.css(".DrugPriceBox__best-price___32JXw::text").extract()
        Medicines["Uses"] = response.css("#overview a::text").extract()
        Medicines["How to Use"] = response.css(".DrugOverview__container___CqA8x:nth-child(5) .DrugOverview__content___22ZBX::text").extract()
        Medicines["Alternate Medicines"] = response.css(".SubstituteItem__name___PH8Al::text").extract()
        Medicines["Side Effects"] = response.css(".DrugOverview__list-container___2eAr6 li::text").extract()
        Medicines["Chemical Class and Habit Forming"] = response.css(".DrugFactBox__col-right___36e1P::text").extract()
        current_url = response.request.url
        pos_ = -1
        for p in range(0, 3):
            pos_ = current_url.find('/', (pos_ + 1))
        Medicines["Therapeutic Class"] = self.get_key(self.url_to_therapy[current_url[pos_:]])
        Medicines["Image Link"] = self.url_to_img[current_url[pos_:]]
        yield Medicines
