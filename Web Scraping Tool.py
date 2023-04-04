from xml.dom.minidom import Element
from numpy import place
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

# ys is dictonary whcih contains ASIN numbers the format should be ys=['B00JD242MS','B078KZ6LSQ']
ys = ['B00CH9QWOU']
sleep(1)

#we creating empty list for storing reviews
reviewlist=[] 


# for each ASIN in list we are iterating following loop

for y in ys:
    #url here
    url = 'https://www.amazon.com/product-reviews/'+ y +'/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    sleep(2)
#webdriver code
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe', options=options)
    driver.get(url)
    sleep(3)
    #getting product url and finding price
    purl=driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/a')
    purl.click()
    sleep(3)
    try:
       price=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[9]/div[4]/div[4]/div[10]/div/div[2]/div[2]/div/table/tbody/tr/td[2]/span/span[1]')
       p=price.text
       try:
           price=driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span/span[1]')
           p=price.text
       except:
           p="NA"
    except:
        p='NA'
    #fetching reviews
    driver.get(url)      
    while range(1,999): 
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')
        #with help of beautifulsoup finding div which contains all reviews div elemnts
        
        reviews = soup.find_all('div', {'data-hook': 'review'})
        #applying try block if some errors are there
        try:
           
            #iterating through all div elemnts to fetch reviews
            for item in reviews:
                if item in reviews:
                   pass
                else:
                   break

                review = {
                'product': soup.title.text.replace('Amazon.com: Customer reviews:', '').strip(),
                'price':p,
                'date':item.find('span',{'data-hook':'review-date'}).text.replace('Reviewed in the United States on','').strip(),
                'ASIN':y,
                'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'verified-purchase':item.find('span',{'data-hook': 'avp-badge'}).text.strip(),
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                print(review,'\n')
                reviewlist.append(review)
        except:
                    pass
        #applying stop function if there are no more reviews left
        if not soup.find('li', {'class': 'a-disabled a-last'}):
                pass
        else:
                break

        
       # clicking next button on reviews page
        try:
           next= driver.find_element_by_class_name('a-last')
           next.click() 
           sleep(2)
        except:
            pass
    driver.close()    

#creating csv files for review
df = pd.DataFrame(reviewlist)
df.to_csv('sv.csv', index=False)

    
print('Fin.')

# print('Finish')