import urllib,urllib2,re,random,xbmcplugin,xbmcgui



nums = '0123456789'
strNumber = ''
count = 0
while (count < 11):
	strNumber += nums[random.randrange(len(nums))]
	count += 1



def CATEGORIES():
        req = urllib2.Request('http://deluxemusic.tv/')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        sender_link=response.read()
        response.close()
        match=re.compile('horizontal tv_scroll_item.+?onclick="changeStationTV\(0,\'(.+?)\'.+?>DELUXE<br>(.+?)</a>.+?<img src="(.+?)"', re.DOTALL).findall(sender_link)
        #onclick="changeStationTV(0,'761036802',0,'101', '<a href=\'/video/item/54-deluxe-lounge\'>DELUXE<br>LOUNGE</a>'
        #<img src="/images/deluxe/DELUXE_TELEVISION_LOUNGE_free_stream.png" alt="DELUXE_TELEVISION_LOUNGE_free_stream" width="45" height="48" />
        for url,art,thumbnail in match:
                if art == 'LOUNGE':
                        addDir('Lounge',url,1,thumbnail)
#                        print 'loungeurl: '+url
                elif art == 'TRAILER':
                        addDir('Trailer',url,1,thumbnail)
#                        print 'trailerurl: '+url
                elif art == 'NEWS':
                        addDir('News',url,1,thumbnail)
                elif art == 'STORIES':
                        addDir('Stories',url,1,thumbnail)
                        addDir('test','url',1,'thumbnail')

               
def INDEX(url):
        req = urllib2.Request('http://deluxemusic.tv/modules/mod_dlx_player/embeddedobjects.js')
        #http://deluxemusic.tv/modules/mod_dlx_player/embeddedobjects.js
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link_appid=response.read()
        response.close()
        match_appid=re.compile('application=(.+?)&').findall(link_appid)
        for appid in match_appid:
#                print 'appid: '+appid
                req = urllib2.Request('http://www.contentforce.de/iptv/player/macros/_x_s-'+appid+'/_s_defaultPlayer_update/_v_f_0_de/xflv/configv2.xml?r=r&r=rjQueryforcedWidth&rd=13'+strNumber)###############random number!!!!!
                #http://www.contentforce.de/iptv/player/macros/_x_s-760217600/_s_defaultPlayer_update/_v_f_0_de/xflv/configv2.xml?r=r&r=rjQueryforcedWidth&rd=1302884352296
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link_xasx=response.read()
                response.close()
                match_xasx=re.compile('<link type="xasx">(.+?)</link>').findall(link_xasx)
                #<link type="xasx">http://www.contentforce.de/player/macros/_v_f_0_de/_s_defaultPlayer_update/_x_s-760217600/xflv/xasxv2.xml</link>
                for xasx in match_xasx:
#                        print 'xasx: '+xasx
                        req = urllib2.Request(xasx+'?r=r&rd=13'+strNumber+'&pl='+url)##################random!!
                        #http://www.contentforce.de/player/macros/_v_f_750_de/_s_defaultPlayer_update/_x_s-760217600/xflv/xasxv2.xml?r=r&rd=1302882687218&pl=761036802
                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                        response = urllib2.urlopen(req)
                        link_videos=response.read()
                        response.close()
                        match_videos=re.compile('<entry(.+?)</entry>', re.DOTALL).findall(link_videos)
                        for videos in match_videos:
#                                print 'videos: '+videos
                                match_video=re.compile('CDATA\[(.+?)\]\]>(.+?)<screenshot width=".+?" height=".+?" href="(.+?)"/>', re.DOTALL).findall(videos)
                                #<video width="768" height="432" href="http://static.cdn.streamfarm.net/13000deluxe/ondemand/app760217600/376045570/742141/742141_on2vp6_768_432_1500kb_de_1500.flv" bandwidth="1500"/>
                                #<screenshot width="80" height="45" href="http://static.cdn.streamfarm.net/13000deluxe/ondemand/app760217600/376045570/742141/742141_screenshot_80_45_5p.jpeg"/>
                                for name,urls,thumbnail in match_video:
                                        match_vid=re.compile('<video width=".+?" height=".+?" href="(.+?)" bandwidth=".+?"/>').findall(urls)
                                        addLink(name,match_vid[-1],thumbnail)

                
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




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
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
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
