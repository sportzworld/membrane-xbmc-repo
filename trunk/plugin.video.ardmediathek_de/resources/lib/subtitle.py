#!/usr/bin/python
# -*- coding: utf-8 -*-import os
import xbmc
import re
import resources.lib.utils as utils
addonID = 'plugin.video.ardmediathek_de'
subFile = xbmc.translatePath("special://profile/addon_data/"+addonID+"/sub.srt")
	
def setNewSubtitle(url):
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
				for line in part.split('\n'):
					if line.strip().startswith('<tt:p'):
						line = line.replace('begin="1','begin="0').replace('end="1','end="0')
						begin = re.compile('begin="(.+?)"').findall(line)[-1]
						begin = begin.replace(".",",")[:-1]
						end = re.compile('end="(.+?)"').findall(line)[-1]
						end = end.replace(".",",")[:-1]
					elif line.strip().startswith('<tt:span'):
						span = re.compile('<tt:span(.+?)>').findall(line)[0]
						t = cleanTitle(re.compile('>(.+?)<').findall(line)[0])
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
"""
def setSubtitle(url):
	if os.path.exists(subFile):
		os.remove(subFile)
	try:
		content = utils.getUrl(url)
	except:
		content = ""
	if content:
		matchLine = re.compile('<p id=".+?" begin="1(.+?)" end="1(.+?)".+?>(.+?)</p>', re.DOTALL).findall(content)
		fh = open(subFile, 'a')
		count = 1
		for begin, end, line in matchLine:
			begin = "0"+begin.replace(".",",")[:-1]
			end = "0"+end.replace(".",",")[:-1]
			match = re.compile('<span(.+?)>', re.DOTALL).findall(line)
			for span in match:
				line = line.replace("<span"+span+">","")
			line = line.replace("<br />","\n").replace("</span>","").strip()
			fh.write(str(count)+"\n"+begin+" --> "+end+"\n"+cleanTitle(line)+"\n\n")
			count+=1
		fh.close()
		xbmc.sleep(1000)
		xbmc.Player().setSubtitles(subFile)
"""		
def _stylesSetup(styles):
	dict = {}
	match_styles = re.compile('<tt:style(.+?)>', re.DOTALL).findall(styles)
	for style in match_styles:
		id = re.compile('xml:id="(.+?)"', re.DOTALL).findall(style)[0]
		if 'tts:color=' in style:
			color = re.compile('tts:color="(.+?)"', re.DOTALL).findall(style)[0]
		else:
			color = False
		dict[id] = color
	return dict


def cleanTitle(title):
    title = title.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#034;", "\"").replace("&#039;", "'").replace("&quot;", "\"").replace("&szlig;", "ß").replace("&ndash;", "-")
    title = title.replace("&Auml;", "Ä").replace("&Uuml;", "Ü").replace("&Ouml;", "Ö").replace("&auml;", "ä").replace("&uuml;", "ü").replace("&ouml;", "ö").replace("&eacute;", "é").replace("&egrave;", "è")
    title = title.replace("&#x00c4;","Ä").replace("&#x00e4;","ä").replace("&#x00d6;","Ö").replace("&#x00f6;","ö").replace("&#x00dc;","Ü").replace("&#x00fc;","ü").replace("&#x00df;","ß")
    title = title.replace("&apos;","'").strip()
    return title