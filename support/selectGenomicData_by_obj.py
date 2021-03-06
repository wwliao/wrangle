import string, sys, os
import json
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))+"/../xena/")
import xenaAPI

def listing (mfile):
    fin = open(mfile,'r')
    dic= {}
    for line in fin.readlines():
        data = string.strip(string.split(line,'\t')[0])
        if data not in dic:
            dic[data]=0
        else:
            print data
    fin.close()
    return dic

def keepProbes (obj, outputFile, keep_dic = None):
    fout = open(outputFile,'w')
    n = int(100000/len(obj["samples"]))
    if n < 100:
        n = 100
    if n > 500:
        n = 500
    print n

    fout.write("id\t" + string.join(obj['samples'], '\t') + '\n')

    if keep_dic:
        IDs = keep_dic.keys()
    else:
        IDs = xenaAPI.dataset_fields (obj['hub'], obj['dataset'])

    for k in range (0, len(IDs), n):
        ids = IDs[k:k+n]
        if obj['mode'] == "gene":
            values_list = xenaAPI.Genes_values(obj['hub'], obj['dataset'], obj['samples'], ids)
        elif obj['mode'] == "probe":
            values_list = xenaAPI.Probes_values(obj['hub'], obj['dataset'], obj['samples'], ids)

        for i in range(0, len(ids)):
            id = ids[i]
            if obj['mode'] == "gene":
                values = values_list[i]["scores"][0]
            elif obj['mode'] == "probe":
                values = values_list[i]
            fout.write(id + '\t'+ string.join(map(lambda x : str(x), values), '\t') +'\n')

    fout.close()

if len(sys.argv[:]) < 3 or len(sys.argv[:]) > 5 :
    print "python selectGenomicData_by_obj.py dataset_obj_file(json) outputMatrix optional_ID_list(first_column_id)"
    sys.exit()

inputfile = sys.argv[1]
fin = open(inputfile,'r')
obj = json.load(fin)
fin.close()

if len(sys.argv[:]) ==4:
    listfile = sys.argv[3]
    keep_dic  = listing (listfile)
else:
    keep_dic = None
    if obj['mode'] == 'gene':
        print "can't do gene selection mode without telling me what genes to select (use optional_ID_list to specify genes)"
        sys.exit()

outputfile = sys.argv[2]

keepProbes (obj, outputfile, keep_dic)
