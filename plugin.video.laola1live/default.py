# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,string,random,cookielib

try:
	import StorageServer
except:
	import storageserverdummy as StorageServer
cache = StorageServer.StorageServer("laola", 24)

cache.table_name = "testtable"


pluginhandle = int(sys.argv[1])


__settings__ = xbmcaddon.Addon(id='plugin.video.laola1live')
__language__ = __settings__.getLocalizedString

baseurl = 'http://www.laola1.tv'







def MAIN():
	addDir(__language__(32001),'http://www.laola1.tv/de-de/calendar/0.html',5,'')
	response=getUrl(baseurl)
	match_all_cats=re.compile('<li class="heading">Sport Channels</li>(.+?)<li class="heading">More</li>', re.DOTALL).findall(response)
	match_cats=re.compile('<li class=" has_sub">.+?src="(.+?)".+?href="(.+?)">(.+?)<', re.DOTALL).findall(match_all_cats[0])
	for thumb,url,name in match_cats:
		name = name.replace("\n","")
		name = name.replace("	","")
		addDir(name,url,1,'')

def MAIN_NEXT(url,name):#1
	response=getUrl(url)
	match_all_cats=re.compile('<li class="heading">Sport Channels</li>.+?'+name+'(.+?)</ul>', re.DOTALL).findall(response)
	match_cats=re.compile('src="(.+?)".+?href="(.+?)">(.+?)<', re.DOTALL).findall(match_all_cats[0])
	for thumb,url,name in match_cats:
		name = name.replace("\n","")
		addDir(name,url,2,thumb)
		
def LIST_VIDEOS(url):#2
	i = 1
	stuff = ''
	if 'data-stageid' not in url:
		update_view = False
		response=getUrl(url)
		match_data=re.compile('<div class="stage_frame active"(.+?)>', re.DOTALL).findall(response)
		data = match_data[0]
		match_all_vids=re.compile('<span>Werbung</span>(.+?)<!-- STAGE ENDE -->', re.DOTALL).findall(response)
		clearcache()
		
	else:
		update_view = True
		match_stageid=re.compile('data-stageid= "(.+?)"', re.DOTALL).findall(url)
		match_call=re.compile('data-call="(.+?)"', re.DOTALL).findall(url)
		match_htag=re.compile('data-htag="(.+?)"', re.DOTALL).findall(url)
		match_page=re.compile('data-page="(.+?)"', re.DOTALL).findall(url)
		match_startvids=re.compile('data-startvids="(.+?)"', re.DOTALL).findall(url)
		
		new_page = str( int(match_page[0]) + 1 )

		stageid = 'stageid='+match_stageid[0]
		call = '&call='+match_call[0]
		htag = '&htag='+match_htag[0]
		page = '&page='+new_page
		startvids = '&startvids='+match_startvids[0]
		anzahlblock = '&anzahlblock=11'

		post_data = stageid+call+htag+page+startvids+anzahlblock
		post_url = 'http://www.laola1.tv/de-at/nourish.php?key='+htag
		response=postUrl(post_url,post_data)
		
		data = url.replace('data-page="'+match_page[0]+'"','data-page="'+new_page+'"')
		match_all_vids=response,
		
		##recall cached videos
		stuff = recall('stored_list')
		match_stored_vids=re.compile('<vid>(.+?)</vid>', re.DOTALL).findall(stuff)
		for vid in match_stored_vids:
			i = i + 1
			name,url,thumb=vid.split('#')
			addLink(name,url,10,thumb,'')


	match_some_vids=re.compile('<div class="grid(.+?)</div>\n		</div>', re.DOTALL).findall(match_all_vids[0])
	for some_vids in match_some_vids:## Add new videos
		split = some_vids.split('<div class="overlay">')
		for vids in split:
			#match_vids=re.compile('<div class="overlay">.+?<h2>(.+?)</h2>.+?<span class="date">(.+?)</span>.+?<span class="mediatype">(.+?)</span>.+?href="(.+?)".+?src="(.+?)"', re.DOTALL).findall(vids)
			match_name=re.compile('<h2>(.+?)</h2>', re.DOTALL).findall(vids)
			match_date=re.compile('<span class="date">(.+?)</span>', re.DOTALL).findall(vids)
			match_thumb=re.compile('src="(.+?)"', re.DOTALL).findall(vids)
			match_mediatype=re.compile('<span class="mediatype">(.+?)</span>', re.DOTALL).findall(vids)
			match_url=re.compile('href="(.+?)"', re.DOTALL).findall(vids)

			
			try:
				name = match_name[0]
			except:
				name = ''

			try:
				date = match_date[0]
			except:
				date = ''

			try:
				thumb = match_thumb[0]
			except:
				thumb = ''

			try:
				mediatype = match_mediatype[0]
			except:
				mediatype = ''

			try:
				url = match_url[0]
			except:
				url = ''
				

			if __settings__.getSetting('hq_thumbnail') == '2':
				thumb = thumb.replace('188x108','798x449')
				thumb = thumb.replace('195x111','798x449')
				thumb = thumb.replace('396x223','798x449')
			elif __settings__.getSetting('hq_thumbnail') == '1':
				thumb = thumb.replace('188x108','396x223')
				thumb = thumb.replace('195x111','396x223')
			if name != '':
				name = name.replace("\n","")
				name = name.replace("&quot;",'"')
				name = name.replace("&amp;",'&')
				name = date+' - '+name
				addLink(name,baseurl+url,10,thumb,'')
				
				stuff = stuff + '<vid>'+name+'#'+baseurl+url+'#'+thumb+'</vid>'
				
				
	store(stuff,'stored_list')			
	addDir(__language__(32000).encode("utf-8"),data,2,'')
	try:
		wnd = xbmcgui.Window(xbmcgui.getCurrentWindowId())
		wnd.getControl(wnd.getFocusId()).selectItem(i)
	except:
		log('focusing not possible')
	if update_view == True:
		xbmcplugin.endOfDirectory(int(sys.argv[1]), updateListing=True)
	
def LIST_LIVE(url):
	response=getUrl(url)
	match_all_vids=re.compile('<div class="liveprogramm_full">(.+?)<div class="crane_footer has_rightbar inline_footer">', re.DOTALL).findall(response)
	all_vids = match_all_vids[0].split('span class="tag"')
	for some_vids in all_vids:
		match_vids=re.compile('	<img src="(.+?)">.+?<span.+?href="(.+?)".+?<h2>(.+?)</h2>.+?<span class="time live_countdown".+?>(.+?)</span>', re.DOTALL).findall(some_vids)
		match_date=re.compile('>(.+?)</span><div class="stream ">').findall(some_vids)
		for thumb,url,name,time in match_vids:
			addLink(match_date[0]+', '+time+' - '+name,url,11,thumb)
	
	


def PLAY(url,name):#10
	response=getUrl(url)
	match_player=re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(response)
	response=getUrl(match_player[0])
	
	match_m3u8=re.compile('url: "(.+?)"', re.DOTALL).findall(response)
	
	response=getUrl(match_m3u8[0])
	match_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)
	match_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
	res_url=match_url[0].replace('l-_a-','l-L1TV_a-l1tv')
	
	m3u8_url = res_url+'?hdnea='+match_auth[0]+'&g='+char_gen(12)+'&hdcore=3.1.0'

	try:
		response=getUrl(m3u8_url)
		match_sec_m3u8=re.compile('http(.+?)null=', re.DOTALL).findall(response)
		quality = int(__settings__.getSetting('vod_quality'))+1
		
		while quality != 0:
			try:
				quality = quality - 1
				sec_m3u8 = 'http'+match_sec_m3u8[quality]+'null='
				listitem = xbmcgui.ListItem(path=sec_m3u8)
				return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
			except:
				log('Quality setting not available, trying lower one:'+str(quality))
		log('Error: no video found')
	except:
		log('Error: no video found')
	
def PLAY_LIVE(url,name):#11
	response=getUrl(url)
	if 'Dieser Stream beginnt am' in response:
		log('Video has not jet started')
		match_big=re.compile('<big>(.+?)</big>', re.DOTALL).findall(response)
		xbmc.executebuiltin("Notification("+__language__(32002)+","+match_big[0].replace(',',' -')+", 7000)")
	else:
		match_player=re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(response)
		response=getUrl(match_player[0])
		
		match_m3u8=re.compile('url: "(.+?)"', re.DOTALL).findall(response)
		
		response=getUrl(match_m3u8[0].replace('/vod/','/live/'))
		match_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)
		match_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
		res_url=match_url[0].replace('l-_a-','l-L1TV_a-l1tv')
		
		m3u8_url = res_url+'?hdnea='+match_auth[0]
		
		response=getUrl(m3u8_url)
		match_sec_m3u8=re.compile('#EXT-X-STREAM-INF:(.+?)http(.+?)rebase=on', re.DOTALL).findall(response)
		quality = int(__settings__.getSetting('vod_quality'))+1

		
		while quality != 0:
			try:
				quality = quality - 1

				if "RESOLUTION" in match_sec_m3u8[quality][0]:
					sec_m3u8 = 'http'+match_sec_m3u8[quality][1]+'rebase=on'
					listitem = xbmcgui.ListItem(path=sec_m3u8)
					return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
				else:
					log('No video in url detected, trying lower one: '+str(quality))
					
			except:
				log('Quality setting not available, trying lower one: '+str(quality))
		log('Error: no video found')

		
		
def store(stuff,name):
	stuff = stuff.replace('ä','&auml;')
	stuff = stuff.replace('Ä','&Auml;')
	stuff = stuff.replace('ö','&ouml;')
	stuff = stuff.replace('Ö','&Ouml;')
	stuff = stuff.replace('ü','&uuml;')
	stuff = stuff.replace('Ü','&Uuml;')
	stuff = stuff.replace('ß','&szlig;')
	cache.table_name = "testtable"
	log('store: '+stuff)
	#cache.set('test', urllib.quote_plus(stuff))
	cache.set('cache', stuff)
	return True
	
def recall(name):
	cache.table_name = "testtable"
	stuff = cache.get('cache')
	stuff = stuff.encode("utf-8")
	stuff = stuff.replace('&auml;','ä')
	stuff = stuff.replace('&Auml;','Ä')
	stuff = stuff.replace('&ouml;','ö')
	stuff = stuff.replace('&Ouml;','Ö')
	stuff = stuff.replace('&uuml;','ü')
	stuff = stuff.replace('&Uuml;','Ü')
	stuff = stuff.replace('&szlig;','ß')
	log('recall: '+stuff)
	return stuff
	
def clearcache():
	cache.table_name = "testtable"
	cache.delete("cache")
	
def log(message):
	if __settings__.getSetting('debug') == 'true':
		print "#####Laola1 Debug: "+message
	return
	
def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))


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



def getUrl(url):
	log('Opening URL: '+url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link
	
	
def postUrl(url,data):
        req = urllib2.Request(url,data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link


def addLink(name,url,mode,iconimage,plot=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "plotoutline": plot  } )
	liz.setProperty('IsPlayable', 'true')
	if __settings__.getSetting('hq_thumbnail') == '2':
		liz.setProperty('fanart_image',iconimage)
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
        MAIN_NEXT(url,name)

elif mode==2:
        print ""+url
        LIST_VIDEOS(url)

elif mode==5:
        print ""+url
        LIST_LIVE(url)
		
elif mode==10:
        print ""+url
        PLAY(url,name)
		
elif mode==11:
        print ""+url
        PLAY_LIVE(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
