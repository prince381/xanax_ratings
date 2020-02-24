"""
    Script written by: Prince Owusu
    Date: 14/02/2020

"""


import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import json
from dateutil import parser
import pandas as pd
import numpy as np
import sys

# site where we are going to scrape the data from
page1 = 'https://www.drugs.com/comments/alprazolam/xanax.html'

# make the html request
html_page = requests.get(page1)

# verify if request is successful. If not, print the error message and exit the program.
try:
    html_page.raise_for_status
except Exception as error:
    print(error)
    sys.exit()


# parse the html page with BeautifulSoup
soup = bs(html_page.text,'html.parser')
# find all the html tags that hold the details of the comments and store them in a list
comments_list = soup.find_all(name='div',attrs={'class':"ddc-comment"})

page = 2   # next page index

print('Please wait for some minutes while data is extracting'+'.'*40)

while True:
	# link to the page of the site
    next_page = 'https://www.drugs.com/comments/alprazolam/xanax.html?page={}'.format(page)
    # make a new request 
    next_html_page = requests.get(next_page)
    # verify if request is successful. If not, print the error message and break from the loop
    try:
        next_html_page.raise_for_status
    except Exception as error:
        print(error)
        break

    # parse the html page if request was successful
    parsed_html = bs(next_html_page.text,'html.parser')
    # find all the html tags that hold the details of the comments and store them in a new list
    next_comments_list = parsed_html.find_all(name='div',attrs={'class':"ddc-comment"})
    # append the new list to the old list
    comments_list += next_comments_list
    page += 1  # increase the page index to help navigate to the next page
    # break from the loop if the page index is out of range
    if page >= 33:
        break
    else:
        continue


dates = []
conditions = []
reviews = []
ratings = []

# loop through the comments list and extract the neccessary information we need
for tag in comments_list:
	# extract the date
    date = tag.find(name='span',attrs={'class':"comment-date text-color-muted"}).text

    # try and extract the rating given by the user. If not available, replace with none
    try:
        rating = tag.find(name='div',attrs={'class':"comment-rating-score"}).text
    except Exception:
        rating = 'NaN'

    # extract the comment of the drug user and the condition he/she was suffering from
    comment_holder = tag.find(name='p',attrs={'class':"ddc-comment-content"})
    try:
        condition = comment_holder.find('b').text
    except:
        condition = 'NaN'
    review = comment_holder.find('span').text

    # append the values into their respective lists
    dates.append(date)
    conditions.append(condition[4:])
    reviews.append(review.strip('"'))
    ratings.append(rating)
    
# create a data frame with the information extracted.
data_frame = pd.DataFrame({'date':dates,'condition':conditions,'review':reviews,'rating':ratings})

# save the data into a csv file
data_frame.to_csv('Xanas_drug_reviews.csv',index=False)

print('Data frame saved to hard drive')