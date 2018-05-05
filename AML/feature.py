import wikipedia
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm, tqdm_notebook
import time
import requests
import datefinder

def num_links(page_title):
	w=wikipedia.page(page_title)
	num_links=len(w.links)
	return num_links

def num_external_links(page_title):
	w=wikipedia.page(page_title)
	num_external_links=len(w.references)

def getMetadata(train):
	page_metadata=train.Page.str.extract(r'(?P<article>.*)\_(?P<language>.*).wikipedia.org\_(?P<access>.*)\_(?P<type>.*)', expand=False)
	return page_metadata

def num_unique_categories(page_title):
	w=wikipedia.page(page_title)
	return len(w.categories)



SLEEP_TIME_S = 0.1
def extract_URL_and_Name(page):
    """ From the page name in the input file extract the Name and the URL """
    return (['_'.join(page.split('_')[:-3])]
            + ['http://' + page.split("_")[-3:-2][0] +
               '/wiki/' + '_'.join(page.split('_')[:-3])]) # Load the dataset



def fetch_wikipedia_text_content(row):
    """Fetch the all text data of a given page"""
    try:
        r = requests.get(row['URL'])
        # Sleep for 100 ms so that we don't use too many Wikipedia resources
        time.sleep(SLEEP_TIME_S)
        to_return = [x.get_text() for x in
                     BeautifulSoup(
                         r.content, "html.parser"
                     ).find(id="mw-content-text").find_all('p')]
    except:
        to_return = [""]
    return to_return # This will fail due to lack of Internet


def find_dates(row):
    """
    :returns a list of datetime objects added the row
    :param row:
    :return:
    """
    try:
        r = requests.get(row['TextData'])
        x = datefinder.find_dates(str(r))
        l=[]
        for d in x:
            # print(d)
            # print(type(d))
            l.append()
        to_return=l
    except:
        to_return = [""]


train = pd.read_csv('data/train_2.csv')
#train = train.sample(2)
page_data = pd.DataFrame(
    list(train['Page'].apply(extract_URL_and_Name)),
    columns=['Name', 'URL'])

page_data.head()
tqdm.pandas(tqdm_notebook)
page_data['TextData'] = page_data.progress_apply(fetch_wikipedia_text_content, axis=1)

page_data['TextData'] = page_data.progress_apply(fetch_wikipedia_text_content, axis=1)
page_data.head()

page_data['Dates'] = page_data.progress_apply(find_dates, axis=1)
page_data.head()

