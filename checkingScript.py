"""
------------------------------------------------------------
checkScript.py
------------------------------------------------------------
This script checks the .txt files in a specified folder for
proper preprocessing before they are uploaded for
annotation.

Each .txt file is scanned to identify any missing opening or
closing tags e.g. <section></section>

After that, each .txt file is scanned to identify any
excessively long sentences (>30 words).

Run using
  python checkingScript.py <folder>
  python checkingScript.py <textfile>
where <folder> is the relative folder address terminated
with a forward slash (/) and <textfile> is the textfile name
terminated with ".txt".
------------------------------------------------------------
"""

import os
import re

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
  if len(sys.argv)==2:
    inputFile = sys.argv[1]
    if inputFile[-4:]==".txt": processSingleFile(inputFile)
    elif inputFile[-1]=="/": processMultipleFiles(inputFile)
    else: error()
  else: error()

def error():
    print ""
    print "Usage: checkingScript.py textfile"
    print "Usage: checkingScript.py folder"
    print ""
    print "Please make sure that textfile names are terminated with '.txt'."
    print "Please make sure that folder names are terminated with a forward slash (/)."
    print ""

def processMultipleFiles(folder):
  for row in os.listdir(folder):
    if row[-4:]==".txt":
      filename = folder+row
      processSingleFile_tagtest(filename)
  #for row in os.listdir(folder):
  #  if row[-4:]==".txt":
  #    filename = folder+row
  #    processSingleFile_wordlengthtest(filename)

def processSingleFile_tagtest(file1):

  #inputFile = sys.argv[1]
  #if inputFile[-1]

  #file1 = 'Faces_Ghost_RAT.txt'
  #file1 = 'From-Bahrain-With-Love-FinFishers-Spy-Kit-Exposed-2.txt'
  #file1 = 'guide1.txt'
  text = []
  textholder = ""

  with open(file1,'r') as f:
    for line in f:
      text.append(line)
      textholder+=line

  title = "="*len(file1)+"\n"+file1+"\n"+"="*len(file1)
  print title

  tagTest(text,'<doc>','</doc>')
  tagTest(text,'<toc>','</toc>')
  tagTest(text,'<cover>','</cover>')
  tagTest(text,'<section>','</section>')
  tagTest(text,'<heading>','</heading>')
  tagTest(text,'<figure>','</figure>')
  tagTest(text,'<caption>','</caption>')
  tagTest(text,'<code>','</code>')
  tagTest(text,'<table>','</table>')
  tagTest(text,'<fn>','</fn>')
  tagTest(text,'<footnote>','</footnote>')
  tagTest(text,'<header>','</header>')
  tagTest(text,'<footer>','</footer>')
  tagTest(text,'<noncontent>','</noncontent>')
  tagTest(text,'<box>','</box>')
  tagTest(text,'<list>','</list>')

def processSingleFile_wordlengthtest(file1):

  #inputFile = sys.argv[1]
  #if inputFile[-1]

  #file1 = 'Faces_Ghost_RAT.txt'
  #file1 = 'From-Bahrain-With-Love-FinFishers-Spy-Kit-Exposed-2.txt'
  #file1 = 'guide1.txt'
  text = []
  textholder = ""

  with open(file1,'r') as f:
    for line in f:
      text.append(line)
      textholder+=line

  title = "="*len(file1)+"\n"+file1+"\n"+"="*len(file1)
  print title

  textholder = removeIrrelevant(textholder)
  wordLengthTest(textholder)

def tagTest(text,startTag,endTag):
  startTagLines = []
  endTagLines = []
  startTagRE = re.compile(startTag)
  endTagRE = re.compile(endTag)
  for lineNo,line in enumerate(text):
    if re.sub(startTagRE,'',line)!=line: startTagLines.append(lineNo+1)
    if re.sub(endTagRE,'',line)!=line: endTagLines.append(lineNo+1)

  #print startTagLines
  #print endTagLines

  tagNo = 0
  while tagNo<len(startTagLines) or tagNo<len(endTagLines):
    if tagNo<len(startTagLines): startTag1 = startTagLines[tagNo]
    else:
      startTagLines.insert(tagNo,'No start-tag')
      startTag1 = startTagLines[tagNo]
    if tagNo<len(startTagLines)-1: startTag2 = startTagLines[tagNo+1]
    else: startTag2 = "END"
    if tagNo<len(endTagLines):
      endTag = endTagLines[tagNo]
      if isinstance(startTag1,basestring)==False and isinstance(endTag,basestring)==False:
        if startTag1>endTag:
          startTagLines.insert(tagNo,'No start-tag')
        elif startTag1<=endTag:
          if isinstance(startTag2,basestring)==False:
            if endTag>startTag2: endTagLines.insert(tagNo,'No end-tag')
            else: tagNo+=1
          else: tagNo+=1
      else: tagNo+=1
    else: endTagLines.insert(tagNo,'No end-tag')

  title = "--------------------\n"+startTag+"\n--------------------"
  printedTitle = False
  for tagNo,startTag in enumerate(startTagLines):
    endTag = endTagLines[tagNo]
    if isinstance(startTag,basestring)==True:
      if printedTitle==False:
        print title
        printedTitle = True
      if tagNo>0: print str(endTagLines[tagNo-1])+" -> "+str(startTag)+" -> "+str(endTag)
      else: print "SOD"+" -> "+str(startTag)+" -> "+str(endTag)
    elif isinstance(endTag,basestring)==True:
      if printedTitle==False:
        print title
        printedTitle = True
      if tagNo<len(startTagLines)-1: print str(startTag)+" -> "+str(endTag)+" -> "+str(startTagLines[tagNo+1])
      else: print str(startTag)+" -> "+str(endTag)+" -> "+"EOD"

def wordLengthTest(textholder):
  eosRE = re.compile('\.\s|\.\n|:\n|\."\n|\."\s|\?\s')
  textholder = re.split(eosRE,textholder)
  longSentences = []
  for sentenceNo,text in enumerate(textholder):
    text = text.replace('\t ',' ')
    text = text.replace(' \t',' ')
    text = removeMultiple(text,' ')
    text = removeMultiple(text,'\n')
    text = removeMultiple(text,'\t')
    text = removeMultiple(text,'\n ')

    text = text.replace('\n \n','\n')
    text = text.replace('\n ','\n')
    text = text.replace('\n\t','\n')
    text = text.replace('\n',' ')
    textholder[sentenceNo] = text

  for sentenceNo,sentence in enumerate(textholder):
    wordNo = len(sentence.split(' '))
    longestWordLen = 0
    for word in sentence.split(' '):
      if len(word)>longestWordLen:longestWordLen = len(word)
    if wordNo>50:
      print '['+str(sentenceNo)+'] '+str(wordNo)+' words -> longest word has '+str(longestWordLen)+' characters'
      longSentences.append(sentenceNo)

  for sentenceNo in longSentences:
    print [sentenceNo]+[textholder[sentenceNo]]
    x = raw_input("")

  return

def removeIrrelevant(textholder):
  tagRE = re.compile(r'(<doc>|</doc>|<section>|</section>)')
  textholder = re.sub(tagRE,'',textholder)

  textholder = textholder.replace(u"\u201C",'"')
  textholder = textholder.replace(u"\u201D",'"')
  textholder = textholder.replace(u"\u2018",'\'')
  textholder = textholder.replace(u"\u2019",'\'')
  textholder = textholder.replace(u"\u2014",'-')
  textholder = textholder.replace('`','\'')

  #textholder = textholder.replace('<doc>','')
  #textholder = textholder.replace('</doc>','')

  textholder = removeSegment('<cover>','</cover>',textholder)
  textholder = removeSegment('<toc>','</toc>',textholder)
  textholder = removeSegment('<header>','</header>',textholder)
  textholder = removeSegment('<footer>','</footer>',textholder)
  textholder = removeSegment('<heading>','</heading>',textholder)
  textholder = removeSegment('<figure>','</figure>',textholder)
  textholder = removeSegment('<caption>','</caption>',textholder)
  textholder = removeSegment('<table>','</table>',textholder)
  textholder = removeSegment('<code>','</code>',textholder)
  textholder = removeSegment('<noncontent>','</noncontent>',textholder)
  textholder = removeSegment('<box>','</box>',textholder)
  textholder = removeSegment('<pointer>','</pointer>',textholder)
  textholder = removeSegment('<fn>','</fn>',textholder)
  textholder = removeSegment('<footnote>','</footnote>',textholder)
  textholder = removeSegment('<list>','</list>',textholder)
  return textholder

def removeSegment(startTag,endTag,textholder):
  tagRE = re.compile(r'('+startTag+'|'+endTag+')')
  startTagRE = re.compile(startTag)
  endTagRE = re.compile(endTag)
  textArray = re.split(tagRE,textholder)
  textholder = ''
  relevant = True
  for i,text in enumerate(textArray):
    if(startTagRE.match(text)): relevant = False
    if relevant: textholder+=text
    if(endTagRE.match(text)): relevant = True
  return textholder

def removeMultiple(string, toRemove):
  substring = 2*toRemove
  while True:
    if(string.find(substring)>=0):
      string = string.replace(substring,toRemove)
    else:
      break
  return string

if __name__ == "__main__": main()
