#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def main():

    #keyWords('0.6')
    #makeQuery('dev')
    makeQuery(sys.argv[1])

def keyWords(flag):

    base = '/Users/mengfei/Documents/learning Data/NLP/MA/data/'
    #base = '/mnt/proj/zhou/MA/data/'

    instances = []

    with open(base + 'query_' + flag + '.txt') as data:
        for line in data:
            #print (line)

            eles = line.split('\t##')
            rels = eles[1]

            #print (rels.strip())
            others = eles[0]
            words = others.split('\t')

            query1Set = set([])
            query2Set = set([])
            query3Set = set([])
            query4Set = set([])

            #print(words[0])
            #print (filterKeyWords(words[0]))

            query1Set.add(filterKeyWords(words[0]))
            query1Set.add(filterKeyWords(words[2].split('/')[3]))

            query2Set.add(filterKeyWords(words[0]))
            query2Set.add(filterKeyWords(words[2].split('/')[3]))

            query3Set.add(filterKeyWords(words[0]))
            query3Set.add(filterKeyWords(words[2].split('/')[3]))

            query4Set.add(filterKeyWords(words[0]))
            query4Set.add(filterKeyWords(words[2].split('/')[3]))

            for word in words[3:]:
                query2Set.add(filterKeyWords(word))

            for word in words[3:]:
                query3Set.add(filterKeyWords(word))

            for rel in rels.split('\t')[:-1]:
                if len(rel.split('/'))==4:
                    query3Set.add(filterKeyWords(rel.split('/')[3]))

            for rel in rels.split('\t')[:-1]:
                if len(rel.split('/')) == 4:
                    query4Set.add(filterKeyWords(rel.split('/')[3]))

            targetWord = words[1]

            instances.append((query1Set, query2Set, query3Set, query4Set,targetWord, words[2].split('/')[3]))

    #print (instances)

    return instances


def makeQuery(flag):

    #d = {'$0028': "'", '$0029': "'", '$00E2': 'a', '$0103': 'a', '$0163': 't', '$015F': 's', '$0219': 's','$01CE': 'a', '$0162': 'T', '$00F3': 'o', '$015E': 'S', '$0027': "'", '$002C': ',', '$003A': ':','$002E': '.', '$00E9': 'e', '$0026': '-', '$2153': '1/3'}

    # wget -U 'Firefox/3.0.15' http://www.google.com/search?q=frank+zappa+mother -O zappa.html

    base = '/Users/mengfei/Documents/learning Data/NLP/MA/data/'

    instances = keyWords(flag)

    i = 0

    instForWriters = []

    f_name_query1 = base + 'googleQuery1_' + flag + '.txt'
    f_name_query2 = base + 'googleQuery2_' + flag + '.txt'
    f_name_query3 = base + 'googleQuery3_' + flag + '.txt'
    f_name_query4 = base + 'googleQuery4_' + flag + '.txt'

    f_name_statistic = base + 'googleQuery_stat_' + flag +  '.txt'

    f_name_rel = base + 'rel' + flag + '.txt'

    fw1 = open(f_name_query1, 'w')
    fw2 = open(f_name_query2, 'w')
    fw3 = open(f_name_query3, 'w')
    fw4 = open(f_name_query4, 'w')

    fw5 = open(f_name_rel, 'w')

    fw_stat = open(f_name_statistic, 'w')

    """
    for j in range(3):
        num = j+1
        f_name_query = base + 'googlQuery'+num+'_' + flag + '.txt'
        fw = open(f_name_query,'w')
    """

    for instance in instances:

        instForWriter = []

        i += 1

        fw5.write(str(i)+'\t'+instance[5]+'\n')

        for j in range(4):
            num = j+1
            idQ = "query"+str(num)+"_" + str(i)
            querySet = instance[j]
            queryList = list(querySet)
            query = "wget -U 'Firefox/3.0.15' http://www.google.ca/search?q="

            fw_stat.write(str(len(queryList))+' ')

            for word in list(queryList)[:-1]:
                query += word + '+'
            query += queryList[-1]
            query += " -O " + idQ + '.html'

            if not '$' in query:
                #print (query)
                """
                for character in d:
                    if character in query:
                        #print query
                        query = query.replace(character,d[character])
                        #print query
                """
                instForWriter.append(query)

        fw_stat.write('\n')

        instForWriters.append(instForWriter)

    for instForWriter in instForWriters:

        if len(instForWriter)==4:
            query1 = instForWriter[0]
            query2 = instForWriter[1]
            query3 = instForWriter[2]
            query4 = instForWriter[3]


        fw1.write(query1+'\n')
        fw2.write(query2+'\n')
        fw3.write(query3+'\n')
        fw4.write(query4+'\n')

def filterKeyWords(keyword):

    word = ''

    midWord = ''
    eles = keyword.split(' ')
    for e in eles[:-1]:
        midWord += e+'+'
    midWord += eles[-1]

    eles = midWord.split('_')
    for e in eles[:-1]:
        word += e+'+'

    word += eles[-1]

    return word


if __name__=='__main__':
    main()
