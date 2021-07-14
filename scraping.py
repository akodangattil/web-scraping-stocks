import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from urllib.request import urlopen as uReq  # Web client
import chromedriver_binary
import string
pd.options.display.float_format = '{:.0f}'.format

is_link = input('Enter Yahoo Finance Company Url- ')
#is_link = "https://finance.yahoo.com/quote/AAPL?p=AAPL"
driver = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
driver.get(is_link)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml')

out_filename = "stocks.csv"

f = open(out_filename, "w")

# opening up connection, grabbing the page
uClient = uReq(is_link)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

features = soup.find_all('div', class_='D(tbr)')

target = input("enter target price")
headers = []
temp_list = []
label_list = []
final = []
index = 0
#create headers
for item in features[0].find_all('div', class_='D(ib)'):
    headers.append(item.text)
    f.write(item + "|" +"\n")
#statement contents
while index <= len(features)-1:
    #filter for each line of the statement
    temp = features[index].find_all('div', class_='D(tbc)')
    for line in temp:
        #each item adding to a temporary list
        temp_list.append(line.text)
        f.write(line + "|" +"\n")
    #temp_list added to final list
    final.append(temp_list)
    #clear temp_list
    temp_list = []
    index+=1
df = pd.DataFrame(final[1:])
df.columns = headers

#function to make all values numerical
def convert_to_numeric(column):
    first_col = [i.replace(',','') for i in column]
    second_col = [i.replace('-','') for i in first_col]
    final_col = pd.to_numeric(second_col)
    
    return final_col
for column in headers[1:]:
    
    df[column] = convert_to_numeric(df[column])
final_df = df.fillna('-')

f.write(brand + ", " + product_name.replace(",", "|") + ", " + shipping + "\n")

f.close()

