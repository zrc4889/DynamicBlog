import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

input = ''
citys = {'福建省,福州市,连江县', '黑龙江省,哈尔滨市'}
# todo: 独立于代码，添加在线配置文件。

def weather(city):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    url = "https://www.msn.cn/zh-cn/weather/forecast/in-" + city
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    txt = soup.get_text()
    txt = txt.replace('\n', '')
    txt = txt.replace(' ', '')
    
    p = txt.find('看到了不同的天气?') # 有两种返回格式
    
    ans = ''
          
    if p != -1:
        t0 = txt.find('当前天气')
        # ans = ans + txt[t0 + 4: t0 + 9]
        # ans = ans + '\n'
        t1 = txt.find('?')
        t2 = txt.find('体')
        ans = ans + txt[t1 + 1 : t2]
        
    else:
        t0 = txt.find('当前天气')
        # ans = ans + txt[t0 + 4: t0 + 9]
        # ans = ans + '\n'
        t1 = txt.find('体')
        ans = ans + txt[t0 + 9 : t1]
        t2 = txt.find('°', t1)
        t3 = txt.find('空气质量')
        ans = ans + txt[t2 + 1 : t3]
    
    return ans

if __name__ == "__main__":
    
    for i in citys:
        input = input + i + ' ' + weather(i) + '\n'
        
    with open('weather.txt', 'w') as file: 
        file.write(input)
