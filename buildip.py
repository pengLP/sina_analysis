# coding:utf-8
# version:python3.7
# author:Ivy
import random

import requests
import re

# 爬取代理网站上可以用的代理，建立代理池
class Proxies:
    def __init__(self):
        self.proxy_list = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/45.0.2454.101 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, sdch',
        }

    # 爬取西刺代理的国内高匿代理
    def get_proxy_nn(self):
        proxy_list = []
        res = requests.get("http://www.xicidaili.com/nn", headers=self.headers)
        ip_list = re.findall('<td>(\d+\.\d+\.\d+\.\d+)</td>', res.text)
        port_list = re.findall('<td>(\d+)</td>', res.text)
        for ip, port in zip(ip_list, port_list):
            proxy_list.append(ip + ":" + port)
        return proxy_list

    # 验证代理是否能用
    def verify_proxy(self, proxy_list):
        for proxy in proxy_list:
            proxies = {
                "http": proxy
            }
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=5).status_code == 200:
                    if proxy not in self.proxy_list:
                        self.proxy_list.append(proxy)
                    print('Success',proxy)
            except:
                print('Fail',proxy)

    # 保存到ippool这个List里
    def save_proxy(self):
        ippool=[]
        print("开始存入代理池...")
        # 把可用的代理添加到代理池中
        for proxy in self.proxy_list:
            proxies={"http":proxy}
            ippool.append(proxies)
        return ippool


# 使用上面的类建立代理池
def buildippool():
    p = Proxies()
    results = p.get_proxy_nn()
    print("爬取到的代理数量", len(results))
    print("开始验证：")
    p.verify_proxy(results)
    print("验证完毕：")
    print("可用代理数量：", len(p.proxy_list))
    ippool = p.save_proxy()
    return ippool


# 随机选择一个代理
def random_ip(ippool):
    num = random.randint(0,len(ippool)-1) #随机选一个0到10的整数
    return ippool[num]



if __name__ == '__main__':
    ippool = buildippool()
    print(ippool)
