"""Gradi graf kompetencija za linearne funkcije iz podataka Learning Commons Knowledge Graph
(preuzeto preko Learning Commons MCP konektora, 2026-11-15). Licenca podataka: CC BY 4.0."""
import csv, subprocess
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, SKOS, DCTERMS, XSD

S = {  # code: (uuid, grade, core?, description)
 "7.RP.A.2": ("6b9d7951-d7cc-11e8-824f-0242ac160002", "7", False, "Recognize and represent proportional relationships between quantities."),
 "7.G.A.1": ("6b9c342f-d7cc-11e8-824f-0242ac160002", "7", False, "Solve problems involving scale drawings of geometric figures, including computing actual lengths and areas from a scale drawing and reproducing a scale drawing at a different scale."),
 "8.G.A.5": ("6b9f89a0-d7cc-11e8-824f-0242ac160002", "8", False, "Use informal arguments to establish facts about the angle sum and exterior angle of triangles, about the angles created when parallel lines are cut by a transversal, and the angle-angle criterion for similarity of triangles."),
 "8.EE.B.5": ("6b9f8362-d7cc-11e8-824f-0242ac160002", "8", True, "Graph proportional relationships, interpreting the unit rate as the slope of the graph. Compare two different proportional relationships represented in different ways."),
 "8.EE.B.6": ("6b9fff6f-d7cc-11e8-824f-0242ac160002", "8", True, "Use similar triangles to explain why the slope m is the same between any two distinct points on a non-vertical line in the coordinate plane; derive the equation y = mx for a line through the origin and the equation y = mx + b for a line intercepting the vertical axis at b."),
 "8.F.A.1": ("6b9c4367-d7cc-11e8-824f-0242ac160002", "8", True, "Understand that a function is a rule that assigns to each input exactly one output. The graph of a function is the set of ordered pairs consisting of an input and the corresponding output."),
 "8.F.A.2": ("6b9d816d-d7cc-11e8-824f-0242ac160002", "8", True, "Compare properties of two functions each represented in a different way (algebraically, graphically, numerically in tables, or by verbal descriptions)."),
 "8.F.A.3": ("6b9e5396-d7cc-11e8-824f-0242ac160002", "8", True, "Interpret the equation y = mx + b as defining a linear function, whose graph is a straight line; give examples of functions that are not linear."),
 "8.F.B.4": ("6b9ef36a-d7cc-11e8-824f-0242ac160002", "8", True, "Construct a function to model a linear relationship between two quantities. Determine the rate of change and initial value of the function from a description of a relationship or from two (x, y) values, including reading these from a table or from a graph. Interpret the rate of change and initial value of a linear function in terms of the situation it models, and in terms of its graph or a table of values."),
 "8.F.B.5": ("6b9f86d5-d7cc-11e8-824f-0242ac160002", "8", True, "Describe qualitatively the functional relationship between two quantities by analyzing a graph. Sketch a graph that exhibits the qualitative features of a function that has been described verbally."),
 "HSF-IF.A.1": ("6b9c6130-d7cc-11e8-824f-0242ac160002", "HS", False, "Understand that a function from one set (domain) to another (range) assigns to each element of the domain exactly one element of the range; function notation f(x)."),
 "HSF-IF.B.6": ("6ba00b75-d7cc-11e8-824f-0242ac160002", "HS", True, "Calculate and interpret the average rate of change of a function (presented symbolically or as a table) over a specified interval. Estimate the rate of change from a graph."),
 "HSF-IF.C.7.a": ("6ba16016-d7cc-11e8-824f-0242ac160002", "HS", True, "Graph linear and quadratic functions and show intercepts, maxima, and minima."),
 "HSF-LE.A.1": ("6b9c644f-d7cc-11e8-824f-0242ac160002", "HS", False, "Distinguish between situations that can be modeled with linear functions and with exponential functions."),
 "HSF-LE.A.1.b": ("6ba1e7bb-d7cc-11e8-824f-0242ac160002", "HS", True, "Recognize situations in which one quantity changes at a constant rate per unit interval relative to another."),
 "HSF-LE.A.2": ("6b9d9ca7-d7cc-11e8-824f-0242ac160002", "HS", True, "Construct linear and exponential functions, including arithmetic and geometric sequences, given a graph, a description of a relationship, or two input-output pairs (include reading these from a table)."),
 "HSF-LE.B.5": ("6b9f97c6-d7cc-11e8-824f-0242ac160002", "HS", False, "Interpret the parameters in a linear or exponential function in terms of a context."),
 "HSA-CED.A.2": ("6b9d8f41-d7cc-11e8-824f-0242ac160002", "HS", False, "Create equations in two or more variables to represent relationships between quantities; graph equations on coordinate axes with labels and scales."),
 "HSF-BF.A.1.a": ("6ba15907-d7cc-11e8-824f-0242ac160002", "HS", False, "Determine an explicit expression, a recursive process, or steps for calculation from a context."),
 "HSF-BF.A.2": ("6b9d974a-d7cc-11e8-824f-0242ac160002", "HS", False, "Write arithmetic and geometric sequences both recursively and with an explicit formula, use them to model situations, and translate between the two forms."),
 "HSS-ID.C.7": ("6ba08773-d7cc-11e8-824f-0242ac160002", "HS", False, "Interpret the slope (rate of change) and the intercept (constant term) of a linear model in the context of the data."),
}

# buildsTowards (preduslov -> sledbenik), iz find_standards_progression_from_standard
EDGES = [
 ("7.RP.A.2","8.EE.B.5"),
 ("7.G.A.1","8.EE.B.6"),("7.RP.A.2","8.EE.B.6"),("8.G.A.5","8.EE.B.6"),
 ("7.RP.A.2","8.F.A.1"),
 ("8.F.A.1","8.F.A.2"),("7.RP.A.2","8.F.A.2"),("8.EE.B.5","8.F.A.2"),("8.EE.B.6","8.F.A.2"),
 ("8.F.A.1","8.F.A.3"),("8.F.A.2","8.F.A.3"),("8.EE.B.6","8.F.A.3"),
 ("7.RP.A.2","8.F.B.4"),("8.F.A.3","8.F.B.4"),
 ("8.F.A.1","8.F.B.5"),("8.F.A.2","8.F.B.5"),("8.F.A.3","8.F.B.5"),
 ("8.F.B.4","HSF-IF.B.6"),
 ("HSF-IF.A.1","HSF-IF.C.7.a"),
 ("HSF-LE.A.1","HSF-LE.A.2"),("8.F.B.4","HSF-LE.A.2"),
 ("8.F.B.4","HSF-LE.A.1"),("8.F.B.4","HSA-CED.A.2"),("8.F.B.4","HSF-BF.A.2"),("8.F.B.4","HSF-LE.B.5"),
 ("8.F.B.4","HSF-IF.B.6"),("8.F.B.4","HSS-ID.C.7"),("8.F.B.4","HSF-BF.A.1.a"),
]
EDGES = sorted(set(EDGES))

LC = {  # standard: [(uuid, description)]
 "8.EE.B.5": [("0edaa02c-0e8e-5b84-a494-665b641dba4b","Graph proportional relationships"),
              ("c7ca6f31-ac92-53a4-aa20-6cd3ccb6b797","Interpret the slope of the graph of a proportional relationship as the unit rate"),
              ("fbbff3cd-ef58-5383-ab5a-94c445fcd933","Compare two proportional relationships represented in different ways")],
 "8.EE.B.6": [("650c0c11-6bac-5dfd-b42b-93aef8079aef","Use similar triangles to explain why the slope of a line graphed on the coordinate plane is consistent"),
              ("c931c413-a900-5840-9634-597c5ba0dfdc","Write the equation y = mx for a line graphed through the origin"),
              ("3e7febf4-233b-564a-8db2-a612fc5e3de5","Write the equation y = mx + b for a line graphed not through the origin")],
 "8.F.A.1": [("f50b9fed-bce3-5365-a39c-188686c9b2c1","Identify a relationship as a function if it assigns exactly one output to every input"),
             ("d37fc186-0516-5779-9949-4b14f28cafa2","Identify a relationship as a function if its graph is the set of ordered pairs, (x, y), consisting of an input, x, and its corresponding output, y")],
 "8.F.A.2": [("74b65cd2-9ddc-5362-a276-2d6dfa20b0bd","Compare properties of two functions each represented in a different way")],
 "8.F.A.3": [("646a03d8-7880-5331-8ac5-ab4912d891ca","Identify the equation y = mx + b as representing a linear function"),
             ("19cec163-412b-5bb2-bddf-f54d76cbd37a","Identify the graph of a line as representing a linear function"),
             ("469afc42-3bc5-5b32-b937-e05b8bdcbd2e","Recognize and give examples of functions that are (or are not) linear")],
 "8.F.B.4": [("dab9e9b0-faa3-5080-9f2e-ac82c0ba0346","Model a linear relationship between two quantities with a function"),
             ("1944c542-6fe1-5883-beee-d6fe87cc5e7f","Determine the rate of change of a function from a mathematical context presented with a verbal description"),
             ("e1ce9802-e05b-541d-ae86-641087a49faf","Determine the rate of change of a function from a mathematical context presented in a table or graph"),
             ("dd4d95c3-4e5b-511f-b490-f0bf52638e99","Determine the rate of change of a function from a real-world context presented with a verbal description"),
             ("c6f0747b-6ee8-5e35-95d9-d25d8f5debc6","Determine the rate of change of a function from a real-world context presented in a table or graph"),
             ("411f2a23-973d-5338-9a16-93f6c252b221","Determine the initial value of a function from a mathematical context presented with a verbal description"),
             ("5f3a9252-5252-54ed-9c00-f4c910b3b9a4","Determine the initial value of a function from a mathematical context presented in a table or graph"),
             ("c8e759d8-4ed5-597d-a8ae-6a20147a354d","Determine the initial value of a function from a real-world context presented with a verbal description"),
             ("443d082c-df90-5586-8d15-fc375f4a8b4f","Determine the initial value of a function from a real-world context presented in a table or graph"),
             ("b2a9431b-e28d-5c7c-8a46-e0012eef91b8","Interpret the rate of change of a linear function in the context of the situation it models"),
             ("6c340f89-4534-5ed4-acee-bb1e959071d4","Interpret the initial value of a linear function in the context of the situation it models")],
 "8.F.B.5": [("13cc406a-cb0c-5917-9440-9be51de9017f","Qualitatively describe the relationship between two quantities by analyzing the graph of a function that relates the two quantities"),
             ("f0af8f05-3a5f-5ea0-a04b-f29e2ae8e2a9","Sketch by hand a graph that exhibits particular qualitative features that are described verbally")],
 "HSF-IF.B.6": [("da9534b0-d837-5e37-ae66-d506a2231d78","Calculate the average rate of change over a specified interval of a function presented symbolically or in a table"),
                ("ec373d80-fbd7-58c3-b8c2-d71abefa9039","Estimate the average rate of change over a specified interval of a function from the function's graph"),
                ("5409556b-2f94-54b7-8d77-4ce5d3e86e27","Interpret, in context, the average rate of change of a function over a specified interval")],
 "HSF-IF.C.7.a": [("5ee603c3-6430-5a02-92ef-bc00f7cb1a6d","Graph linear functions from mathematical contexts, showing intercepts"),
                  ("67ef0ce9-3dbe-53c0-ac19-9baa91cba7bd","Graph linear functions from real-world contexts, showing intercepts")],
 "HSF-LE.A.1.b": [("646e93bc-23b5-57bc-9e03-b7ae4f4ef83c","Describe situations where one quantity changes at a constant rate per unit interval as compared to another")],
 "HSF-LE.A.2": [("35102d70-6aea-505b-85c7-fdff4ceb58af","Construct a linear function for a mathematical context given an arithmetic sequence, a graph, a description of a relationship, or two input-output pairs (include reading these from a table)"),
                ("f206886c-6628-5dbd-a241-acc362587b88","Construct a linear function for a real-world context given an arithmetic sequence, a graph, a description of a relationship, or two input-output pairs (include reading these from a table)"),
                ("0481241f-0379-5894-af6e-94c154b5c75c","Construct a linear function for a real-world context given a graph of the relationship"),
                ("31441479-cfd2-5fe3-8bee-9c0bfd8c6157","Construct a linear function for a real-world context given the slope of the line and a point"),
                ("b1c76477-8b9c-5600-a773-80d468f1828b","Construct a linear function for a real-world context given two sets of integer coordinates"),
                ("292473be-87e5-56b0-b12f-1c7d1f4c22f5","Construct a linear function for a real-world context that can be modeled with a horizontal line"),
                ("b175a42f-27b6-525a-b33a-6e518abb2c73","Construct a linear function for a real-world context that can be modeled with a vertical line")],
}
# Izostavljeno jer nije o linearnim funkcijama: 2 LC za kvadratne funkcije (HSF-IF.C.7.a) i 2 za eksponencijalne (HSF-LE.A.2).

# Miskoncepcije (Eedi, približno poklapanje po sličnosti teksta; izbačene one koje nisu o temi)
MIS = [
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","0b5ba855-bf2d-50d4-85f4-226213d94eea","Believes the rate of change represents the initial fixed value in a linear relationship"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","5279057e-1ed9-594b-a0b8-4dec30664925","Confuses the slope with the initial value on a graph"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","3700b545-f19c-543d-98a6-29cd5fa7e709","Believes the initial fixed value on a graph is the highest value on the y-axis"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","54fecd97-4a5f-5e9f-9a51-60aa031a27b9","Thinks the 'initial fixed value' on a graph is at x=1"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","b4b7c0a7-23b2-5a2c-af82-d15f1858321e","Assumes that values in a table are consecutive"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented in a table or graph","38a03c13-8788-53fe-9141-6ed1ea249c8d","Confuses original and additional amounts in proportion problems"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented with a verbal description","342a9ea5-5e69-5dfd-b88e-0211cc1268c8","Confuses variable and fixed expenses"),
 ("8.F.B.4","Determine the initial value of a function from a real life context presented with a verbal description","cf42df6a-cdac-5d23-a59f-607a9f4a60c6","Thinks pages read per day equals total pages"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","21b5f6d5-d83e-5c27-bff8-fe29514dc278","Believes a downward line has a positive gradient"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","8d44e01f-35dd-5f9b-a02a-d850a0016ef6","Believes an upward line has a negative gradient"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","71160496-8f83-5ebc-89df-0a75868e752d","Believes gradient = change in x/change in y"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","8dc5e255-d927-5dff-a1f0-f7b8c61c3517","Thinks the scale factor is the gradient when using similar triangles"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","d9a0180b-352d-51f3-90a3-44072c76b13c","Believes similar triangles have different slopes"),
 ("8.EE.B.6","Know that the hypotenuses of two similar right triangles constructed along the same line will share the same slope","e6ab0635-9ded-55d7-8061-9b857fa8fec2","Believes the gradient of corresponding sides in similar triangles is multiplied by the scale factor"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","b6289710-fc25-5c99-9267-56dbe6473508","Believes gradient = change in x"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","c78634f7-8f10-5f84-a6bf-b5c3d3ff7ec1","Believes gradient = change in y"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","eb490118-f707-5f23-8efd-e68c678f55b3","When finding the gradient from 2 points, believes they use absolute values of the changes in x and y, so all gradients are positive"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","4a53afc3-124b-5766-9227-12c941d8c7ed","Believes that the y intercept is (0, y) where y is any y coordinate on the line"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","6379d05d-9805-5d45-9de0-a08b6220c19f","Believes the y intercept is given by the difference between the y coordinates of any two points on the line"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","6e540ad2-7398-58a3-acf5-7d936a2537a8","Believes that the y intercept is where the y coordinate is 0"),
 ("8.EE.B.6","Work out the equation of a line given two points on the line, one of which is the y-intercept","0cf7d721-fe3d-5ded-924c-ae5251dbc6aa","Believes subtracting a positive number from a negative number makes the answer less negative"),
 ("8.F.A.3","Express a function machine as a linear equation","d05fb3db-c8a9-59c4-8676-4b8a024c8550","When using a function machine, confuses the input and the output"),
 ("8.F.A.3","Express a function machine as a linear equation","6467d077-7d4e-54bc-b95f-6d7dc525e491","Believes that terms can be combined regardless of their variables or indices, including constants"),
 ("8.F.A.3","Express a function machine as a linear equation","77ac8b91-442b-5dfa-b8d7-5bb58125c2e1","Thinks the fraction bar only goes under the constant even when the whole expression needs dividing"),
]

# ---------- CSV ----------
with open("standardi.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["kod","case_uuid","razred","jezgro_linearnih_funkcija","opis"])
    for k,(u,g,c,d) in S.items(): w.writerow([k,u,g,int(c),d])
with open("preduslovi.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["preduslov","sledbenik","relacija"])
    for a,b in EDGES: w.writerow([a,b,"buildsTowards"])
with open("vestine.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["lc_uuid","standard","opis"])
    for k,l in LC.items():
        for u,d in l: w.writerow([u,k,d])
with open("miskoncepcije.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["standard","eedi_konstrukt","miskoncepcija_uuid","miskoncepcija","poklapanje"])
    for s,c,u,d in MIS: w.writerow([s,c,u,d,"priblizno (Eedi, slicnost teksta)"])

# ---------- RDF ----------
LF = Namespace("https://example.org/linearne-funkcije/lc#")
CASE = Namespace("urn:uuid:")  # CASE caseIdentifierUUID kao URN
LCC = Namespace("https://learningcommons.org/kg/")
g = Graph(); g.bind("lf",LF); g.bind("skos",SKOS); g.bind("dct",DCTERMS); g.bind("lc",LCC)
for cls,lbl in [(LF.Standard,"Standard"),(LF.LearningComponent,"Learning component (veština)"),(LF.Misconception,"Miskoncepcija")]:
    g.add((cls,RDF.type,URIRef("http://www.w3.org/2002/07/owl#Class"))); g.add((cls,RDFS.label,Literal(lbl,lang="sr")))
for p,lbl,dom,rng in [(LF.buildsTowards,"vodi ka (preduslov → sledbenik)",LF.Standard,LF.Standard),
                      (LF.supports,"podržava standard",LF.LearningComponent,LF.Standard),
                      (LF.misconceptionOf,"miskoncepcija za standard",LF.Misconception,LF.Standard)]:
    g.add((p,RDF.type,URIRef("http://www.w3.org/2002/07/owl#ObjectProperty"))); g.add((p,RDFS.label,Literal(lbl,lang="sr")))
    g.add((p,RDFS.domain,dom)); g.add((p,RDFS.range,rng))
g.add((LF.coreLinearFunctions,RDF.type,URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")))
def sid(k): return LF["std_"+k.replace(".","_").replace("-","_")]
for k,(u,gr,c,d) in S.items():
    n=sid(k); g.add((n,RDF.type,LF.Standard)); g.add((n,SKOS.notation,Literal(k))); g.add((n,DCTERMS.identifier,Literal(u)))
    g.add((n,SKOS.definition,Literal(d,lang="en"))); g.add((n,LF.gradeLevel,Literal(gr))); g.add((n,LF.coreLinearFunctions,Literal(c,datatype=XSD.boolean)))
    g.add((n,SKOS.exactMatch,CASE[u]))
for a,b in EDGES: g.add((sid(a),LF.buildsTowards,sid(b)))
g.add((sid('HSF-LE.A.1.b'),DCTERMS.isPartOf,sid('HSF-LE.A.1')))
for k,l in LC.items():
    for u,d in l:
        n=LF["lc_"+u]; g.add((n,RDF.type,LF.LearningComponent)); g.add((n,DCTERMS.identifier,Literal(u)))
        g.add((n,RDFS.label,Literal(d,lang="en"))); g.add((n,LF.supports,sid(k)))
for s,c,u,d in MIS:
    n=LF["mis_"+u]; g.add((n,RDF.type,LF.Misconception)); g.add((n,DCTERMS.identifier,Literal(u)))
    g.add((n,RDFS.label,Literal(d,lang="en"))); g.add((n,LF.misconceptionOf,sid(s))); g.add((n,RDFS.comment,Literal("Eedi; matched construct: "+c,lang="en")))
ont=URIRef("https://example.org/linearne-funkcije/lc")
g.add((ont,RDF.type,URIRef("http://www.w3.org/2002/07/owl#Ontology")))
g.add((ont,DCTERMS.source,URIRef("https://docs.learningcommons.org/knowledge-graph/")))
g.add((ont,DCTERMS.license,URIRef("https://creativecommons.org/licenses/by/4.0/")))
g.add((ont,RDFS.comment,Literal("Podgraf Learning Commons Knowledge Graph za linearne funkcije (Math Coherence Map, Math learning components, Eedi misconceptions), preuzet 2026-11-15.",lang="sr")))
g.serialize("lc_linearne_funkcije.ttl",format="turtle")
print("tripleta:",len(g))

# ---------- slika ----------
core={k for k,v in S.items() if v[2]}
lines=['digraph G {','rankdir=LR; nodesep=0.25; ranksep=0.6; bgcolor="white";',
 'node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, color="#555555"];',
 'edge [color="#888888", arrowsize=0.7];']
for k,(u,gr,c,d) in S.items():
    nlc=len(LC.get(k,[]))
    fill = "#1f6feb" if c else "#e6e6e6"; fc = "white" if c else "#333333"
    lab=k+(f"\\n{nlc} veština" if nlc else "")
    lines.append(f'"{k}" [label="{lab}", fillcolor="{fill}", fontcolor="{fc}"];')
for a,b in EDGES: lines.append(f'"{a}" -> "{b}";')
lines.append('"HSF-LE.A.1.b" -> "HSF-LE.A.1" [style=dashed, label=" deo od", fontsize=9, fontname="Helvetica"];')
lines.append('}')
open("graf.dot","w").write("\n".join(lines))
subprocess.run(["dot","-Tpng","-Gdpi=150","graf.dot","-o","graf_preduslova.png"],check=True)
print("standarda",len(S),"veza",len(EDGES),"vestina",sum(len(v) for v in LC.values()),"miskoncepcija",len(MIS))
