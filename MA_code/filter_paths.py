import math
import multiprocessing as mp
import sys
import os

def main():
    threshold = 0.1
    for i in range(15):
        print("Threshold {}".format(threshold))
        bw = open("/mnt/proj/zhou/MA/program/filtered_paths_15/paths_{}_with_relation.tsv".format(
            threshold), 'w')
        rels = []
        with open("/home/mitarb/public/kotnis/pra/data/freebase_relations.txt") as data:
            for line in data:
                line = line.rstrip().replace("\"","").replace(",","")
                rels.append(line)

        manager = mp.Manager()
        q = manager.Queue()
        pool = mp.Pool(10)
        #pool.apply_async(writer,(q,bw))

        jobs = []
        for rel in rels:
            job = pool.apply_async(worker,(rel,threshold))
            jobs.append(job)

        for job in jobs:
            print("Writing relation...")
            bw.write(job.get()+"\n")

        q.put('kill')
        pool.close()
        bw.close()
        threshold += 0.1

def worker(rel_name,threshold):

    base_dir = "/home/mitarb/public/kotnis/chains_reasoning_data/release_with_entities_akbc/"
    write_buffer = []
    useful_paths = get_useful_paths(rel_name,threshold)
    dir = base_dir + rel_name.replace("/","_")
    for file in os.listdir(dir):
        if "negative" in file:
            continue
        with open(os.path.join(dir,file)) as data:
            for line in data:
                parts = line.strip().split("\t")
                if len(parts)>3:
                    continue
                paths = get_filtered_paths(rel_name,parts,useful_paths)
                write_buffer.extend(paths)

    return "\n".join(write_buffer)


def writer(q,bw):

    while 1:
        msg = q.get()
        if msg=='kill':
            print("Done.")
            break
        bw.write(str(msg)+"\n")
        print("Writing...")
        bw.flush()




def get_filtered_paths(rel,parts,useful_paths):
    write_buffer = []
    for p in parts[2].split("###"):
        p_type = p.split("-")
        p_type ="-".join(p_type[::2])
        if p_type in useful_paths:
            write_buffer.append("{}\t{}\t{}\t{}".format(parts[0],parts[1],rel,p))
    return write_buffer



def get_useful_paths(rel_name,threshold):
    pra_base = "/home/mitarb/kotnis/pra/data/results/sfe_bfs_pra_freebase_all/"
    paths = set()
    with open(pra_base + os.path.join(rel_name, "weights.tsv")) as data:
        threshold = get_threshold(data,threshold)
        for line in data:
            parts = line.strip().split()
            # Only positively correlated paths
            if len(parts) != 2 or float(parts[-1]) > threshold:
                paths.add(parts[0][1:-1])
    return paths

def get_threshold(file,threshold):
    for line in file:
        parts = line.strip().split()
        threshold = float(parts[-1]) * threshold
        return threshold

def get_path_stats(rel_name,threshold):
    pra_base = "/home/mitarb/kotnis/pra/data/results/sfe_bfs_pra_freebase_all/"
    paths = [set(),set(),set(),set(),set()]
    with open(pra_base+os.path.join(rel_name,"weights.tsv")) as data:
        for line in data:
            parts = line.strip().split()
            # Only positively correlated paths
            if len(parts)!=2 or float(parts[-1]) > threshold:

                parts = parts[0][1:-1]
                path = parts.split("-")
                if len(path)==1 and 'NULL' not in parts:
                    paths[0].add(parts)
                elif len(path) == 2:
                    paths[1].add(parts)
                elif len(path) == 3:
                    paths[2].add(parts)
                elif len(path) == 4:
                    paths[3].add(parts)
                else:
                    paths[4].add(parts)
                            #return paths
    return [len(x) for x in paths]
if __name__=='__main__':
    main()