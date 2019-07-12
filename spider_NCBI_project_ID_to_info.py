# -*- coding: utf-8 -*-
from selenium import webdriver #使用selenium来爬ncbi，因为ncbi安全性较高
from selenium.webdriver.support.select import Select
import requests
import sys
import time
from scrapy import Selector

NCBI_URL = 'https://www.ncbi.nlm.nih.gov/Traces/study/?acc={}&go=go' # {}代表ID
headers = {}

def try_many_time(times):
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

def param_project(project_str):
    project_dict = {}
    lines =  project_str.split('\n')
    lines.pop(0)
    index = 0
    for i in range(int(len(lines)/2)):
        tkey = lines[index]
        tvalue = lines[index+1]
        project_dict[tkey] = tvalue
        headers[tkey] = ''
        index += 2
    return project_dict

# 打开浏览器，同时打开首页
# url = 'https://www.taobao.com/'
#url = 'https://www.ebi.ac.uk/ebisearch/overview.ebi/about'
#projecturl = 'https://www.ncbi.nlm.nih.gov/Traces/study/?acc={}&go=go' #ERP002469
@try_many_time(3) #修饰器，尝试多次
def get_project(acc): #传入ID
    driver = webdriver.Chrome(executable_path="D:\python_program\chromedriver.exe") #调用谷歌浏览器
    projecturl = NCBI_URL.format(acc) #ERP002469 #获取对应ID的url
    driver.get(projecturl)
    try: #搜索有结果
        div = driver.find_element_by_css_selector('div#ph-right-top') #元素抽取
        time.sleep(7) #网页需要时间渲染才开始收集数据
        project_info = div.text #这就是想要的信息了
        dd = param_project(project_info)
       # print(dd)
    except Exception as e: #若搜索无结果
        print("Project no find!")
        #print(str(e))
        dd = {}
    driver.close()
    return dd

if __name__ == '__main__':
    out = open("depli_NCBI_out.txt","w")
    projectID = open("projectID.txt","r") 
    projects = []
    for line in projectID.readlines():
        pdict = get_project(line)
        pdict['ProjectID'] = line.strip()
        projects.append(pdict)

    out.write("ProjectID\t%s\n" % "\t".join(headers.keys()))
    for p in projects: 
        line = p["ProjectID"]
        for k in headers.keys():
            v = ''
            if k in p.keys():
                v = p[k]
            line = "%s\t%s" %(line, v)
        out.write("%s\n" % line)

#下面是selenium带的一些
# page = driver.page_source
# selector = Selector(text=page)
# div = selector.css('#id-common-fields')
# spans = div.css('span').getall()
# for span in spans:
#     print(span)
# h2 = driver.find_element_by_css_selector('div#ph-right-top')
# time.sleep(1)
# sp = h2.find_element_by_css_selector('div.expand-body')
# h1 = h2.get_attribute('textContent')
# yes_or_no = driver.find_element_by_css_selector('div#ph-right-top').is_displayed() #判断值是否被隐藏
#print(yes_or_no) #返回False表明该值被隐藏

#aa = driver.find_element_by_class_name('expand-body')
#a0 = h2.get_attribute('innerHTML')
#a00 = driver.execute_script("return arguments[0].innerHTML",h2)
#a1 = h2.get_attribute('textContent')
#a2 = driver.execute_script("return arguments[0].textContent",h2)
#print(a1)
#aa = .get_attribute('textContent')

#info = h2.text
#def get_pro_info(ID):
#   url = projecturl.format(ID)
    # driver = webdriver.Chrome()
#    driver.get(url)
 #   response = driver.find_element_by_css_selector('div#ph-right-top')
 #   info = json.loads(response.text)
 #   return info

#projectID = open("aa.txt","r")
#for line in projectID.readlines():
#    bioproinfo = get_pro_info(line)

# s = driver.find_element_by_css_selector('div.tbh-nav.J_Module.tb-pass.tb-bg')
# h2 = s.find_element_by_css_selector('h2')
# a = driver.find_element_by_id('username')
# 通过js改密码登录
# js = "document.getElementById('zhanghaoLogin').style.display='block'"
# js2 = "document.getElementById('mobileLogin').style.display='none'"
# driver.execute_script(js)
# driver.execute_script(js2)
#
# # 通过id定位搜索框，同时输入登录用户名密码
# driver.find_element_by_id('username').clear()
# # xxx是账号和密码
# driver.find_element_by_id('username').send_keys('xxx')
# driver.find_element_by_id('password').clear()
# driver.find_element_by_id('password').send_keys('xxx')
# driver.find_element_by_id('login_btn').click()
# time.sleep(3)
#
# #进入首页搜索
# driver.find_element_by_id('queryInput').send_keys('西藏家家乐购信息技术股份有限公司')
# driver.find_element_by_class_name('query-button').click()
# print("cccccccccccc")
# time.sleep(2)
# #点击企业名
# #driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[3]/div[1]/div[2]/div/span[2]/div[1]/span[1]').click()
# driver.find_element_by_css_selector(' body > div.jc-header-and-main2 > div.monitor-content-container > div > div.main-content-right-container > div.monitor-right-section > div:nth-child(2) > div > span:nth-child(2) > div.list-title > span.company-title.pointer.ng-binding').click()
# #company-title pointer ng-binding
# #company-title.pointer.ng-binding
# print("aaaaaaaaaaaaa")
# time.sleep(3)
# print("bbbbbbbbbbbbb")
# cookies = driver.get_cookies()
# print(cookies)
# handle = driver.current_window_handle
# handles = driver.window_handles
# for i in handles:
#    # driver.switch_to.window(i)
#    # break
#    print(i)
#    print(handle)
#    #if i == handle:
#
#    driver.switch_to.window(i)
#
#
# driver.find_element_by_id('opinionMsg').click()
# time.sleep(3)
# driver.find_element_by_css_selector('div#opinionMsgNewsdiv div.rel.time-range').click()
# time.sleep(2)
# driver.find_element_by_css_selector('div#opinionMsgNewsdiv ul.dropdown-menu.change-list-all li:nth-of-type(1) a').click()
