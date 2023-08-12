"""
--------------------------------------------------------------
Name: SectionFinder.py
--------------------------------------------------------------
Purpose:
This script collects the content between tags and store them
into a list for all the .txt files in the same folder as this
program

This script runs through the whole txt file to find these tags
and store the content into a list for each of them

Last edited: 10/11/2018
--------------------------------------------------------------
"""
import os

def finder(start,tag,tagSlash,content,tagList):          #finds the tags in the content
    tagstart = content.find(tag,start)
    findstart = tagstart + len(tag)
    tagend = content.find(tagSlash,start)
    print("Script at",tagstart)
    if tagstart == -1 or tagend == -1:  #check if any tags still exist
        return tagList
    else:
        Astring = ""
        for i in range(findstart,tagend):
            Astring += content[i]
        tagList.append(Astring)
        newStart = tagend+len(tag)
        return finder(newStart,tag,tagSlash,content,tagList)  #set the starting point to after the closing tag
def main():
    Sections = {"doc":[],                      # This stalls all the section content into a list
                "cover":[],
                "header":[],
                "heading":[],
                "figure":[],
                "caption":[],
                "section":[],
                "fn":[],
                "footnote":[],
                "footer":[],
                "code":[]}
    dirList = os.listdir()
    for file in dirList:
        if file.endswith(".txt"):
            for tag,tagList in Sections.items():
                f = open(file,"r", encoding = "utf-8") #open file and convert the format to be able to read
                content = f.read()
                tagSlash = str("</"+tag+">")
                tag = str("<"+tag+">")
                tagstart = 0
                tagend = 0
                start = 0
                finder(start,tag,tagSlash,content,tagList)  
                f.close()
main()
