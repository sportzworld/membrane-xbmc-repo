# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,string,random,cookielib,xbmcvfs


enable_servus = False
enable_fanartdl = True
thumbquality = '1'
pluginhandle = int(sys.argv[1])

__settings__ = xbmcaddon.Addon(id='plugin.video.servushockeynight')
__language__ = __settings__.getLocalizedString


default_fanart = xbmc.validatePath(xbmc.translatePath('special://home')+'/addons/plugin.video.servushockeynight/fanart.jpg')
default_logo = xbmc.validatePath(xbmc.translatePath('special://home')+'/addons/plugin.video.servushockeynight/icon.jpg')
logo = 'http://www.servustv.com/var/stvd/storage/images/www_root/sendungen/servus-hockey-night-del/15737-3-ger-AT/Servus-Hockey-Night-DEL.jpg'
background = 'http://www.servustv.com/var/stvd/storage/images/www_root/themen/sport/9642-68-ger-AT/Sport_stvd_teaser_stage.jpg'
base_laola = 'http://www.laola1.tv/partner/v4player/index.php'
base_servus = 'http://www.servustv.com'

lastrun = '0_0_0' ###TODO!!!
teamnames = { 'Adler':'Adler Mannheim',
              'Bad Nauheim':'Bad Nauheim',#TODO
              'DEG':'Düsseldorfer EG',
              'ESV':'ESV',#TODO
              'Eisbären':'Eisbären Berlin',
              'Eislöwen':'Dresdner Eislöwen',
              'Eispiraten':'Eispiraten Crimmitschau',
              'Freezers':'Hamburg Freezers',
              'Grizzlies':'Grizzly Adams Wolfsburg',
              'Haie':'Kölner Haie',
              'Ice Tigers':'Thomas Sabo Ice Tigers',
              'Ingolstadt':'ERC Ingolstadt',
              'Krefeld':'Krefeld Pinguine',
              'Panther':'Augsburger Panther',
              'Red Bulls':'EHC Red Bull München',
              'Roosters':'Iserlohn Roosters',
              'Tigers':'Straubing Tigers',
              'Wild Wings':'Schwenninger Wild Wings',
			  
              'Black Wings':'EHC Liwest Black Wings Linz',#ok
              'Capitals':'UPC Vienna Capitals',#ok
              'Die Haie':'HC TWK Innsbruck "Die Haie"',#ok
              'Dornbirn':'Dornbirner Eishockey Club',#ok
              'EV Vienna Capitals':'UPC Vienna Capitals',#ok
              'Farjestad':'Farjestad',#TODO
              'Graz 99ers':'Moser Medical Graz 99ers',#ok
              'HCB':'HCB Südtirol',#ok
              'Jesenice':'Jesenice',#TODO
              'KAC':'EC KAC',#ok
              'Olimpija':'HDD Olimpija Ljubljana',#TODO
              'RBS':'EC Red Bull Salzburg',#ok
              'Sapa Fehervar':'Sapa Fehervar AV19',#ok
              'VSV':'EC VSV',#ok
              'Zagreb':'KHL Medveščak Zagreb',
              'Znojmo':'Orli Znojmo'}#ok
#HC Innsbruck#HC Bozen
			  
logos = { 'Adler Mannheim':'http://images.laola1.at/wappen/b3853_100x100.png',
          'Augsburger Panther':'http://images.laola1.at/wappen/b3851_100x100.png',
          'Düsseldorfer EG':'http://images.laola1.at/wappen/b3862_100x100.png',
          'EHC Red Bull München':'http://images.laola1.at/wappen/b5426_100x100.png',
          'Eisbären Berlin':'http://images.laola1.at/wappen/b3856_100x100.png',
          'ERC Ingolstadt':'http://images.laola1.at/wappen/b3863_100x100.png',
          'Grizzly Adams Wolfsburg':'http://images.laola1.at/wappen/b5430_100x100.png',
          'Hamburg Freezers':'http://images.laola1.at/wappen/b3848_100x100.png',
          'Iserlohn Roosters':'http://images.laola1.at/wappen/b3860_100x100.png',
          'Kölner Haie':'http://images.laola1.at/wappen/b3847_100x100.png',
          'Krefeld Pinguine':'http://images.laola1.at/wappen/b3852_100x100.png',
          'Schwenninger Wild Wings':'http://images.laola1.at/wappen/b5431_100x100.png',
          'Straubing Tigers':'http://images.laola1.at/wappen/b5434_100x100.png',
          'Thomas Sabo Ice Tigers':'http://images.laola1.at/wappen/b3858_100x100.png',

          'Dornbirner Eishockey Club':'http://www.erstebankliga.at/images/pages/teams/logos/dec.png',#ok
          'UPC Vienna Capitals':'http://www.erstebankliga.at/images/pages/teams/logos/vic.png',#ok
          'EC Red Bull Salzburg':'http://www.erstebankliga.at/images/pages/teams/logos/rbs.png',#ok
          'EC KAC':'http://www.erstebankliga.at/images/pages/teams/logos/kac.png',#ok
          'EC VSV':'http://www.erstebankliga.at/images/pages/teams/logos/vsv.png',#ok
          'EHC Liwest Black Wings Linz':'http://www.erstebankliga.at/images/pages/teams/logos/ehl.png',#ok
          'Moser Medical Graz 99ers':'http://www.erstebankliga.at/images/pages/teams/logos/g99.png',#ok
          'HC TWK Innsbruck "Die Haie"':'http://www.erstebankliga.at/images/pages/teams/logos/hci.png',#ok
          'HCB Südtirol':'http://www.erstebankliga.at/images/pages/teams/logos/hcb.png',#ok
          'Orli Znojmo':'http://www.erstebankliga.at/images/pages/teams/logos/zno.png',
          'Sapa Fehervar AV19':'http://www.erstebankliga.at/images/pages/teams/logos/avs.png',#ok
          'HDD Olimpija Ljubljana':'http://www.erstebankliga.at/images/pages/teams/logos/oll.png',
          '13':'',
          '13':''}
		  
def checklastrun():
	if __settings__.getSetting('lastrun') != '0_0_1':
		__settings__.setSetting('lastrun','0_0_1')
		if enable_fanartdl:
			if xbmcvfs.exists(default_fanart) == False:
				buffer = getUrl(background)
				file = default_fanart
				f = xbmcvfs.File(file, 'w')
				result = f.write(buffer)
				f.close()
			"""
			if xbmcvfs.exists(default_logo) == False:
				buffer = getUrl(logo)
				file = default_logo
				f = xbmcvfs.File(file, 'w')
				result = f.write(buffer)
				f.close()
			"""


vod_quality = __settings__.getSetting('vod_quality')
if vod_quality == '0':
	max_bw = 350000
elif vod_quality == '1':
	max_bw = 600000
elif vod_quality == '2':
	max_bw = 1500000
elif vod_quality == '3':
	max_bw = 9999999




def MAIN():
	checklastrun()
	addDir(__language__(30500),'del',1,default_logo)
	addDir(__language__(30501),'ebel',1,default_logo)
	
	
def LIGA(name,url):#1
	addDir(__language__(30502),base_laola+'?identifier=servustv_'+url+'&menu1=16&menu2=&menu3=',3,default_logo)
	addDir(__language__(30503),base_laola+'?identifier=servustv_'+url+'&menu1=86&menu2=&menu3=',3,default_logo)
	addDir(__language__(30504),url,2,default_logo)
	if url == 'del':
		addDir(__language__(30513),base_laola+'?identifier=servustv_del&menu1=92&menu2=&menu3=',4,default_logo)#top tore
		addDir(__language__(30514),base_laola+'?identifier=servustv_del&menu1=98&menu2=&menu3=',4,default_logo)#starting six
		addDir(__language__(30515),base_laola+'?identifier=servustv_del&menu1=101&menu2=&menu3=',4,default_logo)#Glaskugel
		addDir(__language__(30516),base_laola+'?identifier=servustv_del&menu1=104&menu2=&menu3=',4,default_logo)#hangouts
		addDir(__language__(30505),base_laola+'?identifier=servustv_del&menu1=164&menu2=&menu3=',4,default_logo)
		addDir(__language__(30506),base_laola+'?identifier=delorg&menu1=33&menu2=&menu3=',4,default_logo)
		addDir(__language__(30507),base_laola+'?identifier=delorg&menu1=&menu2=1868&menu3=',4,default_logo)
	elif url == 'ebel':
		addDir(__language__(30508),base_laola+'?identifier=servustv_ebel&menu1=89&menu2=&menu3=',4,default_logo)
		addDir(__language__(30509),base_laola+'?identifier=servustv_ebel&menu1=77&menu2=&menu3=',4,default_logo)
		addDir(__language__(30510),base_laola+'?identifier=servustv_ebel&menu1=92&menu2=&menu3=',4,default_logo)
		addDir(__language__(30511),base_laola+'?identifier=servustv_ebel&menu1=74&menu2=&menu3=',4,default_logo)
		addDir(__language__(30512),base_laola+'?identifier=erstebankehl&menu1=128&menu2=&menu3=',4,default_logo)
		addDir(__language__(30506),base_laola+'?identifier=erstebankehl&menu1=33&menu2=&menu3=',4,default_logo)
		addDir(__language__(30507),base_laola+'?identifier=erstebankehl&menu1=&menu2=1868&menu3=',4,default_logo)

	
	if enable_servus:
		if name == 'DEL':
			url = base_servus+'/de/Themen/Sport/DEL/Videos2'
		elif name == 'EBEL':
			url = base_servus+'/de/Themen/Sport/EBEL/Videos'
		response=getUrl(url)
		match=re.compile('<h2 class="ato headline headline-link section-large">.+?href="(.+?)" >(.+?)</a>', re.DOTALL).findall(response)
		for url,name in match:
			name = name.replace('            ','')
			name = name.replace('\n','')
			if not 'Alle Videos' in name:
				addDirServus(name,base_servus+url,'')

	
def TEAMS(url):#2
	response=getUrl(base_laola+'?identifier=servustv_'+url+'&menu1=&menu2=&menu3=')
	match_teams=re.compile('Teams</a>(.+?)</ul>', re.DOTALL).findall(response)
	match=re.compile('<a href="(.+?)" title="(.+?)">', re.DOTALL).findall(match_teams[0])
	for url,team in match:
		if team != 'Alle' and not ',' in url:
			if team in teamnames:
				team=teamnames[team]
			if team in logos:
				logo=logos[team]
			else:
				logo=default_logo
			addDir(team,base_laola+url,4,logo)
	
def LIST_LAOLA_EXTRA(url):#3
	LIST_LAOLA(url,False)
	#LIST_LAOLA(url,True)
	
def LIST_LAOLA(url,extrainfo=False):#4
	response=getUrl(url)
	match_table=re.compile('<table cellpadding="0" cellspacing="0">(.+?)</table>', re.DOTALL).findall(response)
	print match_table[0]
	match=re.compile('<a href="(.+?)">(.+?)</a>.+?<span class="date">, (.+?)</span>', re.DOTALL).findall(match_table[0])
	i = 0
	for url,name,date in match:
		if i < 100:
			tmp = url.split('=')
			id = tmp[-1]
			if thumbquality == '1':
				thumb = 'http://images.laola1.tv/'+id+'_396x223.jpg'
			elif thumbquality == '2':
				thumb = 'http://images.laola1.tv/'+id+'_798x449.jpg'
			else:
				thumb = default_logo
			i = i + 1
		else:
			thumb = default_logo
		if extrainfo:
			name_list=name.split('/')#TODO: conferences
			for name in name_list:
				if ' - ' in name:
					home_name,guest_name=name.split(' - ')
					home_name.replace('Relive: ','')
					guest_name.replace('Relive: ','')
					
					if home_name in logos:
						home_logo = logos[home_name]
					else:
						home_logo = default_logo
						
					if guest_name in logos:
						guest_logo = logos[guest_name]
					else:
						guest_logo = default_logo
					addLink(date+' - '+name.replace('Relive: ',''),base_laola+url,10,thumb,'',True,True,'','',home_name,guest_name,home_logo,guest_logo)
		else:
			addLink(date+' - '+name.replace('Relive: ',''),base_laola+url,10,thumb)
		
			



def PLAY(url,name):#10
	dialog = xbmcgui.DialogProgress()
	dialog.create(__language__(30610), __language__(30611))
	dialog.update(0)
	
	response=getUrl(url)

	if 'Dieser Stream beginnt' in response:
		dialog.update(100, __language__(30616))

		log('Video has not jet started')
		match_big=re.compile('<big>(.+?)</big>', re.DOTALL).findall(response)
		xbmc.executebuiltin("Notification("+__language__(30602)+","+match_big[0].replace(',',' -')+", 7000)")
		dialog.close()
		return

	dialog.update(25, __language__(30612))
	match_player=re.compile('<iframe(.+?)src="(.+?)"', re.DOTALL).findall(response)
	for iframestuff,possible_player in match_player:
		if 'class="main_tv_player"' in iframestuff:
			player = possible_player
	response=getUrl(player)
	
	match_streamid=re.compile('streamid: "(.+?)"', re.DOTALL).findall(response)
	streamid = match_streamid[0]
	
	match_partnerid=re.compile('partnerid: "(.+?)"', re.DOTALL).findall(response)
	partnerid = match_partnerid[0]

	match_portalid=re.compile('portalid: "(.+?)"', re.DOTALL).findall(response)
	portalid = match_portalid[0]

	match_sprache=re.compile('sprache: "(.+?)"', re.DOTALL).findall(response)
	sprache = match_sprache[0]

	match_auth=re.compile('auth = "(.+?)"', re.DOTALL).findall(response)
	auth = match_auth[0]
	
	match_v5ident=re.compile('v5ident = "(.+?)"', re.DOTALL).findall(response)
	v5ident = match_v5ident[0]

	match_timestamp=re.compile('timestamp = "(.+?)"', re.DOTALL).findall(response)
	timestamp = match_timestamp[0]

	response=getUrl('http://www.laola1.tv/server/hd_video.php?play='+streamid+'&partner='+partnerid+'&portal='+portalid+'&v5ident='+v5ident+'&lang='+sprache)
	match_url=re.compile('<url>(.+?)<', re.DOTALL).findall(response)

	response=getUrl(match_url[0].replace('&amp;','&').replace('l-_a-','l-L1TV_a-l1tv')+'&timestamp='+timestamp+'&auth='+auth)

	dialog.update(50, __language__(30613))
	"""
	response=getUrl(match_m3u8[0])
	match_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)
	match_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
	res_url=match_url[0].replace('l-_a-','l-L1TV_a-l1tv')
	
	m3u8_url = res_url+'?hdnea='+match_auth[0]+'&g='+char_gen(12)+'&hdcore=3.1.0'
	"""
	match_new_auth=re.compile('auth="(.+?)"', re.DOTALL).findall(response)
	match_new_url=re.compile('url="(.+?)"', re.DOTALL).findall(response)

	m3u8_url = match_new_url[0].replace('/z/','/i/').replace('manifest.f4m','master.m3u8')+'?hdnea='+match_new_auth[0]+'&g='+char_gen(12)+'&hdcore=3.2.0'
	try:
		dialog.update(75, __language__(30614))
		response=getUrl(m3u8_url)
		dialog.update(100, __language__(30615))
		match_sec_m3u8=re.compile('http(.+?)null=', re.DOTALL).findall(response)
		quality = int(__settings__.getSetting('vod_quality'))+1
		
		choose_url = False
		stored_bw = 0
		lines = response.split('\n')
		for line in lines:
			if '#EXT-X-STREAM-INF' in line:
				match_bw=re.compile('BANDWIDTH=(.+?),', re.DOTALL).findall(line)
				bw = int(match_bw[0])
				if bw > stored_bw and bw <= max_bw:
					choose_url = True
					stored_bw = bw

			elif choose_url == True:
				sec_m3u8 = line
				choose_url = False

		listitem = xbmcgui.ListItem(path=sec_m3u8)
		dialog.close()
		return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
		

	except:
		log('Error: Video not found')

	dialog.close()
	
def make_pretty(name):
	name = name.replace('&auml;','ä')
	name = name.replace('&Auml;','Ä')
	name = name.replace('&ouml;','ö')
	name = name.replace('&Ouml;','Ö')
	name = name.replace('&uuml;','ü')
	name = name.replace('&Uuml;','Ü')
	name = name.replace('&szlig;','ß')
	return name
	
def log(message):
	if __settings__.getSetting('debug') == 'true':
		try:
			print "#####Servus Hockey Night Debug: "+message.encode('ascii', 'ignore')
		except:
			print "#####Servus Hockey Night: Debug function failed thanks to unicode from HELL"
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


def addLink(name,url,mode,iconimage,plot='',hd=False,extrainfo=False,home_city='',guest_city='',home_name='',guest_name='',home_logo='',guest_logo='',home_score='',guest_score='',game_dd='',game_mm='',game_yyyy=''):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	if extrainfo:
		liz.setInfo( type="Video", infoLabels={ "Title": name , "Plot": plot, "plotoutline": plot , "home_city": home_city , "guest_city": guest_city , "home_name": home_name , "guest_name": guest_name , "home_logo": home_logo , "guest_logo": guest_logo , "home_score": home_score , "guest_score": guest_score , "game_dd": game_dd , "game_mm": game_mm , "game_yyyy": game_yyyy } )
		print home_name
		print guest_name
		print home_logo
		print guest_logo
	else:
		liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot, "plotoutline": plot  } )
	
	liz.setProperty('IsPlayable', 'true')
	if __settings__.getSetting('useasfanart') == 'true':
		liz.setProperty('fanart_image',iconimage)
	else:
		liz.setProperty('fanart_image',background)
	if hd:
		liz.addStreamInfo('video', { 'Codec': 'h264', 'Width' : 1280 })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
	return ok
	

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',background)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirServus(name,url,iconimage):
        u='plugin://plugin.video.servustv_com/'+"?url="+urllib.quote_plus(url)+"&mode=listVideos"
        print u
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',background)
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
        LIGA(name,url)

elif mode==2:
        print ""+url
        TEAMS(url)
		
elif mode==3:
        print ""+url
        LIST_LAOLA_EXTRA(url)

elif mode==4:
        print ""+url
        LIST_LAOLA(url)

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
