import cPickle as pickle


def statDas(relname,flag):

    base = "/mnt/proj/zhou/MA/data_final/release_with_entities_akbc/"

    c_inst = 0

    with open(base + relname + '/' + flag + '_matrix.tsv.translated') as data:

        for line in data:

            eles = line.split('\t')

            if len(eles) == 4:

                posNeg = eles[3]

                if posNeg.strip()=="1":

                    c_inst += 1
            elif len(eles) == 3:
                c_inst += 1

    return c_inst

def statDasAll(flag):

    c_all = 0

    c_path_all = 0

    with open('/mnt/proj/zhou/MA/data/relations.txt') as data:

        for line in data:
            line = line.strip()
            c_inst = statDas(line,flag)
            c_all += c_inst

            c_path = process(line,flag)

            c_path_all += c_path




    #print c_all

    #ave = c_all/46

    ave2 = c_path_all/46

    #print "instances : " + str(ave)
    #sprint "path types: " + str(ave2)

    print "paths: " + str(ave2)



def process(relname,flag):

    base = "/mnt/proj/zhou/MA/data_final/release_with_entities_akbc/"

    count = dict()

    c_inst = 0

    total = 0

    with open(base+relname+'/'+flag+'_matrix.tsv.translated') as data:

        for line in data:



            #c_inst += 1

            eles = line.split('\t')



            if len(eles) == 4:

                pathsString = eles[2]

                posNeg = eles[3]

                #print posNeg.strip()

                if posNeg.strip()=="1":
                    c_inst += 1

                    paths = pathsString.split('###')

                    for p in paths:
                        rels = []
                        iNAndRels =  p.split('-')

                        #print (iNAndRels)

                        for ele in iNAndRels:
                            if not ele.startswith('/m/'):
                                if not ele.startswith('_'):
                                    rels.append(ele)
                                else:
                                    rels.append(ele.replace('_','',1))

                            #print (rels)

                        relationString = ""

                        for re in rels:
                            relationString += re+'==='

                            #print (relationString)

                        if not count.has_key(relationString):
                            count[relationString]=1
                        else:
                            count[relationString]+=1

            #print len(count.keys())

            #l = sorted(count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

            #print l

            #return count, c_inst, l

            """            
            elif len(eles)==3:
            
            c_inst += 1

            pathsString = eles[2]

            paths = pathsString.split('###')

            for p in paths:
                rels = []
                iNAndRels = p.split('-')

                # print (iNAndRels)

                for ele in iNAndRels:
                    if not ele.startswith('/m/'):
                        if not ele.startswith('_'):
                            rels.append(ele)
                        else:
                            rels.append(ele.replace('_', '', 1))

                                # print (rels)

                relationString = ""

                for re in rels:
                    relationString += re + '==='

                        # print (relationString)

                if not count.has_key(relationString):
                    count[relationString] = 1
                else:
                    count[relationString] += 1
                """
        for ele in count.values():

            total += ele

    return total


def filterPath(flag):

    base = "/mnt/proj/zhou/MA/data/"

    count = dict()

    with open(base + 'relations.txt') as data:
        for line in data:
            rel = line.strip()

            count1 = process(rel,flag)[0]


            for ele in count1:
                #print (ele)
                if not count.has_key(ele):
                    count[ele]=count1[ele]
                else:
                    count[ele]+=count1[ele]

    #l = sorted(count.items(), lambda x, y: cmp(x[1], y[1]))

    #print l

    #print count
    return count

def countTfIdf(flag):

    relations_b = dict()

    base = "/mnt/proj/zhou/MA/data/"

    count2 = filterPath(flag)


    with open(base + 'relations.txt') as data:
        for line in data:

            relations = []

            rel = line.strip()

            #print rel

            cc = process(rel,flag)

            count1 = cc[0]
            c_inst = cc[1]
            l = cc[2]

            #print("c_inst: " + str(c_inst))

            #print("l: " + str(l))

            c_good_rel = 0

            #print rel

            #for relation in count1:
            for pair in l:
                #print pair

                relation = pair[0]
                length = relation.split('===')

                c1 = count1[relation]
                c2 = count2[relation]



                score1 = c1/float(c2)
                score2 = c1/float(c_inst)

                #print relation
                #print "score1: " + str(score1)
                #print "score2: " + str(score2)

                #s = rel + "\t"+ relation + "\t" + str(score1) + "\t" + str(score2)

                #print s


                # s1 = 1.0 , s2 = 0.005
                #if score1 == s1 and score2 > s2:

                filter = True

                for ele in length[:-1]:
                    if not len(ele.split('/')) == 4:
                        filter = False

                #print "score1: " + str(score1)
                #print "len_length: " + str(len(length))
                #print "filter: " + str(filter)

                if score1 > 0.7 and len(length)<=5 and filter==True:
                #if score1 == 1.0 and len(length) <= 5 and filter == True:
                    c_good_rel += 1
                    #print relation
                    relations.append(relation)
                    #print pair

                if c_good_rel >= 5:
                    break

            #print c_good_rel
            #print c_good_rel/float(len(count1))
            relations_b[rel]=relations

        #pickle.dump(relations_b, open("/mnt/proj/zhou/MA/data/relations"+"_score1_"+str(s1)+'_score2_'+str(s2)+'_'+flag+'.p', "wb"))
        pickle.dump(relations_b, open("/mnt/proj/zhou/MA/data/relations_first2_"  + flag + ".p", "wb"))
        return relations_b

def extractPath(relname,flag):
    base = "/mnt/proj/zhou/MA/data/release_with_entities_akbc/"
    base2   = "/mnt/proj/zhou/MA/data/"

    extractL = []

    #relations_b = pickle.load(open(base2+"relations_score1_"+str(s1)+'_score2_'+str(s2)+'_'+flag+'.p',"rb"))
    relations_b = pickle.load(open(base2 + "relations_first2_" + flag + ".p", "rb"))

    r_eles = relname.split('_')

    if len(r_eles) <= 4:
        right_relname = '/'+r_eles[1]+'/'+r_eles[2]+'/'+r_eles[3]
    else:
        right_relname = '/' + r_eles[1] + '/' + r_eles[2] + '/' + r_eles[3]
        for e in r_eles[4:]:
            right_relname += '_'+e

    relations = relations_b[relname]

    c = 0

    limit = dict()

    with open(base + relname + '/'+flag+'_matrix.tsv.translated') as data:
        for line in data:

            eles = line.split('\t')

            posNeg = eles[3]

            if posNeg.strip() == "1":

                node1 = eles[0]
                node2 = eles[1]
                pathsString = eles[2]
                paths = pathsString.split('###')

                for p in paths:
                    rels = []
                    iNAndRels = p.split('-')

                    for ele in iNAndRels:
                        if not ele.startswith('/m/'):
                            if not ele.startswith('_'):
                                rels.append(ele)
                            else:
                                rels.append(ele.replace('_', '', 1))

                    relationString = ""

                    for re in rels:
                        relationString += re + '==='

                    if relationString in relations:

                        if not limit.has_key(relationString):
                            limit[relationString] = 0
                        else:
                            limit[relationString] += 1

                        # if limit[relationString] < 170 (for dev data):
                        if limit[relationString] < 100:
                        #if limit[relationString] < 30:
                            #fw.write(relationString+'\n')

                            c+=1
                            extractL.append(node1 + '\t' + node2 + '\t' + right_relname + '\t' + p)

    print relname
    print c
    return extractL

def extractAllPath(flag):
    base = "/mnt/proj/zhou/MA/data/"

    f_name = base + flag+'_path.txt'
    fw = open(f_name,'w')

    with open(base + 'relations_small.txt') as data:
        for line in data:
            rel = line.strip()
            extracL = extractPath(rel,flag)

            for ele in extracL:
                fw.write(ele+'\n')

def extractRelations(relname,flag):
    base2 = "/mnt/proj/zhou/MA/data/"
    relations_b = pickle.load(open(base2 + "relations_first2_" + flag + ".p", "rb"))

    r_eles = relname.split('_')

    relations = relations_b[relname]

    return relations

def extractAllRelations(flag):
    base = "/mnt/proj/zhou/MA/data/"

    f_name = base + flag + '_relations.txt'
    fw = open(f_name, 'w')

    with open(base + 'relations_small.txt') as data:
        for line in data:
            rel = line.strip()
            extracL =extractRelations(rel,flag)

            fw.write(rel)

            fw.write('\n')

            for ele in extracL:
                fw.write(ele + '\n')

if __name__== '__main__':


    statDasAll('test')

    #process('_book_book_characters','dev')

    #countTfIdf("test")
    #extractPath('_book_book_characters')
    #extractAllPath("test")

    #extractAllRelations("dev")