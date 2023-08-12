"""
--------------------------------------------------------------
Name: tagFinder.py
--------------------------------------------------------------
Purpose:
This script outputs the content in between the tags that was
keyed into this script.

This script receives the txt file name and tag as inputs from
the user and runs through the whole txt file to find these tags
and display the content inside each of them.

Last edited: 9/14/2018
--------------------------------------------------------------
"""

def finder(start,tag,tagSlash,content):  #finds the tags in the content
    tagstart = content.find(tag,start)
    findstart = tagstart + len(tag)
    tagend = content.find(tagSlash,start)
    print("Script at",tagstart)
    if tagstart == -1 or tagend == -1:  #check if any tags still exist
        return print("---END---")
    else:
        
        for i in range(findstart,tagend):
            print(content[i], end='')
        print()
        newStart = tagend+len(tag)
        return finder(newStart,tag,tagSlash,content)  #set the starting point to after the closing tag
def main():
    file = str(input("Enter the txt file to use: "))
    tag = str(input("Enter the tag that you wish to find: "))
    tagSlash = str("</"+tag+">")
    tag = str("<"+tag+">")
    f = open(file,"r", encoding = "utf-8") #open file and convert the format to be able to read
    content = f.read()
    tagstart = 0
    tagend = 0
    start = 0
    finder(start,tag,tagSlash,content)
    f.close()           
            
main()
