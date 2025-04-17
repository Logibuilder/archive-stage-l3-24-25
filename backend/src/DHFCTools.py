from rdflib import Graph, Literal, RDF, URIRef, XSD,  RDFS
from SPARQLWrapper import SPARQLWrapper, JSON
import sys
import requests
import random
import json

# Convert the result of a SPARQL query into a list
def toList(dic) :
    l=[] 
    for e in dic :
        f=[]
        for el in e.values() :
            f.append(el["value"])
        l.append(f)
    return l

#Convert a list coming out of a SPARQL query with one result variable into a set
def toSet(l) :
    s=set()
    for e in l :
        s.add(str(e[0]))
    return s


def flatten(l) :
    res=[]
    for e in l :
        res.append(e)
    return res



#Do a SPARQL update operation
def updateSPARQL(endpoint, query) :
    sparql = SPARQLWrapper(endpoint)
    sparql.setMethod("POST")
    sparql.setQuery(query)
    ret = sparql.query()
    ret.response.read()

# Send a SPARQL query
def querySPARQL(endpoint, query, wHeader=True) :
    if wHeader :
        query="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dhfc: <https://w3id.org/DHFC#>
PREFIX tsn: <http://purl.org/net/tsn#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
"""+query
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    return ret["results"]["bindings"]
# Returns the set of entities to align in a SPARQL endpoint
def getEntitySet(sparqlRepo) :
    query="""SELECT DISTINCT ?entity WHERE {?entity rdf:type/rdfs:subClassOf* dhfc:Entity.}"""
    objets=toSet(toList(querySPARQL(sparqlRepo, query)))
    return objets

#Select all triples involving an entity from class1 and an entity from class2
def getTriplesClassToClassDic(sparqlRepo, class1, class2):
    query="""SELECT DISTINCT ?o ?p ?q WHERE {?o ?p ?q. ?o rdf:type/rdfs:subClassOf* """+class1+""". ?q rdf:type/rdfs:subClassOf* """+class2+""".}"""
    triples=toList(querySPARQL(sparqlRepo, query))
    dico={}
    for e in triples:
        if e[0] not in dico.keys() :
            dico[e[0]]={e[2] : [e[1]]}
        else :
            if e[2] not in dico[e[0]] :
                dico[e[0]][e[2]]=[e[1]]
            else :
                dico[e[0]][e[2]].append(e[1])
    return dico

#Example of comparison function
def supInt(i1,i2) :
    return i1>i2

#Intersection of two intervals
def intersect(i1, i2, compare=supInt) :
    if compare(i1[0], i2[0]) :
        begin=i1[0]
    else :
        begin=i2[0]
    if compare(i1[1], i2[1]) :
        end=i2[1]
    else :
        end=i1[1]
    if compare(begin, end) :
        return (None, None)
    else :
        return (begin, end)

# Selects all property and property pathes allowing to go from an entity to another entity. Returns both those paths and the associated triples.   
#TODO : gérer classes. Améliorer avec propriétés inverses
def getComplexPropertySet(sparqlRepo, wTime=False, TimeCoord=None) :
    #query="""SELECT ?property WHERE {?entity rdf:type owl:Property. FILTER NOT EXISTS{?entity (rdfs:domain|rdfs:range)/rdfs:subClassOf* dhfc:Statement.}}"""
    query="""SELECT DISTINCT ?p WHERE {?o ?p ?q. ?o rdf:type/rdfs:subClassOf* dhfc:Entity. ?q rdf:type/rdfs:subClassOf* dhfc:Entity.}"""
    objets=toSet(toList(querySPARQL(sparqlRepo, query)))
    s2s=getTriplesClassToClassDic(sparqlRepo, "dhfc:Statement", "dhfc:Statement")
    e2s=getTriplesClassToClassDic(sparqlRepo, "dhfc:Entity", "dhfc:Statement")
    s2e=getTriplesClassToClassDic(sparqlRepo, "dhfc:Statement", "dhfc:Entity")
    if wTime :
        if TimeCoord is None :
            temporal="""SELECT DISTINCT ?s ?b ?e WHERE {?s rdf:type/rdfs:subClassOf* dhfc:TemporalStatement.
            ?temp rdfs:subPropertyOf+ dhfc:hasTemporalMarker.
            ?s ?temp ?int.
            ?beg rdfs:subPropertyOf+ dhfc:hasBeginning.
            ?end rdfs:subPropertyOf+ dhfc:hasEnd.
            ?int ?beg ?b.
            ?int ?end ?e}"""
        else :
            temporal="""SELECT DISTINCT ?s ?b ?e WHERE {?s rdf:type/rdfs:subClassOf* dhfc:TemporalStatement.
            ?s """+TimeCoord["intervalPath"]+""" ?temp. ?temp """+TimeCoord["startPath"]+""" ?b. ?temp """+TimeCoord["endPath"]+""" ?e.}"""
        print(temporal)
        instants=toList(querySPARQL(sparqlRepo, temporal))
        existences={}
        for i in instants :
            existences[i[0]] = (i[1], i[2])
    triples=[]
    print("Begin triple analysis...")
    for o in e2s :
        for s in e2s[o]:
            if s in s2s :
                for s2 in s2s[s] :
                    if s2 in s2e and s2!=s: #Improve condition for Inverse Properties
                        for e2 in s2e[s2] :
                            if e2!=o : #Improve condition for Inverse Properties
                                for r1 in e2s[o][s] :
                                    for r2 in s2s[s][s2] :
                                        for r3 in s2e[s2][e2] :
                                            objets.add((r1,r2,r3))
                                            if wTime :
                                                if s in existences :
                                                    if s2 in existences :
                                                        if TimeCoord is None :
                                                            time=intersect(existences[s], existences[s2])
                                                        else :
                                                            time=intersect(existences[s], existences[s2], compare=TimeCoord["compareFun"])
                                                    else :
                                                        time=existences[s]
                                                elif s2 in existences :
                                                    time=existences[s2]
                                                else :
                                                    time=(None, None)
                                                triples.append([o,(r1,r2,r3), e2, time])
                                            else:
                                                triples.append([o,(r1,r2,r3), e2])

            if s in s2e :
                for e2 in s2e[s] :
                    if e2!=o : #Improve condition for Inverse Properties
                        for r1 in e2s[o][s] :
                            for r2 in s2e[s][e2] :
                                objets.add((r1, r2))
                                if wTime :
                                    if s in existences :
                                        time=existences[s]
                                    else :
                                        time=(None, None)
                                    triples.append([o,(r1,r2), e2, time])
                                else :
                                    triples.append([o,(r1,r2), e2])
    return (objets, triples)

#Select all mere entity to entity triples
def basicTriples(sparqlRepo) :
    query="""SELECT DISTINCT ?o ?p ?q WHERE {?o ?p ?q. ?o rdf:type/rdfs:subClassOf* dhfc:Entity. ?q rdf:type/rdfs:subClassOf* dhfc:Entity.}"""
    triples=toList(querySPARQL(sparqlRepo, query))
    return triples

#Encode an entity series into a file
def encode(l, filename, start, common, merge=False):
    if merge :
        file=open(filename, "a")
    else :
        file=open(filename, "w")
    dico={}
    for i in range(len(l)):
        if l[i] in common :
            if not merge :
                file.write(common[l[i]]+"\t"+str(l[i])+ "\n")
            dico[l[i]]=common[l[i]]
        else :
            file.write(str(i+start)+"\t"+str(l[i])+ "\n")
            dico[l[i]]=str(i+start)
    file.close()
    return dico

#Main function to generate the input files. 
def generateFiles(sparqlRepo, n, encodedObj, encodedProp, encodedTime, wTime=False, TimeCoord=None, common=False) : #TODO : Path to time instants,
    start=len(encodedObj)+1
    startP=len(encodedProp)+1
    startI=len(encodedTime)+1
    print("Querying entities...")
    entities =list(getEntitySet(sparqlRepo))
    print("Encoding entitites...")
    if not common :
        ent=encode(entities,"ent_ids_"+str(n), start, {})
    else :
        ent=encode(entities,"ent_ids_"+str(n), start, encodedObj)
    print("Encoding relations...")
    complexData=getComplexPropertySet(sparqlRepo, wTime=wTime, TimeCoord=TimeCoord)
    relations =list(complexData[0])
    if not common :
        rel=encode(relations, "rel_ids_"+str(n), startP, {})
    else :
        rel=encode(relations, "rel_ids_"+str(n), startP, encodedProp)
    instants=set()
    if wTime :
        print("Encoding Time...")
        
        for t in complexData[1] :
            instants.add(t[3][0])
            instants.add(t[3][1])
        if None in instants :
            instants.remove(None)
        if not common :
            ins=encode(list(instants), "time_ids", startI, {})
        else : 
            ins=encode(list(instants), "time_ids", startI, encodedTime, merge=common)
        ins[None]=0  
    print("Encoding triples...")
    l=basicTriples(sparqlRepo)+complexData[1]
    file=open("triples_"+str(n), "w")
    for e in l :
        file.write(ent[e[0]]+"\t"+rel[e[1]]+"\t"+ent[e[2]])
        if wTime :
            if len(e)>3 :
                file.write("\t"+str(ins[e[3][0]])+"\t"+str(ins[e[3][1]]))
            else :
                file.write("\t0\t0")
        file.write("\n")
    file.close()
    return (ent, rel, instants)

# Another function to compare instants
def compareDateTime(i1,i2) :
    return int(i1[0:3])>int(i2[0:3])

#Changes IRIs of entities but retains the former IDs in a file. This is used to avoid IRI matching.
def shuffle(sparqlRepo) :
    file=open("equivalences.json", "r")
    dic=json.load(file)
    file.close()
    entities=getEntitySet(sparqlRepo)
    entityCount=0
    for e in entities :
        if e not in dic :
            dic[e]={}
        newId="https://example.org/"+str(entityCount)
        rename="""DELETE {"""+e+""" ?r ?o. } INSERT {"""+newId+""" ?r ?o. } WHERE {"""+e+""" ?r ?o.} """
        rename2="""DELETE { ?a"""+e+""" ?z.} INSERT {?a"""+newId+""" ?z.} WHERE { ?a"""+e+""" ?z.} """
        rename3="""DELETE {?i ?p"""+e+""". } INSERT {?i ?p"""+newId+""". } WHERE {?i ?p"""+e+""". } """
        updateSPARQL(sparqlRepo, rename)
        updateSPARQL(sparqlRepo, rename2)
        updateSPARQL(sparqlRepo, rename3)
        dic[e][sparqlRepo]=newId
        entityCount+=1
    file=open("equivalences.json", "w")
    dic=json.dump(file)
    file.close()

#Generate all the matching pairs from two datasets.
def pairing(sparqlRepo1, sparqlRepo2) :
    file=open("equivalences.json", "r")
    dic=json.load(file)
    file.close()
    pairs=[]
    for e in dic :
        if sparqlRepo1 in dic[e] and sparqlRepo2 in dic[e] :
            pairs.append(dic[e][sparqlRepo1], dic[e][sparqlRepo2])
    return pairs


#################################### Definite edition ########################################################################

ttlGenerator ={
    "ObjectProperty" : "$target$ $property$ $value$",
    "DataProperty" : "$target$ $property$ \"$value$\"^^<$range$>",
    "FluentValueProperty" : "$target$ $property$ $version$. $version$ $Temp$ $value$. $version$ $time$  [time:hasBeginning [time:inXSDgYear \"$start$\"^^xsd:gYear]; time:hasEnd [time:inXSDgYear \"$end$\"^^xsd:gYear]]].",
    "FluentLinkProperty" : "$target$ $property$ $version$. $version$ $Temp$ $value$. $version$ $time$ [time:hasBeginning [time:inXSDgYear \"$start$\"^^xsd:gYear]; time:hasEnd [time:inXSDgYear \"$end$\"^^xsd:gYear]]].",
    "ReifiedProperty" : "$target$ $property$ $value$. [ a rdf:Statement ; rdf:subject $target$; rdf:property $property$; rdf:object $value^$] $time$ [time:hasBeginning [time:inXSDgYear \"$start$\"^^xsd:gYear]; time:hasEnd [time:inXSDgYear \"$end$\"^^xsd:gYear]].",
    "NAryProperty" : "$target$ $property$ [$Temp$ $value$ ; $time$ [time:hasBeginning [time:inXSDgYear \"$start$\"^^xsd:gYear]; time:hasEnd [time:inXSDgYear \"$end$\"^^xsd:gYear]]].",
    "SingletonProperty" : "$target$ $singleton$ $value$. $singleton$ rdfs:subPropertyOf $property$. $singleton$ $time$ [time:hasBeginning [time:inXSDgYear \"$start$\"^^xsd:gYear]; time:hasEnd [time:inXSDgYear \"$end$\"^^xsd:gYear]]." 

}


def getAvailableClasses(sparqlEndpoint) :
    query=""" 
        SELECT ?class WHERE {
        GRAPH ?g {?class a owl:Class.
        ?class rdfs:subClassOf* dhfc:Entity.}
        ?g a dhfc:DomainGraph.
    }
"""
    classes=flatten(toList(querySPARQL(sparqlEndpoint, query)))
    return classes

#TODO reverse fluent
def reverse(prop) :
    proper=dict(prop)
    if proper["type"] not in ("DataProperty", "FluentLinkProperty", "FluentValueProperty", "NAryProperty") :
        if "inverse" in proper :
            inverse=proper["inverse"]
            proper["inverse"]=proper["property"]
            proper["property"]=inverse
            return proper
    elif proper["type"]=="NAryProperty" :
        if "inverse" in proper and "inverseTemp" in proper :
            inverse=proper["inverse"]
            proper["inverse"]=proper["Temp"]
            proper["Temp"]=inverse
            inverse=proper["inverseTemp"]
            proper["inverseTemp"]=proper["property"]
            proper["property"]=inverse
            return proper
    return None
    

def vals(dic) :
    dico={}
    for e in dic :
        dico[e]=dic[e]["value"]
    return dico

#TODO ajouter temporal properties pour Datatypes
def getProperties(sparqlEndpoint, classIRI) :
    properties=[]
    queryObject=""" 
        SELECT ?property ?inverse ?range ?label WHERE {
        GRAPH ?g { {?property rdfs:domain/rdfs:subclassOf* <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
        ?property rdfs:range ?range. ?range rdfs:subclassOf* dhfc:Entity. OPTIONAL {?property owl:inverseOf ?inverse}}
        ?g a dhfc:DomainGraph.
        ?property rdfs:label ?label.
    }
"""
    objectPs=querySPARQL(sparqlEndpoint, queryObject)
    for entry in objectPs :
        res=vals(entry)
        res["type"]="ObjectProperty"
        res["temporality"]=False
        properties.append(res)
    queryDatatype=""" 
        SELECT ?property ?range ?label WHERE {
        GRAPH ?g { ?property a owl:DatatypeProperty. {?property rdfs:domain/rdfs:subclassOf* <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
        ?property rdfs:range ?range}
        ?g a dhfc:DomainGraph.
    }
    """
    objectPs=querySPARQL(sparqlEndpoint, queryDatatype)
    for entry in objectPs :
        res=vals(entry)
        res["type"]="DataProperty"
        res["temporality"]=False
        properties.append(res)
    
    queryFluents="""
        SELECT ?property ?inverse ?Temp ?inverseTemp ?towardSlice ?inverseToward ?hasId ?inverseId ?time ?tempLabel ?tempRange ?rangeToward ?towardLabel WHERE {
    	?g a dhfc:DomainGraph.
        GRAPH ?g { 
        {?property (rdfs:domain/rdfs:subclassOf*) <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
        ?property rdfs:range ?r. ?r rdfs:subclassOf* dhfc:4DFluentsVersion.
        OPTIONAL {?Temp rdfs:subPropertyOf* dhfc:TimeRelativeValue. {?Temp (rdfs:domain/rdfs:subclassOf*) ?r.} UNION {?Temp rdfs:domain ?class2. ?r rdfs:subclassOf* ?class2.} ?Temp rdfs:label ?tempLabel. ?Temp rdfs:range ?tempRange. OPTIONAL {?Temp owl:inverseOf ?inverseTemp}}
    	OPTIONAL {?towardSlice rdfs:subPropertyOf* dhfc:relationToVersion. 
            	{?towardSlice (rdfs:domain/rdfs:subclassOf*) ?r.} UNION {?towardSlice rdfs:domain ?class3. ?r rdfs:subclassOf* ?class3.}
        		?towardSlice rdfs:range ?sliceType. ?sliceType dhfc:hasIdentityProperty ?hasId.
                ?hasId rdfs:range ?rangeToward.
                ?towardSlice rdfs:label ?towardLabel.
                OPTIONAL {?towardSlice owl:inverseOf ?inverseToward}
            OPTIONAL {?hasId owl:inverseOf ?inverseId}
        }
        OPTIONAL {?property owl:inverseOf ?inverse}
        ?time rdfs:subPropertyOf dhfc:hasTemporalMarker. {?time (rdfs:domain/rdfs:subclassOf*) ?r.} UNION {?Temp rdfs:domain ?class4. ?r rdfs:subclassOf* ?class4.}    
    }
    }
    """
    objectPs=querySPARQL(sparqlEndpoint, queryFluents)
    r={}
    for entry in objectPs :
        if "Temp" in entry :
            cop=dict(entry)
            for e in cop :
                if "oward" in e or "Id" in e :
                    del cop[e]
            cop["label"]=cop["tempLabel"]
            del cop["tempLabel"]
            cop["range"]=cop["tempRange"]
            del cop["tempRange"]
            cop["type"]="FluentValueProperty"
            cop["temporality"]=True
            r[(entry["property"], entry["Temp"])]=cop
        if "towardsSlice" in entry :
            cop=dict(entry)
            for e in cop :
                if "Temp" in e or "temp" in e :
                    del cop[e]
            cop["label"]=cop["towardLabel"]
            del cop["towardLabel"]
            cop["range"]=cop["rangeToward"]
            del cop["rangeToward"]
            cop["type"]="FluentLinkProperty"
            cop["temporality"]=True
            r[(entry["property"], entry["towardsSlice"])]=cop
    for entry in r :
        properties.append(r[entry])


    queryReif="""SELECT ?property ?inverse ?time ?label ?range WHERE {
    	?g a dhfc:DomainGraph.
        GRAPH ?g { 
        ?property rdfs:subPropertyOf* dhfc:ReifiedTemporalProperty. 
        ?property rdfs:label ?label.
        ?property rdfs:range ?range.
        {?property (rdfs:domain/rdfs:subclassOf*) <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
         ?property dhfc:usesTemporalMarker ?time.
         OPTIONAL {?property owl:inverseOf ?inverse}
    }
    }"""

    objectPs=querySPARQL(sparqlEndpoint, queryReif)
    for entry in objectPs :
        res=vals(entry)
        res["type"]="ReifiedProperty"
        res["temporality"]=True
        properties.append(res)

    queryNAry="""
SELECT ?property ?inverse ?Temp ?inverseTemp ?time ?label ?range WHERE {
    	?g a dhfc:DomainGraph.
        GRAPH ?g { 
        {?property (rdfs:domain/rdfs:subclassOf*) <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
        ?property rdfs:range ?r. ?r rdfs:subclassOf* dhfc:TemporalNAryProperty.
        ?Temp rdfs:subPropertyOf dhfc:TimeRelativeValue. {?Temp (rdfs:domain/rdfs:subclassOf*) ?r.} UNION {?Temp rdfs:domain ?class2. ?r rdfs:subclassOf* ?class2.} ?Temp rdfs:label ?label. ?Temp rdfs:range ?range.
        OPTIONAL {?property owl:inverseOf ?inverse}
        OPTIONAL {?Temp owl:inverseOf ?inverseTemp}
       	?time rdfs:subPropertyOf dhfc:hasTemporalMarker. {?time (rdfs:domain/rdfs:subclassOf*) ?r.} UNION {?Temp rdfs:domain ?class4. ?r rdfs:subclassOf* ?class4.}
    
    }
    }
"""
    objectPs=querySPARQL(sparqlEndpoint, queryNAry)
    for entry in objectPs :
        res=vals(entry)
        res["type"]="NAryProperty"
        res["temporality"]=True
        properties.append(res)

    querySingleton="""
        SELECT ?property ?inverse ?time ?label ?range WHERE {
    	    ?g a dhfc:DomainGraph.
        GRAPH ?g { 
            ?property rdfs:subPropertyOf* dhfc:SingletonTemporalProperty. 
            {?property (rdfs:domain/rdfs:subclassOf*) <"""+classIRI+""">.} UNION {?property rdfs:domain ?class. <"""+classIRI+"""> rdfs:subclassOf* ?class.}
            ?property rdfs:range ?range. ?property rdfs:label ?label.
        ?property dhfc:usesTemporalMarker ?time.
        OPTIONAL {?property owl:inverseOf ?inverse} 
    }
    }
"""
    objectPs=querySPARQL(sparqlEndpoint, querySingleton)
    for entry in objectPs :
        res=vals(entry)
        res["type"]="SingletonProperty"
        res["temporality"]=True
        properties.append(res)
    return properties

def mapOntology(sparqlEndpoint) :
    availableClasses=getAvailableClasses(sparqlEndpoint)
    result={}
    for cl in availableClasses :
        result[cl]=getProperties(sparqlEndpoint, cl)
    return result

def generate(content, documentBaseIRI) :
    result=""
    for key in content :
        IRI=documentBaseIRI+"#"+key
        result+=IRI+" a <"+content[key]["class"]+">.\n"
        for entry in  content[key]["assertions"] :
            base=ttlGenerator[entry[1]["type"]]
            for key in entry[1] :
                base.replace("$"+key+"$", "<"+entry[1][key]+">")
            target=documentBaseIRI+"#"+entry[0]
            base.replace("$target$", "<"+target+">")
            value=documentBaseIRI+"#"+entry[2]
            base.replace("$value$", "<"+value+">")
            if entry[1]["temporality"] :
                base.replace("$start$", str(entry[4][0]))
                base.replace("$end$", str(entry[4][1]))
            if entry[1]["type"]=="FluentValueProperty" or entry[1]["type"]=="FluentLinkProperty" :
                base.replace("$version$", target+"__"+str(entry[4][0])+"_"+str(entry[4][1]))
            if entry[1]["type"]=="SingeltonProperty" :
                base.replace("$singleton$", entry[1]["property"]+"__"+str(entry[0])+"_"+str(entry[2][1]))
            result+=base + "\n"
    return result

def updateDoc(entityContent, documentContents) :
    documentContents[entityContent[0]]=entityContent[1]
    for prop in documentContents[entityContent[0]]["assertions"] :
        if "Data" not in prop[1]["type"] :
            if prop[2] not in documentContents :
                documentContents[prop[2]]={"class" : prop[2]["type"], "assertions" : [] }
            if reverse(prop[1])!=None :
                documentContents[prop[2]]["assertions"].append((prop[2],reverse(prop[1]), prop[1] ))
    return documentContents
                
            


    


