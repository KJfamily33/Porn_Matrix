from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from random import randint, choice
import youtube_dl, json

#--------------------------------------------------

def simple_get(url):
    cookies = {'SRCHHPGUSR':'HV=1580011455&ADLT=OFF'}

    try:
        with closing(post(url, cookies=cookies)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
                
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    print(e)

#--------------------------------------------------

def search_to_vid_url(search, results=None, length=None, hd=None):
    return bing_url(search, results, length, hd)

def bing_url(search, results=1, length=None, hd=None):
    # max of count 105, will need to work around that
    supported_sites = ["pornhub.com", "xvideos.com", "cliphunter.com"]
    site_param = ' AND ('
    for site in supported_sites:
        site_param += 'site:www.' + site + ' OR '
    site_param = site_param[:-4] + ')'

    page = '&first=0&count=' + str(results)

    if length and int(length) >= 20:
        length = '+filterui:duration-long'
    else:
        length = ''

    search = 'https://www.bing.com/videos/asyncv2?q=' + search.lower() + ' site:www.' + choice(supported_sites) + '&async=content' + page + '&qft=' + length
    random_n = randint(1000,9999)
    print(random_n, " SEARCH: ", search)

    raw_html = simple_get(search)
    html = BeautifulSoup(raw_html, 'html.parser')

    # extract video results from search page
    narrowed_html = html.find_all(class_='vrhdata')
    link_list = []
    for n_html in narrowed_html:
        link_list.append(json.loads(n_html["vrhm"])["pgurl"])

    final_list = []
    for site in supported_sites:
        final_list += [l for l in link_list if site in l]
    link_list = final_list
    
    print(random_n, " RESULTS: ", len(link_list))

    # get direct link for one of the video results
    while True:
        if link_list:
            v_link = choice(link_list)
            print(random_n, " TRYING: ", v_link)
            mp4_url = yt_dl_on_link(v_link)
            if mp4_url:
                break
            link_list.remove(v_link)
        else:
            mp4_url = ''
            break

    print(random_n, " MP4 URL: ", mp4_url)
    return mp4_url
    

def yt_dl_on_link(vid_link):
    try:
        return ydl.extract_info(vid_link, download=False).get("url", None)
    except:
        return 0


ydl_opts = {'format':'([protocol=https]/[protocol=http])[ext=mp4]','quiet':True,'no_warnings':True,'noplaylist':True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

if __name__ == "__main__":
    import time
    
    start = time.time()
    url = bing_url("emma mae")
    print('It took {0:0.2f} seconds'.format(time.time() - start))