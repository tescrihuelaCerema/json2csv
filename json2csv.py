# -*- coding: utf-8 -*-

"""
Script de conversion d'un json en csv. Il faut modifier à la main les paramètres (chemin vers le json) dans le script.

Usage :
-------
    python json2csv.py

"""

__author__ = "Thomas Escrihuela"
__contact__ = "Thomas.Escrihuela@cerema.fr"
__date__ = "2020/05"


import json
import csv

jsonfile = r"./BASIAS_GUA.json"
csvfile = jsonfile.replace('json','csv')

def reduce_item(key,value,bool):
    
    #Si c'est une liste
    if isinstance(value,list):
        i=0
        for sub_item in value:
            reduce_item(key+str('_' if bool else '')+str(i), sub_item,True)
            i=i+1

    #Si c'est un dict
    elif isinstance(value,dict):
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key+str('_' if bool else '')+sub_key, value[sub_key],True)
    
    #Sinon objet déjà réduit
    else:
        reduced_item[key] = value


if __name__ == "__main__":

    f = open(jsonfile, 'r', encoding="utf8")
    data = json.load(f)
    f.close()

    processed_data = []
    header = []
    for item in data:
        reduced_item = {}
        reduce_item("",item,False)
        header += reduced_item.keys()
        processed_data.append(reduced_item)

    header = list(set(header))
    header.sort()

    with open(csvfile,'w+',encoding="utf8",newline='') as f:
        w = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for row in processed_data:
            w.writerow(row)

    print ("CSV '{}' de {} colonnes et {} lignes écrit !".format(csvfile, len(header),len(processed_data)))
