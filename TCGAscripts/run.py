import sys,os,string, glob

print "python run.py configfile logfile"
print

#analysis run version firehose website: http://gdac.broadinstitute.org/runs/analyses__latest/reports/ 
def FHANAdate():
    l=string.strip(os.popen("/inside/home/jzhu/scripts/firehose_get -r |grep analyses |tail -n 1").read())
    return l[10:]
    #return "2015_04_02"

def FHANAdateVersion():
    print FHANAdate()
    return string.replace(FHANAdate(),"_","")
    
fin = open(sys.argv[1],'r')
flog = open(sys.argv[2],'w')

kvArgs={}
for line in fin.readlines():
    if line[0]=="$":
        data =string.strip(line)
        if string.find(data,"=")!=-1:
            k,v = string.split(data,"=")
            k = string.strip(k)
            v = string.strip(v)
        else:
            if data=="$FIREHOSEDATE_ana":
                k=data
                v=FHANAdate()
            if data=="$FIREHOSEDATE_ana_version":
                k=data
                v=FHANAdateVersion()
        kvArgs[k]=v
fin.close()


fin = open(sys.argv[1],'r')
for line in fin.readlines():
    if string.strip(line)=="":
        continue
    if line[0]=="#":
        continue
    data= string.split(line[:-1],"\t")

    if len(data) ==6:
        run = int(data[0])
        REALRUN = int(data[1])
        module =data[2]
        function =data[3]
        inDir = data[4]
        outDir = data[5]

        if not run:
            continue

        for k in kvArgs:
            v= kvArgs[k]
            if string.find(inDir,k)!=-1:
                inDir= string.replace(inDir, k, v)
            if string.find(outDir,k)!=-1:
                outDir= string.replace(outDir, k, v)
            
        pattern= string.split(inDir,"*")
        #PAAD=0

        for dir in glob.glob(inDir):
            cancer =dir
            for p in pattern:
                cancer =string.replace(cancer,p,"")
            cancer=string.upper(cancer)
            cancer = string.replace(cancer,"TCGA.","")
            cancer = string.replace(cancer,".SAMPLEMAP","")

            #if cancer not in ["OV"]:
            #    continue

            """
            if cancer in ["PAAD"]:
                PAAD=1
            if not PAAD:
                continue
            """
            if run:
                print module, function
                m = __import__(module)
                func = getattr(m,function)
                apply(func,[dir, outDir,cancer,flog, REALRUN])
fin.close()
flog.close()


