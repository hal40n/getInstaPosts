import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_basic_info():
    basic_info = dict()

    basic_info['instagram_user_name'] = os.getenv("INSTAGRAM_USER_NAME")
    basic_info['instagram_business_account_id'] = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    basic_info['instagram_access_token'] = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    basic_info['version'] = 'v20.0'

    basic_info['graph_domain'] = 'https://graph.facebook.com/'
    basic_info['endpoint'] = basic_info['graph_domain'] + basic_info['version'] + '/'

    return basic_info

def callInstagramGraphApi(url, params):
    req = requests.get(url, params)
    res = dict()
    res['url'] = url
    res['endpoint_params'] = params
    res["endpoint_params_pretty"] = json.dumps(params, indent=4)
    res["json_data"]              = json.loads(req.content)
    res["json_data_pretty"]       = json.dumps(res["json_data"], indent=4)

    return res

def getInstagramPosts(params, paging_url=''):
    params_endpoint = dict()
    params_endpoint['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username'
    params_endpoint['access_token'] = params['instagram_access_token']

    if paging_url=='':
        url = params['endpoint'] + params['instagram_business_account_id'] + '/media'
    else :
        url = paging_url

    return callInstagramGraphApi(url, params_endpoint)

def showInstagramPosts(params):
    response = getInstagramPosts(params)
    print ("\n----------"+str(response['json_data']['data'][0]["username"])+"の投稿内容 ----------\n")
    for i, post in enumerate(response['json_data']['data']) :
        print ("\n----------投稿内容("+str(i+1)+")----------\n")
        print ("投稿日: " + post['timestamp'])
        print ("投稿メディアID: "+post['id'])
        print ("メディア種別: " + post['media_type'])
        print ("投稿リンク: " + post['permalink'])
        if 'caption' in post:
            print("\n投稿文: " + post['caption'])
        else:
            print("\n投稿文: ")

    try:
        response = getInstagramPosts(params, response['json_data']['paging']['next'])
        print ("\n----------"+str(response['json_data']['data'][0]["username"])+"の投稿内容 ----------\n")
        for i, post in enumerate(response['json_data']['data']) :
            print ("\n----------投稿内容("+str(i+1)+")----------\n")
            print ("投稿日: " + post['timestamp'])
            print ("投稿メディアID: "+post['id'])
            print ("メディア種別: " + post['media_type'])
            print ("投稿リンク: " + post['permalink'])
            if 'caption' in post:
                print("\n投稿文: " + post['caption'])
            else:
                print("\n投稿文: ")
    except:
        pass