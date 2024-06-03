# https://catalogscore.site/

## This is a website designed for Buyer Apps in ONDC to Score the Seller Catalogs.
## For this Project We took "Meesho"(https://ondc.meesho.org/) as our client. We Scored Products from the perspective of Meesho Buyer App. 
    --> our website has three pages.
        --> First page shows the complete product details and Scores assigned including Completenss, Correctness, Compliance.
            -->In this page we can put any product URL from (https://ondc.meesho.org/).It'll show that product details and score.
        -->Secong Page is used to scrape the Seller Catalog, Since Seller is only found upon searching in ONDC, 
            • We thought, as of now scraping is best way to collect seller data for scoring.
                Example of Seller catalog URL: https://ondc.meesho.org/seller/slrp-1336654.
            • In This page also we can put any seller URL, it'll scrape those products and store in database,
                we can see collected catalog in third page.
        -->Third Page shows the catalogs scraped in second page.
           This page shows complete information and scores of all products in catalog.

Tech Stack: 
  ### Web Development FrameWork: Flask(python).
  ### Fontend : HTML, CSS, Java Script.
  ### Database : MongoDB.
  ### Web Hosting : Google Cloud.

![image](https://github.com/2deva/catalog-score/assets/111851690/aeccf406-146f-4989-8086-33cb3e58217b)
![image](https://github.com/2deva/catalog-score/assets/111851690/240ffd4e-9218-41ee-9b9a-37284681d70e)
![image](https://github.com/2deva/catalog-score/assets/111851690/a024dc73-82aa-4f66-9924-5c09663850d0)
![image](https://github.com/2deva/catalog-score/assets/111851690/efa66d1a-93a3-4495-8a88-3fe8d2dddf16)
![image](https://github.com/2deva/catalog-score/assets/111851690/4497887c-7afd-4866-9695-ffdbb1f82aec)
