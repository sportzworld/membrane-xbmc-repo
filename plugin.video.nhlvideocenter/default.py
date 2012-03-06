# -*- coding: utf-8 -*-
import urllib,urllib2,re,random,xbmcplugin,xbmcgui
from time import gmtime, strftime

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())

pluginhandle = int(sys.argv[1])


def MAIN():
	addDir('New Videos','&year='+year+'&month='+month,2,'')
	addDir('Interviews','http://video.nhl.com/videocenter/',3,'')
	end_year = 2009
	count_year = int(year)
	while count_year >= end_year:
		addDir(str(count_year),'&year='+str(count_year),1,'')
		count_year -= 1

def MONTH(url):#1
	count_month = 1

	if '2009' in url:
		count_month = 10

	if year in url:
		end_month = int(month.replace('0',''))
		print end_month
	else:
		end_month = 12


	while count_month <= end_month:
		name = str(count_month)
		name = name.replace('12','December')
		name = name.replace('11','November')
		name = name.replace('10','October')
		name = name.replace('1','January')
		name = name.replace('2','February')
		name = name.replace('3','March')
		name = name.replace('4','April')
		name = name.replace('5','May')
		name = name.replace('6','June')
		name = name.replace('7','July')
		name = name.replace('8','August')
		name = name.replace('9','September')



		addDir(name,url+'&month='+str(count_month),2,'')
		count_month += 1


def RESULTS(url):#2     
        req = urllib2.Request('http://video.nhl.com/videocenter/highlights?xml=0'+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<game>(.+?)</game>', re.DOTALL).findall(link)
	for game in match:
		"""
		date = 'DATE'
		guestname = 'GUESTNAME'
		guestcity = 'GUESTCITY'
		guestgoals = 'GUESTGOALS'
		homename = 'HOMENAME'
		homecity = 'MOMECITY'
		homegoals = 'HOMEGOALS'
		url = 'URL'
		possiblethumb = 'POSSIBLETHUMB'
		"""

	        match_date=re.compile('<game-date>(.+?)</game-date>', re.DOTALL).findall(game)

	        match_guest=re.compile('<away-team>(.+?)</away-team>', re.DOTALL).findall(game)
	        match_guest_name=re.compile('<name>(.+?)</name>', re.DOTALL).findall(match_guest[0])
	        match_guest_city=re.compile('<city>(.+?)</city>', re.DOTALL).findall(match_guest[0])
	        match_guest_goals=re.compile('<goals>(.+?)</goals>', re.DOTALL).findall(match_guest[0])

	        match_home=re.compile('<home-team>(.+?)</home-team>', re.DOTALL).findall(game)
	        match_home_name=re.compile('<name>(.+?)</name>', re.DOTALL).findall(match_home[0])
	        match_home_city=re.compile('<city>(.+?)</city>', re.DOTALL).findall(match_home[0])
	        match_home_goals=re.compile('<goals>(.+?)</goals>', re.DOTALL).findall(match_home[0])

	        match_url=re.compile('<alt-video-clip>(.+?)</alt-video-clip>', re.DOTALL).findall(game)

	        match_possiblethumb=re.compile('<video-clip-thumbnail>(.+?)</video-clip-thumbnail>', re.DOTALL).findall(game)

		date = match_date[0]
		guestname = match_guest_name[0]

		try:
			guestcity =  match_guest_city[0]+' '
		except:
			guestcity =  ''

		guestgoals =  match_guest_goals[0]

		homename = match_home_name[0]

		try:
			homecity =  match_home_city[0]+' '
		except:
			homecity =  ''
		homegoals = match_home_goals[0]

		try:
			url = match_url[0]
		except:
	       		match_rtmp=re.compile('<video-clip>(.+?)</video-clip>', re.DOTALL).findall(game)
			url = match_rtmp[0]+' swfurl=http://nhl.cdn.neulion.net/u/videocenter/console.swf swfvfy=true'


		possiblethumb = match_possiblethumb[0]

		date_thumb = date.split('/')
		thumb = ''
		if int(date_thumb[2]) > 2010:
			thumb = possiblethumb
		if int(date_thumb[2]) == 2010 and int(date_thumb[0].replace('0','')) > 8:
			thumb = possiblethumb
		name = date+' '+homecity+homename+' vs. '+guestcity+guestname+' - '+homegoals+':'+guestgoals
		name = name.replace('&#233;','é')
                addLinkOld(name,url,thumb)

def INTERVIEW(url):#3     
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_teams=re.compile('<select onchange="goTeamVideoSite\(this\)">(.+?)</select>', re.DOTALL).findall(link)
	for team in match_teams:
	        match_team=re.compile('<option value="(.+?)">(.+?)</option>', re.DOTALL).findall(team)
		for url,name in match_team:
			url = 'http://video.'+url+'.nhl.com/videocenter'
			name = name
			if name != "NHL":
				addDir(name,url,4,'')

def TEAMS(url):#4   
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        match_css=re.compile('<link rel="stylesheet" type="text/css" href="(.+?)" />').findall(link)
        match_catid=re.compile('catid=(.+?)">(.+?)</a>', re.DOTALL).findall(link)

        req = urllib2.Request(match_css[-1])
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match_bg=re.compile('background-image:url\((.+?)\)').findall(link)

	for catid,name in match_catid:
		if catid != '0':
			print match_bg[0]
			name = name.replace('\n','')
			name = name.replace('	','')
			url2 = url+'/servlets/browse?cid='+catid+'&component=_browse&ispaging=true&large=true&menuChannelId='+catid+'&menuChannelIndex='+'2'+'&pm=0&pn=1&ps=12&ptrs=3'
			#           /servlets/browse?cid=647      &component=_browse&ispaging=true&large=true&menuChannelId=647      &menuChannelIndex=2      &pm=0&pn=1&ps=12&ptrs=3
			addDirFan(name,url2,5,'',match_bg[0])

def VIDEOS(url,name,fanart):#5  
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile("<table title=\"(.+?)\".+?_console.playVideo\('.+?','.+?','(.+?)'.+?src=\"(.+?)\"", re.DOTALL).findall(link)

	for name,url,thumb in match:
		url = url.replace(':','%3A')
		url = url.replace('/','%2F')
		url = url.replace('.','%2E')
		url = url.replace('_','%5F')
		url = url.replace('?','%3F')
		url = url.replace('=','%3D')
		url = url.replace('&','%26')
		url = 'http://video.bruins.nhl.com/videocenter/servlets/encryptvideopath?path=' + url + '&isFlex=true&type=fvod'

                addLink(name,url,6,thumb)

def PLAY(url,name):#6
        req = urllib2.Request('http://video.ducks.nhl.com/videocenter/servlets/browse?cid=647&component=_browse&ispaging=false&large=true&menuChannelId=647&menuChannelIndex=2&pm=0&pn=1&ps=12&ptrs=3')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()


        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	match=re.compile('\[CDATA\[(.+?)\]').findall(link)
	print link
	print match[0]

	item = xbmcgui.ListItem(path=match[0])
	return xbmcplugin.setResolvedUrl(pluginhandle, True, item)


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
        
def addDirFan(name,url,mode,iconimage,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image',fanart)

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
        MONTH(url)
        
elif mode==2:
        print ""+url
        RESULTS(url)

elif mode==3:
        print ""+url
        INTERVIEW(url)

elif mode==4:
        print ""+url
        TEAMS(url)

elif mode==5:
        print ""+url
        VIDEOS(url,name,fanart)

elif mode==6:
        print ""+url
        PLAY(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))
