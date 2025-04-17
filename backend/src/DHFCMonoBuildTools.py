import os
from SPARQLWrapper import SPARQLWrapper, JSON
import itertools
from rdflib import Graph
import jpype
import jpype.imports
from threading import Thread

# The repository access to send queries.
sparqlQuery="http://c2200024:7200/repositories/dhfc"
# The repository access to send queries.
sparqlUpdate="http://localhost:7200/repositories/dhfc/statements"
# A prefix that will be used to create IRIs for entities
baseNameSpace="https://cluedo4kg.irit.fr/repositories/sparqluedo"
# The prefix of DHFC.
dhfc="https://w3id.org/DHFC#"

#This portion is used to carry out the connexion with the java portion of the code (Pellet)
classpath = []
for jar in os.listdir("lib"):
    classpath.append(r"lib\\"+jar)
jpype.startJVM(classpath=classpath)
from java.util import ArrayList
from java.io import ByteArrayInputStream
from org.semanticweb.owlapi.rdf.model import RDFTranslator
from org.semanticweb.owlapi.apibinding import OWLManager
from java.util.concurrent.atomic import AtomicInteger
from java.util import IdentityHashMap, HashSet
from  org.semanticweb.owlapi.util import AlwaysOutputId 
from org.semanticweb.owlapi.formats import TurtleDocumentFormat
from com.clarkparsia.pellet.owlapiv3 import PelletReasonerFactory
from org.semanticweb.owlapi.reasoner import InferenceType
from com.clarkparsia.owlapi.explanation import PelletExplanation
from  org.semanticweb.owlapi.util import InferredPropertyAssertionGenerator, InferredClassAssertionAxiomGenerator, InferredOntologyGenerator


# Used to send a SPARQL update query (query) to a SPARQL endpoint (endpoint).
# The step parameter is used to split the query into subqueries whenever it is too long to be handled by the repository.
# By default the step is at 0, and will increment every time the query is split in two. When it reaches 5, the query is abandonned.
def updateSPARQL(endpoint, query, step=0) :
    print(query)
    sparql = SPARQLWrapper(endpoint)
    sparql.setMethod("POST")
    sparql.setQuery(query)
    try :
        ret = sparql.query()
        ret.response.read()
    except : 
        sp=query.split("GRAPH ")
        qr=query.split("{")
        q1=""
        for x in range(len(sp)//2) :
            if x>0 :
                q1+="GRAPH "
            q1+=sp[x]
        q1+="}"
        q2=qr[0]+"{"
        for x in range(len(sp)//2, len(sp)) :
            q2+="GRAPH "
            q2+=sp[x]
        if step<5 :
                updateSPARQL(endpoint, q1, step=step+1)
                updateSPARQL(endpoint, q2, step=step+1)
        else :
                print("Step: "+str(step))
                raise
        
# A class to get results from threads
class ReturnableThread(Thread):
    # This class is a subclass of Thread that allows the thread to return a value.
    def __init__(self, target):
        Thread.__init__(self)
        self.target = target
        self.result = None
    
    def run(self) -> None:
        self.result = self.target()

# Used to send a SPARQL query (query) to a SPARQL endpoint (endpoint).
def querySPARQL(endpoint, query) :
    print(endpoint)
    print(query)
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    ret = sparql.queryAndConvert()

    return ret["results"]["bindings"]

# A utility function to convert the result of a query into a list to facilitate iteration.
# Each entry is represented as a list of which the nth variable of the query is the nth element.
def toList(dic) :
    l=[] 
    for e in dic :
        f=[]
        for el in e.values() :
            f.append(el["value"])
        l.append(f)
    return l

# A utility function that takes as argument a list of lists and returns a list that is the concatenation of the elements of the parameter.
def flatten(l) :
    res=[]
    for e in l :
        res.append(e)
    return res


# A funtion that queries the repository and returns the number of interpretation universes that currently exist for a source (sourceName). 
# sourceName is the non-prefixed name of the source, and not the full IRI.
def interpretationCount(sourceName) :
    query="PREFIX dhfc: <"+dhfc+"> SELECT (COUNT(?i) AS ?count) {<"+baseNameSpace+"/"+sourceName+"> dhfc:hasInterpretation ?i} "
    ret=querySPARQL(sparqlQuery, query)
    for e in ret :
        for el in e.values() :
            return int(el["value"])

# A funtion that queries the repository and returns the number of assertion by a specific content producer (author) that currently exist for a source (sourceName). 
# sourceName is the non-prefixed name of the source, and not the full IRI. So is author.
def assertionCount(sourceName, author) :
    query="PREFIX dhfc: <"+dhfc+"> SELECT (COUNT(?o) AS ?count) {?o dhfc:assertedFrom <"+baseNameSpace+"/"+sourceName+">. <"+baseNameSpace+"/"+author+"> dhfc:assertsThrough ?a. ?a dhfc:assertsOver ?o} "
    ret=querySPARQL(sparqlQuery, query)
    for e in ret :
        for el in e.values() :
            return int(el["value"])

# Sends a query to add the typing triple for a new source.
# sourceName is the non-prefixed name of the source, and not the full IRI.
def newSource(sourceName) :
    query="""PREFIX dhfc: <"""+dhfc+""">INSERT DATA {<"""+baseNameSpace+"/"+sourceName+"""> a dhfc:Source} """
    updateSPARQL(sparqlUpdate, query)

# Checks whether an entity (eName) is referenced within the repository as subject of a triple.
# eName is the non-prefixed name of the source, and not the full IRI.
def exists(eName) :
        sparql = SPARQLWrapper(sparqlQuery)
        sparql.setQuery("""
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                ASK WHERE {
            <"""+baseNameSpace+"/"+eName+"""> ?p ?o.
            }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results["boolean"]

# Sends a query that is used to merge blank nodes that reify the same triple.
def normalize() :
    query="""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dhfc: <http://dhfc/> 
DELETE  {?bNode a rdf:Statement.?bNode rdf:subject ?s. 
                        ?bNode rdf:predicate ?p. ?bNode rdf:object ?o.		
                        ?bNode ?p2 ?o2.
                        ?s2 ?p3 ?bNode.
						?bNode dhfc:inNamedGraph ?l.
}
INSERT {?b a rdf:Statement.?b rdf:subject ?s. 
                        ?b rdf:predicate ?p. ?b rdf:object ?o.		
                        ?b ?p2 ?o2.
                        ?s2 ?p3 ?b.
						?b dhfc:inNamedGraph ?l.
}
WHERE {
  {SELECT  ?s ?p ?o ?l (SAMPLE(?bNode) AS ?b) WHERE {
    ?bNode a rdf:Statement.?bNode rdf:subject ?s. 
    ?bNode rdf:predicate ?p. ?bNode rdf:object ?o.
  } GROUP BY ?s ?p ?o ?l
  }
   ?bNode a rdf:Statement.?bNode rdf:subject ?s. 
   ?bNode rdf:predicate ?p. 
   ?bNode rdf:object ?o.
   OPTIONAL{?bNode dhfc:inNamedGraph ?l} 
   ?bNode ?p2 ?o2.
   ?s2 ?p3 ?bNode.
}"""
    updateSPARQL(sparqlUpdate, query)

# Sends an update to add a new interpretation to a source (sourceName)
# sourceName is the non-prefixed name of the source, and not the full IRI.
def newInterpretation(sourceName) :
    if not exists(sourceName) :
        newSource(sourceName)
    number=interpretationCount(sourceName)
    query="""PREFIX dhfc: <"""+dhfc+"""> INSERT DATA {<"""+baseNameSpace+"/"+sourceName+"#interpretation"+str(number)+"""> a dhfc:InterpretationUniverse. <"""+baseNameSpace+"/"+sourceName+"""> dhfc:hasInterpretation <"""+baseNameSpace+"/"+sourceName+"#interpretation"+str(number)+""">} """
    updateSPARQL(sparqlUpdate, query)
    return baseNameSpace+"/"+sourceName+"#interpretation"+str(number)

# The core function, which handles adding or editing an assertion.
# This function handles the addition or edition of a specified assertion (assertion) and notably handles the edition of the interpretation universes with the new assertion. It also handles the addition of the inferences.
# sourceName is the non-prefixed name of the source, and not the full IRI.
# assertion is the IRI of the assertion to add/edit.
# triplesSerialization is the turtle serialization of the content of the assertion.
# New is a boolean parameter that specifies whether the assertion is a new one, or if it is an old one that is edited.
# author is an optional parameter and is the non-prefixed name of the author, and not the full IRI.
def assertionProtocol(sourceName, assertion, triplesSerialization, new, author=None) :
    print(triplesSerialization)
    query="""PREFIX dhfc: <"""+dhfc+"""> INSERT DATA {
            GRAPH <"""+assertion+"""> {"""+triplesSerialization+"""}."""
    if new and author!=None :
        query+="""<"""+baseNameSpace+"/"+author+"""> dhfc:assertsThrough [dhfc:assertsOver [dhfc:assertedFrom <"""+baseNameSpace+"/"+sourceName+""">; dhfc:assertsOver  <"""+baseNameSpace+"/"+sourceName+"#interpretation"+str(assertionCount(sourceName, author))+"_"+author+""">]]"""    
    query+="""}"""
    updateSPARQL(sparqlUpdate, query)
    if new :
        pattern=checkInterpretations(sourceName, toAdd=[assertion])
    else : 
        pattern={}
        interpretationsToCheck=getListInterpretation(assertion)
        threads={}
        for interp in interpretationsToCheck :
            t=ReturnableThread(target = lambda : checkInterpretationConsistency(getListAssertion(interp),toAdd= []))
            t.start()
            threads[interp]=t
        for interp in threads :
            threads[interp].join()
            pattern[interp]=threads[interp].result
    l=[]
    for interpretation in pattern :
        t=Thread(target=editGraph, args=(pattern, interpretation, sourceName, assertion, new))
        t.start()
        l.append(t)
    for t in l :
        t.join()
        
# Sends updates to add/remove an assertion to an interpretation universe.
# pattern is a dictionnary with the keys being the interpretation, and the values being a boolean which indicates whether the assertion is coherent with this interpreation universe.
# interpretation is the IRI of the interpretation universe.
# sourceName is the non-prefixed name of the source, and not the full IRI.
# assertion is the IRI of the assertion.
# New is a boolean parameter that specifies whether the assertion is a new one, or if it is an old one that is edited.
def editGraph(pattern, interpretation, sourceName, assertion, new) :
    if pattern[interpretation] and new :
            query="""PREFIX dhfc: <"""+dhfc+""">INSERT DATA {
                <"""+interpretation+"""> dhfc:hasAssertion <"""+assertion+""">.
            }
            """
            updateSPARQL(sparqlUpdate, query)
            addInferenceResults(interpretation)
    else :
            if not new :
                query="""PREFIX dhfc: <"""+dhfc+""">DELETE DATA {
                    <"""+interpretation+""""> dhfc:hasAssertion <"""+assertion+""">.
                }"""
                updateSPARQL(sparqlUpdate, query)
            fragmentInterpretation(sourceName,interpretation, assertion)

# The function that should be called to add a new assertion. The addition includes handling interpretation universe and adding inferences.
# sourceName is the non-prefixed name of the source, and not the full IRI.
# author is the non-prefixed name of the author, and not the full IRI.
# triplesSerialization is the turtle serialization of the content of the assertion.
def newAssertionSet(sourceName, author, triplesSerialization) :
    if reasonerConsistency(triplesSerialization) :
        if interpretationCount(sourceName)==0:
            newInterpretation(sourceName)
        n=assertionCount(sourceName, author)
        assertion=baseNameSpace+"/"+sourceName+"#interpretation"+str(n)+"_"+author
        assertionProtocol(sourceName, assertion, triplesSerialization, True, author=author)
    else :
        print("Inconsistent triples not added !")

# The function that should be called to edit an assertion. The edition includes handling interpretation universe and adding inferences.
# sourceName is the non-prefixed name of the source, and not the full IRI.
# assertion is the IRI of the assertion.
# triplesSerialization is the turtle serialization of the new content of the assertion. 
def editAssertionSet(sourceName, assertion, triplesSerialization) :
    if reasonerConsistency(triplesSerialization) :
        assertionProtocol(sourceName,assertion,triplesSerialization, False)

# This function returns a dictionnary indicating for all interpretations universes of a source whether it is consistent, in particular with the addition of some assertions 
# sourceName is the non-prefixed name of the source, and not the full IRI.
# toAdd is the list of assertions whose content are added to that of the interpretation universe when checking consistency.
def checkInterpretations(sourceName, toAdd=[]) :
    query="PREFIX dhfc: <"+dhfc+"> SELECT ?i {<"+baseNameSpace+"/"+sourceName+"> dhfc:hasInterpretation ?i} "
    ret=toList(querySPARQL(sparqlQuery, query))
    dic={}
    threads={}
    for e in ret :
        t=ReturnableThread(target=lambda : checkInterpretationConsistency(getListAssertion(e[0]),toAdd= [toAdd]))
        t.start()
        threads[e[0]]=t
    for e in threads :
        threads[e].join()
        dic[e]=threads[e].result
    return dic


# Queries the repository and returns a serialization of the content of the dhfc:DomainGraph 
def ontologyContent():
    sparql = SPARQLWrapper(sparqlQuery)
    sparql.setQuery("""
            PREFIX dhfc: <"""+dhfc+""">
            CONSTRUCT {
            ?s ?p ?o
            }
            WHERE {
            GRAPH ?g {?s ?p ?o}
            ?g a dhfc:DomainGraph.
            }
        """)
    return sparql.queryAndConvert().serialize()
    
# Returns the list of assertions that are part of an interpretation.
# interpretation is the IRI of the interpretation
def getListAssertion(interpretation) :
    query="""PREFIX dhfc: <"""+dhfc+"""> SELECT ?a {<"""+interpretation+"""> dhfc:hasAssertion ?a}
        """
    return flatten(toList(querySPARQL(sparqlQuery, query)))

# Returns the list of interpretations an assertion takes part into.
# assertion is the IRI of the assertion
def getListInterpretation(assertion) :
    query="""PREFIX dhfc: <"""+dhfc+"""> SELECT ?a {?a dhfc:hasAssertion <"""+assertion+"""> }
        """
    return flatten(toList(querySPARQL(sparqlQuery, query)))

# This function returns boolean indicating whether a list assertion remains coherent when adding to it another list of assertions
# assertions is the list of IRIs of the initial set of assertions.
# toAdd is the list of assertions whose content are added to that of the interpretation universe when checking consistency.
def checkInterpretationConsistency( assertions, toAdd=[]) :
    if assertions!=None :
        ret=assertions+toAdd
        construct=ontologyContent()
        for asert in ret :
            sparql = SPARQLWrapper(sparqlQuery)
            sparql.setQuery("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                CONSTRUCT {
                ?s ?p ?o
                }
                WHERE {
                GRAPH <"""+asert[0]+"""> {?s ?p ?o.}
                }
            """)
            construct+= str(sparql.queryAndConvert().serialize())
        return reasonerConsistency(construct)
    else :
        return True

#A utility function used to create an IRI from a triple. It is used to generate IRIs for reifications so that they can be referenced outside their named graph.
def hashEncoding(triple):
    return hex(hash(triple[0]))+hex(hash(triple[1]))+hex(hash(triple[2]))

# A utility function that is used to generate the turtle serialization of a reified triple or OWL axiom.
# It returns a couple (serialization, IRI of the reified resource)
def reification(t, graphLocation=None) :
    if len(t)==1 :
        triple=reifiedVersion(t[0], graphLocation)
    else : 
        triple=reifiedOWLAxiom(t, graphLocation)
    if graphLocation!=None :
        triple=("GRAPH <"+graphLocation+"> {"+triple[0]+"}", triple[1])
    return triple

# A utility function that is used to generate the turtle serialization of a reified OWL axiom.
# It returns a couple (serialization, IRI of the reified resource)
def reifiedOWLAxiom(triples,  graphLocation=None) :
    axiomName=baseNameSpace
    for triple in triples :
        axiomName+=hashEncoding(triple)
    sparql="""<"""+axiomName+"""> a dhfc:owlAxiom. """
    for triple in triples :
        res=reifiedVersion(triple, graphLocation=graphLocation)

        sparql+=res[0]+""" <"""+axiomName+"""> dhfc:hasRDFPart <"""+res[1]+">. "
    return (sparql, axiomName)

# A utility function that is used to generate the turtle serialization of a reified triple.
# It returns a couple (serialization, IRI of the reified resource)
def reifiedVersion(triple, graphLocation=None):
    blankNodeName=baseNameSpace+hashEncoding(triple)
    sparql="""<"""+blankNodeName+"""> a rdf:Statement. <"""+blankNodeName+"""> rdf:subject <"""+triple[0]+""">. 
                        <"""+blankNodeName+"""> rdf:predicate <"""+triple[1]+""">. 
                        <"""+blankNodeName+"""> rdf:object <"""+triple[2]+""">. """
    if graphLocation!=None :
        sparql+= """<"""+blankNodeName+"""> dhfc:inNamedGraph <"""+graphLocation+""">. """
    return (sparql,blankNodeName)

# Updates the repository to clear the inference graph of an intepretation universe (interpretation), including all supports targeting it.
def clearInferenceGraph(interpretation) :
    print("Suppression")
    query="""PREFIX dhfc: <"""+dhfc+"""> SELECT ?g WHERE {<"""+interpretation+"""> dhfc:entails ?g."""
    try :
        res=toList(querySPARQL(sparqlQuery, query))[0][0]
        clearSuppports=""" PREFIX dhfc: <"""+dhfc+"""> DELETE {?s ?p ?o. ?o2 ?p ?s.} WHERE {{?s dhfc:inNamedGraph <"""+res+""">.}UNION {?s dhfc:hasRDFPart ?s1. ?s1 dhfc:inNamedGraph <"""+res+""">.} UNION {?s dhfc:isSupportFor ?s2. ?s2 dhfc:hasRDFPart ?s1. ?s1 dhfc:inNamedGraph <"""+res+""">.} UNION {?s dhfc:isSupportFor ?s2. ?s2 dhfc:inNamedGraph <"""+res+""">.} ?s ?p ?o. ?o2 ?p2 ?s.}"""
        updateSPARQL(sparqlUpdate, clearSuppports)
        updateSPARQL(sparqlUpdate, """DROP GRAPH <"""+res+""">""")
    except :
        print("No Inference Graph Found for : "+interpretation)

# Updates the repository to add a graph that contains the inferences that can be made using a OWL reasoner from the content of an interpretation universe (interpretation). It also adds the supports to explain the inferences (one explantion for each inference)
def addInferenceResults(interpretation) :
    # Clear previous inference
    clearInferenceGraph(interpretation)
    #Collect and map data from the interpretation
    locationsDic={}
    construct=""
    assertions=getListAssertion(interpretation)
    for asert in  assertions :
        sparql = SPARQLWrapper(sparqlQuery)
        sparql.setQuery("""
            CONSTRUCT {
            ?s ?p ?o
            }
            WHERE {
            GRAPH <"""+asert[0]+"""> {?s ?p ?o}
            }
        """)
        res = str(sparql.queryAndConvert().serialize())
        g=Graph()
        g.parse(data=res)
        for s, p, o in g :
            triple=(str(s), str(p), str(o))
            if triple not in locationsDic :
                locationsDic[triple]=[]
            locationsDic[triple].append(asert)
        construct+=res
    # Get ontology content :
    construct+=ontologyContent()
    # Get reasoning results :
    inferences=getInferedAxiomWithExplanation(construct)
    #Act upon reasoning results
    #Edit for correct representation(OWL Axiom)
    inferGraph=interpretation+"___"+"inferences"
    query="""PREFIX dhfc: <"""+dhfc+"> INSERT DATA {<"""+interpretation+"""> dhfc:entails <"""+inferGraph+">.<"+inferGraph+"> a dhfc:InferenceGraph. GRAPH <"+inferGraph+"> {"
    supportQuery= """PREFIX dhfc: <"""+dhfc+"""> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>  INSERT DATA {"""
    count=0
    expCount=0
    for infered in inferences :
        iTrip=splitTurtle(infered)
        for inf in iTrip :
            query+="<"+inf[0]+"> <" +inf[1]+"> <"+ inf[2]+">. "
        for explanation in inferences[infered] :
            # Ajouter le support au KG
            reif=reification(iTrip,inferGraph )
            supportQuery += reif[0] +"_:explanation"+str(expCount)+" dhfc:isSupportFor <"+reif[1]+">. "
            for triples in explanation :
                rTrip=splitTurtle(triples)
                aT=rTrip[0]
                if aT in locationsDic :
                    loc=locationsDic[aT][0][0]
                else :
                    loc=None
                reif=reification(rTrip,loc)
                supportQuery+= reif[0]+ "<"+reif[1]+"> dhfc:isPartOfSupport _:explanation"+str(expCount)+". "
                count+=1
            #TODO Reasonning pattern ?
            expCount+=1
    supportQuery+="}"
    updateSPARQL(sparqlUpdate, supportQuery) 
    query+="}}"
    updateSPARQL(sparqlUpdate, query)
    #normalize()

# Uses the Pellet reasoner and returns a boolean indicating whether some OWL based RDF content (turtleContent) is consistent.
def reasonerConsistency(turtleContent: str) : 
    input_stream = ByteArrayInputStream(turtleContent.encode())
    manager = OWLManager.createOWLOntologyManager()
    ontology = manager.loadOntologyFromOntologyDocument(input_stream)
    
    reasoner = PelletReasonerFactory().getInstance().createNonBufferingReasoner(ontology)
    manager.addOntologyChangeListener(reasoner)

    l=reasoner.isConsistent()
    if not l :
        expGen = PelletExplanation(reasoner)
        explanations=expGen.getInconsistencyExplanation()
        #TODO pour plus tard : ajouter un print de ça
    return l

# Returns the RDF serialization of an OWL axiom
def RDFserialization(axiom) :
    input_stream = ByteArrayInputStream("".encode())
    manager = OWLManager.createOWLOntologyManager()
    ontology = manager.loadOntologyFromOntologyDocument(input_stream)
    ontology.addAxiom(axiom)
    translator=RDFTranslator(manager, ontology, TurtleDocumentFormat(), False, AlwaysOutputId(), AlwaysOutputId(), AtomicInteger(1), IdentityHashMap(), HashSet())
    translator.translate(axiom)
    triples= ArrayList(translator.getGraph().getAllTriples())
    l=""
    try :
        for el in triples :
            l+=str(el)
    except Exception as err :
        print(err)
    return l

#Takes as entry an RDF serialization and returns a list of the triples.
def splitTurtle(l) :
    g=Graph()
    g.parse(data=l)
    l=[]
    for s, p, o in g :
        l.append((str(s), str(p), str(o)))
    return l

# Uses the pellet reasoner to compute all the inferences of an RDF serialization (turtleContent), and an explanation for each.
# Returns a dictionnary with structure as example :
# {<Inferred triple> : [[<Explanationp1>, <Explanationp2>]]}
def getInferedAxiomWithExplanation(turtleContent) :
    PelletExplanation.setup()
    input_stream = ByteArrayInputStream(turtleContent.encode())
    man = OWLManager.createOWLOntologyManager()
    ont = man.loadOntologyFromOntologyDocument(input_stream)
    axioms=ont.getAxioms()
    reasoner = PelletReasonerFactory().getInstance().createNonBufferingReasoner(ont)
    reasoner.precomputeInferences([InferenceType.CLASS_ASSERTIONS, InferenceType.OBJECT_PROPERTY_ASSERTIONS, InferenceType.DATA_PROPERTY_ASSERTIONS])
    gens = ArrayList()
    gens.add(InferredPropertyAssertionGenerator())
    gens.add(InferredClassAssertionAxiomGenerator())
    infOnt = man.createOntology()
    iog = InferredOntologyGenerator(reasoner, gens)
    iog.fillOntology(man.getOWLDataFactory(), infOnt) 
    infAxioms = infOnt.getAxioms()
    finals=ArrayList()
    for el in infAxioms :
        if el not in axioms :
            finals.add(el)
    expGen = PelletExplanation(reasoner)
    explanations = {}
    for ax in finals :
        rdf=RDFserialization(ax)
        try :   
            # exp=expGen.getEntailmentExplanations(ax)
            # explain=[]
            # for el in exp :
            #     subExp=[]
            #     for axiom in el :
            #         subExp.append(RDFserialization(axiom))
            #     explain.append(subExp)
            exp=expGen.getEntailmentExplanation(ax)
            explain=[]
            subExp=[]
            for axiom in exp :
                subExp.append(RDFserialization(axiom))
            explain.append(subExp)
            explanations[rdf]=(explain)
        except :
            None  
    return explanations


# Takes an interpretation universe and a new assertion and looks for sub-sets of the universe that might be coherent with this assertion. Then updates the graph with the new interpretation universes.
# sourceName is the non-prefixed name of the source, and not the full IRI.
# interpretation is the IRI of the interpretation universe
# newAssertion is the IRI of the new assertion
def fragmentInterpretation(sourceName,interpretation, newAssertion) :
    toFragment=getListAssertion(interpretation)
    l=[]
    fragmentInterpretation_rec(sourceName,toFragment, newAssertion, l)

# An auxiliary recursive function used by fragmentInterpretation
def fragmentInterpretation_rec(sourceName, assertions, newAssertion, l) :
    print(assertions)
    if len(assertions)>0 :
        frags=list(itertools.combinations(assertions, len(assertions)-1))
        thrs=[]
        for e in frags :
            t=Thread(target=fragment, args=(sourceName, e, newAssertion, l))
            t.start()
            thrs.append(t)
        for t in thrs :
            t.join()          

# A function used by fragmentInterpretation_rec to parallilize a section
def fragment(sourceName, e, newAssertion, l) :
    if e not in l :
        l.append(e)
        if checkInterpretationConsistency(list(e), toAdd=[[newAssertion]]) :
                i=newInterpretation(sourceName)
                query=query="""PREFIX dhfc: <"""+dhfc+""">INSERT DATA {"""
                eliste=list(e)
                eliste.append([newAssertion])
                for asert in eliste:
                    query+=""" <"""+i+"""> dhfc:hasAssertion <"""+asert[0]+""">."""
                query+="""}"""
                updateSPARQL(sparqlUpdate, query)
                addInferenceResults(i)
        else : 
                fragmentInterpretation_rec(sourceName, list(e), newAssertion, l)