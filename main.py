from ruamel.yaml import YAML
# from ruamel.yaml import YAML #居然有的是ruamel.yaml包，真是坑了
yaml=YAML(typ="safe", pure=True)

import requests

import os
import sys

import time
daystring=time.strftime("%m%d", time.localtime())
# 生成日期字符串，类似于1126


# gitee_chenx转换
url0='https://pub-api-1.bianyuan.xyz/sub?target=clash&url=https%3A%2F%2Fgitee.com%2Fchenx58%2Fclash%2Fraw%2Fmaster%2FV2R&insert=false&emoji=true&list=false&tfo=false&scv=false&fdn=false&sort=false&new_name=true'
# github freefq转换 
url1='https://pub-api-1.bianyuan.xyz/sub?target=clash&url=https://raw.githubusercontent.com/freefq/free/master/v2&insert=false&emoji=true&list=false&tfo=false&scv=false&fdn=false&sort=false&new_name=true'
# github_skywolf
url2='https://raw.githubusercontent.com/skywolf627/ProxiesActions/main/subscribe/vmess.txt'
# telegram_ssrsub 
url3='https://raw.githubusercontent.com/ssrsub/ssr/master/Clash.yml'
# github_clash-freenode 
url4='https://raw.githubusercontent.com/oslook/clash-freenode/main/clash.yaml'
# 代理池etproxypool需要全局模式
url5='https://etproxypool.ga/clash/proxies?c=HK,TW,SG,US&speed=30,100&type=vmess,ssr,trojan'
# free_proxy_ss需要全局模式
url6='https://cdn.jsdelivr.net/gh/learnhard-cn/free_proxy_ss@main/clash/clash.provider.yaml'

# github_pojieziyuan更改日期，
url7='https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/{}clash.yml'.format(daystring)
# 类似于1126clash.yml的格式，需要每日生成

## 生成yaml文件夹
yaml_folder='./yaml_folder'
if not os.path.exists(yaml_folder):
    os.makedirs(yaml_folder)

## 生成clash配置文件夹
dirs = './subscribe'
if not os.path.exists(dirs):
    os.makedirs(dirs)


## 访问所有的url链接，下载成yaml文件
def request_url_extract_proxies_lst():
    proxies_lst=[]
    urls=[url0,url1,url2,url3,url4,url5,url6,url7,]
    for i,url in enumerate(urls):
        print('requesting url:{}\n'.format(i))
        try:
            resp=requests.get(url).text
            print('success {} url\n'.format(i,url))
            try:
                proxies_yml=yaml.load(resp)
                proxies_yml_lst=proxies_yml.get('proxies',[])
                # dict.get(key, None),不要加上key和default，否则会报错，TypeError: get() takes no keyword arguments
                # 
                ## yaml列表节点前增加日期和url标识
                for j in proxies_yml_lst:
                    j['name']=daystring+'_'+str(i)+'_'+str(j['name'])
                ## 拼接节点列表
                proxies_lst=proxies_lst+proxies_yml_lst 
                
            except Exception as e:
                print('warning, reading url{} raise exception {}\n'.format(i,e))

        except Exception as e:
            print('failed url{} , exception {}\n'.format(i, e))

    print('拼接后节点列表长度{}'.format(len(proxies_lst)))
    return proxies_lst


## 读取yaml文件夹，进行节点列表拼接
def read_yaml_concat_proxies_list():
    yaml_files = [yaml_folder+'/'+file for file in os.listdir(yaml_folder) if file.endswith(".yml")]
    # print(yaml_files)
    ## 节点列表拼接
    proxies_lst=[]
    for file in yaml_files:
        # 加上额外的标识，表明该节点来自于哪个url
        urlnum=file[-5:-4]
        with open(file,encoding='utf-8') as f:
            try:
                proxies_yml=yaml.load(f)
                # print(proxies_yml.get('proxies',[]))
                proxies_yml_lst=proxies_yml.get('proxies',[])
                # dict.get(key, None),不要加上key和default，否则会报错，TypeError: get() takes no keyword arguments
                # 
                ## yaml列表节点前增加日期和url标识
                for i in proxies_yml_lst:
                    i['name']=daystring+'_'+str(urlnum)+'_'+str(i['name'])
                ## 拼接节点列表
                proxies_lst=proxies_lst+proxies_yml_lst 
                
            except Exception as e:
                print('warning, reading {} raise exception {}'.format(file,e))


    print('拼接后节点列表长度{}'.format(len(proxies_lst)))
    # print(proxies_lst)
    # ## 保存节点列表
    # with open('proxies_lst.yml', 'w+',encoding='utf-8') as fn:
    #     yaml.dump({'proxies':proxies_lst}, fn)
    return proxies_lst

# # 读取样例生成新的文件 
# def gen_clash(proxies_lst):
#     # 读取clash样例 
#     with open('clash_template.yml',encoding='utf-8') as f:
#         clash_template_yml=yaml.load(f)
#         clash_template_yml['proxies']=proxies_lst
#     # 生成新的clash文件
#     with open(dirs+'/gen_clash.yml', 'w+',encoding='utf-8') as fn:
#         yaml.dump(clash_template_yml, fn)
#         print('新的clash文件生成成功!!!!')


# 读取样例生成新的文件 
def gen_clash(proxies_lst):
    # # 读取节点列表 
    # with open('proxies_lst.yml',encoding='utf-8') as f:
    #     proxies_yml=yaml.load(f)
    #     # print(proxies_yml.get('proxies',[]))
    #     proxies_lst=proxies_yml.get('proxies',[])

    # 抽取节点列表名字
    proxies_lst_name=[i['name'] for i in proxies_lst]
    # print(proxies_lst_name)

    # 读取clash样例 
    with open('clash_template2.yml',encoding='utf-8') as f:
        clash_template_yml=yaml.load(f)
        # 修改proxies
        clash_template_yml['proxies']=proxies_lst
        # 修改proxy-groups
        # print(clash_template_yml['proxy-groups'])

        for group in (clash_template_yml['proxy-groups']):
            if (group['name']=='🔰 节点选择'):
                group['proxies']=['♻️ 自动选择', '🎯 全球直连']+proxies_lst_name
                # print(group)
            elif(group['name']=='♻️ 自动选择'):
                group['proxies']=proxies_lst_name

            elif(group['name']=='🎥 NETFLIX'):
                group['proxies']=['🔰 节点选择','♻️ 自动选择', '🎯 全球直连']+proxies_lst_name
            # ⛔️ 广告拦截 跳过
            # 🚫 运营劫持 跳过
            elif(group['name']=='🌍 国外媒体'):
                group['proxies']=['🔰 节点选择','♻️ 自动选择', '🎯 全球直连']+proxies_lst_name
            elif(group['name']=='🌏 国内媒体'):
                group['proxies']=['🎯 全球直连']+proxies_lst_name
            elif(group['name']=='Ⓜ️ 微软服务'):
                group['proxies']=['🎯 全球直连','🔰 节点选择']+proxies_lst_name
            elif(group['name']=='📲 电报信息'):
                group['proxies']=['🔰 节点选择','🎯 全球直连']+proxies_lst_name

            elif(group['name']=='🍎 苹果服务'):
                group['proxies']=['🔰 节点选择','🎯 全球直连','♻️ 自动选择']+proxies_lst_name
            # 🎯 全球直连 跳过
            # 🛑 全球拦截 跳过
            elif(group['name']=='🐟 漏网之鱼'):
                group['proxies']=['🔰 节点选择','🎯 全球直连','♻️ 自动选择']+proxies_lst_name

    # 生成新的clash文件
    with open('gen_clash.yml', 'w+',encoding='utf-8') as fn:
        yaml.dump(clash_template_yml, fn)
        print('新的clash文件生成成功!!!!')

if __name__ == '__main__':
    proxies_lst=request_url_extract_proxies_lst()
    # print(proxies_lst)
    # request_url_download_yaml()
    # proxies_lst=read_yaml_concat_proxies_list()
    gen_clash(proxies_lst)
    pass
