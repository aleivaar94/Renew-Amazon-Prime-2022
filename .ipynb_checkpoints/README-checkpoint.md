
# Scrapping Food Recalls from Government of Canada Recalls and Safety Alerts - Part I and Part II

A food recall is the removal of a food product from the market to avoid further sale or use, or the correction of its label at any point in the supply chain. It's the industry's responsibility to remove the recalled food from the marketplace, while the Canadian Food Inspection Agency's (CFIA) role is to inform the consumers, oversee implementation the recall and verify that the industry removed the product from the marketplace.

In this project, I extract food recalls from 2022 to 2011 from the Government of Canada Recalls and Safety Alerts [website](https://recalls-rappels.canada.ca/en/search/site?search_api_fulltext=&archived=1&f%5B0%5D=category%3A144&page=0) using webscrapping python libraries Selenium and Beautiful Soup.

<sub><sup>*Recalls before 2011 are [archived](https://epe.lac-bac.gc.ca/100/206/301/cfia-acia/2011-09-21/www.inspection.gc.ca/english/corpaffr/recarapp/recal2e.shtml). Recalls from 2006-1997 are no longer available in the archive.</sup></sub>

<sub><sup>To learn more about CFIA's food recall system, click [here](https://inspection.canada.ca/food-safety-for-consumers/canada-s-food-safety-system/how-we-decide-to-recall-a-food-product/eng/1332206599275/1332207914673).</sup></sub>

## Demo
![demo](https://github.com/aleivaar94/images-projects/blob/master/extracting-recalls-links.gif)



## Methodology

### Part I

I used Selenium and Beautiful Soup to parse the html page to extract:

1. URL of recall
2. Title of recall
3. Info or summary of recall
4. Date of recall

Each element is stored as a list and then put together as a Dataframe using pandas and exported in a csv file.

![df](https://github.com/aleivaar94/images-projects/blob/master/part-1-recall-links-dataframe.png)

### Part II

I used the links scrapped in Part I to access each recall and its information such as title, company issuing the recall, recall class, etc.

The pattern of reporting food recalls has changed overtime. For example, from 2022-08-24 to 2021-10-21 the information to extract is contained in the upper and lower part of the html page, while from 2021-10-15 to 2011-01-04 is contained in the upper part of the html page. Therefore the html tags and their pattern change. This change is accounted in the webscrapping code.

| From 2022-08-24 | To 2021-10-21 |
| :- | -: |
| ![image](https://github.com/aleivaar94/images-projects/blob/master/part-2-recall-pattern-1.png) | ![image](https://github.com/aleivaar94/images-projects/blob/master/part-2-recall-pattern-2.png) |


| From 2021-10-15 | To 2011-01-04 |
| :- | -: |
| ![image](https://github.com/aleivaar94/images-projects/blob/master/part-2-recall-pattern-3.png) | ![image](https://github.com/aleivaar94/images-projects/blob/master/part-2-recall-pattern-4.png) |

## Results

### Part I
A total of 4680 recall links were scrapped. Saved in `recalls-links-2022.csv`

### Part II
A total of 4680 recall details were scrapped. Save in `recalls-p-2022-2021, recalls-2021, recalls-2020, recalls-2019, recalls-2018, recalls-2017, recalls-2016, recalls-2015, recalls-2014, recalls-2013, recalls-2012, recalls-2011`

## Next Steps
Clean and analyze the recalls extracted. See [Part III and Part IV](https://github.com/aleivaar94/Part-III-Part-IV-Scrapping-Food-Recalls-from-Government-of-Canada-Recalls-and-Safety-Alerts) of this project.

## Future Work
It's expected that webscrapping doesn't output 100% clean data ready for analysis. Another approach to this project is exploring if the recall website has an API, then code an API command to extract the recalls in a more clean and perhaps more efficient way.

## Workflow
Follow the jupyter notebooks in the order below:
    
    1. Part-I-extracting-recall-links-BS4-Selenium.ipynb
    2. Part-II-extracting-recall-details-BS4-Selenium.ipynb

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://alejandroleiva.notion.site/Data-Portfolio-5c5257235e044c6b9a8846131edac973)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ale-leivaar/)
