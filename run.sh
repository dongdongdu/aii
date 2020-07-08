echo "Start to craw whiter papers"
scrapy crawl white_papers

echo "Start to craw publications"
scrapy crawl publications

echo "Start to craw technical standards"
scrapy crawl tech_standards

echo "Start to craw expert views"
scrapy crawl expert_views