#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import xbmc
import re
import resources.lib.utils as utils
import xbmcaddon
import HTMLParser
addonID = 'plugin.video.ardmediathek_de'
addon = xbmcaddon.Addon(id=addonID)
subFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/sub.srt")
baseUrl = "http://www.ardmediathek.de"
coloredSubtitles = addon.getSetting("coloredSubtitles") == "true"
	
def setSubtitle(uri,offset=0):
	#if offset != 0:
	#	print offset
	if uri.startswith('/subtitle'):
		_newSubtitle(baseUrl+uri)
	else:
		_oldSubtitle(baseUrl+uri)

def _newSubtitle(url):
	if os.path.exists(subFile):
		os.remove(subFile)
	try:
		content = utils.getUrl(url)
	except:
		content = ""
	if content:
		dict = _stylesSetup(re.compile('<tt:styling>(.+?)</tt:styling>', re.DOTALL).findall(content)[0])
		div = re.compile('<tt:div.+?>(.+?)</tt:div>', re.DOTALL).findall(content)[0]
		fh = open(subFile, 'a')
		parts = div.split('</tt:p>')
		count = 1
		for part in parts:
			if '<tt:span' in part:
				text = ''
				buffer = ''
				if count > 1:
					buffer += '\n'
				buffer += str(count)+'\n'
				part = part.replace('\nend=','end=')
				for line in part.split('\n'):
					if line.strip().startswith('<tt:p'):
						line = line.replace('begin="1','begin="0').replace('end="1','end="0')
						begin = re.compile('begin="(.+?)"').findall(line)[-1]
						begin = begin.replace(".",",")[:-1]
						end = re.compile('end="(.+?)"').findall(line)[-1]
						end = end.replace(".",",")[:-1]
					elif line.strip().startswith('<tt:span'):
						span = re.compile('<tt:span(.+?)>').findall(line)[0]
						t = _cleanTitle(re.compile('>(.+?)<').findall(line)[0], False)
						if 'style=' in span:
							style = re.compile('style="(.+?)"').findall(span)[0]
							if dict[style]:
								t = '<font color="'+dict[style]+'">'+t+'</font>'
						text += t + '\n'
				buffer += begin+" --> "+end+"\n" + text
				fh.write(buffer)
				count+=1

		fh.close()
		xbmc.sleep(1000)
		xbmc.Player().setSubtitles(subFile)

def _oldSubtitle(url):
	if os.path.exists(subFile):
		os.remove(subFile)
	try:
		content = utils.getUrl(url)
	except:
		content = ""
	if content:
		dict = _stylesSetup(re.compile('<styling>(.+?)</styling>', re.DOTALL).findall(content)[0])
		matchLine = re.compile('<p id=".+?" begin="1(.+?)" end="1(.+?)".+?style="(.+?)">(.+?)</p>', re.DOTALL).findall(content)
		fh = open(subFile, 'a')
		count = 1
		for begin, end, style, line in matchLine:
			begin = "0"+begin.replace(".",",")[:-1]
			end = "0"+end.replace(".",",")[:-1]
			text = ''
			line = line.replace("<br />","\n")
			s = line.split('<')
			for entry in s:
				if entry.startswith('span'):
					if 'tts:color' in entry.split('>')[0]:
						color = re.compile('tts:color="(.+?)"', re.DOTALL).findall(entry.split('>')[0])[0]
						text += '<font color="'+color+'">'+entry.split('>')[1]+'</font>'
					elif dict[style]:
						text += '<font color="'+dict[style]+'">'+entry.split('>')[1]+'</font>'
				elif entry.startswith('/span'):
					if dict[style]:
						text += '<font color="'+dict[style]+'">'+entry.split('>')[1]+'</font>'
					else:
						text += entry.split('>')[1]
				#elif len(entry.split('>')) > 1:
				elif len(entry.split('>')) > 1:
					if dict[style]:
						text += '<font color="'+dict[style]+'">'+entry.split('>')[1]+'</font>'
					else:
						text += entry.split('>')[1]
				else:
					if dict[style]:
						text += '<font color="'+dict[style]+'">'+entry+'</font>'
					else:
						text += entry

			fh.write(str(count)+"\n"+begin+" --> "+end+"\n"+_cleanTitle(text)+"\n\n")
			count+=1
		fh.close()
		xbmc.sleep(1000)
		xbmc.Player().setSubtitles(subFile)
"""	
def _oldSubtitle(url):
	if os.path.exists(subFile):
		os.remove(subFile)
	try:
		content = utils.getUrl(url)
	except:
		content = ""
	if content:
		dict = _stylesSetup(re.compile('<styling>(.+?)</styling>', re.DOTALL).findall(content)[0])
		matchLine = re.compile('<p id=".+?" begin="1(.+?)" end="1(.+?)".+?style="(.+?)">(.+?)</p>', re.DOTALL).findall(content)
		fh = open(subFile, 'a')
		count = 1
		for begin, end, style, line in matchLine:
			begin = "0"+begin.replace(".",",")[:-1]
			end = "0"+end.replace(".",",")[:-1]
			match = re.compile('<span(.+?)>', re.DOTALL).findall(line)
			for span in match:
				line = line.replace("<span"+span+">","")
			line = line.replace("<br />","\n").replace("</span>","").strip()
			if dict[style]:
				line = '<font color="'+dict[style]+'">'+line+'</font>'
			fh.write(str(count)+"\n"+begin+" --> "+end+"\n"+_cleanTitle(line)+"\n\n")
			count+=1
		fh.close()
		xbmc.sleep(1000)
		xbmc.Player().setSubtitles(subFile)
"""	
def _stylesSetup(styles):
	dict = {}
	styles = styles.replace('tt:','').replace('xml:','')
	match_styles = re.compile('<style(.+?)>', re.DOTALL).findall(styles)
	for style in match_styles:
		id = re.compile('id="(.+?)"', re.DOTALL).findall(style)[0]
		if 'color=' in style and coloredSubtitles:
			color = re.compile('color="(.+?)"', re.DOTALL).findall(style)[0]
		else:
			color = False
		dict[id] = color
	return dict


def _cleanTitle(title,html=True):
	if html:
		title = HTMLParser.HTMLParser().unescape(title)
		return title.encode("utf-8")
	else:
		title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
		title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
		title = title.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
		title = title.replace("&apos;","'").strip()
		return title