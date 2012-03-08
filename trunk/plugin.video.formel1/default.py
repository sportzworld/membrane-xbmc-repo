# -*- coding: utf-8 -*-
import urllib,urllib2,re,random,xbmcplugin,xbmcgui
from time import gmtime, strftime

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())

pluginhandle = int(sys.argv[1])


def MAIN():
	req = urllib2.Request('http://www.formel1.de/de/610/Videos')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<select name="playlist" id="playlist">(.+?)</select>', re.DOTALL).findall(link)

	addLink('Live','http://www.rtl.de/formel1/livestream/index',1,'')
#	addDir('News und Analysen','http://www.rtl.de/cms/sport/formel-1/videos.html',2,'')
	for entry in match:
     		match_option=re.compile('<option value="(.+?)">(.+?)</option>', re.DOTALL).findall(entry)
		for value,name in match_option:
			addDir(name,'http://www.formel1.de/de/610/Videos/playlist/'+value,4,'')
		


def LIVE(url,name):#1
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match_swf=re.compile("swfobject.embedSWF\('(.+?)'", re.DOTALL).findall(link)
        match=re.compile('<div id="f1ls_stream">(.+?)</div>', re.DOTALL).findall(link)
	match_rtmp=re.compile('CDATA\[(.+?)\]', re.DOTALL).findall(match[0])
	
	url = match_rtmp[-1]+' swfurl='+match_swf[0]+' swfvfy=true'
	item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)




def RTL_VIDEOS(url):#2 
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile('<div class="videoListBoxContainer" id="videoleisten_pl">(.+?)<div class="related">', re.DOTALL).findall(link)
	for videos in match:
		print videos
		match_videos=re.compile('<div class="imgBox">.+?src="(.+?)".+?alt="(.+?)".+?videoid: \'(.+?)\'', re.DOTALL).findall(videos)
		for thumb,name,videoid in match_videos:
			addLink(name,videoid,3,thumb)



def RTL_VIDEOS_PLAY(video_id,name):#3 
	req = urllib2.Request('http://www.rtl.de/video/playerlayer/show/format/html/contensobject/0/videoid/'+video_id+'/farbwelt/rtl/playlist/28,0/modul/playlisturl')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	req.add_header('X-Requested-With', 'XMLHttpRequest')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	video_id_split = video_id.split('_')
	video_id = video_id_split[0]
	print'video_id '+video_id
	match=re.compile(video_id+'.+?"url".+?"(.+?)"', re.DOTALL).findall(link)
	rtmp = match[0].replace('\\','')
	url = rtmp+' swfurl=http://bilder.rtl.de/rtl09/flash/rtl_player.swf?cachebuster=1331067600 swfVfy=true'
        item = xbmcgui.ListItem(path=url)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def FORMEL_VIDEOS(url):#4   
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
#	print link
        match_videos=re.compile('<ul class="thumbs slide-wrapper counter(.+?)</ul>', re.DOTALL).findall(link)
	for videos in match_videos:
	        match_video=re.compile('<a href="http://www.youtube.com/watch\?v=(.+?)&amp;.+?title="(.+?)"', re.DOTALL).findall(videos)
		for url,name in match_video:
			addLink(name,url,5,'http://img.youtube.com/vi/'+url+'/2.jpg')

def FORMEL_VIDEOS_PLAY(url,name):#5     
	play_youtube_video(url,name)


def play_youtube_video(video_id, name):
        print ("Playing video " + name + " id: " + video_id)
        url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % (video_id)
        listitem = xbmcgui.ListItem( label = str(name), iconImage = "DefaultVideo.png", thumbnailImage = xbmc.getInfoImage( "ListItem.Thumb" ), path=url )
        infolabels = { "title": name, "plot": name}
        listitem.setInfo( type="Video", infoLabels=infolabels)
        xbmc.Player( xbmc.PLAYER_CORE_DVDPLAYER ).play( str(url), listitem)


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




def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('IsPlayable', 'true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
fanart=None

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
        MAIN()

elif mode==1:
        print ""+url
        LIVE(url,name)
        
elif mode==2:
        print ""+url
        RTL_VIDEOS(url)

elif mode==3:
        print ""+url
        RTL_VIDEOS_PLAY(url,name)

elif mode==4:
        print ""+url
        FORMEL_VIDEOS(url)

elif mode==5:
        print ""+url
        FORMEL_VIDEOS_PLAY(url,name)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
