#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
articut = Articut(username="", apikey="", version="latest", level="lv1")

import json
import os
import random
import re

#<這段產生特定詩人的詞彙字典>
#inputDIR = "./poem/楊牧"

#posDICT = {"enty":[],
            #"mod":[],
            #"verb":[]
            #}

#fileLIST = os.listdir(inputDIR)
#for i in fileLIST[:2]:
    #if i.endswith(".txt"):
        #with open("{}/{}".format(inputDIR, i), encoding="utf-8") as f:
            #txtLIST = [t.replace("　", "") for t in f.read().split("\n") if len(t)>1]
        #resultDICT = articut.parse(",".join(txtLIST))
        #entityLIST = articut.getNounStemLIST(resultDICT)
        #for s in entityLIST:
            #if len(s)>0:
                #posDICT["enty"].extend([enty[2] for enty in s if "◎" not in enty[2]])
        #verbLIST = articut.getVerbStemLIST(resultDICT)
        #for s in verbLIST:
            #if len(s)>0:
                #posDICT["verb"].extend([verb[2] for verb in s if "◎" not in verb[2]])
        #contentWordLIST = articut.getContentWordLIST(resultDICT)
        #for s in contentWordLIST:
            #if len(s)>0:
                #posDICT["mod"].extend([cont[2] for cont in s if "◎" not in cont[2]])

#nounverbSET = set(posDICT["enty"] + posDICT["verb"])
#posDICT["mod"] = list(set(posDICT["mod"]).difference(nounverbSET))
#posDICT["verb"] = list(set(posDICT["verb"]))
#posDICT["enty"] = list(set(posDICT["enty"]))

#with open("./楊牧DICT.json", "w", encoding="utf-8") as f:
    #json.dump(posDICT, f, ensure_ascii=False)
#</這段產生特定詩人的詞彙字典>

#<這段讀入特定詩人的詞彙典字來做動詞、名詞和形容詞/副詞的替換>
with open("./楊牧DICT.json") as f:
    lexiconDICT = json.loads(f.read())

sourceSTR = """甚麼聲音
或許是鼷鼠在屋樑上磨牙
是睡蓮
在水缸裏悄悄延長它的根
蠹魚游過我心愛的晚唐詩
是冷霜落瓦
燭蕊爆開兩朵花"""

verbPat = re.compile("(?<=<ACTION_verb>)[^<]+?(?=</ACTION_verb>)")
entityPat = re.compile("(?<=<ENTITY_nounHead>)[^<]+?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]+?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]+?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]+?(?=</ENTITY_oov>)")
modifierPat = re.compile("(?<=<MODIFIER>)[^<]+?(?=</MODIFIER>)|(?<=<ModifierP>)[^<]+?(?=</ModifierP>)|(?<=<DegreeP>)[^<]+?(?=</DegreeP>)")
resultLIST = []
posPat = re.compile("</?[a-zA-Z_]+?>")

templateDICT = articut.parse(sourceSTR)
for i in templateDICT["result_pos"]:
    if len(i)<1:
        resultLIST.append(i)
    else:
        verbLIST = [(v.start(), v.end(), v.group()) for v in reversed(list(verbPat.finditer(i)))]
        for v in verbLIST:
            verb = random.choice(lexiconDICT["verb"])
            counter = 0
            while len(verb) != v[-1] and counter <10:
                verb = random.choice(lexiconDICT["verb"])
                counter = counter+1
            i = "{}{}{}".format(i[:v[0]], verb, i[v[1]:])

        entyLIST = [(e.start(), e.end(), e.group()) for e in reversed(list(entityPat.finditer(i)))]
        for e in entyLIST:
            enty = random.choice(lexiconDICT["enty"])
            counter = 0
            while len(enty) != e[-1] and counter <10:
                enty = random.choice(lexiconDICT["enty"])
                counter = counter+1
            i = "{}{}{}".format(i[:e[0]], enty, i[e[1]:])

        modLIST = [(m.start(), m.end(), m.group()) for m in reversed(list(modifierPat.finditer(i)))]
        for m in modLIST:
            mod = random.choice(lexiconDICT["mod"])
            counter = 0
            while len(mod) != m[-1] and counter <10:
                mod = random.choice(lexiconDICT["mod"])
                counter = counter+1
            i = "{}{}{}".format(i[:m[0]], mod, i[m[1]:])
        resultLIST.append(re.sub(posPat, "", i))

print("".join(resultLIST))
#</這段讀入特定詩人的詞彙典字來做動詞、名詞和形容詞/副詞的替換>