#!/usr/bin/python

import os
import sys
import datetime
from optparse import OptionParser

sys.path.append('silme/lib')

import silme.diff
import silme.core
import silme.format
import silme.io


silme.format.Manager.register('dtd', 'properties')

def getchaine1(package,dir):
    for item in package:
            aa=item[0]
            bb=item[1]
            if (type(bb) is not silme.core.structure.Blob) and not(isinstance(bb,silme.core.Package)):
                    for id in bb:
                        chaines[dir+":"+aa+":"+id]=bb[id].get_value()



    for pack in package.packages():
        for item in pack:
            if isinstance(item[1], silme.core.Package):
                getchaine1(item[1],dir)

        else:
                aa=item[0]
                bb=item[1]
            if type(bb) is not silme.core.structure.Blob:
                    for id in bb:
                        chaines[dir+":"+aa+":"+id]=bb[id].get_value()
    return chaines

def getchaine2(package,dir):
    for item in package:
            aa=item[0]
            bb=item[1]
            if (type(bb) is not silme.core.structure.Blob) and not(isinstance(bb,silme.core.Package)):
                    for id in bb:
                        chaines2[dir+":"+aa+":"+id]=bb[id].get_value()
    for pack in package.packages():
        for item in pack:
            if isinstance(item[1], silme.core.Package):
                getchaine2(item[1],dir)
        else:
                aa=item[0]
                bb=item[1]
            if type(bb) is not silme.core.structure.Blob:
                    for id in bb:
                        chaines2[dir+":"+aa+":"+id]=bb[id].get_value()
    return chaines2

def tmxheader(file,langcode2):

    from datetime import datetime
    file.write('<?xml version="1.0" encoding="UTF-8"?>')
    file.write("\n")
    file.write('<tmx version="1.4">')
    file.write("\n")
    file.write(' <header o-tmf="plain text" o-encoding="UTF8" adminlang="en" creationdate="'+str(datetime.now())+'" creationtoolversion="0.1" creationtool="tmxmaker_transvision" srclang="'+langcode2+'" segtype="sentence" datatype="plaintext">')
    file.write("\n")
    file.write(' </header>')
    file.write("\n")
    file.write(' <body>')
    file.write("\n")

def addtu(ent,ch1,ch2,file,langcode1,langcode2):
        ch1=ch1.replace('&','&amp;')
        ch2=ch2.replace('&','&amp;')
        ch1=ch1.replace('<','&lt;')
        ch1=ch1.replace('>','&gt;')
        ch2=ch2.replace('<','&lt;')
        ch2=ch2.replace('>','&gt;')
        ch1=ch1.replace('"','')
        ch2=ch2.replace('"','')
        ch1=ch1.replace('\\','')
        ch2=ch2.replace('\\','')
        ch1=ch1.replace('{','')
        ch2=ch2.replace('{','')
        ch1=ch1.replace('}','')
        ch2=ch2.replace('}','')

        file.write('    <tu tuid="'+ent+'" srclang="'+langcode2+'">')
        file.write("\n")
        file.write("        <tuv xml:lang=\""+langcode2+"\"><seg>"+ch1.encode('utf-8')+"</seg></tuv>")
        file.write("\n")
        file.write("        <tuv xml:lang=\""+langcode1+"\"><seg>"+ch2.encode('utf-8')+'</seg></tuv>')
        file.write("\n")
        file.write("    </tu>")
        file.write("\n")

def tmxclose(file):
    file.write('</body>\n</tmx>')

def cacheheader(file):
    file.write("<?php")
    file.write("\n")

def cacheadd(ent,ch,file):
    ch=ch.replace('&','&amp;')
    ch=ch.replace('<','&lt;')
    ch=ch.replace('>','&gt;')
    ch=ch.replace('"','')
    ch=ch.replace('\\','')
    ch=ch.replace('}','')
    ch=ch.replace('{','')
    ch=ch.replace('$','\$')
    file.write('$tmx[\''+ent.encode('utf-8')+'\']="'+ch.encode('utf-8')+'";')
    file.write("\n")

def cacheclose(file):
    file.write('?>')


if __name__ == "__main__":
    usage = "test"
    parser = OptionParser(usage, version='%prog 0.1')
    (options, args) = parser.parse_args(sys.argv[1:])

    chaine={}
    chaine2={}
    chaines={}
    chaines2={}
        if len(args) < 1:
            fr = "../fr/"
        en_US  = "../hg.frenchmozilla.fr/"
    else:
            if len(args) < 2:
                    fr=args[0]
            en_US  = "../hg.frenchmozilla.fr/"
        else:
                    fr=args[0]
                    en_US=args[1]
    if len(args)<3:
        langcode1="fr"
        langcode2="en-US"
    if 4>len(args)>2:
        langcode1=args[2]
        langcode2="en_US"
    if len(args)>3:
        langcode1=args[2]
        langcode2=args[3]
    if len(args)>4:
        depot=args[4]
    if len(args)>5:
        doublon=True
    else:
        doublon=False

    dirs1 = os.listdir(fr)
    dirs2=["b2g", "browser","calendar","dom","editor","embedding","extensions","layout","mail","mobile","netwerk","other-licenses","security","services","suite","testing","toolkit"]
    dirs=filter(lambda x:x in dirs1,dirs2)

    nomfichier="/var/www/frenchmozilla.org/frmoz/transvision/TMX/"+depot+"/"+langcode1+"/memoire_"+langcode2+"_"+langcode1+".tmx"
    nomfichier2="/var/www/frenchmozilla.org/frmoz/transvision/TMX/"+depot+"/"+langcode1+"/cache_"+langcode2+".php"
    nomfichier3="/var/www/frenchmozilla.org/frmoz/transvision/TMX/"+depot+"/"+langcode1+"/cache_"+langcode1+".php"
    nomfichier4="/var/www/frenchmozilla.org/frmoz/transvision/TMX/"+depot+"/"+langcode1+"/doublons_"+langcode1+".php"
    nomfichier5="/var/www/frenchmozilla.org/frmoz/transvision/TMX/"+depot+"/"+langcode1+"/doublons_unique_"+langcode1+".php"
    fichier = open(nomfichier, "w")
    fichier2 = open(nomfichier2, "w")
    fichier3 = open(nomfichier3, "w")
    tmxheader(fichier,langcode2)
    cacheheader(fichier2)
    cacheheader(fichier3)
    total={}
    total2={}
    for dir in dirs:
        chaine={}
        chaine2={}
        chaines={}
        chaines2={}
        path1=en_US+dir
        path2=fr+dir

        rcsClient = silme.io.Manager.get('file')
        l10nPackage = rcsClient.get_package(path1 , object_type='entitylist')
        rcsClient2 = silme.io.Manager.get('file')
        l10nPackage2 = rcsClient.get_package(path2 , object_type='entitylist')

        getchaine1(l10nPackage,dir)
        getchaine2(l10nPackage2,dir)
        chaine=chaines
        chaine2=chaines2
        for entity in chaine:
            if len(chaine[entity])>2:
                addtu(entity,chaine[entity],chaine2.get(entity,""),fichier,langcode1,langcode2)
                cacheadd(entity,chaine[entity],fichier2)
                cacheadd(entity,chaine2.get(entity,""),fichier3)
                total[entity]=chaine.get(entity,"")
                total2[entity]=chaine2.get(entity,"")

    if doublon:
        fichier4 = open(nomfichier4, "w")
        fichier5 = open(nomfichier5, "w")
        cacheheader(fichier4)
        cacheheader(fichier5)
        i=0
        j=0
        total3=total.copy()
        for entity in total:
            del total3[entity]
            if (len(total[entity]))>2&(total2[entity]!=""):
                for entity2 in total3:
                    if (total[entity]==total[entity2])&(total2[entity]!=total2[entity2])&(total2[entity2]!=""):
                        i=i+1
                        total[entity]=total[entity].replace('<','&lt;')
                        total2[entity]=total2[entity].replace('<','&lt;')
                        total2[entity2]=total2[entity2].replace('<','&lt;')
                        total[entity]=total[entity].replace('>','&gt;')
                        total2[entity]=total2[entity].replace('>','&gt;')
                        total2[entity2]=total2[entity2].replace('>','&gt;')
                        total[entity]=total[entity].replace('"','')
                        total2[entity]=total2[entity].replace('"','')
                        total2[entity2]=total2[entity2].replace('"','')
                        fichier4.write("$entity1["+str(i)+"]=htmlspecialchars(\""+entity.encode('utf-8')+"\");")
                        fichier4.write('\n')
                        fichier4.write("$enus["+str(i)+"]=htmlspecialchars(\""+total[entity].encode('utf-8')+"\");")
                        fichier4.write('\n')
                        fichier4.write("$fr1["+str(i)+"]=htmlspecialchars(\""+total2[entity].encode('utf-8')+"\");")
                        fichier4.write('\n')
                        fichier4.write("$entity2["+str(i)+"]=htmlspecialchars(\""+entity2.encode('utf-8')+"\");")
                        fichier4.write('\n')
                        fichier4.write("$fr2["+str(i)+"]=htmlspecialchars(\""+total2[entity2].encode('utf-8')+"\");")
                        fichier4.write('\n')
                        ent2=entity2.rpartition(":")[-1]
                        ent=entity.rpartition(":")[-1]
                        if ent2==ent:
                            j=j+1
                                                fichier5.write("$entity1["+str(j)+"]=htmlspecialchars(\""+entity.encode('utf-8')+"\");")
                                                fichier5.write('\n')
                                                fichier5.write("$enus["+str(j)+"]=htmlspecialchars(\""+total[entity].encode('utf-8')+"\");")
                                                fichier5.write('\n')
                                                fichier5.write("$fr1["+str(j)+"]=htmlspecialchars(\""+total2[entity].encode('utf-8')+"\");")
                                                fichier5.write('\n')
                                                fichier5.write("$entity2["+str(j)+"]=htmlspecialchars(\""+entity2.encode('utf-8')+"\");")
                            fichier5.write('\n')
                                                fichier5.write("$fr2["+str(j)+"]=htmlspecialchars(\""+total2[entity2].encode('utf-8')+"\");")
                            fichier5.write('\n')
        fichier4.write('$k='+str(i)+';')
        fichier5.write('$k='+str(j)+';')
        cacheclose(fichier4)
        cacheclose(fichier5)

    tmxclose(fichier)
    cacheclose(fichier2)
    cacheclose(fichier3)
    fichier.close()
    fichier2.close()
    fichier3.close()
