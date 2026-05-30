import json

ALLE_FRAGEN = [
    # ── ALLGEMEINWISSEN ────────────────────────────────────
    {"kategorie":"Allgemeinwissen","frage":"Welches Land hat die laengste Kuestenlinie?","antworten":{"A":"Russland","B":"Kanada","C":"Norwegen","D":"Australien"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist das schwerste natuerlich vorkommende Element?","antworten":{"A":"Uran","B":"Blei","C":"Osmium","D":"Plutonium"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Knochen hat ein erwachsener Mensch?","antworten":{"A":"196","B":"206","C":"216","D":"226"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Tier hat das groesste Herz?","antworten":{"A":"Elefant","B":"Blauwal","C":"Nilpferd","D":"Giraffe"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"In welchem Land liegt der Kilimandscharo?","antworten":{"A":"Kenia","B":"Uganda","C":"Tansania","D":"Aethiopien"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer malte die Mona Lisa?","antworten":{"A":"Michelangelo","B":"Raffael","C":"Da Vinci","D":"Donatello"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Planeten hat unser Sonnensystem?","antworten":{"A":"7","B":"8","C":"9","D":"10"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Australien?","antworten":{"A":"Sydney","B":"Melbourne","C":"Brisbane","D":"Canberra"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welche Sprache wird in Brasilien gesprochen?","antworten":{"A":"Spanisch","B":"Englisch","C":"Portugiesisch","D":"Franzoesisch"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Farben hat ein Regenbogen?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Element hat das Symbol Au?","antworten":{"A":"Silber","B":"Kupfer","C":"Gold","D":"Aluminium"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer schrieb Romeo und Julia?","antworten":{"A":"Goethe","B":"Shakespeare","C":"Schiller","D":"Dickens"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"In welchem Jahr fiel die Berliner Mauer?","antworten":{"A":"1987","B":"1988","C":"1989","D":"1990"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches ist das groesste Land der Welt?","antworten":{"A":"China","B":"USA","C":"Kanada","D":"Russland"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist H2O?","antworten":{"A":"Sauerstoff","B":"Salz","C":"Wasser","D":"Zucker"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Tier ist das schnellste Landtier?","antworten":{"A":"Loewe","B":"Gepard","C":"Pferd","D":"Antilope"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Kontinente gibt es?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Japan?","antworten":{"A":"Osaka","B":"Kyoto","C":"Tokio","D":"Hiroshima"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welcher Planet ist der groesste im Sonnensystem?","antworten":{"A":"Saturn","B":"Jupiter","C":"Neptun","D":"Uranus"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Seiten hat ein Wuerfel?","antworten":{"A":"4","B":"5","C":"6","D":"8"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer erfand das Telefon?","antworten":{"A":"Edison","B":"Tesla","C":"Bell","D":"Marconi"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Kanada?","antworten":{"A":"Toronto","B":"Vancouver","C":"Montreal","D":"Ottawa"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Beine hat eine Spinne?","antworten":{"A":"6","B":"8","C":"10","D":"12"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Instrument hat 88 Tasten?","antworten":{"A":"Orgel","B":"Akkordeon","C":"Klavier","D":"Synthesizer"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"In welchem Land liegt der Amazonas?","antworten":{"A":"Peru","B":"Kolumbien","C":"Brasilien","D":"Venezuela"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die kleinste Primzahl?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Saiten hat eine Gitarre?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches ist das kleinste Land der Welt?","antworten":{"A":"Monaco","B":"San Marino","C":"Liechtenstein","D":"Vatikan"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Aegypten?","antworten":{"A":"Alexandria","B":"Kairo","C":"Luxor","D":"Gizeh"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Herzkammern hat der Mensch?","antworten":{"A":"2","B":"3","C":"4","D":"5"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welcher Ozean ist der groesste?","antworten":{"A":"Atlantik","B":"Indik","C":"Arktis","D":"Pazifik"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die chemische Formel fuer Kochsalz?","antworten":{"A":"KCl","B":"NaCl","C":"CaCl","D":"MgCl"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer schrieb Faust?","antworten":{"A":"Schiller","B":"Kafka","C":"Goethe","D":"Brecht"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Nullen hat eine Million?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Argentinien?","antworten":{"A":"Santiago","B":"Lima","C":"Buenos Aires","D":"Bogota"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"In welchem Jahr begann der Erste Weltkrieg?","antworten":{"A":"1912","B":"1914","C":"1916","D":"1918"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt der Schweiz?","antworten":{"A":"Zuerich","B":"Genf","C":"Basel","D":"Bern"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Wochen hat ein Jahr?","antworten":{"A":"50","B":"52","C":"54","D":"56"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Element ist am haeufigsten in der Erdatmosphaere?","antworten":{"A":"Sauerstoff","B":"Kohlendioxid","C":"Stickstoff","D":"Argon"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie heisst der hoechste Berg der Welt?","antworten":{"A":"K2","B":"Kangchendzoenga","C":"Mount Everest","D":"Lhotse"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer war der erste Mensch auf dem Mond?","antworten":{"A":"Buzz Aldrin","B":"Yuri Gagarin","C":"Neil Armstrong","D":"John Glenn"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Zähne hat ein erwachsener Mensch?","antworten":{"A":"28","B":"30","C":"32","D":"34"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Indien?","antworten":{"A":"Mumbai","B":"Kolkata","C":"Chennai","D":"Neu-Delhi"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer erfand das World Wide Web?","antworten":{"A":"Bill Gates","B":"Steve Jobs","C":"Tim Berners-Lee","D":"Mark Zuckerberg"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches ist das dichteste Metall?","antworten":{"A":"Blei","B":"Gold","C":"Osmium","D":"Platin"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Kammern hat das menschliche Herz?","antworten":{"A":"2","B":"3","C":"4","D":"5"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt von Suedkorea?","antworten":{"A":"Busan","B":"Seoul","C":"Incheon","D":"Daegu"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welche Farbe hat Gold?","antworten":{"A":"Silber","B":"Kupfer","C":"Gelb","D":"Weiss"},"richtig":"C","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie heisst die Hauptstadt von Mexiko?","antworten":{"A":"Guadalajara","B":"Monterrey","C":"Tijuana","D":"Mexiko-Stadt"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wer schrieb Die Verwandlung?","antworten":{"A":"Goethe","B":"Kafka","C":"Mann","D":"Hesse"},"richtig":"B","seq":None},

    # ── GESCHICHTE ────────────────────────────────────────
    {"kategorie":"Geschichte","frage":"In welchem Jahr entdeckte Kolumbus Amerika?","antworten":{"A":"1488","B":"1490","C":"1492","D":"1495"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war der erste Kaiser Frankreichs?","antworten":{"A":"Ludwig XIV","B":"Napoleon Bonaparte","C":"Karl der Grosse","D":"Heinrich IV"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Wann endete der Zweite Weltkrieg in Europa?","antworten":{"A":"1944","B":"1945","C":"1946","D":"1947"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Welche Stadt war die Hauptstadt des Roemischen Reiches?","antworten":{"A":"Athen","B":"Karthago","C":"Alexandria","D":"Rom"},"richtig":"D","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war Martin Luther King?","antworten":{"A":"US-Praesident","B":"Buergerrechtler","C":"General","D":"Wissenschaftler"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"In welchem Jahr begann der Zweite Weltkrieg?","antworten":{"A":"1937","B":"1938","C":"1939","D":"1940"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Wer baute die Chinesische Mauer?","antworten":{"A":"Kaiser Qin Shi Huang","B":"Kaiser Yongle","C":"Dschingis Khan","D":"Kublai Khan"},"richtig":"A","seq":None},
    {"kategorie":"Geschichte","frage":"Was war die Titanic?","antworten":{"A":"Kriegsschiff","B":"Passagierschiff","C":"Frachtschiff","D":"U-Boot"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"In welchem Jahr wurde die USA unabhaengig?","antworten":{"A":"1774","B":"1776","C":"1778","D":"1780"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war Adolf Hitler?","antworten":{"A":"Koenig","B":"Kaiser","C":"Diktator","D":"Praesident"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Welches Land wurde zuerst demokratisch?","antworten":{"A":"USA","B":"Frankreich","C":"Athen","D":"England"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Wann fand die Franzoesische Revolution statt?","antworten":{"A":"1779","B":"1789","C":"1799","D":"1809"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war Kleopatra?","antworten":{"A":"Roemische Kaiserin","B":"Aegyptische Koenigin","C":"Griechische Goettin","D":"Persische Prinzessin"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"In welchem Jahr landeten Menschen auf dem Mond?","antworten":{"A":"1967","B":"1968","C":"1969","D":"1970"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Was war der Kalte Krieg?","antworten":{"A":"Ein Krieg in Russland","B":"Politischer Konflikt USA vs USSR","C":"Ein Krieg in der Arktis","D":"Ein Wirtschaftskrieg"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war Winston Churchill?","antworten":{"A":"US-Praesident","B":"Franzoesischer General","C":"Britischer Premierminister","D":"Kanadischer Premier"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"In welchem Jahr wurde Deutschland wiedervereinigt?","antworten":{"A":"1989","B":"1990","C":"1991","D":"1992"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Wer war Julius Caesar?","antworten":{"A":"Roemischer Kaiser","B":"Roemischer Feldherr und Politiker","C":"Griechischer Philosoph","D":"Aegyptischer Pharao"},"richtig":"B","seq":None},
    {"kategorie":"Geschichte","frage":"Was war die Magna Carta?","antworten":{"A":"Roemisches Gesetz","B":"Franzoesische Verfassung","C":"Englisches Rechtsdokument","D":"Deutsches Grundgesetz"},"richtig":"C","seq":None},
    {"kategorie":"Geschichte","frage":"Wann wurde Hitler geboren?","antworten":{"A":"1887","B":"1889","C":"1891","D":"1893"},"richtig":"B","seq":None},

    # ── WISSENSCHAFT ─────────────────────────────────────
    {"kategorie":"Wissenschaft","frage":"Was ist die Lichtgeschwindigkeit?","antworten":{"A":"200.000 km/s","B":"300.000 km/s","C":"400.000 km/s","D":"500.000 km/s"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Aus wie vielen Atomen besteht ein Wassermolekuel?","antworten":{"A":"1","B":"2","C":"3","D":"4"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist DNA?","antworten":{"A":"Ein Protein","B":"Ein Enzym","C":"Erbgut","D":"Ein Virus"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wer entwickelte die Relativitaetstheorie?","antworten":{"A":"Newton","B":"Einstein","C":"Bohr","D":"Curie"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist Photosynthese?","antworten":{"A":"Zellteilung","B":"Atmung von Tieren","C":"Energiegewinnung durch Licht","D":"Wasseraufnahme"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wie viele Elektronen hat Wasserstoff?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist der Siedepunkt von Wasser?","antworten":{"A":"90 Grad","B":"95 Grad","C":"100 Grad","D":"105 Grad"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Welches Gas atmen Menschen ein?","antworten":{"A":"Kohlendioxid","B":"Stickstoff","C":"Sauerstoff","D":"Wasserstoff"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist die Schwerkraft?","antworten":{"A":"Magnetische Kraft","B":"Anziehungskraft zwischen Massen","C":"Elektrische Kraft","D":"Kernkraft"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wie heisst das Zentrum einer Zelle?","antworten":{"A":"Mitochondrium","B":"Ribosom","C":"Zellmembran","D":"Zellkern"},"richtig":"D","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist ein schwarzes Loch?","antworten":{"A":"Ein toter Stern","B":"Ein Objekt mit extremer Schwerkraft","C":"Eine leere Region im All","D":"Ein Nebel"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wer entdeckte die Schwerkraft?","antworten":{"A":"Einstein","B":"Galilei","C":"Newton","D":"Kepler"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist der Gefrierpunkt von Wasser?","antworten":{"A":"-5 Grad","B":"0 Grad","C":"5 Grad","D":"10 Grad"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wie viele Chromosomen hat der Mensch?","antworten":{"A":"42","B":"44","C":"46","D":"48"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist ein Atom?","antworten":{"A":"Ein Molekuel","B":"Kleinste Einheit eines Elements","C":"Ein Elektron","D":"Ein Proton"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Welches ist das leichteste Element?","antworten":{"A":"Helium","B":"Lithium","C":"Wasserstoff","D":"Beryllium"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist Evolution?","antworten":{"A":"Zellwachstum","B":"Artenwandel ueber Generationen","C":"Fotosynthese","D":"Zellteilung"},"richtig":"B","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wie alt ist die Erde?","antworten":{"A":"2 Milliarden Jahre","B":"3 Milliarden Jahre","C":"4,5 Milliarden Jahre","D":"6 Milliarden Jahre"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Was ist ein Proton?","antworten":{"A":"Negativ geladenes Teilchen","B":"Neutral geladenes Teilchen","C":"Positiv geladenes Teilchen","D":"Kein geladenes Teilchen"},"richtig":"C","seq":None},
    {"kategorie":"Wissenschaft","frage":"Wer entdeckte das Penicillin?","antworten":{"A":"Pasteur","B":"Koch","C":"Fleming","D":"Lister"},"richtig":"C","seq":None},

    # ── SPORT ────────────────────────────────────────────
    {"kategorie":"Sport","frage":"Wie viele Spieler hat eine Fussballmannschaft?","antworten":{"A":"9","B":"10","C":"11","D":"12"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"In welchem Land wurde Fussball erfunden?","antworten":{"A":"Deutschland","B":"England","C":"Brasilien","D":"Frankreich"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Ringe hat das Olympische Symbol?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Wer hat die meisten WM-Titel im Fussball?","antworten":{"A":"Deutschland","B":"Argentinien","C":"Brasilien","D":"Italien"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wie lange dauert ein Fussballspiel?","antworten":{"A":"80 Minuten","B":"90 Minuten","C":"100 Minuten","D":"120 Minuten"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"In welchem Jahr fanden die ersten modernen Olympischen Spiele statt?","antworten":{"A":"1892","B":"1894","C":"1896","D":"1898"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Punkte gibt es beim Tennis fuer den ersten Punkt?","antworten":{"A":"10","B":"15","C":"20","D":"25"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Wo fanden die Olympischen Sommerspiele 2021 statt?","antworten":{"A":"Paris","B":"London","C":"Tokio","D":"Seoul"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wer ist Rekordtorschuetze in der Bundesliga?","antworten":{"A":"Thomas Mueller","B":"Robert Lewandowski","C":"Gerd Mueller","D":"Klaus Fischer"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Spieler hat eine Basketballmannschaft?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Was ist ein Birdie im Golf?","antworten":{"A":"Ein Schlag unter Par","B":"Ein Schlag ueber Par","C":"Ein Loch in einem","D":"Zwei Schlaege unter Par"},"richtig":"A","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Spiele hat eine NBA-Saison regulaer?","antworten":{"A":"72","B":"78","C":"82","D":"88"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"In welchem Land liegt Wimbledon?","antworten":{"A":"USA","B":"Australien","C":"Frankreich","D":"England"},"richtig":"D","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Meter ist ein Marathon lang?","antworten":{"A":"40.195 m","B":"41.195 m","C":"42.195 m","D":"43.195 m"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Welcher Sportler hat die meisten Grand-Slam-Titel?","antworten":{"A":"Roger Federer","B":"Rafael Nadal","C":"Novak Djokovic","D":"Andre Agassi"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Punkte braucht man fuer ein Tor im American Football?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wo fand die erste Fussball-WM statt?","antworten":{"A":"Brasilien","B":"Uruguay","C":"Argentinien","D":"Chile"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Was ist ein Hat-Trick?","antworten":{"A":"2 Tore in einem Spiel","B":"3 Tore in einem Spiel","C":"4 Tore in einem Spiel","D":"5 Tore in einem Spiel"},"richtig":"B","seq":None},
    {"kategorie":"Sport","frage":"Wie viele Spieler stehen beim Volleyball auf dem Feld?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","seq":None},
    {"kategorie":"Sport","frage":"Wer gewann die Fussball-WM 2022?","antworten":{"A":"Frankreich","B":"Brasilien","C":"Argentinien","D":"Deutschland"},"richtig":"C","seq":None},

    # ── MATHEMATIK ────────────────────────────────────────
    {"kategorie":"Mathematik","frage":"Was ist Pi gerundet auf 2 Dezimalstellen?","antworten":{"A":"3,12","B":"3,14","C":"3,16","D":"3,18"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist die Quadratwurzel von 144?","antworten":{"A":"10","B":"11","C":"12","D":"13"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 15% von 200?","antworten":{"A":"20","B":"25","C":"30","D":"35"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 2 hoch 8?","antworten":{"A":"128","B":"256","C":"512","D":"1024"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist die Summe der Winkel in einem Dreieck?","antworten":{"A":"90 Grad","B":"120 Grad","C":"180 Grad","D":"360 Grad"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 1000 - 357?","antworten":{"A":"633","B":"643","C":"653","D":"663"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist die Flaeche eines Kreises mit Radius 5? (Pi=3)","antworten":{"A":"65","B":"70","C":"75","D":"80"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 12 x 13?","antworten":{"A":"144","B":"152","C":"156","D":"162"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 50% von 50% von 400?","antworten":{"A":"50","B":"75","C":"100","D":"125"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Wie viele Primzahlen gibt es zwischen 1 und 10?","antworten":{"A":"3","B":"4","C":"5","D":"6"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 3 hoch 4?","antworten":{"A":"64","B":"81","C":"96","D":"108"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist der Umfang eines Kreises mit Radius 7? (Pi=3)","antworten":{"A":"38","B":"40","C":"42","D":"44"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 144 / 12?","antworten":{"A":"10","B":"11","C":"12","D":"13"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 7 x 8 x 9?","antworten":{"A":"494","B":"504","C":"514","D":"524"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 1/4 + 1/2?","antworten":{"A":"1/2","B":"3/4","C":"1","D":"5/4"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 25 hoch 2?","antworten":{"A":"525","B":"600","C":"625","D":"650"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Wie viele Seiten hat ein Hexagon?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"B","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 999 x 9?","antworten":{"A":"8881","B":"8891","C":"8901","D":"8991"},"richtig":"D","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist die Quadratwurzel von 225?","antworten":{"A":"13","B":"14","C":"15","D":"16"},"richtig":"C","seq":None},
    {"kategorie":"Mathematik","frage":"Was ist 40% von 150?","antworten":{"A":"50","B":"55","C":"60","D":"65"},"richtig":"C","seq":None},

    # ── LOGIK & ZAHLENFOLGEN ──────────────────────────────
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n5 - 10 - 20 - 40 - ?","antworten":{"A":"60","B":"70","C":"80","D":"90"},"richtig":"C","seq":"5  -  10  -  20  -  40  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Fibonacci: was kommt als naechstes?\n1 - 1 - 2 - 3 - 5 - 8 - ?","antworten":{"A":"11","B":"12","C":"13","D":"14"},"richtig":"C","seq":"1  1  2  3  5  8  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n81 - 27 - 9 - 3 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":"81  -  27  -  9  -  3  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n2 - 5 - 10 - 17 - 26 - ?","antworten":{"A":"33","B":"35","C":"37","D":"39"},"richtig":"C","seq":"2  5  10  17  26  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n3 - 6 - 12 - 24 - ?","antworten":{"A":"36","B":"40","C":"48","D":"52"},"richtig":"C","seq":"3  -  6  -  12  -  24  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Quadratzahlen - was kommt als naechstes?\n1 - 4 - 9 - 16 - 25 - ?","antworten":{"A":"30","B":"35","C":"36","D":"49"},"richtig":"C","seq":"1  4  9  16  25  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Arzt zu Krankenhaus wie Lehrer zu?","antworten":{"A":"Buch","B":"Schueler","C":"Schule","D":"Unterricht"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n2 - 6 - 18 - 54 - ?","antworten":{"A":"108","B":"126","C":"162","D":"180"},"richtig":"C","seq":"2  -  6  -  18  -  54  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches passt nicht?\nRose - Tulpe - Eiche - Lilie","antworten":{"A":"Rose","B":"Tulpe","C":"Eiche","D":"Lilie"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n256 - 64 - 16 - 4 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":"256  -  64  -  16  -  4  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Primzahlen - was kommt als naechstes?\n2 - 3 - 5 - 7 - 11 - 13 - ?","antworten":{"A":"15","B":"16","C":"17","D":"19"},"richtig":"C","seq":"2  3  5  7  11  13  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n1000 - 100 - 10 - ?","antworten":{"A":"0","B":"1","C":"2","D":"5"},"richtig":"B","seq":"1000  -  100  -  10  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Tag zu Nacht wie Sommer zu?","antworten":{"A":"Herbst","B":"Fruehling","C":"Winter","D":"Jahreszeit"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n1 - 2 - 4 - 8 - 16 - ?","antworten":{"A":"24","B":"28","C":"32","D":"36"},"richtig":"C","seq":"1  2  4  8  16  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches passt nicht?\nAuto - Zug - Flugzeug - U-Boot - Fahrrad","antworten":{"A":"Auto","B":"Zug","C":"Flugzeug","D":"U-Boot"},"richtig":"D","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n5 - 11 - 23 - 47 - ?","antworten":{"A":"89","B":"93","C":"95","D":"97"},"richtig":"C","seq":"5  -  11  -  23  -  47  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn heute Mittwoch ist, was ist in 10 Tagen?","antworten":{"A":"Freitag","B":"Samstag","C":"Sonntag","D":"Montag"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n3 - 8 - 15 - 24 - 35 - ?","antworten":{"A":"42","B":"46","C":"48","D":"50"},"richtig":"C","seq":"3  8  15  24  35  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Pianist zu Klavier wie Geiger zu?","antworten":{"A":"Musik","B":"Geige","C":"Konzert","D":"Orchester"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n2 - 4 - 12 - 48 - ?","antworten":{"A":"120","B":"192","C":"240","D":"288"},"richtig":"C","seq":"2  -  4  -  12  -  48  -  ?"},

    # ── KONZENTRATION ─────────────────────────────────────
    {"kategorie":"Konzentration","frage":"Wie viele gerade Zahlen liegen zwischen 14 und 26?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Ein Zug faehrt 90 km/h. Wie weit in 40 Minuten?","antworten":{"A":"50 km","B":"55 km","C":"60 km","D":"65 km"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"15 x 4 - 18 / 3 = ?","antworten":{"A":"52","B":"54","C":"56","D":"58"},"richtig":"B","seq":"15 x 4  -  18 / 3  =  ?"},
    {"kategorie":"Konzentration","frage":"Umfang eines Quadrats mit Seite 7 cm?","antworten":{"A":"21 cm","B":"28 cm","C":"35 cm","D":"49 cm"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Monate haben 31 Tage?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"8 x 7 + 6 - 5 = ?","antworten":{"A":"55","B":"57","C":"59","D":"61"},"richtig":"B","seq":"8 x 7 + 6 - 5 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viele Sekunden hat eine Stunde?","antworten":{"A":"1200","B":"2400","C":"3600","D":"4800"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"25% von 200 = ?","antworten":{"A":"25","B":"40","C":"50","D":"75"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Flaeche eines Rechtecks 8 x 6 = ?","antworten":{"A":"42","B":"46","C":"48","D":"52"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Minuten hat ein Tag?","antworten":{"A":"720","B":"1440","C":"2880","D":"360"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"33 + 47 - 15 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"C","seq":"33 + 47 - 15 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viel ist 12 hoch 2?","antworten":{"A":"124","B":"134","C":"144","D":"154"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Ein Rechteck Laenge 12, Breite 5. Umfang?","antworten":{"A":"30","B":"34","C":"38","D":"60"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Stunden hat eine Woche?","antworten":{"A":"148","B":"158","C":"168","D":"178"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"9 x 9 - 9 / 9 = ?","antworten":{"A":"72","B":"78","C":"80","D":"81"},"richtig":"C","seq":"9 x 9 - 9 / 9 = ?"},
    {"kategorie":"Konzentration","frage":"75% von 80 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Tage hat ein Schaltjahr?","antworten":{"A":"364","B":"365","C":"366","D":"367"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"3 hoch 5 = ?","antworten":{"A":"125","B":"215","C":"243","D":"315"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"120 / 8 + 5 = ?","antworten":{"A":"18","B":"20","C":"22","D":"24"},"richtig":"B","seq":"120 / 8 + 5 = ?"},
    {"kategorie":"Konzentration","frage":"17 x 3 - 11 = ?","antworten":{"A":"38","B":"40","C":"42","D":"44"},"richtig":"B","seq":"17 x 3 - 11 = ?"},
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

def get_random_fragen(anzahl=15):
    import random
    pool = ALLE_FRAGEN.copy()
    random.shuffle(pool)
    fragen = []
    for i, f in enumerate(pool[:anzahl]):
        frage = f.copy()
        frage['level'] = i + 1
        fragen.append(frage)
    return fragen
