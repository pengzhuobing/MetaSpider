#爬EMBL的数据，通过projectID得到项目信息

from bs4 import BeautifulSoup
import requests
import sys
import json
import time

PROJECT_URL = "https://www.ebi.ac.uk/ebisearch/ws/rest/metagenomics_projects?format=json&size=1&start=0&fields=ENA_PROJECT%2CMETAGENOMICS_SAMPLES%2Cbiome_name%2Cname&query={}&facets="
#搜索的URL,将ID号替换成{}


def try_many_time(times): #重复多次爬取动作
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print("Error: %s" %str(e))
                    time.sleep(1)
            return False
        return wrapper
    return decorator

@try_many_time(3) #修饰器，重复3此爬取动作，该修饰器需要放在修饰的动作上面

def get_pro_info(ID): #爬呀爬
    purl = PROJECT_URL.format(ID) #形成ID对应的url
    response = requests.request("GET", purl) #爬取动作
    response.encoding = 'utf-8'
    ps = json.loads(response.text) #解析json
    entries = ps["entries"] #取得想要信息
    # if ps["hitCount"] == 0:
    #     return ID
    return entries

#if len(sys.argv) < 2:
#    print("python aa.py projectID.txt")
#    sys.exit(0)

#p = sys.argv[1]
#projectID = open(p)

if __name__ ==  '__main__':
    pro_info = []
    fields = ['ENA_PROJECT', 'name','biome_name','METAGENOMICS_SAMPLES']
    projectID = open("projectID.txt","r")
    out = open("depli_EMDL_out.txt","w") #收集的项目ID
    out.write("Project\t" + "\t".join(fields) + "\tSAMPLES_NUM\n")  #将爬取的信息输出到文件中
    for line in projectID.readlines():
        proinfo = get_pro_info(line)
        new_line = line.strip()
        if len(proinfo) == 0:
            out.write("%s\n" % new_line)
            continue
        for i in fields:
            new_line = "%s\t%s" %(new_line, ",".join(proinfo[0]["fields"][i]))
        out.write("%s\t%s\n" %(new_line,len(proinfo[0]["fields"]["METAGENOMICS_SAMPLES"])))
