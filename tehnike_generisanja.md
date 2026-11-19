## 1. Stanje
- **Graf kompetencija:** Learning Commons KG (Math Coherence Map + learning components), podgraf oko linearnih funkcija: 11 jezgrenih standarda (8.EE.B.5–6, 8.F.A.1–3, 8.F.B.4–5, HSF-IF.B.6, HSF-IF.C.7.a, HSF-LE.A.1.b, HSF-LE.A.2), 10 standarda preduslova i nastavaka, 27 veza preduslova, 38 learning components. Profesor je potvrdio da je ovo dobar početak.
- 8.EE.C (rešavanje linearnih jednačina i sistema) nije među preduslovima nijednog 8.F standarda u Coherence Map, pa nije uključen u jezgro.
- **Granulacija kompetencije:** razmatrana su dva nivoa, standard i learning component. Standard je pregrub za kolonu Q-matice (npr. 8.F.B.4 obuhvata određivanje nagiba, početne vrednosti i njihovo tumačenje). Learning components za 8.F.B.4 (11 veština) razlikuju se po tri dimenzije: šta se određuje (nagib / početna vrednost), kontekst (matematički / realni) i reprezentacija (opis / tabela ili grafik), što odgovara parametrima šablona. Learning Commons daje preduslove samo između standarda; preduslovi između veština mogu se izvesti sa nivoa standarda.
- **Prioritet:** istraživanje generisanja zadataka.

## 2. Rad o RL-u: „Frontier Learning"
Faro, Ramesh, Bogunovic, Lucchi (Univerzitet u Bazelu, UCL), arXiv 2609.35426, objavljen 28.9.2026. U tekstu rada nije navedena konferencija.

- **Ideja:** umesto fiksnog skupa zadataka, proceduralni generator tokom treninga stalno daje nove zadatke, a trening se drži na granici sposobnosti modela.
- **Generator:** Reasoning Gym (Stojanovski et al., NeurIPS 2025, Datasets and Benchmarks). Taskovi u radu: Countdown, Sokoban, Dice, Decimal Arithmetic, Largest Island; nijedan nije iz algebre.
- **Nivo:** kombinacija parametara generatora. Težina se meri u odnosu na trenutnu politiku, a ne unapred.
- **Izbor nivoa:**
  - regret problema = 1[rešen bar jednom] − s/n; regret nivoa = pokretni prosek (prozor 16, početna vrednost 0,5);
  - prioritet = regret + 0,05 · (vreme od poslednjeg izbora); Zipf uzorkovanje po prioritetu;
  - 30% mesta u batch-u dobija nasumičan nivo;
  - mutacija jednog atributa, sa verovatnoćom 0,4 za informativne, 0,25 za prelake i 0,02 za preteške nivoe;
  - bafer do 100 nivoa, početno 8; po koraku 4 nivoa × 16 zadataka × 8 pokušaja.
- **Rezultati:** bolji od svih baseline-ova na svih 6 podešavanja. Ablacija na Dice: PLR + mutacija 62,5, PLR + istraživanje 33,5, tj. najveći deo dobitka daje mutacija.
- **Srodne metode:** PAIRED, PLR i ACCEL (unsupervised environment design); ACCEL je algoritamski najbliži.
- **Verifikacija:** programske nagradne funkcije iz Reasoning Gym. Kod za frontier learning nije objavljen.
- **Veza sa projektom:** zadaci iz našeg generatora mogu se koristiti za ovakav trening modela, gde je nivo kombinacija kompetencije i parametara šablona. Za učenike regret nije primenljiv jer po zadatku nema dovoljno ponovljenih pokušaja; analogni pojam u teoriji prostora znanja je spoljašnja granica (outer fringe), tj. kompetencije čiji su svi preduslovi savladani.

## 3. Postojeće biblioteke za generisanje zadataka (isprobano 19.11.)
| Biblioteka | Šta daje | Rezultat provere |
|---|---|---|
| **Reasoning Gym** 0.1.25 (Python ≥ 3.11) | `create_dataset(naziv, size, seed, **parametri)`, `score_answer`; 106 dataseta; za svaki dataset klasa `...Curriculum` sa diskretnim nivoima atributa; `register_dataset(name, dataset_cls, config_cls, curriculum_cls)` za dodavanje sopstvenih generatora | Radi. `simple_equations` daje npr. „Solve for e: 56 - 98*e = -1218"; kurikulum ima po 4 nivoa za `min_terms`, `max_terms`, `min_value`, `max_value`, `operators_weights`. Algebra: `simple_equations`, `polynomial_equations`, `polynomial_multiplication`, integrali. Nema zadataka o linearnim funkcijama ni veze sa kompetencijama. |
| **mathgenerator** 1.5.0 | 126 generatora (problem + rešenje), uključujući `linear_equations`, `system_of_equations`, `intersection_of_two_lines`, `equation_of_line_from_two_points` | Radi, ali autor ga više ne održava (poslednji push april 2024). `linear_equations` daje sistem dve jednačine. Uočene greške u obliku odgovora: presek pravih daje neskraćen koeficijent (`y = -2/6x - 8`), a odgovor traženi u obliku y = kx + n glasi `3y = -19x + 326`. Nema kontrole težine ni metapodataka o veštinama. |
| **DeepMind mathematics_dataset** | Moduli `algebra__linear_1d`, `linear_2d` i `_composed` varijante, oko 2 miliona primera po modulu (Saxton et al., 2019) | Nije pokretan. Standardni skup za treniranje i poređenje neuronskih mreža. |
| **MathCAMPS** (Mishra et al.) | Common Core standardi zapisani kao gramatike; SymPy daje odgovor; LLM prevodi zadatak u tekst, a povratni prevod proverava vernost | Nije pokretan. Po ideji najbliži projektu (zadaci izvedeni iz standarda), ali bez ontologije, Q-matice i preduslova. |
| **Reasoning Core** | Formalni domeni, uključujući sisteme jednačina, sa spoljnim solverom i kontinualnom težinom; kompatibilan sa Reasoning Gym | Nije pokretan. |
| **Learning Commons tutorijal** | Preduslovi iz Coherence Map → learning components → prompt za LLM koji generiše zadatke | Nije pokretan. Tačnost odgovora nije garantovana. |
| **mathy_core** 0.9.4 (feb. 2024) | Tokenizer, parser, pravila transformacije izraza | Nije isproban. Relevantan za rešenja po koracima. |
| **mathmaker** | Radni listovi + rešenja (jednačine prvog stepena…) | Zahteva LaTeX i dosta zavisnosti; namenjen štampanim listovima. |
| **examgen / zadanko** | SymPy + LaTeX šabloni | Primeri pisanja šablona preko SymPy; nisu održavani. |

**Zaključak:** nijedna biblioteka ne povezuje zadatke sa grafom kompetencija niti daje Q-maticu. Reasoning Gym ima kontrolu težine preko kurikuluma i mehanizam za dodavanje sopstvenih generatora. Prostor za doprinos projekta: šabloni po kompetenciji opisani u ontologiji, sa ograničenjima parametara i SymPy-jem za rešenje i proveru.

## 4. Rešavanje i provera
- **SymPy** (`solve`, `linsolve`, `solve_univariate_inequality`) pokriva linearne funkcije, jednačine, sisteme i nejednačine.
- Poređenje odgovora zahteva kanonski oblik (npr. `y = kx + n` sa skraćenim koeficijentima), kao u ranijem generatoru za oduzimanje razlomaka.
- Reasoning Gym `score_answer` je postojeći obrazac za interfejs verifikatora.
- Prema opisu projekta, kvalitet se proverava reasonerom, SHACL pravilima i stručnim pregledom uzorka zadataka.

## 5. Predložena arhitektura generatora
| Deo | Predlog |
|---|---|
| Graf | Learning Commons KG, podgraf linearnih funkcija |
| Kompetencija | learning component; standard kao grupa veština; preduslovi izvedeni sa nivoa standarda |
| Šablon | RDF resurs u ontologiji: parametri, domeni, ograničenja, kompetencije, formula odgovora |
| Generator | sopstveni, registrovan kao Reasoning Gym dataset; šabloni se učitavaju SPARQL upitom; nivoi težine su atributi RG kurikuluma |
| Odgovor i provera | SymPy + kanonski oblik; `score_answer` |
| Kvalitet | SHACL oblici za šablone, reasoner za izvedene preduslove, stručni pregled uzorka |
| Izvoz | zadatak, odgovor, red Q-matice, nivo, seed; CSV i JSONL |
| Baseline | mathgenerator, DeepMind `linear_1d`/`linear_2d`, LLM generator iz Learning Commons tutorijala |

Tok: SPARQL vraća šablon za kompetenciju → generator uzorkuje parametre po nivou i odbacuje kombinacije koje krše ograničenja → SymPy računa i kanonizuje odgovor → izvoz sa Q-maticom → provera (SHACL, reasoner, stručni pregled).

## Izvori
- Frontier Learning: https://arxiv.org/abs/2609.35426
- Reasoning Gym: https://arxiv.org/abs/2505.24760 , https://github.com/open-thought/reasoning-gym
- mathgenerator: https://github.com/lukew3/mathgenerator
- DeepMind mathematics_dataset: https://github.com/deepmind/mathematics_dataset , https://huggingface.co/datasets/deepmind/math_dataset
- MathCAMPS: https://arxiv.org/abs/2407.00900
- Reasoning Core: https://arxiv.org/abs/2603.02208
- Learning Commons tutorijal: https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/generate-practice-questions.md
- mathy_core: https://github.com/mathy/mathy_core
- mathmaker: https://pypi.org/project/mathmaker/
- examgen: https://github.com/thearn/examgen ; zadanko: https://github.com/jacadzaca/zadanko