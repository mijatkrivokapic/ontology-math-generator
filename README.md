# Projekat 7 - Generator matematičkih zadataka zasnovan na ontologiji kompetencija

Domen: linearne funkcije. Ovaj fajl je istraživački dnevnik: kratak pregled onoga što je rađeno po nedeljama, sa glavnim nalazima i fajlovima.

**Polazna osnova.** Pre projekta je, za drugi predmet, napravljen generator zadataka oduzimanja razlomaka po uzoru na 20 Tatsuokinih zadataka. Tip zadatka je tamo torka strukturnih svojstava (`features`), svi zadaci u opsegu se nabrajaju, a originali se izbacuju iz skupova za trening i probu. Neuronska mreža trenirana na svim tipovima dostiže 99,7% na probnom skupu, a trenirana samo na 20 originalnih tipova pada na 4–25% za retke tipove.

---

## Nedelja 1

### Pregled literature
- Ontološki generator zadataka za linearne funkcije, sa Q-maticom i strukturom preduslova poznatim po konstrukciji, nije pronađen. Svaki deo projekta pojedinačno ima razvijenu literaturu.
- **Isti domen:** GAEMS (Lmati et al., ontologija + SPARQL, bez Q-matice), ontologija sistema linearnih jednačina (2018), AQG za linearno programiranje (šabloni + ontologija), Singh/Gulwani i Andersen/Gulwani/Popović (tip zadatka kao apstrakcija ili trag procedure), DeepMind Mathematics (`linear_1d`, `linear_2d`).
- **Didaktika linearnih funkcija:** najveće teškoće su pri prelazu između reprezentacija (formula, grafik, tabela, reči); miskoncepcije o nagibu i odsečku (Leinhardt et al. 1990, Birgin 2012, Hattikudur et al. 2012, Eedi).
- **Šire:** ontološko generisanje pitanja (Kurdi et al. 2020, Alsubait, Keet, Alkhuzaey 2025), automatsko generisanje ajtema (Gierl i Lai), teorija prostora znanja i CbKST (Doignon i Falmagne, Heller et al., Milovanović i Jeuring 2016), Q-matice (Tatsuoka 1983), sintetički skupovi i kontaminacija (MathCAMPS, GSM-Symbolic, EFAGen), kognitivna dijagnostika LLM-ova.
- Najbliži savremeni rad je **MathCAMPS** (zadaci iz Common Core standarda preko gramatika), ali bez ontologije, Q-matice i preduslova.

### Traženje grafa kompetencija
- **Learning Commons KG:** Math Coherence Map (veze `buildsTowards` između standarda) + learning components (veštine). Izvoz fajlova nije bio dostupan iz radnog okruženja, pa je korišćen Learning Commons konektor.
- **Junyi Academy:** graf preduslova koji su označili stručnjaci; izdvojen podgraf za linearne funkcije (37 veština, 25 veza), grub i redak.
- **Dynamic Learning Maps:** 2.554 čvora i 5.605 veza, sa čvorovima za linearne funkcije, ali podaci nisu otvoreni.
- **Srpski standardi postignuća** (2024): imaju nazive kompetencija, ali nemaju graf preduslova.

### Izvlačenje podgrafa iz Learning Commons
- 21 standard (11 jezgrenih: 8.EE.B.5–6, 8.F.A.1–3, 8.F.B.4–5, HSF-IF.B.6, HSF-IF.C.7.a, HSF-LE.A.1.b, HSF-LE.A.2), 27 veza preduslova, 38 learning components, 24 miskoncepcije (Eedi, povezane po sličnosti teksta).
- 8.F.B.4 ima najviše veština (11), a one se razlikuju po tome šta se određuje (nagib / početna vrednost), kontekstu (matematički / realni) i reprezentaciji (opis / tabela ili grafik).
- Ograničenja: veze u Coherence Map znače „pomaže u učenju“, a ne strogi preduslov; progresija unapred izvučena je samo za 8.F.B.4.
- Izvoz: Turtle (470 tripleta, CASE UUID-ovi sačuvani), CSV tabele, slika grafa.

### Interaktivni graf (Jupyter)
- Graf se čita iz Turtle fajla SPARQL upitima (`rdflib`) i prikazuje pomoću vis-network.
- Klik na čvor prikazuje detalje (opis, razred, preduslovi, sledbenici, veštine, miskoncepcije) i podebljava veze; prekidač prikazuje veštine kao zasebne čvorove.
- Primer SPARQL upita sa putanjom `lf:buildsTowards+` (svi posredni preduslovi).

**Fajlovi:** `projekat7-pregled-literature.md`, `junyi_linearne_funkcije_preduslovi.csv`, `lc_linearne_funkcije.ttl`, `standardi.csv`, `preduslovi.csv`, `vestine.csv`, `miskoncepcije.csv`, `graf_preduslova.png`, `build.py`, `graf_kompetencija.ipynb`, `graf_kompetencija.html`

---

## Nedelja 2

### Graf
- Profesor je potvrdio Learning Commons podgraf kao dobar početak.
- 8.EE.C (rešavanje jednačina i sistema) nije među preduslovima nijednog 8.F standarda, pa nije u jezgru.
- Otvoreno pitanje granulacije: standard ili learning component. Standard je pregrub za kolonu Q-matice; learning components odgovaraju parametrima šablona. Learning Commons daje preduslove samo između standarda.

### Rad „Frontier Learning“ (arXiv 2609.35426)
- Proceduralni generator tokom treninga daje nove zadatke; nivo je kombinacija parametara generatora, a bira se po regretu u odnosu na trenutni model (pokretni prosek, bonus za zapostavljene nivoe, Zipf uzorkovanje, 30% nasumičnih nivoa, mutacija jednog atributa, bafer do 100 nivoa).
- Taskovi su iz Reasoning Gym (Countdown, Sokoban, Dice, Decimal Arithmetic, Largest Island); nijedan nije iz algebre. Najveći deo dobitka daje mutacija nivoa. Kod nije objavljen.
- Rad je objavljen na arXivu 28.9.2026; u tekstu nije navedena konferencija.
- Regret pristup je primenljiv za trening modela na našim zadacima. Za učenike je analogan pojam spoljašnja granica znanja (outer fringe) iz teorije prostora znanja.

### Isprobane biblioteke za generisanje (19.11.)
- **Reasoning Gym 0.1.25:** 106 dataseta, `score_answer`, klase kurikuluma sa nivoima atributa i `register_dataset` za sopstvene generatore. Algebra pokriva samo jednačine i polinome.
- **mathgenerator 1.5.0:** 126 generatora, ali nije održavan. Uočene su greške u obliku odgovora: neskraćen koeficijent kod preseka pravih, a jednačina prave nije u obliku y = kx + n.
- **Ostalo:** mathy_core, mathmaker, examgen, zadanko (stariji ili neodržavani); DeepMind mathematics_dataset, MathCAMPS, Reasoning Core i Learning Commons tutorijal za LLM generisanje evidentirani su kao baseline ili uzor.
- Nijedna biblioteka ne povezuje zadatke sa kompetencijama niti daje Q-maticu. Postojeći generatori pokrivaju uglavnom jednačine (8.EE.C), a od 38 veština za linearne funkcije samo jednu (prava kroz dve tačke).

### Provera plana prema opisu projekta
- Plan za generator (Python + SymPy šabloni) nije obuhvatio ontologiju šablona, SPARQL, Q-maticu, SHACL ni reasoner, koji su deo opisa projekta.
- Prvi predloženi šablon (8.EE.C.7, jednačina sa jednom nepoznatom) bio je van domena linearnih funkcija; zamenjen je sa 8.F.B.4.
- Zajednički dokument o napretku je prepravljen u činjenični izveštaj.

### Povezivanje grafa sa generatorima
Razmotrena su tri načina, koji se međusobno dopunjuju:
1. **Mapiranje:** postojeći generator se upisuje u ontologiju kao šablon (`lf:meri`, `lf:generator`, `lf:parametri`). Pristup je jednostavan, ali pokriva malo.
2. **Naknadno označavanje:** kompetencije se računaju iz strukturnih svojstava generisanog zadatka (kao `features` kod razlomaka), pomoću pravila u ontologiji (SPARQL `CONSTRUCT` ili SHACL rules). Q-matica se tako dobija po zadatku.
3. **Sopstveni šabloni kao Reasoning Gym dataseti:** parametri, domeni, ograničenja, formula odgovora i kompetencije opisani su u ontologiji; jedna opšta klasa ih čita SPARQL-om i registruje u Reasoning Gym, a nivoi kurikuluma su parametri težine.

LLM generisanje uz SymPy proveru je dodatni izvor za tekstualne zadatke. Predloženi tok: SPARQL bira šablon, generator pravi zadatak, pravila računaju stvarne kompetencije, SHACL proverava slaganje sa traženim, a zadatak se izvozi sa redom Q-matice.

**Fajlovi:** `projekat7-zajednicki-dokument.md`

### Sledeći koraci
- Pregled izvornog koda Reasoning Gym `simple_equations` i `SimpleEquationsCurriculum`.
- RDF model šablona i SHACL oblik za njega.
- Prvi šablon za 8.F.B.4 (nagib i početna vrednost iz dve tačke), registrovan u Reasoning Gym.
- Pokretanje baseline generatora (mathgenerator, DeepMind `linear_1d`/`linear_2d`).