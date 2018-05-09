#!/usr/bin/python3
import uuid
from urllib import parse,request
def get_mac_address(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

username=input("UserName:")
password=input("Password:")
mac=input("mac:")
print(get_mac_address())

textmod={'userName':username,'password':password,'mac':mac}
textmod = parse.urlencode(textmod)
print(textmod)
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
url='http://10.0.2.15:8080/regMac'
req = request.Request(url='%s%s%s' % (url,'?',textmod),headers=header_dict)
res = request.urlopen(req)
res = res.read()
print(res)
print(res.decode(encoding='utf-8'))
