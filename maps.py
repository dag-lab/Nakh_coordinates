import re
import urllib.request
import html

def rpage(url):
    """
    this function provides an access to the HTML code of a page
    its only argument - the page's URL
    """
    req = urllib.request.Request(url, headers={'User-Agent':'Safari/537.36'})
    page = urllib.request.urlopen(req).read().decode('utf-8')
    page = html.unescape(page)
    return page


def get_crdnts_ch(url):
    """
    this function returns as an output an array, each element of which
    contains a string with the following information:
    'LANGUAGE; LOCALITY; LATITUDE; LONGITUDE'
    function argument is an URL of Wikipedia page with
    a list of Chechen settlements
    """
    st = []
    crdnts = []
    p = rpage(url)
    gorodasela = re.findall('<td align=\"left\"><a href=\"([^"]*)\" title="[^"]*\">([^<]*)</a></td>\n<td align="left">(?:город|село)', p, flags = re.DOTALL)
    #finds URLs of all Checen settlements
    for i in gorodasela:
        page = rpage('https://ru.wikipedia.org'+i[0])
        try:
            geohack = 'https:' + re.findall('href=\"(//tools.wmflabs.org/geohack/[^"]+)\"', page, flags=re.DOTALL)[0]
            gh_page = rpage(geohack)
            geohack2 = re.findall('<span class="geo">[^1-90]+([1-90\.]+)<[^1-90]+([1-90\.]+)</span>', gh_page, flags=re.DOTALL)[0]
            if i[1] in st:
                continue
            st.append(i[1]) 
            ll = 'Чеченский;' + i[1] + ';' + ';'.join(geohack2)
            crdnts.append(ll)
        except:
            print(i[1])
    return crdnts

def get_crdnts_i(url):
    """
    this function returns as an output an array, each element of which
    contains a string with the following information:
    'LANGUAGE; LOCALITY; LATITUDE; LONGITUDE'
    function argument is an URL of Wikipedia page with
    a list of Ingush settlements
    """
    st = []
    crdnts = []
    p = rpage(url)
    gorodasela = re.findall('<li>(?:город|село|станица) <a href=\"([^"]+)\"[^>]*>([^<]+)<', p, flags=re.DOTALL)
    #finds URLs of all Ingush settlements
    for i in gorodasela:
        page = rpage('https://ru.wikipedia.org'+i[0])
        try:
            #finds GeoHack link _if such exists_
            geohack = 'https:' + re.findall('href=\"(//tools.wmflabs.org/geohack/[^"]+)\"', page, flags=re.DOTALL)[0]
            gh_page = rpage(geohack)
            #finds coordinates on a GeoHack page
            geohack2 = re.findall('<span class="geo">[^1-90]+([1-90\.]+)<[^1-90]+([1-90\.]+)</span>', gh_page, flags=re.DOTALL)[0]
            if i[1] in st:
                continue
            st.append(i[1]) 
            ll = 'Ингушский;' + i[1] + ';' + ';'.join(geohack2)
            crdnts.append(ll)
        except:
            print(i[1])
    return crdnts


c = get_crdnts_i('https://ru.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%98%D0%BD%D0%B3%D1%83%D1%88%D0%B5%D1%82%D0%B8%D0%B8')
c += get_crdnts_ch('https://ru.wikipedia.org/wiki/%D0%9D%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%A7%D0%B5%D1%87%D0%BD%D0%B8')    
#writes all the coordinates in a file in CSV-format
f= open('koordinaty.txt', 'w', encoding='utf-8')
f.write('\n'.join(c))
f.close
