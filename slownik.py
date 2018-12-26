#!/usr/bin/env python
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import urllib.request as urllib2
import re
from subprocess import *
import sys

class MyHTMLParser(HTMLParser):

   #Initializing lists
   lsStartTags = list()
   lsEndTags = list()
   lsStartEndTags = list()
   lsComments = list()

   #HTML Parser Methods
   def handle_starttag(self, startTag, attrs):
       self.lsStartTags.append(startTag)

   def handle_endtag(self, endTag):
       self.lsEndTags.append(endTag)

   def handle_startendtag(self,startendTag, attrs):
       self.lsStartEndTags.append(startendTag)

   def handle_comment(self,data):
       self.lsComments.append(data)

#creating an object of the overridden class
parser = MyHTMLParser()

#zamiana polskich znakow na hex unicode

unicode_hex = { "ą":"%C4%85",
                "ż":"%C5%BC",
                "ź":"%C5%BA",
                "ć":"%C4%87",
                "ń":"%C5%84",
                "ł":"%C5%82",
                "ó":"%C3%B3",
                "ę":"%C4%99",
                "ś":"%C5%9B" }
lista_fraz = []
lista_fraz = lista_fraz + sys.argv
lista_fraz = lista_fraz[1:]
for k in unicode_hex:
    fraz = [f.replace(k,unicode_hex[k]) for f in lista_fraz] #aby strona mogła odczytać polskie znaki

html_page = html_page = urllib2.urlopen("http://www.sjp.pl/"+'+'.join(fraz))

#Wyrażenie regularne
regex = re.findall('<p style="margin:.*?;?">(?:.|[żźćńółęąśŻŹĆĄŚĘŁÓŃ])*?(?<=<\/p>)',str(html_page.read()));

utf_8bytes = {"\\xc3\\x93":"Ó","\\xc3\\xb3":"ó","\\xc4\\x84":"Ą","\\xc4\\x85":"ą","\\xc4\\x86":"Ć","\\xc4\\x87":"ć","\\xc4\\x98":"Ę","\\xc4\\x99":"ę","\\xc5\\x81":"Ł","\\xc5\\x82":"ł","\\xc5\\x83":"Ń","\\xc5\\x84":"ń","\\xc5\\x9a":"Ś","\\xc5\\x9b":"ś","\\xc5\\xb9":"Ź","\\xc5\\xba":"ź","\\xc5\\xbb":"Ż","\\xc5\\xbc":"ż"}

if not regex:
    print ("\'" + ' '.join(lista_fraz) +'\'' + " nie występuje w słowniku.")
else:
    #Pętla zamieniająca slashe na polskie znaki bez zamiany listy w string
    for klucz in utf_8bytes:
        regex=[w.replace(klucz,utf_8bytes[klucz]) for w in regex];
    regex=[w.replace("<br />",'\n') for w in regex];
    regex=[w.replace("&quot;",'\"') for w in regex]
    str1 = ''.join(regex); #zamiana list w string
    str1 = str1[str1.index('>')+1:]
    str1 = str1[:str1.index('<')]
    fraza = ' '.join(lista_fraz) #zamiana listy fraz w string
    print("\t\t\t\t"+fraza.title()+"\n\n"+str1)
