# -*- coding: utf8 -*-

import urllib,urllib2,re,xbmcplugin,xbmcgui

pluginhandle = int(sys.argv[1])

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

#xip = xbmcplugin.getSetting(pluginhandle,"ip")
#print 'xip: '+xip
                       
#if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#	print 'laola: use trick'



def INDEX():
        addDir('Live',livestream_url,4,'')

        response = get_url(videos_url)

        match=re.compile('<div id="sitemap"><a (.+?)</div>').findall(response)

        for something in match:
                match1=re.compile('href="(.+?)".*?>(.+?)</a>').findall(something)
                for url,name in match1 or match2:
                        addDir(name,url,1,'')



def TOPICSELECTION(url):
	response = get_url(url)

        match=re.compile("<td style=\".+?\" width=\".+?\"><h2><a href=\"(.+?)\" style=\".+?\">(.+?)</a></h2></td>").findall(response) 

        for url,name in match:
                addDir(name,url,2,'')

                

def VIDEOSELECTION(url):
	response = get_url(url)

        match1=re.compile('<div class="teaser_bild_video" title=".+?"><a href="(.+?)"><img src="(.+?)" border=".+?" /></a></div>.+?<div class="teaser_head_video" title=".+?">(.+?)</div>.+?<div class="teaser_text" title=".+?"><a href=".+?>(.+?)</a>', re.DOTALL).findall(response)

        match2=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(response)

        for url,thumbnail,date,name in match1:
                addLink(date+' - '+name,url,3,thumbnail)

        for url in match2:
                addDir('Next Site',url,2,'')



def get_playkeys(url):
	log("GET playkey1,playkey2")

	response = get_url(url)
	playkeys=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(response)

	for playkey1,playkey2 in playkeys:
		log('playkey1: "'+playkey1+'"')
		log('playkey2: "'+playkey2+'"')

	return playkeys

def VIDEOLINKS(url,name):
	pageurl = url #this is messy

	playkeys = get_playkeys(url)

	for playkey1,playkey2 in playkeys:
		playkey1 = playkey1
		playkey2 = playkey2
	

	log('GET streamquality,server,servertype,playpath,title')
	response = get_url('http://www.laola1.tv/server/ondemand_xml_esi.php?playkey='+playkey1+'-'+playkey2)

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
	response = get_url('http://streamaccess.laola1.tv/flash/vod/22/'+playkey1+'_'+streamquality+'.xml')

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
	response = get_url('http://'+server+'/fcs/ident')

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

                match2=re.compile("<a href=\"(.+)\" class=\"teaser_text\">vor</a>").findall(link)
	        for url,thumbnail,date,name in match1:
#                for url,thumbnail,date,name in match1:
                        addLink(date+' - '+name,url,5,thumbnail)
                for url in match2:
                        addDir('Next Site',url,4,'')


def VIDEOLIVELINKS(url,name):
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
	match_ready=re.compile('Dieser Stream beginnt am (.+?), (.+?) um (.+?) Uhr CET.').findall(link)
	for weekday,date,time in match_ready:
		#xbmcplugin.getSetting(pluginhandle,"streamquality") == '1':
		xbmc.executebuiltin("Notification(Livestream has not started,This stream starts on "+weekday+", "+date+" at "+time+" CET,14000)")
		return

	match_streamtype=re.compile('"src", "(.+?)"').findall(link)
        match_playkey=re.compile('"playkey=(.+?)-(.+?)&adv.+?"').findall(link)

	if match_streamtype[0] == 'http://www.laola1.tv/swf/hdplayer':

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

                        item = xbmcgui.ListItem(path=match_http[0]+match_quality[-1])

			return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

		print 'laola: use streamtype 1b'
		match_live_1b=re.compile('isLiveStream=true&videopfad=(.+?)&sendeerkennung').findall(link)
		req = urllib2.Request(match_live_1b[0])
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#		if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#			req.add_header('X-Forwarded-For', xip)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		#print link


		match_rtmp=re.compile('<meta name="rtmpPlaybackBase" content="(.+?)" />').findall(link)
		match_http=re.compile('<meta name="httpBase" content="(.+?)" />').findall(link)
		match_quality=re.compile('<video src="(.+?)" system-bitrate=".+?"/>').findall(link)

##http://sportsmanlive-f.akamaihd.net/khl_2_1_450@s7077?primaryToken=1327601291_6d4b5709d7c7b8c364cad2036168a57a&p=1&e=74022&i=&q=&k=&c=DE&a=&u=&t=&l=&v=2.4.5&fp=LNX%2010,3,162,29&r=UEEBM&g=UICJXUGLJHOM
		http = match_http[0].replace("&i=&q=&k=&c=DE&a=&u=&t=&l=","&i=&q=&k=&c=DE&a=&u=&t=&l=&v=2.4.5&fp=LNX%2010,3,162,29&r=UEEBM&g=UICJXUGLJHOM")

                if livequality == '0':
			video = match_quality[0]
                if livequality == '1':
			video = match_quality[1]
                if livequality == '2':
			video = match_quality[-1]

		item = xbmcgui.ListItem(path=http+video)

		return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


#        match_over=re.compile('<p>Lieber LAOLA(.+?)-User,</p>').findall(link)
#        if match_over[0] == '1':
#                addDir('vorbei/zu frueh',' ',5,'')
        ##"playkey=47060-Gut1cOWmlyix.&adv=laola1.tv/de/eishockey/ebel&adi=laola1.tv/de/eishockey/ebel&aps=Video1&szo=eishockey&deutschchannel=true&channel=222&teaser=1153&play=47060&fversion=player.v10.2"
	else:        
		print 'laola: use streamtype 2'
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


def get_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
#	if xbmcplugin.getSetting(pluginhandle,"inside") == 'false':
#		print 'Try to use X-Forwarded-For trick'
#		req.add_header('X-Forwarded-For', xip)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	return link


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
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
