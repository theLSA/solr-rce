solr-rce：apache solr RCE 漏洞利用工具
==

# 概述

20191031 网上爆出apache solr velocity模板注入的rce漏洞，该漏洞由国外安全研究员s00py公开，当solr默认插件VelocityResponseWrite中params.resource.loader.enabled参数值为true（默认false），再通过精心构造的get请求即可RCE。
<br/>
//如果存在solr未授权访问，可post直接修改params.resource.loader.enabled参数值为true


# 影响范围

apache solr 5.x - 8.2.0 rce (with config api)

# 快速开始

pip install requests

直接获取cmdshell,注意最后不要有斜杠！
<br/>
python solr-rce.py -u "http://1.2.3.4"

![](https://github.com/theLSA/solr-rce/raw/master/solrce00.png)

# 反馈

[issus](https://github.com/theLSA/solr-rce/issues)
<br/>
gmail：lsasguge196@gmail.com
<br/>
qq：2894400469@qq.com



