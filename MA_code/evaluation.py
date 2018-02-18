from query_builder import *
from rank_metrics import *
import re
import cPickle as pickle



def getTargets(weight,L):

    instances = keyWords(weight)

    targets = []

    for i in L:
        target = filterKeyWords(instances[i][4])

        targets.append(target)

    return targets

"""

def hasTarget(weight, L):

    instances = keyWords(weight)

    BigBigL = []

    wikiWords = wikistring()

    for j in range(4):

        BigL = []

        count = 0

        for i in L:
            try:

                target = filterKeyWords(instances[i][4])

                #print (target)

                #with open("/Users/mengfei/Documents/learning Data/NLP/MA/data/query_dev_ca/query"+str(j+1)+"_"+str(i+1)+".txt") as data:
                with open("/mnt/proj/zhou/MA/data/query_dev_right/query"+str(j+1)+"_"+str(i+1)+".txt") as data:

                    l = []

                    pages = data.read().split('\n\n')[:-1]

                    if len(pages) == 10:
                        #print len(pages)
                        #print data

                        for page in pages:


                            #page = re.sub(r'</?\w+[^>]*>', '', page)

                            if target in page:
                                l.append(1)

                                #print(target)
                                #print(page)
                                #print(data)

                                count+=1

                            #for ws in wikiWords:

                                #print ws

                            else:
                                l.append(0)

                        BigL.append((l,data))

            except IOError:
                #print ('cannot open'), i
                pass

        print("count: "+str(count))

        BigBigL.append(BigL)

    #print (BigBigL[1])

    return BigBigL

"""

def hasTarget(weight, L, wikiname,queryData,pNum):

    base = "/Users/mengfei/Documents/learning Data/NLP/MA/data/"
    #base = "/mnt/proj/zhou/MA/data/"

    instances = keyWords(weight)


    #print instances

    BigBigL = []

    intersections = []

    wikiWords = pickle.load(open(base + wikiname, "rb"))


    #print wikiWords

    for j in range(4):

        BigL = []

        count = 0

        intersection = []

        for i in L:
            try:

                target = filterKeyWords(instances[i][4])

                #print (target)

                with open("/Users/mengfei/Documents/learning Data/NLP/MA/data/"+queryData+"/query"+str(j+1)+"_"+str(i+1)+".txt") as data:
                #with open("/mnt/proj/zhou/MA/data/query_dev_right/query"+str(j+1)+"_"+str(i+1)+".txt") as data:

                    l = []

                    pages = data.read().split('\n\n')[:-1]

                    if len(pages) >= pNum:

                        intersection.append(i+1)

                        #print len(pages)
                        #print data

                        for page in pages:

                            #page = re.sub(r'</?\w+[^>]*>', '', page)

                            if len(target)<=2:
                                target = " "+target+" "
                            if target.lower() in page.lower():

                                #print ("target: " + target)

                                l.append(1)

                                #print(target)
                                #print(page)
                                #print(data)

                                count+=1

                            #for ws in wikiWords:

                                #print ws

                            else:

                                f = False

                                for ws in wikiWords:
                                    if target.lower() in ws:
                                        for w in ws:
                                            if len(w)<=2 and w is not "":
                                                w = " "+w+" "
                                            if w in page.lower() and w is not "":
                                                #print ("w: " + w)
                                                f = True

                                if f == True:
                                    l.append(1)
                                    count += 1
                                else:
                                    l.append(0)

                        #print data
                        #print l

                        BigL.append((l,data))

            except IOError:
                #print ('cannot open'), i
                pass

        #print("count: "+str(count))

        BigBigL.append(BigL)
        intersections.append(intersection)

    #print (BigBigL[1])

    return BigBigL,intersections


def relation_weight(weight,wikiname,queryData,pNum):

    BigBigBigL = []
    
    #d = {'first':0, 'serves':51,'characters':111,'series':171,'work':231,'artist':289,'content_genre':349,'companies':409,'videogame':469, 'version_game':529, 'version_platform':589, 'institution_campuses':647, 'institution_school_type':707, 'cinematography':767,'country':827,'directed':869,'film':929,'language':989,'music':1049,'rating':1109,'sequel':1163,'cities':1179,'mouth':1239,'contains':1298, 'album_genre':1358, 'artist_genre':1416,'label':1476,'origin':1503,'composer':1563,'lyricist':1617,'albums':1677,'founders':1735,'organization_locations':1773,'sectors':1779,'person_cause_of_death':1838,'person_place_of_death':1874,'people':1934,'members':1989,'nationality':2029,'place_of_birth':2038,'profession':2096,'religion':2155,'player':2215,'event_locations':2275,'program_country_of_origin':2324, 'program_genre':2384}

    
    #d = {'first':0, 'nationality':258, 'place_of_birth':346, 'profession':869}

    d = {'first':0, 'serves':59, 'characters':119, 'series':179, 'work':237, 'artist':297, 'content_genre':357, 'companies':417, 'videogame':477, 'version_game':537, 'version_platform':597, 'institution_campuses':657, 'institution_school_type': 717, 'cinematography':775, 'country':835, 'directed':893, 'film':953, 'language':1012, 'music':1072, 'rating': 1132, 'sequel':1188,'cities':1241,'mouth':1299, 'contains':1358,'album_genre':1418, 'artist_genre':1473,'label':1533,'origin':1591,'composer':1651,'lyricist':1707,'albums':1765,'founders':1823,'organization_locations':1881,'sectors':1904,'person_cause_of_death':1964, 'person_place_of_death':2016,'people':2076,'members':2134,'nationality':2176,'place_of_birth':2193,'profession':2253,'religion':2313,'player':2372, 'event_locations':2432,'program_country_of_origin':2492, 'program_genre':2548}
    #d = {'first':0, 'nationality':430, 'place_of_birth':599, 'profession':1096}
    sortedL = sorted(d.items(), lambda x, y: cmp(x[1], y[1]), reverse=False)

    l = [ele[1] for ele in sortedL]

    names = [ele[0] for ele in sortedL]

    #print names
    #print l

    for i in range(len(l))[1:]:

        print names[i]

        L = range(l[i])[l[i-1]:l[i]]

        #print ("L: ") + str(L)

        BigBigL,intersections = hasTarget(weight,L,wikiname,queryData,pNum)

        BigBigBigL.append((names[i],BigBigL,l[i]-l[i-1],intersections,l[i]))

    #print len(BigBigBigL)

    #print BigBigBigL

    return BigBigBigL

def filterKeyWords(keyword):

    word = ''

    eles = keyword.split('_')
    for e in eles[:-1]:
        word += e+' '

    word += eles[-1]

    return word


def evaluation(flag,number,wikiname,queryData, pNum):

    BigBigL,intersections = hasTarget(flag,range(number),wikiname,queryData,pNum)

    intersection = getIntersectionNum(flag,number,intersections)

    #print intersection

    interLength =len(intersection)

    print("interLength: ") + str(interLength)



    for BigL in BigBigL:

        #print BigL[0]

        i = 0
        num = 0
        num_com = 0
        for ele in BigL:

            l = ele[0]
            data = ele[1]

            #if len(l)<10:
                #print(len(l))
                #l.extend([0]*(10-len(l)))
            #print (len(l))

            i+=1
            #precision = precision_at_k(l,10)
            num += precision_at_k(l,pNum)

            #if precision>0.5:
                #print precision
                #print data

        for ele in BigL:

            l = ele[0]
            data = ele[1]

            #print data.name
            if flag == 'test':
            #print data.name.split('_')[3].split('.')[0]
                idNum = int(data.name.split('_')[2].split('.')[0])
            elif flag == 'test_rel':
                idNum = int(data.name.split('_')[3].split('.')[0])


            if idNum in intersection:
                num_com += precision_at_k(l, pNum)

        print ("i: "+str(i))

        print ("num: " + str(num))

        print("Precision: " + str(num/i))

        print("Recall: " + str(num/number))

        print (len(BigL))


        print("comparable precision: " + str(num_com/interLength))


def evaluation_rel(flag, wikiname,queryData,pNum):

    BigBigBigL = relation_weight(flag,wikiname,queryData,pNum)

    s = ", Q(S+R), Q(S+R+IN), Q(S+R+P), Q(S+R+RP)" + "\n"
    s2 = ", Q(S+R), Q(S+R+IN), Q(S+R+P), Q(S+R+RP)" + "\n"
    s3 = ", Q(S+R), Q(S+R+IN), Q(S+R+P), Q(S+R+RP)" + "\n"

    numbers = []

    for BigBigL in BigBigBigL:

        number = []
        number.append(BigBigL[0])

        #print BigBigL

        s += BigBigL[0]+","
        s2 += BigBigL[0] + ","
        s3 += BigBigL[0] + ","


        totalNum = BigBigL[2]

        #print ("totalNum: " + str(totalNum))

        #print ("BigBigL: " + str(BigBigL[3]))

        intersection = getIntersectionNum(flag, BigBigL[4], BigBigL[3])

        #print intersection

        interLength = len(intersection)


        #print ("interLength: ") + str(interLength)

        for BigL in BigBigL[1]:

            numbersm = []

            #print BigL

            i = 0
            num = 0
            num_com = 0

            for ele in BigL:


                #print ele

                l = ele[0]
                data = ele[1]

                # if len(l)<10:
                # print(len(l))
                # l.extend([0]*(10-len(l)))
                # print (len(l))

                i += 1
                #precision = precision_at_k(l, 10)
                num += precision_at_k(l, pNum)

            for ele in BigL:

                l = ele[0]
                data = ele[1]

                # print data.name
                if flag == 'test':
                    # print data.name.split('_')[3].split('.')[0]
                    idNum = int(data.name.split('_')[2].split('.')[0])
                elif flag == 'test_rel':
                    idNum = int(data.name.split('_')[3].split('.')[0])

                if idNum in intersection:
                    num_com += precision_at_k(l, pNum)

            try:
                #print("i: " + str(i))

                #print("num: " + str(num))

                #print ("Precision: " + str(num/i))

                #print("Recall: " + str(num/totalNum))



                #print("comparable precision: " + str(num_com / interLength))

                s+= str(num/i)+','
                s2+= str(str(num/totalNum)) + ','
                s3+= str(num_com / interLength) + ','


                numbersm.append(float(num/i))
                numbersm.append(float(num/totalNum))
                numbersm.append(float(num_com/interLength))


                #print(len(BigL))
            except ZeroDivisionError:
                print("i: " + str(i))
                print("num: " + str(num))

            number.append(numbersm)

        s+='\n'
        s2+='\n'
        s3+='\n'

        #print
        numbers.append(number)
    #print s
    #print s2
    #print s3

    return numbers


def average_score(flag, wikiname,queryData,pNum):

    numbers = evaluation_rel(flag, wikiname, queryData, pNum)

    #print numbers

    rels = []

    p_max_index = []
    r_max_index = []
    cp_max_index = []

    score_p = []
    score_r = []
    score_cp = []

    base_score_p = []
    base_score_r = []
    base_score_cp = []

    for l in numbers:

        rels.append(l[0])

        print l[0]

        p = []
        r = []
        cp = []

        try:

            for i in range(5)[1:]:
                p.append(l[i][0])
                r.append(l[i][1])
                cp.append(l[i][2])

            p_b = max(p)
            r_b = max(r)
            cp_b = max(cp)

            p_max_index_sig = [i for i, v in enumerate(p) if v == p_b][0]

            print p_max_index_sig

            r_max_index_sig = [i for i, v in enumerate(r) if v == r_b][0]
            cp_max_index_sig = [i for i, v in enumerate(cp) if v == cp_b][0]

            score_p_big = p[p_max_index_sig]
            score_r_big = r[r_max_index_sig]
            score_cp_big = cp[cp_max_index_sig]

            #print score_p_big
            #print score_r_big
            #print score_cp_big
            #print

            p_max_index.append([i for i, v in enumerate(p) if v == p_b])
            print p_max_index

            r_max_index.append([i for i, v in enumerate(r) if v == r_b])
            cp_max_index.append([i for i, v in enumerate(cp) if v == cp_b])

            score_p.append(score_p_big)
            score_r.append(score_r_big)
            score_cp.append(score_cp_big)

            base_score_p.append(l[1][0])
            base_score_r.append(l[1][1])
            base_score_cp.append(l[1][2])


        except IndexError:
            pass

            #print p_max_index
            #print r_max_index
            #print cp_max_index

        #print score_p
        #print score_r
        #print score_cp

    pair_p = zip(p_max_index,score_p,base_score_p, rels)
    print pair_p

    pair_r = zip(r_max_index,score_r,base_score_r, rels)
    pair_cp = zip(cp_max_index,score_cp,base_score_cp, rels)

    print "precision: "
    av_score(pair_p,flag, wikiname, queryData, pNum)

    print "recall: "
    av_score(pair_r,flag, wikiname, queryData, pNum)

    print "comparable precision: "
    av_score(pair_cp,flag, wikiname, queryData, pNum)



def av_score(pair, flag, wikiname, queryData, pNum):

    #numbers = evaluation_rel(flag, wikiname, queryData, pNum)

    #print pair

    scores_1 = 0
    scores_2 = 0
    scores_3 = 0
    scores_4 = 0

    score_base_1 = 0
    score_base_2 = 0
    score_base_3 = 0
    score_base_4 = 0

    n1 = 0
    n2 = 0
    n3 = 0
    n4 = 0

    for ele in pair:

        #print ele

        max_index = ele[0]
        score = ele[1]
        base_score = ele[2]
        rel = ele[3]

        #print max_index
        #print score

        for index in max_index:

            if index == 0 :
                scores_1 += score
                #print scores_1

                n1 += 1
                score_base_1 += base_score
                #print score_base_1

                print "0 -- base score: " + str(base_score) + ", relation: " + rel

            elif index == 1:
                scores_2 += score
                n2 += 1
                score_base_2 += base_score

                print "1 -- base score: " + str(base_score) + ", relation: " + rel

            elif index == 2:
                scores_3 += score
                n3 += 1
                score_base_3 += base_score

                print "2 -- base score: " + str(base_score) + ", relation: " + rel
            elif index == 3:
                scores_4 += score
                n4 += 1
                score_base_4 += base_score

                print "3 -- base score: " + str(base_score) + ", relation: " + rel


    if not n1 == 0:
        print "expansion1: " + str(scores_1/n1)
        print "base score average: " +str(score_base_1/n1)
    else:
        print "expansion1: 0.0"
    if not n2 == 0:
        print "expansion2: " + str(scores_2/n2)
        print "base score average: " + str(score_base_2/n2)
    else:
        print "expansion2: 0.0"
    if not n3 == 0:
        print "expansion3: " + str(scores_3/n3)
        print "base score average: " + str(score_base_3/n3)
    else:
        print "expansion3: 0.0"
    if not n4 == 0:
        print "expansion4: " + str(scores_4/n4)
        print "base score average: " + str(score_base_4/n4)
    else:
        print "expansion4: 0.0"



def analyseNumber(flag, wikiname,queryData,pNum):

    #numbers = evaluation_rel(flag, wikiname,queryData,pNum)

    p_max_index = []
    r_max_index = []
    cp_max_index = []


    for l in numbers:

        #print l

        p = []
        r = []
        cp = []

        try:

            for i in range(5)[1:]:
                p.append(l[i][0])
                r.append(l[i][1])
                cp.append(l[i][2])


        #print p
        #print r
        #print cp

            p_b = max(p)
            r_b = max(r)
            cp_b = max(cp)

            p_max_index.extend( [i for i, v in enumerate(p) if v == p_b])
            r_max_index.extend([i for i, v in enumerate(r) if v == r_b])
            cp_max_index.extend([i for i, v in enumerate(cp) if v == cp_b])

        except IndexError:
                pass


    #print p_max_index

    print "precision: "
    countMax(p_max_index)

    print "recall: "
    countMax(r_max_index)

    print "comparable precision: "
    countMax(cp_max_index)

def countMax(max):
    c_sr = 0
    c_in = 0
    c_p = 0
    c_pr = 0

    for ele in max:
        if ele == 0:
            c_sr += 1
        elif ele == 1:
            c_in += 1
        elif ele == 2:
            c_p += 1
        elif ele == 3:
            c_pr += 1

    #print c_sr
    #print c_in
    #print c_p
    #print c_pr

    total = c_sr+c_in+c_p+c_pr

    per_sr = c_sr/float(total)
    per_in = c_in/float(total)
    per_p = c_p/float(total)
    per_pr = c_pr/float(total)

    print(per_sr)
    print(per_in)
    print(per_p)
    print(per_pr)

    print(c_sr)
    print(c_in)
    print(c_p)
    print(c_pr)



def wikistring():

    l = []

    #with open("/Users/mengfei/Documents/learning Data/NLP/MA/data/reversed_index.en.txt") as data:

    with open("/mnt/proj/zhou/MA/data/reversed_index.en.txt") as data:

        for line in data:

            #print line

            words = []

            eles = line.strip().split('"en":')

            #print eles[1:]

            for w in eles[1:]:
                w = re.sub('"(.*?)"', r'\1', w)

                words.append(w.lower().strip())


            #   print words

            l.append(words)

    #print l
    return l

def smallWikiString():

    l = wikistring()

    targets = getTargets('test_rel',range(1096))

    smallWiki = []

    for t in targets:
        for ws in l:
            if t.lower() in ws:
                smallWiki.append(ws)
                #print smallWiki


    #print smallWiki
    #print len(smallWiki)

    pickle.dump(smallWiki, open("/mnt/proj/zhou/MA/data/smallWiki_test_rel.p", "wb"))

    return smallWiki

def getWikiList():
    base = "/Users/mengfei/Documents/learning Data/NLP/MA/data/"
    wikiWords = pickle.load(open(base + "smallWiki.p", "rb"))

    print wikiWords


def getIntersectionNum(flag,number,intersections):

    #intersections = hasTarget(flag,range(number))[1]

    right = []

    for i in range(number+1):

        t = True

        for interstion in intersections:
            if i not in interstion:
                t = False

        if t == True:
            right.append(i)

    #print right

    return right





if __name__ == '__main__':


    #evaluation('dev',2384,'smallWiki.p','query_dev_ca',1)
    #evaluation('dev_rel', 869, 'smallWiki_rel.p', 'query_dev_rel_ca',1)
    #relation_weight('dev')

    #evaluation_rel('dev_rel','smallWiki_rel.p','query_dev_rel_ca',10)

    #evaluation_rel('dev', 'smallWiki.p', 'query_dev_ca', 10)

    #wikistring()
    #smallWikiString()


    #getIntersectionNum('dev',2384)

    #getWikiList()

    #evaluation('test', 2548, 'smallWiki_test.p', 'query_test', 10)

    #evaluation('test_rel', 1096, 'smallWiki_test_rel.p', 'query_test_rel', 10)

    #evaluation_rel('test_rel','smallWiki_test_rel.p','query_test_rel',10)
    #evaluation_rel('test','smallWiki_test.p','query_test',10)

    #analyseNumber('test','smallWiki_test.p','query_test',3)

    #analyseNumber('test_rel','smallWiki_test_rel.p','query_test_rel',10)

    #analyseNumber('test', 'smallWiki_test.p', 'query_test',3)

    #analyseNumber('dev_rel','smallWiki_rel.p','query_dev_rel_ca',10)

    #analyseNumber('dev', 'smallWiki.p', 'query_dev_ca', 10)

    average_score('test', 'smallWiki_test.p', 'query_test', 10)