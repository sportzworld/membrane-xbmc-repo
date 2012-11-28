# -*- coding: utf8 -*-

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,base64,socket,sys,string,random,cookielib,httplib,base64

from flvlib import tags
from flvlib import helpers
from flvlib.astypes import MalformedFLV

__settings__ = xbmcaddon.Addon(id='plugin.video.laola1live')
__language__ = __settings__.getLocalizedString

#xbmc.PLAYER_CORE_MPLAYER

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.laola1live')
#akamaiProxyServer = xbmc.translatePath(addon.getAddonInfo('path')+"/akamaiSecureHD.py")
testfile = xbmc.translatePath(addon.getAddonInfo('path')+"/test.flv")

COOKIEFILE = xbmc.translatePath(addon.getAddonInfo('path')+"/cookies.lwp")
#USERFILE = xbmc.translatePath(addon.getAddonInfo('path')+"/userfile.js")




###set settings
if xbmcplugin.getSetting(pluginhandle,"streamquality") == '0':
	setting_streamquality = '0'
elif xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
	setting_streamquality = '1'

if xbmcplugin.getSetting(pluginhandle,"livequality") == '0':
	livequality = '0'
elif xbmcplugin.getSetting(pluginhandle,"livequality") == '1':
	livequality = '1'
elif xbmcplugin.getSetting(pluginhandle,"livequality") == '2':
	livequality = '2'

if xbmcplugin.getSetting(pluginhandle,"location") == '0':
	livestream_url = 'http://www.laola1.tv/de/at/home/'
	videos_url = 'http://www.laola1.tv/de/at/home/'
elif xbmcplugin.getSetting(pluginhandle,"location") == '1':
	livestream_url = 'http://www.laola1.tv/de/de/home/'
	videos_url = 'http://www.laola1.tv/de/de/home/'
elif xbmcplugin.getSetting(pluginhandle,"location") == '2':
	livestream_url = 'http://www.laola1.tv/en/int/home/'
	videos_url = 'http://www.laola1.tv/en/int/home/'
	

if xbmcplugin.getSetting(pluginhandle,"debug") == '0':
	debug = '0'
elif xbmcplugin.getSetting(pluginhandle,"debug") == '1':
	debug = '1'

if xbmcplugin.getSetting(pluginhandle,"autoplay") == '0':
	autoPlay = 0
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '1':
	autoPlay = 8
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '2':
	autoPlay = 10
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '3':
	autoPlay = 15
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '4':
	autoPlay = 20
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '5':
	autoPlay = 30
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '6':
	autoPlay = 40
elif xbmcplugin.getSetting(pluginhandle,"autoplay") == '7':
	autoPlay = 50


###set strings

scommercial = __language__(30002)
snotstarted = __language__(30003)
sstartsat = __language__(30004)
sat = __language__(30005)
scet = __language__(30006)


#xip = xbmcplugin.getSetting(pluginhandle,"ip")
#print 'xip: '+xip
                       
#if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#	print 'laola: use trick'







def INDEX():

        addDir('Live',livestream_url,4,'')

        response = getUrl(videos_url)

        match=re.compile('<div id="sitemap"><a (.+?)</div>').findall(response)

        for something in match:
                match1=re.compile('href="(.+?)".*?>(.+?)</a>').findall(something)
                for url,name in match1 or match2:
                        addDir(name,url,1,'')



def TOPICSELECTION(url):
	response = getUrl(url)

        match=re.compile("<td style=\".+?\" width=\".+?\"><h2><a href=\"(.+?)\" style=\".+?\">(.+?)</a></h2></td>").findall(response) 

        for url,name in match:
		if not "LIVE" in name:
			if not "Live" in name:
				addDir(name,url,2,'')

                

def VIDEOSELECTION(url):
	response = getUrl(url)
        match1=re.compile('<div class="teaser_bild_video" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_video" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?"><a href=".+?>(.+?)</a>', re.DOTALL).findall(response)

        for url,thumbnail,date,name in match1:
		"""
		splits = url.split("-")
		video_id = splits[-1].replace('.html','')
		#new_url = "http://streamaccess.unas.tv/hdflash/vod/22/"+video_id+".xml?t=.smil"
                addLink(date+' - '+name,video_id,3,thumbnail)
		"""
                addLink(date+' - '+name,url,3,thumbnail)

        match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(response)
        for url in match_next:
                addDir(__language__(30001),url,2,'')

        match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">next</a>").findall(response)
        for url in match_next:
                addDir(__language__(30001),url,2,'')



def get_playkeys(url):
	log("GET playkey1,playkey2")

	response = getUrl(url)
	print response
	playkeys=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(response)

	for playkey1,playkey2 in playkeys:
		log('playkey1: "'+playkey1+'"')
		log('playkey2: "'+playkey2+'"')

	return playkeys

def VIDEOLINKS(url,name):

	if xbmcplugin.getSetting(pluginhandle,"ads") == '1':
		try:
			ad_url,ad_length = get_video_ad()
			#stacked_url += ad_url + ' , '
			item=xbmcgui.ListItem(scommercial, thumbnailImage='')
			item.setProperty('mimetype', 'video/x-flv')
			xbmc.PlayList(1).add(ad_url, item)
		except:
			log('no commercial recieved')


	item=xbmcgui.ListItem(name, thumbnailImage='')
	item.setProperty('mimetype', 'video/x-flv')
	xbmc.PlayList(1).add('plugin://plugin.video.laola1live/?url='+enc_url(url)+'&mode=10&name='+name, item)



def PLAY_VIDEO(url,name):

	response = getUrl(url)
	match=re.compile('videopfad=(.+?)&', re.DOTALL).findall(response)
        req = urllib2.Request(match[0])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Host', 'streamaccess.unas.tv')
        #req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()



	match_httpBase=re.compile('<meta name="httpBase" content="(.+?)"', re.DOTALL).findall(link)
	match_vod=re.compile('<meta name="vod" content="true" value="/(.+?)"', re.DOTALL).findall(link)
	match_src=re.compile('<video src=".+?primaryToken=(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(link)
	match_srcb=re.compile('<video src="(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(link)
	if setting_streamquality == '0':
		src = match_src[0]
		log("low quality - currently broken")

	else:
		src = match_src[-1]
		log("high quality - currently broken")
	vod = match_vod[0]
	#vod = match_vod[0].replace('bitrate=0','bitrate=950000')
	#vod = vod.replace('bitrate=0','bitrate=950000')


	fullUrl = match_httpBase[0]+vod+"?primaryToken="+src
	#fullUrl = match_httpBase[0]+match_srcb[0]
	fullUrl = fullUrl.replace("&amp;","&")
	#fullUrl = fullUrl.replace("&p=","&p=22")
	#fullUrl = fullUrl.replace("&e=","&e=104258")
	#fullUrl = fullUrl.replace("&a=","&a=l1tvgerfbbl")
	#fullUrl = fullUrl.replace("&l=","&l=L1TV")
	fullUrl = fullUrl + "&v=2.10.3&fp=LNX%2011,1,102,63"
	fullUrl = fullUrl + "&r="+char_gen(5)#random uppercase string
	g = char_gen(12)#random uppercase string
	fullUrl = fullUrl + "&g="+g
	log('fullUrl: '+fullUrl)

	"""
	match_httpBase=re.compile('<meta name="httpBase" content="(.+?)"', re.DOTALL).findall(response)
	match_vod=re.compile('<meta name="vod" content="true" value="/(.+?)"', re.DOTALL).findall(response)
	match_src=re.compile('<video src=".+?primaryToken=(.+?)" system-bitrate=".+?"/>', re.DOTALL).findall(response)

	if setting_streamquality == '0':
		src = match_src[0]
		print "low quality"
	else:
		src = match_src[-1]
		print "high quality"
	
	fullUrl = match_httpBase[0]+match_vod[0]+"?primaryToken="+src
	fullUrl = fullUrl.replace("&amp;","&")
	fullUrl = fullUrl + "&v=2.10.3&fp=LNX%2011,1,102,63"
	fullUrl = fullUrl + "&r="+char_gen(5)#random uppercase string
	fullUrl = fullUrl + "&g="+char_gen(12)#random uppercase string
	"""


	###header inspection###
	"""
        req = urllib2.Request(fullUrl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
	print'####################resp_info'
	print response.info()
        link=response.read()
        response.close()
	"""




        #listitem = xbmcgui.ListItem(path=fullUrl)


	#print int(float(ad_length)*float(1000))

	item=xbmcgui.ListItem(name, thumbnailImage='', path=fullUrl)
	item.setProperty('mimetype', 'video/x-flv')
	#xbmc.Player().play( fullUrl , item)		

	xbmcplugin.setResolvedUrl(pluginhandle, True, item)
	#deb_time = 'debug time\n'

	#deb_time += 'adlength time in ms\n'
	#deb_time += str(int(float(ad_length)*float(1000)))+'\n'


	if autoPlay>0:
		xbmc.sleep(autoPlay*100)
		if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0:
			xbmc.Player().pause()
	"""
	xbmc.sleep(5000)

	mod_vod = vod.replace('mp4.csmil/bitrate=0','mp4.csmil_0_1@14')
	mod_vod = mod_vod+'?cmd=throttle,100&v=2.10.3&r='+char_gen(5)+'&g='+g+'&lvl1=9.84,10,15.458,11.49,12.66,NaN,1488,1488,1,950,16.353,1353800347.83,14.92,16.378,14.945,393.68,1445'

	control = match_httpBase[0]+mod_vod
	print '#################################control'+control
	print getUrl(control)
	"""

#'http://hdvodlaola1tv-f.akamaihd.net/control/hdflash/2012/eishockey/121123_man_kec_,low,high,.mp4.csmil_0_1@14?cmd=throttle,108&v=2.10.3&r=EYXCI&g=RVBLUXVNVBLK&lvl1=9.84,10,15.458,11.49,12.66,NaN,1488,1488,1,950,16.353,1353800347.83,14.92,16.378,14.945,393.68,1445,3.03,0,155,122,15003,u,false')



	"""
	if autoPlay>0:
		xbmc.sleep(autoPlay*100+int(float(ad_length)*float(1000)))
		time_difference = int(xbmc.Player().getTime())*1000 - int(float(ad_length)*float(1000))
		#deb_time += 'player time\n'
		#deb_time += str(int(xbmc.Player().getTime()))+'\n'
		#deb_time += 'time difference\n'
		#deb_time += str(time_difference)+'\n'
		#deb_time += 'round time\n'
		#deb_time += str(round(time_difference))+'\n'
		#deb_time += 'round time/100\n'
		#deb_time += str(round(time_difference/100))
		#print deb_time
		if xbmc.Player().isPlaying()==True and round(time_difference/1000)==0:

			xbmc.Player().pause()
	"""
	"""
    	#core_player = xbmc.PLAYER_CORE_MPLAYER
    	core_player = xbmc.PLAYER_CORE_DVDPLAYER
	stacked_url = stacked_url[:-3] 
	item=xbmcgui.ListItem(name, iconImage='', thumbnailImage='')

	ok=xbmc.Player( core_player ).play( stacked_url , item)
	autoPlay = 5
	if autoPlay>0:
		xbmc.sleep(autoPlay*1000)
		if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0:
			xbmc.Player().pause()	

	return
	#item=xbmcgui.ListItem(name, thumbnailImage='', path=stacked_url)
	#xbmcplugin.setResolvedUrl(pluginhandle, True, item)

	#listitem = xbmcgui.ListItem(name,thumbnailImage='')#TODO:thumb
	#xbmc.PlayList(1).add(fullUrl, listitem)
	"""



	"""
	listitem.setProperty('mimetype', 'video/x-flv')
        return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	"""



"""
	pageurl = url #this is messy

	playkeys = get_playkeys(url)

	for playkey1,playkey2 in playkeys:
		playkey1 = playkey1
		playkey2 = playkey2
	

	log('GET streamquality,server,servertype,playpath,title')
	response = getUrl('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)

	match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(response)

	video = match_video[0]

	match_rtmp=re.compile('<(.+?) .+?erver="(.+?)/(.+?)" pfad="(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '

	for streamquality,server,servertype,playpath,title in match_rtmp:
		streamquality = streamquality
		server = server
		servertype = servertype
		playpath = playpath
		title = title
		if setting_streamquality == '1':
			break

	log('streamquality: "'+streamquality+'"')
	log('server: "'+server+'"')
	log('servertype: "'+servertype+'"')
	log('playpath: "'+playpath+'"')
	log('title: "'+title+'"')


	log('GET auth,url,stream,aifp')
	response = getUrl('http://streamaccess.laola1.tv/flash/vod/22/'+playkey1+'_'+streamquality+'.xml')

	match_token=re.compile('auth="(.+?)".+?url="(.+?)".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(response)

	for auth,url,stream,aifp in match_token:
		auth = auth
		url = url
		stream = stream
		aifp = aifp

	log('auth: "'+auth+'"')
	log('url: "'+url+'"')
	log('stream: "'+stream+'"')
	log('aifp: "'+aifp+'"')


	log('GET ip')
	response = getUrl('http://'+server+'/fcs/ident')

	match_path=re.compile('<ip>(.+?)</ip>').findall(response)

	ip = match_path[0]

	log('ip: "'+ip+'"')


	log('assembling rtmp')
	rtmpbody = 'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream
	swf = ' swfUrl=http://www.laola1.tv/swf/player.v12.4.swf swfVfy=true'
	app = ' app='+servertype+'?_fcs_vhost='+server+'&auth='+auth+'&aifp='+aifp+'&slist='+stream
	page = ' pageUrl='+pageurl

	if '.mp4' in stream:
		playpath = ' playpath=mp4:'+stream
	else:
		playpath = ' playpath='+stream #fix for beachvolleyball

	flashver = ' flashver=LNX\ 10,3,162,29'
	rtmppath = rtmpbody+swf+app+page+playpath
	rtmppath = rtmppath.replace('&amp;','&')
	rtmppath = rtmppath.replace('&p=','&p=22')
	rtmppath = rtmppath.replace('&e=','&e='+playkey1)
	item = xbmcgui.ListItem(path=rtmppath)
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
"""


def LIVESELECTION(url):
        #print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match1=re.compile('<h2><a href="http://www.laola1.tv/(.+?)/upcoming-livestreams/(.+?)"').findall(link)
        #<h2><a href="http://www.laola1.tv/en/int/upcoming-livestreams/video/0-989-.html"
        for lang,videos in match1:
                #print videos
                req = urllib2.Request('http://www.laola1.tv/'+lang+'/upcoming-livestreams/'+videos)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#		if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#			req.add_header('X-Forwarded-For', xip)
                response = urllib2.urlopen(req)
                link=response.read()
                #print link
                response.close()
        	match1=re.compile('<div class="teaser_bild_live" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_live" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?"><a href=".+?>(.+?)</a>', re.DOTALL).findall(link)
#                match1=re.compile('<div class=".+?" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_live" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?">(.+?)</div>', re.DOTALL).findall(link)


	        for url,thumbnail,date,name in match1:
#                for url,thumbnail,date,name in match1:
                        addLink(date+' - '+name,url,5,thumbnail)

                match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(link)
                for url in match_next:
                        addDir(__language__(30001),url,4,'')
                match_next=re.compile("<a href=\"(.+)\" class=\"teaser_text\">next</a>").findall(link)
                for url in match_next:
                        addDir(__language__(30001),url,4,'')


def VIDEOLIVELINKS(url,name):#5
	#print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	#print link

	#break if livestream isn't ready
	match_ready=re.compile('Dieser Stream beginnt am.+?<big>(.+?),(.+?)-(.+?)CET</big>', re.DOTALL).findall(link)
	for weekday,date,time in match_ready:
		#xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
		xbmc.executebuiltin("Notification("+snotstarted+","+sstartsat+" "+weekday.replace(' ','')+" - "+date.replace(' ','')+" "+sat+" "+time.replace(' ','').replace('Uhr','')+" "+scet+", 7000)")
		return

	match_ready=re.compile('This stream starts at.+?<big>(.+?),(.+?)-(.+?)CET</big>', re.DOTALL).findall(link)
	for weekday,date,time in match_ready:
		#xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
		xbmc.executebuiltin("Notification("+snotstarted+","+sstartsat+" "+weekday.replace(' ','')+" - "+date.replace(' ','')+" "+sat+" "+time.replace(' ','')+" "+scet+", 7000)")
		return

	if has_ended(link) == True:
		return

	#item=xbmcgui.ListItem(name, thumbnailImage='')
	#xbmc.PlayList(1).add('', item)


        match_playkey=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(link)

	if '"src", "http://www.laola1.tv/swf/hdplayer",' in link:

        	for playkey1,playkey2 in match_playkey:
			print 'laola: use streamtype 1a'
			req = urllib2.Request('http://streamaccess.laola1.tv/hdflash/1/hdlaola1_'+playkey1+'.xml?streamid='+playkey1+'&partnerid=1&quality=hdlive&t=.smil')

		        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#			if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#				req.add_header('X-Forwarded-For', xip)
		        response = urllib2.urlopen(req)
		        link=response.read()
		        response.close()
			#print link

		        match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
			match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
		        match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)
			item=xbmcgui.ListItem(name, thumbnailImage='')
			item.setProperty('mimetype', 'video/x-flv')
			return xbmc.PlayList(1).add(match_http[0]+match_quality[-1], item)

                        #item = xbmcgui.ListItem(path=match_http[0]+match_quality[-1])
			#return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

		log('use streamtype 1b')
		match_live_1b=re.compile('isLiveStream=true&videopfad=(.+?)&').findall(link)

		ad_length = 0
		if xbmcplugin.getSetting(pluginhandle,"ads") == '1':
			try:
				ad_url,ad_length = get_video_ad()
				item=xbmcgui.ListItem(scommercial, thumbnailImage='')
				xbmc.PlayList(1).add(ad_url, item)
			except:
				log('no commercial recieved')
		#else:
		#	PLAY_LIVE_1B(enc_url,name)


		item=xbmcgui.ListItem(name, thumbnailImage='')
		item.setProperty('mimetype', 'video/x-flv')
		xbmc.PlayList(1).add('plugin://plugin.video.laola1live/?url='+enc_url(match_live_1b[0])+'&mode=11&name='+name, item)



		#item = xbmcgui.ListItem(path=http+video+" live=true")
		#return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


#        match_over=re.compile('<p>Lieber LAOLA(.+?)-User,</p>').findall(link)
#        if match_over[0] == '1':
#                addDir('vorbei/zu frueh',' ',5,'')
        ##"playkey=47060-Gut1cOWmlyix.&adv=laola1.tv/de/eishockey/ebel&adi=laola1.tv/de/eishockey/ebel&aps=Video1&szo=eishockey&deutschchannel=true&channel=222&teaser=1153&play=47060&fversion=player.v10.2"
	else:        
		log('use streamtype 2')
		for playkey1,playkey2 in match_playkey:
        	        print 'playkey1 '+playkey1
        	        print 'playkey2 '+playkey2                
        	        req = urllib2.Request('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)
        	        #print 'http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2
        	        ##http://www.laola1.tv/server/ondemand_xml_esi.php?playkey=47060-Gut1cOWmlyix.
        	        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#			if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#				req.add_header('X-Forwarded-For', xip)
        	        response = urllib2.urlopen(req)
        	        link_playkey=response.read()
        	        #print link_playkey
        	        response.close()
        	        match_video=re.compile('<video.+?>(.+?)</video>', re.DOTALL).findall(link_playkey)
        	        for video in match_video:
	#                        print 'video '+video
        	                match_rtmp=re.compile('<high server="(.+?)/(.+?)" pfad="(.+?)@(.+?)" .+? ptitle="(.+?)"').findall(video)#ugly, but behind low is one space too much: '  '
        	                ##<high server="cp77154.edgefcs.net/ondemand" pfad="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" type="V" aifp="v002"
        	                ##token="true" ptitle="Eishockey Erste Bank EHL Erste Bank Eishockey Liga" etitle="Vienna Capitals - EC Red Bull Salzburg"
        	                ##firstair="2010/01/01" stype="VOD" cat="video ondemand" vidcat="laola1.tv/at/eishockey/ebel" round="" season="2010/2011" />
        	                for server,servertype,playpath1,playpath2,title in match_rtmp:
        	                #for streamquality,server,servertype,playpath1,playpath2,title in match_rtmp:
        	                        #print 'streamquality '+streamquality
        	                        print 'server '+server
        	                        print 'servertype '+servertype
        	                        print 'playpath '+playpath1+'@'+playpath2
        	                        print 'title '+title
        	                        req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_high.xml')
        	                        #req = urllib2.Request('http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml')
        	                        
        	                        #print 'http://streamaccess.laola1.tv/flash/1/'+playkey1+'_'+streamquality+'.xml'
        	                        ##http://streamaccess.laola1.tv/flash/1/47327_high.xml?partnerid=1&streamid=47327
        	                        ##http://streamaccess.laola1.tv/flash/vod/22/47060_high.xml
        	                        ##http://streamaccess.laola1.tv/flash/1/47215_high.xml
        	                        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#					if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#						req.add_header('X-Forwarded-For', xip)
        	                        response = urllib2.urlopen(req)
        	                        link_token=response.read()
        	                        print link_token
        	                        response.close()
        	                        match_token=re.compile('auth="(.+?)&amp;p=.+?".+?url="(.+?)/live".+?stream="(.+?)".+?status=".+?".+?statustext=".+?".+?aifp="(.+?)"', re.DOTALL).findall(link_token)
        	                        ##auth="db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a="
        	                        ##url="cp77154.edgefcs.net/ondemand" stream="77154/flash/2011/ebel/20102011/110327_vic_rbs_high" status="0" statustext="success" aifp="v001" comment="success"
        	                        for auth,url,stream,aifp in match_token:
        	                                print 'auth '+auth
        	                                print 'url '+url
        	                                print 'stream '+stream
        	                                print 'afip '+aifp
        	                                req = urllib2.Request('http://'+server+'/fcs/ident')
        	                                ##http://cp77154.edgefcs.net/fcs/ident
        	                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#						if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#							req.add_header('X-Forwarded-For', xip)
        	                                response = urllib2.urlopen(req)
        	                                link_path=response.read()
        	                                response.close()
        	                                match_path=re.compile('<ip>(.+?)</ip>').findall(link_path)
        	                                ##<ip>213.198.95.204</ip>
        	                                for ip in match_path:
        	                                        print 'ip '+ip
        	                                ##http://cp77154.edgefcs.net/fcs/ident
	#    	                                         if streamquality == 'high':
        	                                        item = xbmcgui.ListItem(path='rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&p=1&e='+playkey1+'&u=&t=livevideo&l='+'&a='+'&aifp='+aifp+' swfUrl=http://www.laola1.tv/swf/player.v12.4.swf swfVfy=true live=true')
							return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
         	                                       #print 'name: '+name
         	                                       #print 'rtmp-link: rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+url+'/'+stream+'?auth='+auth+'&p=1&e='+playkey1+'&u=&t=livevideo&l='+'&a='+'&aifp='+aifp

         	                                       #addLink('High: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')



         	                                               ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=
         	                                               ##&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
         	                                               ##rtmp://213.198.95.204:1935/ondemand?_fcs_vhost=cp77154.edgefcs.net&auth=db.cibycHcwdEbhaKa4a3bUc7cIbpbLdtal-bnKofS-cOW-eS-CkBwmc-m6ke&p=&e=&u=&t=ondemandvideo&l=&a=&aifp=v001&slist=77154/flash/2011/ebel/20102011/110327_vic_rbs_high
         	                                       #elif streamquality == 'low':
         	                                               #addLink('Low: '+name,'rtmp://'+ip+':1935/'+servertype+'?_fcs_vhost='+server+'/'+playpath+'?auth='+auth+'&aifp='+aifp,'')
	

         	                                               ##...yeah


def PLAY_LIVE_1B(url,name):#11
	link=getUrl(url)
	match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
	match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
	match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)
##http://sportsmanlive-f.akamaihd.net/khl_2_1_450@s7077?primaryToken=1327601291_6d4b5709d7c7b8c364cad2036168a57a&p=1&e=74022&i=&q=&k=&c=DE&a=&u=&t=&l=&v=2.4.5&fp=LNX%2010,3,162,29&r=UEEBM&g=UICJXUGLJHOM
	http = match_http[0]
	http = http.replace("&l=","&l=&v=2.4.5&fp=LNX%2010,3,162,29&r="+char_gen(5)+"&g="+char_gen(12))

	if livequality == '0':
		video = match_quality[0]
	if livequality == '1':
		try:
			video = match_quality[1]
		except:
			video = match_quality[0]
	if livequality == '2':
		video = match_quality[-1]

	item=xbmcgui.ListItem(name, thumbnailImage='', path=http+video+" live=true")
	item.setProperty('mimetype', 'video/x-flv')
	xbmcplugin.setResolvedUrl(pluginhandle, True, item)

	
def LIVE(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #print link
        match_base=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
        match_src=re.compile('<video src="(.+?)" system-bitrate="950000"/>').findall(link)
        print match_base[0]
        print match_src[-1]
        addLink('play',match_base[0]+match_src[-1],'')


def has_ended(site):
	if 'Dieser Stream ist bereits beendet.' in site or 'This stream has already finished.' in site:
		xbmc.executebuiltin("Notification("+__language__(30007)+","+__language__(30008)+", 7000)")
		return True
	#elif #TODO:
	else: False

def enc_url(url):
	url = url.replace(':','%3A')
	url = url.replace('/','%2F')
	url = url.replace('?','%3F')
	url = url.replace('=','%3D')
	url = url.replace('&','%26')
	return url

                
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

def char_gen(size=1, chars=string.ascii_uppercase):
	return ''.join(random.choice(chars) for x in range(size))

def num_gen(size=1, chars=string.digits):
	return ''.join(random.choice(chars) for x in range(size))


def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link



def getUrlCookie( url , extraheader=True):
    cj = cookielib.LWPCookieJar()
    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE, ignore_discard=True)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]
    opener.addheaders = [('Host', 'ad.smartclip.net')]
    """
    opener.addheaders = [('Referer', 'http://www.vevo.com'),
                         ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2;)')]

    if extraheader:
        opener.addheaders = [('X-Requested-With', 'XMLHttpRequest')]
    if addoncompat.get_setting('location')==1:
        opener.addheaders = [('X-Forwarded-For', '12.13.14.15')]
    """
    usock=opener.open(url)
    response=usock.read()
    usock.close()
    #if os.path.isfile(COOKIEFILE):
    cj.save(COOKIEFILE, ignore_discard=True)
    return response




def get_video_ad():
	response = getUrlCookie('http://ad.de.doubleclick.net/ad/pushbackde.smartclip/laola1.tv.as3.smartclip/;scadn=0;sccat=adnpbk;scsid=1036492;sz=400x320;dcmt=text/xml;ord='+num_gen(11))
	match_designTheme=re.compile('<adDataURL>(.+?)</adDataURL>').findall(response)
	response = getUrl(match_designTheme[0])
	match_videoPath=re.compile('<videoPath>(.+?)</videoPath>').findall(response)
	match_videoID=re.compile('<videoID>(.+?)</videoID>').findall(response)
	match_videoName=re.compile('<videoName>(.+?)</videoName>').findall(response)
	match_realAdId=re.compile('<realAdId>(.+?)</realAdId>').findall(response)
	match_adId=re.compile('<adId>(.+?)</adId>').findall(response)
	match_videoLength=re.compile('<videoLength>(.+?)</videoLength>').findall(response)

	return match_videoPath[0]+match_videoID[0]+'/fl8_'+match_videoName[0]+'-600.flv?ewadid='+match_realAdId[0]+'&eid='+match_adId[0],match_videoLength[0]

def force_play(url):
	if autoPlay>0:
		xbmc.sleep(autoPlay*1000)
		if xbmc.Player().isPlaying()==True and int(xbmc.Player().getTime())==0:
			xbmc.Player().pause()


def log(message):
	if debug == '1':
		print "#####Laola1 Debug: "+message
	return



def addLinkOld(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addLink(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)##
	ok=True##
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)##
	liz.setInfo( type="Video", infoLabels={ "Title": name } )##
	liz.setProperty('IsPlayable', 'true')##
	liz.setProperty('mimetype', 'video/x-flv')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)##
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
link=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        name=urllib.unquote_plus(params["link"])
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
        INDEX()
       
elif mode==1:
        print ""+url
        TOPICSELECTION(url)
        
elif mode==2:
        print ""+url
        VIDEOSELECTION(url)            

elif mode==3:
        print ""+url
        VIDEOLINKS(url,name)
        
elif mode==4:
        print ""+url
        LIVESELECTION(url)
        
elif mode==5:
        print ""+url
        VIDEOLIVELINKS(url,name)        

elif mode==6:
        print ""+url
        LIVE(url)  

elif mode==10:
        print ""+url
        PLAY_VIDEO(url,name) 

elif mode==11:
        print ""+url
        PLAY_LIVE_1B(url,name) 

  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
