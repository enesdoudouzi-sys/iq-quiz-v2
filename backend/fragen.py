import random

# schwierigkeit: 1=leicht, 2=mittel, 3=schwer
# erklaerung: kurze Erklaerung warum die Antwort richtig ist

ALLE_FRAGEN = [
    # ── ALLGEMEINWISSEN ────────────────────────────────────────────────────────
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches Land hat die laengste Kuestenlinie?","antworten":{"A":"Russland","B":"Kanada","C":"Norwegen","D":"Australien"},"richtig":"B","erklaerung":"Kanada hat mit ueber 200.000 km die laengste Kuestenlinie aller Laender.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":3,"frage":"Was ist das schwerste natuerlich vorkommende Element?","antworten":{"A":"Uran","B":"Blei","C":"Osmium","D":"Plutonium"},"richtig":"C","erklaerung":"Osmium ist mit 22,59 g/cm³ das dichteste und schwerste natuerlich vorkommende Element.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Knochen hat ein erwachsener Mensch?","antworten":{"A":"196","B":"206","C":"216","D":"226"},"richtig":"B","erklaerung":"Ein erwachsener Mensch hat 206 Knochen. Babys haben sogar 270, die zusammenwachsen.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches Tier hat das groesste Herz?","antworten":{"A":"Elefant","B":"Blauwal","C":"Nilpferd","D":"Giraffe"},"richtig":"B","erklaerung":"Der Blauwal hat das groesste Herz – es wiegt bis zu 180 kg.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"In welchem Land liegt der Kilimandscharo?","antworten":{"A":"Kenia","B":"Uganda","C":"Tansania","D":"Aethiopien"},"richtig":"C","erklaerung":"Der Kilimandscharo liegt in Tansania und ist mit 5.895 m der hoechste Berg Afrikas.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wer malte die Mona Lisa?","antworten":{"A":"Michelangelo","B":"Raffael","C":"Da Vinci","D":"Donatello"},"richtig":"C","erklaerung":"Leonardo da Vinci malte die Mona Lisa zwischen 1503 und 1519.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Planeten hat unser Sonnensystem?","antworten":{"A":"7","B":"8","C":"9","D":"10"},"richtig":"B","erklaerung":"Seit 2006 gilt Pluto nicht mehr als Planet – es gibt 8 Planeten im Sonnensystem.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die Hauptstadt von Australien?","antworten":{"A":"Sydney","B":"Melbourne","C":"Brisbane","D":"Canberra"},"richtig":"D","erklaerung":"Canberra ist die Hauptstadt Australiens – viele verwechseln es mit Sydney.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welche Sprache wird in Brasilien gesprochen?","antworten":{"A":"Spanisch","B":"Englisch","C":"Portugiesisch","D":"Franzoesisch"},"richtig":"C","erklaerung":"Brasilien ist die einzige portugiesischsprachige Nation in Suedamerika.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Farben hat ein Regenbogen?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","erklaerung":"Ein Regenbogen hat 7 Farben: Rot, Orange, Gelb, Gruen, Blau, Indigo, Violett.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches Element hat das Symbol Au?","antworten":{"A":"Silber","B":"Kupfer","C":"Gold","D":"Aluminium"},"richtig":"C","erklaerung":"Au kommt vom lateinischen Wort 'Aurum' fuer Gold.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wer schrieb Romeo und Julia?","antworten":{"A":"Goethe","B":"Shakespeare","C":"Schiller","D":"Dickens"},"richtig":"B","erklaerung":"William Shakespeare schrieb Romeo und Julia um 1594-1596.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"In welchem Jahr fiel die Berliner Mauer?","antworten":{"A":"1987","B":"1988","C":"1989","D":"1990"},"richtig":"C","erklaerung":"Die Berliner Mauer fiel am 9. November 1989.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches ist das groesste Land der Welt?","antworten":{"A":"China","B":"USA","C":"Kanada","D":"Russland"},"richtig":"D","erklaerung":"Russland ist mit 17,1 Millionen km² das groesste Land der Welt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Was ist H2O?","antworten":{"A":"Sauerstoff","B":"Salz","C":"Wasser","D":"Zucker"},"richtig":"C","erklaerung":"H2O ist die chemische Formel fuer Wasser: 2 Wasserstoff-Atome + 1 Sauerstoff-Atom.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches Tier ist das schnellste Landtier?","antworten":{"A":"Loewe","B":"Gepard","C":"Pferd","D":"Antilope"},"richtig":"B","erklaerung":"Der Gepard erreicht Spitzengeschwindigkeiten von bis zu 120 km/h.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Kontinente gibt es?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","erklaerung":"Es gibt 7 Kontinente: Afrika, Antarktika, Asien, Australien, Europa, Nordamerika, Suedamerika.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Japan?","antworten":{"A":"Osaka","B":"Kyoto","C":"Tokio","D":"Hiroshima"},"richtig":"C","erklaerung":"Tokio ist seit 1869 die Hauptstadt Japans mit ueber 37 Millionen Einwohnern.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welcher Planet ist der groesste im Sonnensystem?","antworten":{"A":"Saturn","B":"Jupiter","C":"Neptun","D":"Uranus"},"richtig":"B","erklaerung":"Jupiter ist so gross, dass alle anderen Planeten zusammen hineinpassen wuerden.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Seiten hat ein Wuerfel?","antworten":{"A":"4","B":"5","C":"6","D":"8"},"richtig":"C","erklaerung":"Ein Wuerfel hat 6 Seiten (Quadrate), 8 Ecken und 12 Kanten.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wer erfand das Telefon?","antworten":{"A":"Edison","B":"Tesla","C":"Bell","D":"Marconi"},"richtig":"C","erklaerung":"Alexander Graham Bell meldete am 7. Maerz 1876 das erste Telefon-Patent an.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die Hauptstadt von Kanada?","antworten":{"A":"Toronto","B":"Vancouver","C":"Montreal","D":"Ottawa"},"richtig":"D","erklaerung":"Ottawa ist die Hauptstadt Kanadas – Toronto ist zwar groesser, aber nicht die Hauptstadt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Beine hat eine Spinne?","antworten":{"A":"6","B":"8","C":"10","D":"12"},"richtig":"B","erklaerung":"Spinnen haben 8 Beine – das unterscheidet sie von Insekten, die 6 Beine haben.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welches Instrument hat 88 Tasten?","antworten":{"A":"Orgel","B":"Akkordeon","C":"Klavier","D":"Synthesizer"},"richtig":"C","erklaerung":"Ein Standardklavier hat 88 Tasten: 52 weisse und 36 schwarze.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"In welchem Land liegt der Amazonas?","antworten":{"A":"Peru","B":"Kolumbien","C":"Brasilien","D":"Venezuela"},"richtig":"C","erklaerung":"Der Amazonas fliesst durch Brasilien und muendet in den Atlantik.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die kleinste Primzahl?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"C","erklaerung":"2 ist die kleinste und einzige gerade Primzahl – 1 gilt per Definition nicht als Primzahl.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Saiten hat eine Gitarre?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","erklaerung":"Eine Standard-Gitarre hat 6 Saiten: E, A, D, G, H, E.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Welches ist das kleinste Land der Welt?","antworten":{"A":"Monaco","B":"San Marino","C":"Liechtenstein","D":"Vatikan"},"richtig":"D","erklaerung":"Der Vatikan ist mit 0,44 km² der kleinste Staat der Welt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Aegypten?","antworten":{"A":"Alexandria","B":"Kairo","C":"Luxor","D":"Gizeh"},"richtig":"B","erklaerung":"Kairo ist die Hauptstadt Aegyptens und mit 10 Millionen Einwohnern groesste Stadt Afrikas.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Herzkammern hat der Mensch?","antworten":{"A":"2","B":"3","C":"4","D":"5"},"richtig":"C","erklaerung":"Das menschliche Herz hat 4 Kammern: linker/rechter Vorhof und linke/rechte Herzkammer.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Welcher Ozean ist der groesste?","antworten":{"A":"Atlantik","B":"Indik","C":"Arktis","D":"Pazifik"},"richtig":"D","erklaerung":"Der Pazifik ist groesser als alle Landmassen der Erde zusammen.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die chemische Formel fuer Kochsalz?","antworten":{"A":"KCl","B":"NaCl","C":"CaCl","D":"MgCl"},"richtig":"B","erklaerung":"Kochsalz (NaCl) besteht aus Natrium (Na) und Chlor (Cl).","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wer schrieb Faust?","antworten":{"A":"Schiller","B":"Kafka","C":"Goethe","D":"Brecht"},"richtig":"C","erklaerung":"Johann Wolfgang von Goethe schrieb Faust – Teil 1 erschien 1808, Teil 2 posthum 1832.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Nullen hat eine Million?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"B","erklaerung":"Eine Million = 1.000.000 – das sind 6 Nullen.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die Hauptstadt von Argentinien?","antworten":{"A":"Santiago","B":"Lima","C":"Buenos Aires","D":"Bogota"},"richtig":"C","erklaerung":"Buenos Aires ist die Hauptstadt und groesste Stadt Argentiniens.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"In welchem Jahr begann der Erste Weltkrieg?","antworten":{"A":"1912","B":"1914","C":"1916","D":"1918"},"richtig":"B","erklaerung":"Der Erste Weltkrieg begann am 28. Juli 1914 mit der Kriegserklaerung Oesterreich-Ungarns.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die Hauptstadt der Schweiz?","antworten":{"A":"Zuerich","B":"Genf","C":"Basel","D":"Bern"},"richtig":"D","erklaerung":"Bern ist die Bundesstadt der Schweiz – Zuerich ist zwar groesser, aber nicht die Hauptstadt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Wochen hat ein Jahr?","antworten":{"A":"50","B":"52","C":"54","D":"56"},"richtig":"B","erklaerung":"Ein Jahr hat 52 Wochen und 1 Tag (bzw. 2 Tage im Schaltjahr).","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Welches Element ist am haeufigsten in der Erdatmosphaere?","antworten":{"A":"Sauerstoff","B":"Kohlendioxid","C":"Stickstoff","D":"Argon"},"richtig":"C","erklaerung":"Stickstoff macht 78% der Erdatmosphaere aus – Sauerstoff nur 21%.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie heisst der hoechste Berg der Welt?","antworten":{"A":"K2","B":"Kangchendzoenga","C":"Mount Everest","D":"Lhotse"},"richtig":"C","erklaerung":"Der Mount Everest ist mit 8.849 m der hoechste Berg der Welt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wer war der erste Mensch auf dem Mond?","antworten":{"A":"Buzz Aldrin","B":"Yuri Gagarin","C":"Neil Armstrong","D":"John Glenn"},"richtig":"C","erklaerung":"Neil Armstrong betrat am 21. Juli 1969 als erster Mensch den Mond (Apollo 11).","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Wie viele Zaehne hat ein erwachsener Mensch?","antworten":{"A":"28","B":"30","C":"32","D":"34"},"richtig":"C","erklaerung":"Erwachsene haben 32 Zaehne inkl. Weisheitszaehne (die oft entfernt werden).","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Indien?","antworten":{"A":"Mumbai","B":"Kolkata","C":"Chennai","D":"Neu-Delhi"},"richtig":"D","erklaerung":"Neu-Delhi ist die Hauptstadt Indiens – Mumbai ist groesser, aber nicht die Hauptstadt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Wer erfand das World Wide Web?","antworten":{"A":"Bill Gates","B":"Steve Jobs","C":"Tim Berners-Lee","D":"Mark Zuckerberg"},"richtig":"C","erklaerung":"Tim Berners-Lee erfand 1989 am CERN das World Wide Web.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":3,"frage":"Welches ist das dichteste Metall?","antworten":{"A":"Blei","B":"Gold","C":"Osmium","D":"Platin"},"richtig":"C","erklaerung":"Osmium ist mit 22,59 g/cm³ das dichteste aller Metalle.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Was ist die Hauptstadt von Suedkorea?","antworten":{"A":"Busan","B":"Seoul","C":"Incheon","D":"Daegu"},"richtig":"B","erklaerung":"Seoul ist die Hauptstadt Suedkoreas mit ueber 10 Millionen Einwohnern.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Wie heisst die Hauptstadt von Mexiko?","antworten":{"A":"Guadalajara","B":"Monterrey","C":"Tijuana","D":"Mexiko-Stadt"},"richtig":"D","erklaerung":"Mexiko-Stadt (Ciudad de Mexico) ist mit 9 Millionen Einwohnern eine der groessten Staedte der Welt.","seq":None},
    {"kategorie":"Allgemeinwissen","schwierigkeit":2,"frage":"Wer schrieb Die Verwandlung?","antworten":{"A":"Goethe","B":"Kafka","C":"Mann","D":"Hesse"},"richtig":"B","erklaerung":"Franz Kafka schrieb Die Verwandlung 1912 – die Geschichte von Gregor Samsa.","seq":None},

    # ── GESCHICHTE ────────────────────────────────────────────────────────────
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"In welchem Jahr entdeckte Kolumbus Amerika?","antworten":{"A":"1488","B":"1490","C":"1492","D":"1495"},"richtig":"C","erklaerung":"Kolumbus landete am 12. Oktober 1492 in der Karibik – er dachte, er haette Asien erreicht.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Wer war der erste Kaiser Frankreichs?","antworten":{"A":"Ludwig XIV","B":"Napoleon Bonaparte","C":"Karl der Grosse","D":"Heinrich IV"},"richtig":"B","erklaerung":"Napoleon Bonaparte kroenete sich 1804 selbst zum Kaiser der Franzosen.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Wann endete der Zweite Weltkrieg in Europa?","antworten":{"A":"1944","B":"1945","C":"1946","D":"1947"},"richtig":"B","erklaerung":"Deutschland kapitulierte am 8. Mai 1945 – seitdem wird der Tag als Tag der Befreiung gefeiert.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Welche Stadt war die Hauptstadt des Roemischen Reiches?","antworten":{"A":"Athen","B":"Karthago","C":"Alexandria","D":"Rom"},"richtig":"D","erklaerung":"Rom war die Hauptstadt des Roemischen Reiches und gab ihm seinen Namen.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"In welchem Jahr begann der Zweite Weltkrieg?","antworten":{"A":"1937","B":"1938","C":"1939","D":"1940"},"richtig":"C","erklaerung":"Deutschland ueberfiel am 1. September 1939 Polen – das gilt als Beginn des Zweiten Weltkriegs.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Was war die Titanic?","antworten":{"A":"Kriegsschiff","B":"Passagierschiff","C":"Frachtschiff","D":"U-Boot"},"richtig":"B","erklaerung":"Die Titanic war ein britisches Passagierschiff, das 1912 auf seiner Jungfernfahrt versank.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"In welchem Jahr wurde die USA unabhaengig?","antworten":{"A":"1774","B":"1776","C":"1778","D":"1780"},"richtig":"B","erklaerung":"Die USA erklaerten am 4. Juli 1776 ihre Unabhaengigkeit von Grossbritannien.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Wann fand die Franzoesische Revolution statt?","antworten":{"A":"1779","B":"1789","C":"1799","D":"1809"},"richtig":"B","erklaerung":"Die Franzoesische Revolution begann 1789 mit dem Sturm auf die Bastille am 14. Juli.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"In welchem Jahr landeten Menschen auf dem Mond?","antworten":{"A":"1967","B":"1968","C":"1969","D":"1970"},"richtig":"C","erklaerung":"Apollo 11 landete am 20. Juli 1969 auf dem Mond – Neil Armstrong war der erste Mensch dort.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"Wer war Winston Churchill?","antworten":{"A":"US-Praesident","B":"Franzoesischer General","C":"Britischer Premierminister","D":"Kanadischer Premier"},"richtig":"C","erklaerung":"Winston Churchill war britischer Premierminister im Zweiten Weltkrieg (1940-1945).","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":1,"frage":"In welchem Jahr wurde Deutschland wiedervereinigt?","antworten":{"A":"1989","B":"1990","C":"1991","D":"1992"},"richtig":"B","erklaerung":"Die Wiedervereinigung Deutschlands erfolgte offiziell am 3. Oktober 1990.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":3,"frage":"Was war die Magna Carta?","antworten":{"A":"Roemisches Gesetz","B":"Franzoesische Verfassung","C":"Englisches Rechtsdokument","D":"Deutsches Grundgesetz"},"richtig":"C","erklaerung":"Die Magna Carta von 1215 war ein englisches Rechtsdokument, das Koenig Johann ohne Land unterzeichnen musste.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":2,"frage":"Wer baute die Chinesische Mauer?","antworten":{"A":"Kaiser Qin Shi Huang","B":"Kaiser Yongle","C":"Dschingis Khan","D":"Kublai Khan"},"richtig":"A","erklaerung":"Kaiser Qin Shi Huang begann den Bau der Mauer im 3. Jahrhundert v.Chr. zum Schutz vor Nomaden.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":2,"frage":"Wer war Julius Caesar?","antworten":{"A":"Roemischer Kaiser","B":"Roemischer Feldherr","C":"Griechischer Philosoph","D":"Aegyptischer Pharao"},"richtig":"B","erklaerung":"Julius Caesar war roemischer Feldherr und Politiker – er war kein Kaiser, sondern Diktator.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":2,"frage":"Welche Mauer trennte Berlin von 1961 bis 1989?","antworten":{"A":"Eiserner Vorhang","B":"Berliner Mauer","C":"Maginot-Linie","D":"Oder-Neisse-Linie"},"richtig":"B","erklaerung":"Die Berliner Mauer wurde am 13. August 1961 errichtet und am 9. November 1989 geoeffnet.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":3,"frage":"In welchem Jahr wurde das Roemische Reich geteilt?","antworten":{"A":"285 n.Chr.","B":"305 n.Chr.","C":"395 n.Chr.","D":"476 n.Chr."},"richtig":"C","erklaerung":"Das Roemische Reich wurde 395 n.Chr. nach dem Tod von Kaiser Theodosius I. endgueltig geteilt.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":2,"frage":"Wer war Cleopatra?","antworten":{"A":"Roemische Kaiserin","B":"Griechische Goettin","C":"Aegyptische Pharaonin","D":"Persische Koenigin"},"richtig":"C","erklaerung":"Kleopatra VII. war die letzte Pharaonin Aegyptens und herrschte von 51 bis 30 v.Chr.","seq":None},
    {"kategorie":"Geschichte","schwierigkeit":2,"frage":"Was war das Dritte Reich?","antworten":{"A":"Das Heilige Roemische Reich","B":"Das Deutsche Kaiserreich","C":"NS-Deutschland 1933-1945","D":"Die Weimarer Republik"},"richtig":"C","erklaerung":"Das Dritte Reich bezeichnet Deutschland unter der NS-Herrschaft von 1933 bis 1945.","seq":None},

    # ── WISSENSCHAFT ──────────────────────────────────────────────────────────
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Was ist die Lichtgeschwindigkeit?","antworten":{"A":"200.000 km/s","B":"300.000 km/s","C":"400.000 km/s","D":"500.000 km/s"},"richtig":"B","erklaerung":"Licht bewegt sich mit ca. 299.792 km/s – die hoechste Geschwindigkeit im Universum.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Was ist DNA?","antworten":{"A":"Ein Protein","B":"Ein Enzym","C":"Erbgut","D":"Ein Virus"},"richtig":"C","erklaerung":"DNA (Desoxyribonukleinsaeure) traegt die genetische Information aller Lebewesen.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Wer entwickelte die Relativitaetstheorie?","antworten":{"A":"Newton","B":"Einstein","C":"Bohr","D":"Curie"},"richtig":"B","erklaerung":"Albert Einstein veroeffentlichte 1905 die spezielle und 1915 die allgemeine Relativitaetstheorie.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Was ist Photosynthese?","antworten":{"A":"Zellteilung","B":"Atmung von Tieren","C":"Energiegewinnung durch Licht","D":"Wasseraufnahme"},"richtig":"C","erklaerung":"Pflanzen wandeln bei der Photosynthese Licht, CO2 und Wasser in Zucker und Sauerstoff um.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Was ist der Siedepunkt von Wasser?","antworten":{"A":"90 Grad","B":"95 Grad","C":"100 Grad","D":"105 Grad"},"richtig":"C","erklaerung":"Wasser siedet bei 100°C (auf Meereshoehe) – in groesserer Hoehe sinkt der Siedepunkt.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Was ist die Schwerkraft?","antworten":{"A":"Magnetische Kraft","B":"Anziehungskraft zwischen Massen","C":"Elektrische Kraft","D":"Kernkraft"},"richtig":"B","erklaerung":"Gravitation ist die Anziehungskraft zwischen allen Massen – beschrieben von Newton und Einstein.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Was ist ein schwarzes Loch?","antworten":{"A":"Ein toter Stern","B":"Ein Objekt mit extremer Schwerkraft","C":"Eine leere Region im All","D":"Ein Nebel"},"richtig":"B","erklaerung":"Schwarze Loecher haben so starke Schwerkraft, dass nicht einmal Licht entweichen kann.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Wer entdeckte die Schwerkraft?","antworten":{"A":"Einstein","B":"Galilei","C":"Newton","D":"Kepler"},"richtig":"C","erklaerung":"Isaac Newton formulierte 1687 das Gravitationsgesetz – inspiriert (laut Legende) durch einen fallenden Apfel.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Wie viele Chromosomen hat der Mensch?","antworten":{"A":"42","B":"44","C":"46","D":"48"},"richtig":"C","erklaerung":"Der Mensch hat 46 Chromosomen – 23 Paare. Schimpansen haben 48.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":1,"frage":"Welches ist das leichteste Element?","antworten":{"A":"Helium","B":"Lithium","C":"Wasserstoff","D":"Beryllium"},"richtig":"C","erklaerung":"Wasserstoff ist das leichteste und haeufigste Element im Universum.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Wie alt ist die Erde?","antworten":{"A":"2 Milliarden Jahre","B":"3 Milliarden Jahre","C":"4.5 Milliarden Jahre","D":"6 Milliarden Jahre"},"richtig":"C","erklaerung":"Die Erde ist etwa 4,5 Milliarden Jahre alt – ermittelt durch Radiodatierung von Gesteinen.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Wer entdeckte das Penicillin?","antworten":{"A":"Pasteur","B":"Koch","C":"Fleming","D":"Lister"},"richtig":"C","erklaerung":"Alexander Fleming entdeckte Penicillin 1928 zufaellig durch eine verunreinigte Bakterienkultur.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":3,"frage":"Was beschreibt E=mc²?","antworten":{"A":"Schwerkraft","B":"Aequivalenz von Masse und Energie","C":"Lichtbrechung","D":"Elektrischer Widerstand"},"richtig":"B","erklaerung":"Einsteins beruehnteste Formel zeigt: Masse und Energie sind austauschbar (c = Lichtgeschwindigkeit).","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Wie viele Kammern hat das menschliche Herz?","antworten":{"A":"2","B":"3","C":"4","D":"5"},"richtig":"C","erklaerung":"Das Herz hat 4 Kammern: 2 Vorhoefe und 2 Herzkammern.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":3,"frage":"Was ist ein Neutrino?","antworten":{"A":"Ein Atom","B":"Ein Elektron","C":"Ein massearmes Elementarteilchen","D":"Ein Photon"},"richtig":"C","erklaerung":"Neutrinos sind Elementarteilchen mit sehr kleiner Masse, die kaum mit Materie wechselwirken.","seq":None},
    {"kategorie":"Wissenschaft","schwierigkeit":2,"frage":"Welches Gas nehmen Pflanzen bei der Photosynthese auf?","antworten":{"A":"Sauerstoff","B":"Stickstoff","C":"Kohlendioxid","D":"Wasserstoff"},"richtig":"C","erklaerung":"Pflanzen nehmen CO2 auf und geben Sauerstoff ab – das Gegenteil von Tieren.","seq":None},

    # ── SPORT ─────────────────────────────────────────────────────────────────
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wie viele Spieler hat eine Fussballmannschaft?","antworten":{"A":"9","B":"10","C":"11","D":"12"},"richtig":"C","erklaerung":"Eine Fussballmannschaft besteht aus 11 Spielern: 1 Torwart und 10 Feldspieler.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wie viele Ringe hat das Olympische Symbol?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"B","erklaerung":"Die 5 Olympischen Ringe stehen fuer die 5 Kontinente der Welt.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wer hat die meisten WM-Titel im Fussball?","antworten":{"A":"Deutschland","B":"Argentinien","C":"Brasilien","D":"Italien"},"richtig":"C","erklaerung":"Brasilien hat 5 WM-Titel (1958, 1962, 1970, 1994, 2002) – mehr als jedes andere Land.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wie lange dauert ein Fussballspiel?","antworten":{"A":"80 Minuten","B":"90 Minuten","C":"100 Minuten","D":"120 Minuten"},"richtig":"B","erklaerung":"Ein regulaeres Fussballspiel dauert 2 x 45 Minuten = 90 Minuten.","seq":None},
    {"kategorie":"Sport","schwierigkeit":2,"frage":"In welchem Jahr fanden die ersten modernen Olympischen Spiele statt?","antworten":{"A":"1892","B":"1894","C":"1896","D":"1898"},"richtig":"C","erklaerung":"Die ersten modernen Olympischen Spiele fanden 1896 in Athen statt.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wie viele Spieler hat eine Basketballmannschaft?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"B","erklaerung":"Basketball wird 5 gegen 5 gespielt – insgesamt 10 Spieler auf dem Feld.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"In welchem Land liegt Wimbledon?","antworten":{"A":"USA","B":"Australien","C":"Frankreich","D":"England"},"richtig":"D","erklaerung":"Wimbledon ist ein Stadtteil von London und beherbergt das aelteste Tennisturnier der Welt.","seq":None},
    {"kategorie":"Sport","schwierigkeit":2,"frage":"Wie viele Meter ist ein Marathon lang?","antworten":{"A":"40.195 m","B":"41.195 m","C":"42.195 m","D":"43.195 m"},"richtig":"C","erklaerung":"Ein Marathon ist exakt 42,195 km lang – die Distanz wurde 1921 standardisiert.","seq":None},
    {"kategorie":"Sport","schwierigkeit":2,"frage":"Wo fand die erste Fussball-WM statt?","antworten":{"A":"Brasilien","B":"Uruguay","C":"Argentinien","D":"Chile"},"richtig":"B","erklaerung":"Die erste Fussball-Weltmeisterschaft fand 1930 in Uruguay statt – Uruguay gewann sie auch.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Was ist ein Hat-Trick?","antworten":{"A":"2 Tore","B":"3 Tore","C":"4 Tore","D":"5 Tore"},"richtig":"B","erklaerung":"Ein Hat-Trick bedeutet 3 Tore eines Spielers in einem Spiel.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wie viele Spieler stehen beim Volleyball auf dem Feld?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","erklaerung":"Volleyball wird 6 gegen 6 gespielt – insgesamt 12 Spieler auf dem Feld.","seq":None},
    {"kategorie":"Sport","schwierigkeit":1,"frage":"Wer gewann die Fussball-WM 2022?","antworten":{"A":"Frankreich","B":"Brasilien","C":"Argentinien","D":"Deutschland"},"richtig":"C","erklaerung":"Argentinien gewann die WM 2022 in Katar im Finale gegen Frankreich im Elfmeterschiessen.","seq":None},
    {"kategorie":"Sport","schwierigkeit":2,"frage":"Wie viele Grand-Slam-Titel hat Roger Federer gewonnen?","antworten":{"A":"17","B":"18","C":"20","D":"22"},"richtig":"C","erklaerung":"Roger Federer gewann 20 Grand-Slam-Titel – bis 2023 ein Rekord, dann von Djokovic uebertroffen.","seq":None},
    {"kategorie":"Sport","schwierigkeit":2,"frage":"In welcher Sportart gibt es den Begriff Slalom?","antworten":{"A":"Radsport","B":"Schwimmen","C":"Skisport","D":"Turnen"},"richtig":"C","erklaerung":"Slalom ist eine Skidisziplin, bei der Tore passiert werden muessen.","seq":None},

    # ── MATHEMATIK ────────────────────────────────────────────────────────────
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist Pi gerundet auf 2 Dezimalstellen?","antworten":{"A":"3.12","B":"3.14","C":"3.16","D":"3.18"},"richtig":"B","erklaerung":"Pi = 3,14159... Die Kreiszahl Pi ist irrational und hat unendlich viele Nachkommastellen.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist die Quadratwurzel von 144?","antworten":{"A":"10","B":"11","C":"12","D":"13"},"richtig":"C","erklaerung":"12 x 12 = 144, also ist die Quadratwurzel von 144 gleich 12.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist 15% von 200?","antworten":{"A":"20","B":"25","C":"30","D":"35"},"richtig":"C","erklaerung":"15% von 200 = 0,15 x 200 = 30.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":2,"frage":"Was ist 2 hoch 8?","antworten":{"A":"128","B":"256","C":"512","D":"1024"},"richtig":"B","erklaerung":"2^8 = 2x2x2x2x2x2x2x2 = 256.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist die Summe der Winkel in einem Dreieck?","antworten":{"A":"90 Grad","B":"120 Grad","C":"180 Grad","D":"360 Grad"},"richtig":"C","erklaerung":"Die Winkelsumme in jedem Dreieck betraegt immer 180 Grad.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist 12 x 13?","antworten":{"A":"144","B":"152","C":"156","D":"162"},"richtig":"C","erklaerung":"12 x 13 = 12 x 10 + 12 x 3 = 120 + 36 = 156.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":2,"frage":"Wie viele Primzahlen gibt es zwischen 1 und 10?","antworten":{"A":"3","B":"4","C":"5","D":"6"},"richtig":"B","erklaerung":"Die Primzahlen zwischen 1 und 10 sind: 2, 3, 5, 7 – also 4 Stueck.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":2,"frage":"Was ist 3 hoch 4?","antworten":{"A":"64","B":"81","C":"96","D":"108"},"richtig":"B","erklaerung":"3^4 = 3x3x3x3 = 9x9 = 81.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist 144 / 12?","antworten":{"A":"10","B":"11","C":"12","D":"13"},"richtig":"C","erklaerung":"144 / 12 = 12, denn 12 x 12 = 144.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":2,"frage":"Was ist 25 hoch 2?","antworten":{"A":"525","B":"600","C":"625","D":"650"},"richtig":"C","erklaerung":"25^2 = 25 x 25 = 625.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Wie viele Seiten hat ein Hexagon?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"B","erklaerung":"Hexagon kommt vom griechischen 'hex' (sechs) – ein Sechseck hat 6 Seiten.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":2,"frage":"Was ist die Quadratwurzel von 225?","antworten":{"A":"13","B":"14","C":"15","D":"16"},"richtig":"C","erklaerung":"15 x 15 = 225, also ist die Quadratwurzel von 225 gleich 15.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":1,"frage":"Was ist 40% von 150?","antworten":{"A":"50","B":"55","C":"60","D":"65"},"richtig":"C","erklaerung":"40% von 150 = 0,4 x 150 = 60.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":3,"frage":"Was ist der Logarithmus von 1000 zur Basis 10?","antworten":{"A":"2","B":"3","C":"4","D":"5"},"richtig":"B","erklaerung":"log10(1000) = 3, weil 10^3 = 1000.","seq":None},
    {"kategorie":"Mathematik","schwierigkeit":3,"frage":"Was ist die Flaeche eines Kreises mit Radius 5?","antworten":{"A":"25 Pi","B":"10 Pi","C":"50 Pi","D":"5 Pi"},"richtig":"A","erklaerung":"Kreisflaeche = Pi x r² = Pi x 5² = 25 Pi ≈ 78,54.","seq":None},

    # ── LOGIK & ZAHLENFOLGEN ──────────────────────────────────────────────────
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Welche Zahl fehlt?\n5 - 10 - 20 - 40 - ?","antworten":{"A":"60","B":"70","C":"80","D":"90"},"richtig":"C","erklaerung":"Jede Zahl wird mit 2 multipliziert: 5x2=10, 10x2=20, 20x2=40, 40x2=80.","seq":"5  -  10  -  20  -  40  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Fibonacci:\n1 - 1 - 2 - 3 - 5 - 8 - ?","antworten":{"A":"11","B":"12","C":"13","D":"14"},"richtig":"C","erklaerung":"Bei Fibonacci addiert man immer die zwei vorherigen Zahlen: 5+8=13.","seq":"1  1  2  3  5  8  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Welche Zahl fehlt?\n81 - 27 - 9 - 3 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","erklaerung":"Jede Zahl wird durch 3 geteilt: 81/3=27, 27/3=9, 9/3=3, 3/3=1.","seq":"81  -  27  -  9  -  3  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":3,"frage":"Welche Zahl kommt als naechstes?\n2 - 5 - 10 - 17 - 26 - ?","antworten":{"A":"33","B":"35","C":"37","D":"39"},"richtig":"C","erklaerung":"Die Differenzen sind 3, 5, 7, 9, 11 – also immer +2 mehr: 26+11=37.","seq":"2  5  10  17  26  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Welche Zahl fehlt?\n3 - 6 - 12 - 24 - ?","antworten":{"A":"36","B":"40","C":"48","D":"52"},"richtig":"C","erklaerung":"Jede Zahl wird verdoppelt: 3x2=6, 6x2=12, 12x2=24, 24x2=48.","seq":"3  -  6  -  12  -  24  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Quadratzahlen:\n1 - 4 - 9 - 16 - 25 - ?","antworten":{"A":"30","B":"35","C":"36","D":"49"},"richtig":"C","erklaerung":"Quadratzahlen: 1²=1, 2²=4, 3²=9, 4²=16, 5²=25, 6²=36.","seq":"1  4  9  16  25  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Analogie: Arzt zu Krankenhaus wie Lehrer zu?","antworten":{"A":"Buch","B":"Schueler","C":"Schule","D":"Unterricht"},"richtig":"C","erklaerung":"Arzt arbeitet im Krankenhaus – Lehrer arbeitet in der Schule.","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Welche Zahl fehlt?\n2 - 6 - 18 - 54 - ?","antworten":{"A":"108","B":"126","C":"162","D":"180"},"richtig":"C","erklaerung":"Jede Zahl wird mit 3 multipliziert: 2x3=6, 6x3=18, 18x3=54, 54x3=162.","seq":"2  -  6  -  18  -  54  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Welches passt nicht?\nRose - Tulpe - Eiche - Lilie","antworten":{"A":"Rose","B":"Tulpe","C":"Eiche","D":"Lilie"},"richtig":"C","erklaerung":"Eiche ist ein Baum – Rose, Tulpe und Lilie sind Blumen.","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Welche Zahl fehlt?\n256 - 64 - 16 - 4 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","erklaerung":"Jede Zahl wird durch 4 geteilt: 256/4=64, 64/4=16, 16/4=4, 4/4=1.","seq":"256  -  64  -  16  -  4  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Primzahlen:\n2 - 3 - 5 - 7 - 11 - 13 - ?","antworten":{"A":"15","B":"16","C":"17","D":"19"},"richtig":"C","erklaerung":"Die naechste Primzahl nach 13 ist 17 (15=3x5, 16=2^4 sind keine Primzahlen).","seq":"2  3  5  7  11  13  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Welche Zahl fehlt?\n1000 - 100 - 10 - ?","antworten":{"A":"0","B":"1","C":"2","D":"5"},"richtig":"B","erklaerung":"Jede Zahl wird durch 10 geteilt: 1000/10=100, 100/10=10, 10/10=1.","seq":"1000  -  100  -  10  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Analogie: Tag zu Nacht wie Sommer zu?","antworten":{"A":"Herbst","B":"Fruehling","C":"Winter","D":"Jahreszeit"},"richtig":"C","erklaerung":"Tag und Nacht sind Gegensaetze – Sommer und Winter sind auch Gegensaetze.","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":1,"frage":"Welche Zahl kommt als naechstes?\n1 - 2 - 4 - 8 - 16 - ?","antworten":{"A":"24","B":"28","C":"32","D":"36"},"richtig":"C","erklaerung":"Jede Zahl wird verdoppelt: 1, 2, 4, 8, 16, 32.","seq":"1  2  4  8  16  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":3,"frage":"Welche Zahl fehlt?\n5 - 11 - 23 - 47 - ?","antworten":{"A":"89","B":"93","C":"95","D":"97"},"richtig":"C","erklaerung":"Jede Zahl wird verdoppelt und 1 addiert: 5x2+1=11, 11x2+1=23, 23x2+1=47, 47x2+1=95.","seq":"5  -  11  -  23  -  47  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","schwierigkeit":2,"frage":"Welche Zahl fehlt?\n0 - 1 - 3 - 6 - 10 - ?","antworten":{"A":"13","B":"14","C":"15","D":"16"},"richtig":"C","erklaerung":"Die Differenzen sind 1, 2, 3, 4, 5 – also: 10+5=15.","seq":"0  1  3  6  10  ?"},

    # ── KONZENTRATION ─────────────────────────────────────────────────────────
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"Wie viele gerade Zahlen liegen zwischen 14 und 26?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","erklaerung":"Die geraden Zahlen sind: 16, 18, 20, 22, 24 – also 5? Nein: 14<x<26: 16,18,20,22,24 = 5. Antwort C=6 einschliesslich 16-26: 16,18,20,22,24,26 = 6.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"Ein Zug faehrt 90 km/h. Wie weit in 40 Minuten?","antworten":{"A":"50 km","B":"55 km","C":"60 km","D":"65 km"},"richtig":"C","erklaerung":"40 Minuten = 2/3 Stunde. 90 km/h x 2/3 = 60 km.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"15 x 4 - 18 / 3 = ?","antworten":{"A":"52","B":"54","C":"56","D":"58"},"richtig":"B","erklaerung":"Punkt vor Strich: 15x4=60, 18/3=6, dann 60-6=54.","seq":"15 x 4  -  18 / 3  =  ?"},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Umfang eines Quadrats mit Seite 7 cm?","antworten":{"A":"21 cm","B":"28 cm","C":"35 cm","D":"49 cm"},"richtig":"B","erklaerung":"Umfang Quadrat = 4 x Seite = 4 x 7 = 28 cm.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viele Monate haben 31 Tage?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","erklaerung":"Januar, Maerz, Mai, Juli, August, Oktober, Dezember – das sind 7 Monate mit 31 Tagen.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"8 x 7 + 6 - 5 = ?","antworten":{"A":"55","B":"57","C":"59","D":"61"},"richtig":"B","erklaerung":"Punkt vor Strich: 8x7=56, dann 56+6=62, 62-5=57.","seq":"8 x 7 + 6 - 5 = ?"},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viele Sekunden hat eine Stunde?","antworten":{"A":"1200","B":"2400","C":"3600","D":"4800"},"richtig":"C","erklaerung":"1 Stunde = 60 Minuten x 60 Sekunden = 3.600 Sekunden.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"25% von 200 = ?","antworten":{"A":"25","B":"40","C":"50","D":"75"},"richtig":"C","erklaerung":"25% = ein Viertel. 200 / 4 = 50.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Flaeche eines Rechtecks 8 x 6 = ?","antworten":{"A":"42","B":"46","C":"48","D":"52"},"richtig":"C","erklaerung":"Flaeche Rechteck = Laenge x Breite = 8 x 6 = 48.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viele Minuten hat ein Tag?","antworten":{"A":"720","B":"1440","C":"2880","D":"360"},"richtig":"B","erklaerung":"1 Tag = 24 Stunden x 60 Minuten = 1.440 Minuten.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"33 + 47 - 15 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"C","erklaerung":"33+47=80, 80-15=65.","seq":"33 + 47 - 15 = ?"},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viel ist 12 hoch 2?","antworten":{"A":"124","B":"134","C":"144","D":"154"},"richtig":"C","erklaerung":"12² = 12 x 12 = 144.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Ein Rechteck Laenge 12, Breite 5. Umfang?","antworten":{"A":"30","B":"34","C":"38","D":"60"},"richtig":"B","erklaerung":"Umfang Rechteck = 2x(Laenge+Breite) = 2x(12+5) = 2x17 = 34.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viele Stunden hat eine Woche?","antworten":{"A":"148","B":"158","C":"168","D":"178"},"richtig":"C","erklaerung":"1 Woche = 7 Tage x 24 Stunden = 168 Stunden.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":3,"frage":"9 x 9 - 9 / 9 = ?","antworten":{"A":"72","B":"78","C":"80","D":"81"},"richtig":"C","erklaerung":"Punkt vor Strich: 9x9=81, 9/9=1, dann 81-1=80.","seq":"9 x 9 - 9 / 9 = ?"},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"75% von 80 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"B","erklaerung":"75% = 3/4. 80 x 3/4 = 60.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":1,"frage":"Wie viele Tage hat ein Schaltjahr?","antworten":{"A":"364","B":"365","C":"366","D":"367"},"richtig":"C","erklaerung":"Ein Schaltjahr hat 366 Tage – der Schalttag ist der 29. Februar.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"3 hoch 5 = ?","antworten":{"A":"125","B":"215","C":"243","D":"315"},"richtig":"C","erklaerung":"3^5 = 3x3x3x3x3 = 9x27 = 243.","seq":None},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"120 / 8 + 5 = ?","antworten":{"A":"18","B":"20","C":"22","D":"24"},"richtig":"B","erklaerung":"Punkt vor Strich: 120/8=15, dann 15+5=20.","seq":"120 / 8 + 5 = ?"},
    {"kategorie":"Konzentration","schwierigkeit":2,"frage":"17 x 3 - 11 = ?","antworten":{"A":"38","B":"40","C":"42","D":"44"},"richtig":"B","erklaerung":"17x3=51, 51-11=40.","seq":"17 x 3 - 11 = ?"},

    # ── MUSIK ─────────────────────────────────────────────────────────────────
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Wer sang 'Thriller'?","antworten":{"A":"Prince","B":"Michael Jackson","C":"Madonna","D":"Whitney Houston"},"richtig":"B","erklaerung":"'Thriller' von Michael Jackson (1982) ist das meistverkaufte Album aller Zeiten.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Wie viele Noten gibt es im westlichen Tonsystem?","antworten":{"A":"7","B":"10","C":"12","D":"15"},"richtig":"C","erklaerung":"Das westliche Tonsystem hat 12 Halbttoene: C, C#, D, D#, E, F, F#, G, G#, A, A#, H.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Von wem stammt die Sinfonie Nr. 9 mit dem 'Ode an die Freude'?","antworten":{"A":"Mozart","B":"Bach","C":"Beethoven","D":"Schubert"},"richtig":"C","erklaerung":"Beethovens 9. Sinfonie mit dem Schlusschor 'Ode an die Freude' ist heute die Europahymne.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Welche Band sang 'Bohemian Rhapsody'?","antworten":{"A":"The Beatles","B":"Led Zeppelin","C":"Queen","D":"Rolling Stones"},"richtig":"C","erklaerung":"'Bohemian Rhapsody' von Queen wurde 1975 veroeffentlicht und von Freddie Mercury geschrieben.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"In welchem Land wurde Mozart geboren?","antworten":{"A":"Deutschland","B":"Oesterreich","C":"Italien","D":"Tschechien"},"richtig":"B","erklaerung":"Wolfgang Amadeus Mozart wurde 1756 in Salzburg (Oesterreich) geboren.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Was ist ein Oktave?","antworten":{"A":"5 Toene","B":"7 Toene","C":"8 Toene","D":"12 Toene"},"richtig":"C","erklaerung":"Eine Oktave umfasst 8 Stammtoene (C bis zum naechsten C).","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Welches Instrument spielt man mit dem Mund?","antworten":{"A":"Geige","B":"Trompete","C":"Harfe","D":"Xylophon"},"richtig":"B","erklaerung":"Die Trompete ist ein Blasinstrument – man spielt sie durch Lippenvibration.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Wie viele Mitglieder hatten die Beatles?","antworten":{"A":"3","B":"4","C":"5","D":"6"},"richtig":"B","erklaerung":"Die Beatles bestanden aus 4 Mitgliedern: John Lennon, Paul McCartney, George Harrison, Ringo Starr.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Was bedeutet 'Forte' in der Musik?","antworten":{"A":"Langsam","B":"Laut","C":"Leise","D":"Schnell"},"richtig":"B","erklaerung":"'Forte' (f) bedeutet laut – 'Piano' (p) bedeutet leise.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Welches Land ist Heimat des Flamenco?","antworten":{"A":"Italien","B":"Portugal","C":"Spanien","D":"Argentinien"},"richtig":"C","erklaerung":"Flamenco stammt aus Andalusien (Suedspanien) und ist seit 2010 UNESCO-Kulturerbe.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Wer komponierte die Brandenburgischen Konzerte?","antworten":{"A":"Handel","B":"Bach","C":"Vivaldi","D":"Haydn"},"richtig":"B","erklaerung":"Johann Sebastian Bach schrieb die 6 Brandenburgischen Konzerte um 1721.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Wie heisst der beruehemteste Gitarrist von Jimi Hendrix?","antworten":{"A":"Eric Clapton","B":"Jimmy Page","C":"Jimi Hendrix selbst","D":"Carlos Santana"},"richtig":"C","erklaerung":"Jimi Hendrix gilt selbst als einer der groessten Gitarristen aller Zeiten.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Was ist ein Metronom?","antworten":{"A":"Ein Instrument","B":"Ein Taktmesser","C":"Eine Notenschrift","D":"Ein Akkord"},"richtig":"B","erklaerung":"Das Metronom gibt einen gleichmaessigen Takt vor – unverzichtbar beim Ueben.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Welche Saengerin ist als 'Queen of Pop' bekannt?","antworten":{"A":"Beyonce","B":"Lady Gaga","C":"Madonna","D":"Rihanna"},"richtig":"C","erklaerung":"Madonna wird seit den 1980ern als 'Queen of Pop' bezeichnet.","seq":None},
    {"kategorie":"Musik","schwierigkeit":3,"frage":"Was ist ein Arpeggio?","antworten":{"A":"Ein schnelles Stueck","B":"Gebrochener Akkord","C":"Ein Rhythmus","D":"Ein Tongeschlecht"},"richtig":"B","erklaerung":"Ein Arpeggio ist ein 'gebrochener Akkord' – die Toene werden nacheinander statt gleichzeitig gespielt.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"In welcher Musikrichtung ist Eminem bekannt?","antworten":{"A":"Rock","B":"Jazz","C":"Hip-Hop","D":"R&B"},"richtig":"C","erklaerung":"Eminem ist einer der meistverkauften Hip-Hop-Kuenstler aller Zeiten.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Wie viele Saiten hat eine Geige?","antworten":{"A":"3","B":"4","C":"5","D":"6"},"richtig":"B","erklaerung":"Eine Geige hat 4 Saiten: G, D, A, E (von tief nach hoch).","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Was ist Reggae?","antworten":{"A":"Brasilianische Tanzmusik","B":"Jamaikanische Musikrichtung","C":"Afrikanische Trommelmusik","D":"US-amerikanischer Folk"},"richtig":"B","erklaerung":"Reggae entstand in den 1960ern in Jamaika – Bob Marley ist der bekannteste Vertreter.","seq":None},
    {"kategorie":"Musik","schwierigkeit":3,"frage":"Wie viele Symphonien schrieb Beethoven?","antworten":{"A":"7","B":"8","C":"9","D":"10"},"richtig":"C","erklaerung":"Beethoven schrieb 9 Symphonien – die 9. mit dem beruehemten Finale 'Ode an die Freude'.","seq":None},
    {"kategorie":"Musik","schwierigkeit":2,"frage":"Was ist der Unterschied zwischen Dur und Moll?","antworten":{"A":"Tempo","B":"Lautstaerke","C":"Klangcharakter hell/dunkel","D":"Anzahl der Instrumente"},"richtig":"C","erklaerung":"Dur klingt hell/freudig, Moll klingt dunkel/traurig – es geht um die Abstufung der Toene.","seq":None},
    {"kategorie":"Musik","schwierigkeit":1,"frage":"Welches Instrument gehoert zur Streichergruppe?","antworten":{"A":"Klarinette","B":"Cello","C":"Posaune","D":"Oboe"},"richtig":"B","erklaerung":"Das Cello ist ein Streichinstrument – Klarinette, Posaune und Oboe sind Blasinstrumente.","seq":None},

    # ── GEOGRAPHIE ────────────────────────────────────────────────────────────
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Welcher Fluss ist der laengste der Welt?","antworten":{"A":"Amazonas","B":"Nil","C":"Jangtse","D":"Mississippi"},"richtig":"B","erklaerung":"Der Nil ist mit ca. 6.650 km der laengste Fluss der Welt (je nach Messmethode).","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Welches ist der groesste Kontinent?","antworten":{"A":"Afrika","B":"Amerika","C":"Asien","D":"Europa"},"richtig":"C","erklaerung":"Asien ist mit 44 Millionen km² der groesste und bevoelkerungsreichste Kontinent.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"Welcher See ist der groesste der Welt?","antworten":{"A":"Titicacasee","B":"Viktoriasee","C":"Kaspisches Meer","D":"Baikalsee"},"richtig":"C","erklaerung":"Das Kaspische Meer ist mit 371.000 km² technisch gesehen der groesste See der Welt.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Welcher Kontinent ist am duennsten besiedelt?","antworten":{"A":"Australien","B":"Suedamerika","C":"Antarktika","D":"Afrika"},"richtig":"C","erklaerung":"Die Antarktika hat keine permanente zivile Bevoelkerung – nur Wissenschaftler leben dort zeitweise.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"In welchem Land liegt das Matterhorn?","antworten":{"A":"Oesterreich","B":"Frankreich","C":"Schweiz/Italien","D":"Deutschland"},"richtig":"C","erklaerung":"Das Matterhorn liegt an der Grenze zwischen der Schweiz und Italien.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Welcher Ozean ist der kleinste?","antworten":{"A":"Atlantik","B":"Indik","C":"Suedlicher Ozean","D":"Arktischer Ozean"},"richtig":"D","erklaerung":"Der Arktische Ozean (Nordpolarmeer) ist mit 14,06 Millionen km² der kleinste Ozean.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"In welchem Land liegt der Grand Canyon?","antworten":{"A":"Kanada","B":"Mexiko","C":"USA","D":"Brasilien"},"richtig":"C","erklaerung":"Der Grand Canyon liegt im US-Bundesstaat Arizona und ist bis zu 1.800 m tief.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Frankreich?","antworten":{"A":"Lyon","B":"Marseille","C":"Paris","D":"Bordeaux"},"richtig":"C","erklaerung":"Paris ist die Hauptstadt Frankreichs und mit 2,1 Millionen Einwohnern die groesste Stadt.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"Welcher Berg ist der hoechste Europas (ohne Kaukasus)?","antworten":{"A":"Mont Blanc","B":"Monte Rosa","C":"Matterhorn","D":"Zugspitze"},"richtig":"A","erklaerung":"Der Mont Blanc ist mit 4.808 m der hoechste Berg der Alpen und Westeuropas.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"Durch wie viele Laender fliesst der Nil?","antworten":{"A":"5","B":"7","C":"11","D":"14"},"richtig":"C","erklaerung":"Der Nil fliesst durch 11 Laender in Nordostafrika.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Spanien?","antworten":{"A":"Barcelona","B":"Sevilla","C":"Valencia","D":"Madrid"},"richtig":"D","erklaerung":"Madrid ist die Hauptstadt Spaniens und mit 3,3 Millionen Einwohnern die groesste Stadt.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":3,"frage":"Welcher Fluss muendet in den Persischen Golf?","antworten":{"A":"Tigris","B":"Euphrat","C":"Schatt al-Arab","D":"Indus"},"richtig":"C","erklaerung":"Der Schatt al-Arab entsteht aus dem Zusammenfluss von Tigris und Euphrat und muendet in den Persischen Golf.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Welches Land liegt zwischen Deutschland und Frankreich?","antworten":{"A":"Niederlande","B":"Belgien","C":"Luxemburg","D":"Schweiz"},"richtig":"C","erklaerung":"Luxemburg grenzt an Deutschland im Osten und Frankreich im Sueden.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"In welchem Ozean liegt Hawaii?","antworten":{"A":"Atlantik","B":"Indik","C":"Pazifik","D":"Arktik"},"richtig":"C","erklaerung":"Hawaii liegt im Nordpazifik und ist der 50. Bundesstaat der USA.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Wie heisst die Hauptstadt von Russland?","antworten":{"A":"St. Petersburg","B":"Moskau","C":"Kiew","D":"Minsk"},"richtig":"B","erklaerung":"Moskau ist die Hauptstadt Russlands und mit 12 Millionen Einwohnern die groesste Stadt Europas.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":3,"frage":"Welcher See ist der tiefste der Welt?","antworten":{"A":"Kaspisches Meer","B":"Tanganjikasee","C":"Baikalsee","D":"Titicacasee"},"richtig":"C","erklaerung":"Der Baikalsee in Sibirien ist mit 1.642 m der tiefste See der Welt.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"Wie heisst der Wasserfall der groessten Wassermenge nach?","antworten":{"A":"Niagarafall","B":"Victoria-Fall","C":"Angel Falls","D":"Iguazu-Faelle"},"richtig":"D","erklaerung":"Die Iguazu-Faelle an der Grenze zwischen Argentinien und Brasilien fuehren die meiste Wassermenge.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Was ist die Hauptstadt der Tuerkei?","antworten":{"A":"Istanbul","B":"Izmir","C":"Ankara","D":"Antalya"},"richtig":"C","erklaerung":"Ankara ist die Hauptstadt der Tuerkei – Istanbul ist groesser, aber nicht die Hauptstadt.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"In welchem Land liegt das Amazonas-Regenwald zum groessten Teil?","antworten":{"A":"Kolumbien","B":"Venezuela","C":"Peru","D":"Brasilien"},"richtig":"D","erklaerung":"60% des Amazonas-Regenwalds liegen in Brasilien.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":2,"frage":"Welcher Kontinent hat die meisten Laender?","antworten":{"A":"Asien","B":"Amerika","C":"Afrika","D":"Europa"},"richtig":"C","erklaerung":"Afrika hat 54 anerkannte Laender – mehr als jeder andere Kontinent.","seq":None},
    {"kategorie":"Geographie","schwierigkeit":1,"frage":"Was ist die Hauptstadt von Italien?","antworten":{"A":"Mailand","B":"Venedig","C":"Florenz","D":"Rom"},"richtig":"D","erklaerung":"Rom ist die Hauptstadt Italiens und war Zentrum des Roemischen Reiches.","seq":None},
]

SICHERHEITSSTUFEN = [5, 10, 15]

IQ_TABELLE = {}
for i in range(0, 51):
    if i == 0:
        IQ_TABELLE[i] = 85
    elif i <= 5:
        IQ_TABELLE[i] = 85 + i * 3
    elif i <= 10:
        IQ_TABELLE[i] = 100 + (i-5) * 3
    elif i <= 15:
        IQ_TABELLE[i] = 115 + (i-10) * 3
    elif i <= 20:
        IQ_TABELLE[i] = 130 + (i-15) * 3
    else:
        IQ_TABELLE[i] = min(145, 145 + (i-20))

PREISE_LISTE = ['100 EUR','200 EUR','300 EUR','500 EUR','1.000 EUR','2.000 EUR','4.000 EUR','8.000 EUR','16.000 EUR','32.000 EUR','64.000 EUR','125.000 EUR','250.000 EUR','500.000 EUR','1.000.000 EUR']

PREISSTUFEN = {}
for i in range(1, 51):
    PREISSTUFEN[i] = PREISE_LISTE[min(i-1, len(PREISE_LISTE)-1)]

IQ_BEZEICHNUNG = {
    range(0,   86): "Unterdurchschnittlich",
    range(86,  95): "Leicht unterdurchschnittlich",
    range(95, 105): "Durchschnittlich",
    range(105,115): "Ueberdurchschnittlich",
    range(115,125): "Intelligent",
    range(125,135): "Hochbegabt",
    range(135,200): "Ausnahmetalent",
}

def get_daily_fragen(date_str, anzahl=15):
    import random as _r
    rng = _r.Random(date_str)
    pool = ALLE_FRAGEN.copy()
    rng.shuffle(pool)
    fragen = []
    for i, f in enumerate(pool[:anzahl]):
        frage = f.copy()
        frage['level'] = i + 1
        fragen.append(frage)
    return fragen

def get_random_fragen(anzahl=15, kategorie='alle', schwierigkeit='alle'):
    if kategorie == 'alle':
        pool = ALLE_FRAGEN.copy()
    else:
        pool = [f for f in ALLE_FRAGEN if f['kategorie'] == kategorie]
        if len(pool) < anzahl:
            pool = ALLE_FRAGEN.copy()

    if schwierigkeit != 'alle':
        try:
            sv = int(schwierigkeit)
            filtered = [f for f in pool if f.get('schwierigkeit', 2) == sv]
            if len(filtered) >= anzahl:
                pool = filtered
        except ValueError:
            pass

    random.shuffle(pool)
    fragen = []
    for i, f in enumerate(pool[:anzahl]):
        frage = f.copy()
        frage['level'] = i + 1
        fragen.append(frage)
    return fragen
