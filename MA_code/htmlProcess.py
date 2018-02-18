from bs4 import BeautifulSoup
import urllib
from query_builder import *
import re


base = '/Users/mengfei/Documents/learning Data/NLP/MA/data/query_test_rel/'

for i in range(4):
    for j in range(1096):

        try:

            soup = BeautifulSoup(open(base+'query'+str(i+1)+'_'+str(j+1)+'.html'))

            #print (soup.prettify())

            #texts=soup.findAll('span',{'class':'st'})
            texts = soup.findAll('div', {'class': 's'})

            f_name = base + 'query'+str(i+1)+'_'+str(j+1)+'.txt'

            fw = open(f_name, 'w')

            for text in texts:
                text = re.sub(r'</?\w+[^>]*>', '', str(text))
                fw.write(str(text)+'\n\n')

        except IOError:
            pass



"""
soup = BeautifulSoup(open('/Users/mengfei/Documents/learning Data/NLP/MA/data/query_dev_first2/query1_1.html'))
#print (soup.prettify())

texts2 = soup.findAll("div", { "class" : "s" })

for text2 in texts2:

    text2 = re.sub(r'</?\w+[^>]*>', '', str(text2))

    print text2
    print
"""