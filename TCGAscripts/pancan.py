import string, os, sys,stat
import json

sys.path.insert(0,"../CGDataNew")

from CGDataLib import *
import TCGAUtil

def pancan_DNAmethyl (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_DNAMethyl_PANCAN_C18"
    shortTitle="PANCAN DNA methylation"
    longTitle="_PANCAN DNA methylation subtype k=18 (syn1807207)"
    maxSubtype=18
    dataProducer="https://www.synapse.org/#!Synapse:syn1807207"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)

def pancan_icluster (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_icluster_PANCAN_K25"
    shortTitle="PANCAN iCluster"
    longTitle="_PANCAN iCluster subtype k=25 (syn1729611)"
    maxSubtype=25
    dataProducer="https://www.synapse.org/#!Synapse:syn1729611"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)

def pancan_PARADIGM (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_PARADIGM_ConsensusClusters_PANCAN_K12"
    shortTitle="PANCAN PARADIGM"
    longTitle="_PANCAN PARADIGM subtype k=12 (syn1807620)"
    maxSubtype=12
    dataProducer="https://www.synapse.org/#!Synapse:syn1807620"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)

def pancan_UNC_RANseq (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_UNC_RNAseq_PANCAN_K16"
    shortTitle="PANCAN RNAseq"
    longTitle="_PANCAN RNAseq subtype k=16 (syn1715753)"
    maxSubtype=16
    dataProducer="https://www.synapse.org/#!Synapse:syn1715753"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)

def pancan_RPPA (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_RBN_PANCAN_K8"
    shortTitle="PANCAN RPPA"
    longTitle="_PANCAN RPPA subtype k=8 (syn1756922)"
    maxSubtype=8
    dataProducer="https://www.synapse.org/#!Synapse:syn1756922"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)

def  pancan_CNA_named (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_CNA_PANCAN_K8"
    shortTitle="PANCAN CNA"
    longTitle="_PANCAN copy number abnormality subtype named_k8_clusters (syn1712130)"
    maxSubtype = ["BRCA-LUAD+","COAD-READ","GBM","High","Iq","Kirc+","Quiet","Squamous"]
    dataProducer="https://www.synapse.org/#!Synapse:syn1712130"
    
    pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle, maxSubtype)


def individual_DNAmethyl (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name

    featureName="_PANCAN_DNAMethyl_"+ cancer 
    shortTitle= cancer+ " DNA methylation"
    longTitle="_"+cancer+" DNA methylation subtype (syn1701558)"
    dataProducer="https://www.synapse.org/#!Synapse:syn1701558"
    individual_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle)
    
def individual_miRNA (dir, outDir, cancer,log, REALRUN):
    #print status
    print cancer, sys._getframe().f_code.co_name
    #stupid BC OVCA type
    if cancer =="OVCA":
        cancer="OV"
    featureName="_PANCAN_mirna_"+ cancer 
    shortTitle= cancer+ " mirna"
    longTitle="_"+cancer+" microRNA subtype (syn1688309)"
    dataProducer="https://www.synapse.org/#!Synapse:syn1688309"
    individual_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle)


   
def individual_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle):
    filepath=dir

    if not os.path.exists(filepath) or not os.access(filepath,os.R_OK):
        return

    outfile = featureName
    fout= open(outDir+cancer+"/"+outfile,'w')

    #header
    fout.write("sample\t"+featureName+"\n")
        
    #data
    fin= open(filepath,'r')
    fin.readline()
    fout.write(fin.read())
    fout.close()
    fin.close()

    #data json
    J={}
    J['name']=featureName
    J["version"]= datetime.date.today().isoformat()
    J["type"]= "clinicalMatrix"
    J[":sampleMap"]="TCGA."+cancer+".sampleMap"
    J['dataProducer']=dataProducer
    J[":clinicalFeature"] = J['name']+ "_clinicalFeature"
    fout= open(outDir+cancer+"/"+outfile+".json",'w')
    fout.write( json.dumps( J, indent=-1 ) )
    fout.close()

    #clinical feature data
    fout= open(outDir+cancer+"/"+outfile+"_clinicalFeature",'w')
    fout.write(featureName+"\tshortTitle\t"+shortTitle+"\n")
    fout.write(featureName+"\tlongTitle\t"+longTitle+"\n")
    fout.write(featureName+"\tvalueType\tcategory\n")
    fout.close()
    
    #clinical feature json
    fout= open(outDir+cancer+"/"+outfile+"_clinicalFeature.json",'w')
    JC={}
    JC['name']= J[":clinicalFeature"]
    JC["version"]= datetime.date.today().isoformat()
    JC["type"]= "clinicalFeature"
    fout.write( json.dumps( JC, indent=-1 ) )
    fout.close()

    return


def pancan_subtype (dir, outDir, cancer,log, REALRUN, featureName,dataProducer, shortTitle, longTitle,maxSubtype):
    filepath=dir
    if not os.path.exists(filepath) or not os.access(filepath,os.R_OK):
        return

    for cancerDir in os.listdir(outDir):
        outfile = featureName
        fout= open(outDir+cancerDir+"/"+outfile,'w')

        #header
        fout.write("sample\t"+featureName+"\n")
        
        #data
        fin= open(filepath,'r')
        fin.readline()
        fout.write(fin.read())
        fout.close()
        fin.close()

        #data json
        J={}
        J['name']=featureName+"_"+cancerDir
        J["version"]= datetime.date.today().isoformat()
        J["type"]= "clinicalMatrix"
        J[":sampleMap"]="TCGA."+cancerDir+".sampleMap"
        J['dataProducer']=dataProducer
        J[":clinicalFeature"] = J['name']+ "_clinicalFeature"
        fout= open(outDir+cancerDir+"/"+outfile+".json",'w')
        fout.write( json.dumps( J, indent=-1 ) )
        fout.close()

        #clinical feature data
        fout= open(outDir+cancerDir+"/"+outfile+"_clinicalFeature",'w')
        fout.write(featureName+"\tshortTitle\t"+shortTitle+"\n")
        fout.write(featureName+"\tlongTitle\t"+longTitle+"\n")
        fout.write(featureName+"\tvalueType\tcategory\n")
        fout.write(featureName+"\tstateOrderRelax\ttrue\n")

        s=""
        if isinstance(maxSubtype, int):
            for i in range (1,maxSubtype):
                fout.write(featureName+"\tstate\t"+str(i)+"\n")
                s=s+"\""+str(i)+"\","
            fout.write(featureName+"\tstate\t"+str(maxSubtype)+"\n")
            s=s+"\""+str(maxSubtype)+"\""
            fout.write(featureName+"\tstateOrder\t"+s+"\n")

            fout.close()
        elif isinstance( maxSubtype, list):
            for i in range (0,len(maxSubtype)-1):
                fout.write(featureName+"\tstate\t"+maxSubtype[i]+"\n")
                s=s+"\""+maxSubtype[i]+"\","
            fout.write(featureName+"\tstate\t"+maxSubtype[-1]+"\n")
            s=s+"\""+maxSubtype[-1]+"\""
            fout.write(featureName+"\tstateOrder\t"+s+"\n")
            
        else:
            pass
        
        #clinical feature json
        fout= open(outDir+cancerDir+"/"+outfile+"_clinicalFeature.json",'w')
        JC={}
        JC['name']= J[":clinicalFeature"]
        JC["version"]= datetime.date.today().isoformat()
        JC["type"]= "clinicalFeature"
        fout.write( json.dumps( JC, indent=-1 ) )
        fout.close()

    return