from random import sample,randint, choice, shuffle
from rdflib import Graph, Literal, RDF, URIRef, XSD,  RDFS
from SPARQLWrapper import SPARQLWrapper, JSON
import codecs

samplerIRI="http://c2200024:7200/repositories/test"

def querySPARQL(endpoint, query, wHeader=True) :
    if wHeader :
        query="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dhfc: <https://w3id.org/DHFC#>
PREFIX tsn: <http://purl.org/net/tsn#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX hht: <https://w3id.org/HHT#>
PREFIX time: <http://www.w3.org/2006/time#>
"""+query
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    return ret["results"]["bindings"]

def mapAsJson() :
    query="""
    

    select ?entity ?v ?name ?bY ?eY ?sub ?subV ?upper ?upperV ?memberShip where {
        ?entity hht:hasVersion ?v.
        ?v rdfs:label ?name.
        ?v hht:validityPeriod ?i.
        ?i time:hasBeginning ?b.
        ?b time:inXSDgYear ?bY.
        ?i time:hasEnd ?e.
        ?e time:inXSDgYear ?eY.
        OPTIONAL{?v hht:hasSubUnit ?subV. ?sub hht:hasVersion ?subV.}
        OPTIONAL{?upperV hht:hasSubUnit ?v. ?upper hht:hasVersion ?upperV.}
        ?v hht:isMemberOf ?memberShip.
    }"""
    res=querySPARQL(samplerIRI, query)
    dic={}
    for entry in res :
        if entry["entity"]["value"] not in dic:
            dic[entry["entity"]["value"]]={}
        dates= entry["v"]["value"]
        interv=(int(entry["bY"]["value"]),int(entry["bY"]["value"]))
        if dates not in dic[entry["entity"]["value"]] :
            dic[entry["entity"]["value"]][dates]={"sub" : set(), "dates" : interv}
        dic[entry["entity"]["value"]][dates]["name"]=entry["name"]["value"]
        dic[entry["entity"]["value"]][dates]["memberShip"]=entry["memberShip"]["value"]
        if "upper" in entry :
            dic[entry["entity"]["value"]][dates]["upper"]=(entry["upper"]["value"], entry["upperV"]["value"])
        if "sub" in entry  :
            dic[entry["entity"]["value"]][dates]["sub"].add((entry["sub"]["value"], entry["subV"]["value"]))
    return dic

def insert(entity, mapRes, res):
    ent=entity[0]
    v=entity[1]
    if ent not in res :
        res[ent]={}
    if v not in res[ent] :
        res[ent][v]={"name" : mapRes[ent][v]["name"], "dates" : mapRes[ent][v]["dates"]}

def createObject(prefix,text) :
    final=text.replace(" ", "_").replace("(", "").replace(")", "")
    return URIRef(prefix+final)

hht="https://w3id.org/HHT#"

def addDate(toAdd, startDate, endDate, uriV) :
    isAnnee=URIRef('http://www.w3.org/2006/time#inXSDgYear')
    hasBeginning=URIRef('http://www.w3.org/2006/time#hasBeginning')
    hasEnd=URIRef('http://www.w3.org/2006/time#hasEnd')
    gyearStart = Literal(str(startDate), datatype=XSD.gYear)
    gyearEnd=Literal(str(endDate), datatype=XSD.gYear)
    InstantDebut=URIRef('http://www.semanticweb.org/melodi/data#year'+str(startDate))
    InstantFin=URIRef('http://www.semanticweb.org/melodi/data#year'+str(endDate))
    toAdd.add((InstantDebut, isAnnee, gyearStart))
    toAdd.add((InstantFin, isAnnee, gyearEnd))
    Duree=URIRef('http://www.semanticweb.org/melodi/data#duree'+str(startDate)+'-'+str(endDate))
    toAdd.add((Duree, hasEnd, InstantFin))
    toAdd.add((Duree, hasBeginning, InstantDebut))
    toAdd.add((uriV, URIRef('http://www.semanticweb.org/HHT_Ontology#validityPeriod'), Duree))


def addEntity(entity, entityIRI, graph) :
    for version in entity :
        graph.add((URIRef(entityIRI), createObject(hht, "hasVersion"), URIRef(version)))
        if "name" in entity[version] :
            graph.add((URIRef(version), RDFS.label, Literal(entity[version]["name"])))
        if "dates" in entity[version] :
            addDate(graph, entity[version]["dates"][0], entity[version]["dates"][1], URIRef(version))
        if "memberShip" in entity[version] :
            graph.add((URIRef(version), createObject(hht, "isMemberOf"), URIRef(entity[version]["memberShip"])))
        if "upper" in entity[version] :
            graph.add((URIRef(entity[version]["upper"][1]), createObject(hht, "hasSubUnit"), URIRef(version)))
        if "sub" in entity[version] :
            for sub in  entity[version]["sub"] :
                graph.add((URIRef(version), createObject(hht, "hasSubUnit"), URIRef(sub[1])))
    
def getRandomSameLevel(mapRes, entity) :
    level=entity[list(entity.keys())[0]]["memberShip"]
    rand=randint(0, len(mapRes)-1)
    key=list(mapRes.keys())[rand]
    while mapRes[key][list(mapRes[key].keys())[0]]["memberShip"]!=level :
        rand=randint(0, len(mapRes)-1)
        key=list(mapRes.keys())[rand]
    return mapRes[key]


def similarName(string, distance) :
    operations=randint(1, distance)
    min="azertyuiopqsdfghjklmwxcvbn"
    for i in range(operations) :
        command=randint(1, 3)
        position=randint(1, len(string)-1)
        if command==1 :
            if position==len(string)-1 :
                string=string[:position]+choice(min)
            else :
                string=string[:position]+choice(min)+string[position+1:]
        if command==2 :
            string=string[:position]+choice(min)+string[position:]
        if command==3 :
            if position==len(string)-1 :
                string=string[:position]
            else :
                string=string[:position]+string[position+1:]
    return similarName



#TODO Ajouter erreurs attributs, erreurs noms, erreurs valeurs
def sampleGraph(numberEnt, percentSub, memberPercent, upperPercent, mapRes, intCount, errorAttrRate, errorNameRate, errorTimeRate) :
    res={}
    targets=sample(list(mapRes.keys()), numberEnt)
    upperNumber=int(numberEnt*upperPercent/100)
    uppers=sample(targets, upperNumber)
    memberNumber=int(numberEnt*memberPercent/100)
    members= sample(targets, memberNumber)
    errorAttrNumber=int(numberEnt*errorAttrRate/100)
    errorAttr=sample(targets, errorAttrNumber)
    errorNameNumber=int(numberEnt*errorNameRate/100)
    errorName=sample(targets, errorNameNumber)
    errorTimeNumber=int(numberEnt*errorTimeRate/100)
    errorTime=sample(targets, errorTimeNumber)
    for entity in errorAttr :
        toAdd=getRandomSameLevel(mapRes,mapRes[entity])
        for version in toAdd :
            for v2 in mapRes[entity] :
                if (toAdd[version]["dates"][0]>=mapRes[entity][v2]["dates"][0] and toAdd[version]["dates"][0]<mapRes[entity][v2]["dates"][1]) or (toAdd[version]["dates"][1]>=mapRes[entity][v2]["dates"][0] and toAdd[version]["dates"][1]<mapRes[entity][v2]["dates"][1]) or (mapRes[entity][v2]["dates"][0]>=toAdd[version]["dates"][0] and mapRes[entity][v2]["dates"][1]<toAdd[version]["dates"][1]) :
                    mapRes[entity][v2]["upper"]=version
    for entity in errorName :
        for version in mapRes[entity] :
            mapRes[entity][version]["name"]=similarName(mapRes[entity][version]["name"], 10)
    for entity in errorTime :
        times=[]
        for version in mapRes[entity] :
            times.append(mapRes[entity][version]["dates"])
        shuffle(times)
        for i in range(len(mapRes[entity].keys())) :
            mapRes[entity][list(mapRes[entity].keys())[i]]["dates"]=times[i]
    for e in targets:
        if len(mapRes[e])>1 :
            versionN=randint(1,len(mapRes[e])-1)
        else :
            versionN=1
        versions=sample(list(mapRes[e].keys()), versionN)
        entity={}
        for version in versions :
            vers={"name" : mapRes[e][version]["name"], "dates" : mapRes[e][version]["dates"]}
            if len(mapRes[e][version]["sub"])>0 :
                print(len(mapRes[e][version]["sub"]))
                retainSubs=sample(list(mapRes[e][version]["sub"]), int(len(mapRes[e][version]["sub"])*(percentSub/100)) )
                vers["sub"]=retainSubs
                for c in retainSubs :
                    insert(c, mapRes, res)
            if e in uppers and "upper" in mapRes[e][version]:
                vers["upper"]=mapRes[e][version]["upper"]
                insert(mapRes[e][version]["upper"], mapRes, res)
            if e in members :
                vers["memberShip"]=mapRes[e][version]["memberShip"]
            entity[version]=vers
    
        res[e]=entity
        print(res)
    g=Graph()
    for e in res :
        addEntity(res[e], e, g)

    ttl=g.serialize(format='turtle')
    outputName=(str("Test_Sample_N"+str(numberEnt)+"_pSub"+str(percentSub)+"_pMemb"+str(memberPercent)+"_pUp"+str(upperPercent)+"__"+str(intCount)+".ttl"))
    file=codecs.open(outputName, "w", "utf-8")
    file.write(ttl)
    return ttl    

mapRes=mapAsJson()
sampleGraph(20, 50, 50, 50, mapRes, 0, 10, 10, 10)