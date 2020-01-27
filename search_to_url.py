from requests import post
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from random import randint, choice
import youtube_dl, json, time

# Blacklisted sites, these sites "work" with youtube_dl, but don't work for us
blacklist = ["spankbang.com", "youtube.com", "xhamster.com"]

# initialize ydl
ydl_opts = {'format':'([protocol=https]/[protocol=http])[ext=mp4]','quiet':True,'no_warnings':True,'noplaylist':True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

# Need this cookie to set adult content on bing
cookies = {'SRCHHPGUSR':'ADLT=OFF&CW=1117&CH=1771&DPR=2&UTC=-360&HV=' + str(int(time.time()))}

                              # 105 is max results, I could work around that by multiple gets,
                              # but I don't think it's necessary
def get_direct_link(search, results=105, length=0):
    start = time.time()
    
    # Create blacklist site query with form
    # "search terms AND NOT (site:ph.com OR site:xvids.com)"
    blacklist_param = ' AND NOT ('
    for site in blacklist:
        blacklist_param += 'site:' + site + ' OR '
    blacklist_param = blacklist_param[:-4] + ')'

    # Craft search string
    page_param = '&first=0&count=' + str(results)
    if length and int(length) >= 20:
        length_param = '+filterui:duration-long'
    else:
        length_param = ''
    search_url = 'https://www.bing.com/videos/asyncv2?q="' + search.lower() + '"' + blacklist_param + '&async=content' + page_param + '&qft=' + length_param
    random_n = randint(1000,9999)
    print(random_n, " SEARCH URL: ", search_url)

    # get request for search page, create parser
    raw_html = simple_get(search_url)
    html = BeautifulSoup(raw_html, 'html.parser')

    # Extract links to video pages from search results
    narrowed_html = html.find_all(class_='vrhdata')
    print(len(narrowed_html))
    link_list = []
    for n_html in narrowed_html:
        link_list.append(json.loads(n_html["vrhm"])["pgurl"])
    print(random_n, " RESULTS: ", len(link_list))

    # Use youtube_dl to get a direct mp4 from one of the video page links
    while True:
        if link_list:
            v_link = choice(link_list)
            print(random_n, " TRYING: ", v_link)
            try:
                mp4_url = ydl.extract_info(v_link, download=False).get("url", None)
            except:
                mp4_url = 0
            if mp4_url:
                break
            link_list.remove(v_link)
        else:
            mp4_url = ''
            break

    print(random_n, " MP4 URL: ", mp4_url, ' {0:0.2f} seconds'.format(time.time() - start))
    return mp4_url

# Boilerplate requests stuff
def simple_get(url):
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

# test omegalul
if __name__ == "__main__":
    url = get_direct_link("emma mae")