# -*- coding: utf-8 -*-
import urllib,urllib2,re,random,xbmcplugin,xbmcgui
from time import gmtime, strftime

month = strftime("%m", gmtime())
year = strftime("%Y", gmtime())



def YEAR():
	addDir('New Videos','&year='+year+'&month='+month,2,'')
	end_year = 2005
	count_year = int(year)
	while count_year >= end_year:
		addDir(str(count_year),'&year='+str(count_year),1,'')
		count_year -= 1

def MONTH(url):#1
	if year in url:
		end_month = int(month.replace('0',''))
		print end_month
	else:
		end_month = 12

	count_month = 1
	print count_month
	print end_month
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
	print 'http://video.nhl.com/videocenter/highlights?xml=0'+'&year='+year+'&month='+month
        req = urllib2.Request('http://video.nhl.com/videocenter/highlights?xml=0'+url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        print link
        match=re.compile('<game>.+?<game-date>(.+?)</game-date>.+?<name>(.+?)</name>.+?<city>(.+?)</city>.+?<goals>(.+?)</goals>.+?<name>(.+?)</name>.+?<city>(.+?)</city>.+?<goals>(.+?)</goals>.+?<alt-video-clip>(.+?)</alt-video-clip>.+?<video-clip-thumbnail>(.+?)</video-clip-thumbnail>.+?</game>', re.DOTALL).findall(link)
        for date,guestname,guestcity,guestgoals,homename,homecity,homegoals,url,thumb in match:
		name = date+' '+homecity+' '+homename+' vs. '+guestcity+' '+guestname+' - '+homegoals+':'+guestgoals
		name = name.replace('&#233;','é')
                addLink(name,url,thumb)

                
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
        YEAR()

elif mode==1:
        print ""+url
        MONTH(url)
        
elif mode==2:
        print ""+url
        RESULTS(url)



xbmcplugin.endOfDirectory(int(sys.argv[1]))
