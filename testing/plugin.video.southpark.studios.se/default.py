import urllib,urllib2,re,sys,os
import xbmcplugin,xbmcgui
import demjson


pluginhandle = int(sys.argv[1])
fanart = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),'fanart.jpg'))
xbmcplugin.setPluginFanart(pluginhandle, fanart, color2='0xFFFF3300')
TVShowTitle='South Park'



def getURL( url ):
    try:
        print 'Southpark Studios --> getURL :: url = '+url
        req = urllib2.Request(url)
#        req.addheaders = [('Referer', 'http://www.southparkstudios.com/episodes/'),
        req.addheaders = [('Referer', 'http://www.southparkstudios.se/episodes/'),
			  ('X-Forwarded-For', '194.6.243.255')
                          ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
    except urllib2.URLError, e:
        error = 'Error code: '+ str(e.code)
        xbmcgui.Dialog().ok(error,error)
        print 'Error code: ', e.code
        return False
    else:
            return link

def seasons():
    xbmcplugin.setContent(pluginhandle, 'seasons')
    #addRandom('Random Episode','http://www.southparkstudios.com/episodes/random.php',3)
    for sn in range(1,16):
        sn = str(sn)
#        name = 'Season '+sn
        name = 'Staffel '+sn
        url = sn
        mode = 1
        iconimage = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),'resources','images','season'+sn+'.jpg'))
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,
                                                "Season":int(sn),
                                                "TVShowTitle":TVShowTitle
                                                })
        liz.setProperty('fanart_image',fanart)
        xbmcplugin.addDirectoryItem(handle=pluginhandle,url=u,listitem=liz,isFolder=True)
    xbmcplugin.endOfDirectory(pluginhandle)

def addRandom(name,url,mode):
    iconimage = xbmc.translatePath(os.path.join(os.getcwd().replace(';', ''),'icon.png'))
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    liz.setProperty('IsPlayable', 'true')
    liz.setProperty('fanart_image',fanart)
    ok=xbmcplugin.addDirectoryItem(handle=pluginhandle,url=u,listitem=liz)
    return ok

def randomEpisode(url):
    data = getURL(url)
    randomEpisodeid=re.compile('swfobject.embedSWF\("http://media.mtvnservices.com/mgid:cms:content:southparkstudios.com:(.+?)"').findall(data)[0]
    name = re.compile('<title>South Park Episode Player - South Park: (.+?)</title>').findall(data)[0]
    name = name.replace("&#039;","'")
    thumbnail = re.compile('<link rel="image_src" href="(.+?)?width=90&quality=100"').findall(data)[0]
    playVideo(randomEpisodeid,name,thumbnail)

def episodes(season):
    xbmcplugin.setContent(pluginhandle, 'episodes')
    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_EPISODE)
    #url = 'http://www.southparkstudios.com/includes/utils/proxy_feed.php?html=season_json.jhtml%3fseason=' + season'
#    url = 'http://www.southparkstudios.com/feeds/full-episode/carousel/'+season+'/342853'
    url = 'http://www.southparkstudios.se/ajax/seasonepisode/'+season
    json = getURL(url)
    episodes = demjson.decode(json)['season']['episode']
    for episode in episodes:
#        title = episode['title']
        title = episode['title'].encode('latin-1', 'ignore')
#        description = episode['description'].encode('ascii', 'ignore')
        description = episode['description'].encode('latin-1', 'ignore')
        thumbnail = episode['thumbnail'].replace('width=55','')
        episodeid = episode['id']
        senumber = episode['episodenumber']
        date = episode['airdate'].replace('.','-')
        seasonnumber = senumber[:-2]
        episodenumber = senumber[len(seasonnumber):]
        try:
            season = int(seasonnumber)
            episode = int(episodenumber)
        except:
            season = 0
            episode = 0
        mode = 2
        u=sys.argv[0]+"?url="+urllib.quote_plus(episodeid)+"&mode="+str(mode)+"&name="+urllib.quote_plus(title)
        u += "&season="+urllib.quote_plus(str(seasonnumber))
        u += "&episode="+urllib.quote_plus(str(episodenumber))
        u += "&premiered="+urllib.quote_plus(date)
        u += "&plot="+urllib.quote_plus(description)
        u += "&thumbnail="+urllib.quote_plus(thumbnail)
        ok=True
        liz=xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
        liz.setInfo( type="Video", infoLabels={ "Title": title,
                                                "Season":season,
                                                "Episode":episode,
                                                "premiered":date,
                                                "Plot":description,
                                                "TVShowTitle":TVShowTitle
                                                })
        liz.setProperty('IsPlayable', 'true')
        liz.setProperty('fanart_image',fanart)
        ok=xbmcplugin.addDirectoryItem(handle=pluginhandle,url=u,listitem=liz)
    xbmcplugin.endOfDirectory(pluginhandle)

def playVideo(episodeid,name,thumbnail):
    if xbmcplugin.getSetting(pluginhandle,"bitrate") == '0':
            lbitrate = None
    elif xbmcplugin.getSetting(pluginhandle,"bitrate") == '1':
            lbitrate = 700
    elif xbmcplugin.getSetting(pluginhandle,"bitrate") == '2':
            lbitrate = 600
    dname = name
#    swfurl = 'http://media.mtvnservices.com/player/release/?v=4.5.3'
    swfurl = 'http://media.mtvnservices.com/player/prime/mediaplayerprime.1.7.0.swf'
    
    req = urllib2.Request('http://www.southparkstudios.se/episodes/'+episodeid)
    req.addheaders = [('Referer', 'http://www.southparkstudios.se/episodes/'),
                      ('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('swfobject\.embedSWF\("http://media.mtvnservices.com/mgid:hcx:content:southparkstudios.se:(.+?)"').findall(link)
    
#    url =  'http://www.southparkstudios.com/feeds/video-player/mrss/mgid%3Acms%3Acontent%3Asouthparkstudios.com%3A'+episodeid
    #url = 'http://media.mtvnservices.com/player/config.jhtml?uri=mgid%3Acms%3Acontent%3Asouthparkstudios.com%3A'+episodeid+'&group=entertainment&type=network'
    url = 'http://www.southpark.de/feeds/video-player/mrss/mgid%3Ahcx%3Acontent%3Asouthparkstudios.se%3A'+match[0]
    response = getURL(url)
    #rtmp=re.compile('<media:content url="(.+?)" type="text/xml" medium="video" duration=".+?" isDefault=".+?" />').findall(response)
#    rtmp=re.compile('<media:content type=".+?" medium=".+?" duration=".+?" isDefault=".+?" url="(.+?)" />').findall(response)
    rtmp=re.compile('<media:content url="(.+?)" type=".+?" medium=".+?" duration=".+?" isDefault=".+?"').findall(response)
    stacked_url = 'stack://'
    
    for url in rtmp:
        response = getURL(url)
#        rtmps=re.compile('<src>(.+?)</src>').findall(response)
        rtmps=re.compile('<rendition duration=".+?" bitrate="(.+?)" width="(.+?)" height=".+?" type=".+?">\n<src>(.+?)</src>').findall(response)
        hbitrate = 0
        hwidth = 0
        furl = False
#        for rtmpbit in rtmps:
#            filesplit = rtmpbit.split('/')[-1]
#            brsplit  = filesplit.split('_')
#            bitrate = int(brsplit[-1].split('.')[-2].replace('kbps',''))
#            resolution = brsplit[-2].split('x')
#            pixels = int(resolution[0]) * int(resolution[1])
#            if bitrate > hbitrate or pixels > hpixels:
#                if lbitrate == None or bitrate <= lbitrate:
#                    hbitrate = bitrate
#                    hpixels = pixels
#                    furl = rtmpbit + " swfurl=" + swfurl + " swfvfy=true"

        for bitrate,pixels,rtmpbit in rtmps:
            bitrate = int(bitrate)
            pixels = int(pixels)
            if bitrate > hbitrate or pixels > hpixels:
                if lbitrate == None or bitrate <= lbitrate:
                    hbitrate = bitrate
                    hpixels = pixels
                    furl = rtmpbit + " swfurl=" + swfurl + " swfvfy=true"
                    
        if furl is not False:
            stacked_url += furl.replace(',',',,')+' , '

    stacked_url = stacked_url[:-3] 
    item=xbmcgui.ListItem(dname, thumbnailImage=thumbnail, path=stacked_url)
    item.setInfo( type="Video", infoLabels={"Title": dname,
                                            "Season":season,
                                            "Episode":episode,
                                            "premiered":premiered,
                                            "Plot":plot,
                                            "TVShowTitle":TVShowTitle
                                            })
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    

def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param
        
params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    name=''
try:
    mode=int(params["mode"])
except:
    pass
try:
    thumbnail=urllib.unquote_plus(params["thumbnail"])
except:
    thumbnail=''
try:
    season=int(params["season"])
except:
    season=0
try:
    episode=int(params["episode"])
except:
    episode=0
try:
    premiered=urllib.unquote_plus(params["premiered"])
except:
    premiered=''
try:
    plot=urllib.unquote_plus(params["plot"])
except:
    plot=''

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
if mode==None or url==None or len(url)<1:
    print "Seasons"
    seasons()
elif mode==1:
    print "Episodes"
    episodes(url)
elif mode==2:
    print "Get Rtmp"
    playVideo(url,name,thumbnail)
elif mode==3:
    print "Random Episode"
    randomEpisode(url)




