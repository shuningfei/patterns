import sys

def main():

    #makeQuery('query_dev.txt','my_filtered_path/dev_path.txt')
    makeQuery(sys.argv[1],sys.argv[2])

def makeQuery(fName,pathData):
    d = {'$0028': "'", '$0029': "'", '$00E2': 'a', '$0103': 'a', '$0163': 't', '$015F': 's', '$0219': 's', '$01CE': 'a',
         '$0162': 'T', '$00F3': 'o', '$015E': 'S', '$0027': "'", '$002C': ',', '$003A': ':', '$002E': '.', '$00E9': 'e',
         '$0026': '-', '$2153': '1/3'}

    base = '/Users/mengfei/Documents/learning Data/NLP/MA/data/'

    node_dict = read_dict(base+'node_names.tsv')
    #f_name = base+'query_'+weight+'.txt'
    #f_name = base + 'query_dev.txt'
    f_name = base + fName

    writer = open(f_name,'w')

    #with open (base+'filtered_paths_15/paths_'+weight+'_with_relation.tsv') as data:
    #with open(base + 'my_filtered_path/dev_path.txt') as data:
    with open(base + pathData) as data:

        rels = set([])
        for line in data:
            line = line.strip()
            eles = line.split('\t')
            if len(eles)==4:

                s = eles[0]
                t = eles[1]
                r = eles[2]
                rels.add(r)

                try:
                    s_node = node_dict[s]
                    t_node = node_dict[t]
                    for character in d:
                        if character in s_node:
                            s_node = s_node.replace(character, d[character])
                        if character in t_node:
                            t_node = t_node.replace(character, d[character])
                except:
                    KeyError
                    s_node = ""
                    t_node = ""

                path = eles[3]
                mRelMNodes = path.split('-')

                mNodes = []
                mRels = []

                for i in range(len(mRelMNodes)):
                    if i % 2 == 1:
                        mNode = mRelMNodes[i]
                        for character in d:
                            if character in mNode:
                                mNode.replace(character, d[character])
                        mNodes.append(mNode)
                    else:
                        mRel = mRelMNodes[i]
                        mRels.append(mRel)

                #print (mNodes)
                #print (mRels)

                m_node_names = []

                for mNode in mNodes:
                    try:
                        m_node_name = node_dict[mNode]
                    except KeyError:
                        m_node_name = ""
                    if m_node_name != "":
                        m_node_names.append(m_node_name)

                #print (m_node_names)

                print s_node
                print t_node
                print r

                if s_node != "" and t_node != "" and not '$' in s_node and not '$' in t_node:



                    writer.write(s_node+'\t'+t_node+'\t'+r+'\t')

                    for m_node in m_node_names:
                        if not '$' in m_node:
                            writer.write(m_node+'\t')

                    writer.write('##')

                    for mRel in mRels:
                        writer.write(mRel+'\t')

                    writer.write('\n')

def read_dict(f_path):
    node_dict = dict()
    with open(f_path) as data:
        for line in data:
            eles = line.strip().split("\t")
            if len(eles)==2:
                id,name = eles
                if not node_dict.has_key(id):
                    node_dict[id] = name
    return node_dict



if __name__=='__main__':
    main()