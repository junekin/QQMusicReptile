# -*- coding: utf-8 -*-
import requests
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36"
}

def songInfo(page, number, kw):
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?p={}&n={}&w={}&format=json'.format(page, number, kw)
    jsonData = requests.get(url, headers).content.decode()
    url_par_list = []
    singer_name_list = []
    song_name_list = []
    for i in range(number):
        url_par_list.append(json.loads(jsonData)["data"]["song"]["list"][i]["songmid"])
        song_name_list.append(json.loads(jsonData)["data"]["song"]["list"][i]["songname"])
        singer_name_list.append(json.loads(jsonData)["data"]["song"]["list"][i]["singer"][0]["name"])
    return url_par_list, singer_name_list, song_name_list


def getPurlList(url_par_list):
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%2200%22%2C%22songmid%22%3A%5B%22{}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%2200%22%7D%7D%7D'
    url_list = []
    for i in range(20):
        url_list.append(url.format(url_par_list[i]))
    purlList = []
    for i in range(20):
        html = requests.get(url_list[i], headers).content.decode()
        s = json.loads(html)
        purlList.append(str(s["req"]["data"]["freeflowsip"][0]) + str(s["req_0"]["data"]["midurlinfo"][0]["purl"]))
    return purlList


def download(purlList, singer_name_list, song_name_list):
    for i in range(20):
        if (not (os.path.exists('vip_music/' + singer_name_list[i]))):
            os.mkdir('vip_music/' + singer_name_list[i])
        if requests.get(purlList[i], headers).text == "":
            print("第{}首歌曲是付费歌曲".format(i + 1))
        else:
            print("正在下载第{}首歌曲...".format(i + 1))
            m4a = requests.get(purlList[i], headers).content
            path = 'vip_music/' + singer_name_list[i] + '/' + song_name_list[i] + '.m4a'
            with open(path, "wb+") as file:
                file.write(m4a)


def downloadSingle(purlList, singer_name_list, song_name_list, id):
    print("正在下载第{}首歌曲...".format(id))
    id = int(id) - 1
    if (not (os.path.exists('vip_music/' + singer_name_list[id]))):
        os.mkdir('vip_music/' + singer_name_list[id])
    if requests.get(purlList[id], headers).text == "":
        print("{}是付费歌曲".format(song_name_list[id]))
    else:
        m4a = requests.get(purlList[id], headers).content
        path = 'vip_music/' + singer_name_list[id] + '/' + song_name_list[id] + '.m4a'
        with open(path, "wb+") as file:
            file.write(m4a)


if __name__ == '__main__':
    kw = input("请输入你要搜索的歌曲关键字或者歌手名字：")
    url_par_list, singer_name_list, song_name_list = songInfo(1, 20, kw)
    print("\t{0:<4}{1:<16}\t{2:<8}".format("ID", "歌曲", "歌手"))
    for i in range(20):
        print("\t{0:<4}{1:<16}\t{2:<8}".format(i + 1, song_name_list[i], singer_name_list[i]))
    id = input("请输入你要下载的歌曲ID号(回车代表下载当前显示所有歌曲)：")
    if id == "":
        download(getPurlList(url_par_list), singer_name_list, song_name_list)
    else:
        downloadSingle(getPurlList(url_par_list), singer_name_list, song_name_list, id)
