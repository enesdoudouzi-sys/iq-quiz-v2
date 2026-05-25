import random

ALLE_FRAGEN = [
    # ALLGEMEINWISSEN (40 Fragen)
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
    {"kategorie":"Allgemeinwissen","frage":"Welches Tier legt die groessten Eier?","antworten":{"A":"Straus","B":"Adler","C":"Krokodil","D":"Schildkroete"},"richtig":"A","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"In welchem Jahr begann der Erste Weltkrieg?","antworten":{"A":"1912","B":"1914","C":"1916","D":"1918"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Was ist die Hauptstadt der Schweiz?","antworten":{"A":"Zuerich","B":"Genf","C":"Basel","D":"Bern"},"richtig":"D","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Wie viele Wochen hat ein Jahr?","antworten":{"A":"50","B":"52","C":"54","D":"56"},"richtig":"B","seq":None},
    {"kategorie":"Allgemeinwissen","frage":"Welches Element ist das haefigste auf der Erde?","antworten":{"A":"Kohlenstoff","B":"Eisen","C":"Sauerstoff","D":"Silizium"},"richtig":"C","seq":None},

    # LOGIK & ZAHLENFOLGEN (35 Fragen)
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n5 - 10 - 20 - 40 - ?","antworten":{"A":"60","B":"70","C":"80","D":"90"},"richtig":"C","seq":"5  -  10  -  20  -  40  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Fibonacci: was kommt als naechstes?\n1 - 1 - 2 - 3 - 5 - 8 - ?","antworten":{"A":"11","B":"12","C":"13","D":"14"},"richtig":"C","seq":"1  1  2  3  5  8  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n81 - 27 - 9 - 3 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":"81  -  27  -  9  -  3  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n2 - 5 - 10 - 17 - 26 - ?","antworten":{"A":"33","B":"35","C":"37","D":"39"},"richtig":"C","seq":"2  5  10  17  26  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Was ergibt D + F + H?\n(A=1, B=2, C=3 ...)","antworten":{"A":"18","B":"20","C":"22","D":"24"},"richtig":"A","seq":"D=4   F=6   H=8"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n3 - 6 - 12 - 24 - ?","antworten":{"A":"36","B":"40","C":"48","D":"52"},"richtig":"C","seq":"3  -  6  -  12  -  24  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n1 - 4 - 9 - 16 - 25 - ?","antworten":{"A":"30","B":"35","C":"36","D":"49"},"richtig":"C","seq":"1  4  9  16  25  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Arzt zu Krankenhaus wie Lehrer zu?","antworten":{"A":"Buch","B":"Schueler","C":"Schule","D":"Unterricht"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n100 - 50 - 25 - ?","antworten":{"A":"10","B":"12","C":"12","D":"15"},"richtig":"C","seq":"100  -  50  -  25  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches Wort passt nicht?\nRose - Tulpe - Eiche - Lilie","antworten":{"A":"Rose","B":"Tulpe","C":"Eiche","D":"Lilie"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n2 - 6 - 18 - 54 - ?","antworten":{"A":"108","B":"126","C":"162","D":"180"},"richtig":"C","seq":"2  -  6  -  18  -  54  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn 3 Arbeiter 3 Tage brauchen,\nwie lange brauchen 6 Arbeiter?","antworten":{"A":"6 Tage","B":"3 Tage","C":"1.5 Tage","D":"1 Tag"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n0 - 1 - 1 - 2 - 3 - 5 - 8 - ?","antworten":{"A":"11","B":"12","C":"13","D":"14"},"richtig":"C","seq":"0  1  1  2  3  5  8  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Hund zu Welpe wie Katze zu?","antworten":{"A":"Kaetzchen","B":"Kitten","C":"Junges","D":"Baby"},"richtig":"A","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n7 - 14 - 21 - 28 - ?","antworten":{"A":"32","B":"35","C":"38","D":"42"},"richtig":"B","seq":"7  -  14  -  21  -  28  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches passt nicht?\nKreis - Dreieck - Wuerfel - Quadrat","antworten":{"A":"Kreis","B":"Dreieck","C":"Wuerfel","D":"Quadrat"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n1 - 3 - 7 - 15 - 31 - ?","antworten":{"A":"53","B":"57","C":"63","D":"67"},"richtig":"C","seq":"1  3  7  15  31  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn A vor B ist und C nach B,\nwer ist in der Mitte?","antworten":{"A":"A","B":"B","C":"C","D":"Keiner"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n10 - 9 - 7 - 4 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"A","seq":"10  9  7  4  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Buch zu Bibliothek wie Geld zu?","antworten":{"A":"Kasse","B":"Bank","C":"Tresor","D":"Portemonnaie"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n256 - 64 - 16 - 4 - ?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":"256  -  64  -  16  -  4  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches Wort passt nicht?\nAuto - Zug - Flugzeug - Fahrrad - U-Boot","antworten":{"A":"Auto","B":"Zug","C":"Flugzeug","D":"U-Boot"},"richtig":"D","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n2 - 3 - 5 - 7 - 11 - 13 - ?","antworten":{"A":"15","B":"16","C":"17","D":"19"},"richtig":"C","seq":"2  3  5  7  11  13  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn heute Mittwoch ist,\nwas ist in 10 Tagen?","antworten":{"A":"Freitag","B":"Samstag","C":"Sonntag","D":"Montag"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n1000 - 100 - 10 - ?","antworten":{"A":"0","B":"1","C":"2","D":"5"},"richtig":"B","seq":"1000  -  100  -  10  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Tag zu Nacht wie Sommer zu?","antworten":{"A":"Herbst","B":"Fruehling","C":"Winter","D":"Jahreszeit"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n1 - 2 - 4 - 8 - 16 - ?","antworten":{"A":"24","B":"28","C":"32","D":"36"},"richtig":"C","seq":"1  2  4  8  16  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn A=26 B=25 C=24,\nwas ist Z?","antworten":{"A":"0","B":"1","C":"2","D":"3"},"richtig":"B","seq":"A=26  B=25  C=24 ... Z=?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welches passt nicht?\nApfel - Birne - Karotte - Banane","antworten":{"A":"Apfel","B":"Birne","C":"Karotte","D":"Banane"},"richtig":"C","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n5 - 11 - 23 - 47 - ?","antworten":{"A":"89","B":"93","C":"95","D":"97"},"richtig":"C","seq":"5  -  11  -  23  -  47  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Pianist zu Klavier wie Geiger zu?","antworten":{"A":"Musik","B":"Geige","C":"Konzert","D":"Orchester"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl kommt als naechstes?\n3 - 8 - 15 - 24 - 35 - ?","antworten":{"A":"42","B":"46","C":"48","D":"50"},"richtig":"C","seq":"3  8  15  24  35  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Wenn ein Zug um 8:45 faehrt\nund 2h 15min faehrt, wann kommt er an?","antworten":{"A":"10:45","B":"11:00","C":"11:15","D":"11:30"},"richtig":"B","seq":None},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Welche Zahl fehlt?\n2 - 4 - 12 - 48 - ?","antworten":{"A":"120","B":"192","C":"240","D":"288"},"richtig":"C","seq":"2  -  4  -  12  -  48  -  ?"},
    {"kategorie":"Logik & Zahlenfolgen","frage":"Analogie: Sonne zu Tag wie Mond zu?","antworten":{"A":"Stern","B":"Nacht","C":"Licht","D":"Dunkelheit"},"richtig":"B","seq":None},

    # KONZENTRATION (30 Fragen)
    {"kategorie":"Konzentration","frage":"Wie viele gerade Zahlen liegen zwischen 14 und 26?","antworten":{"A":"4","B":"5","C":"6","D":"7"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Ein Zug faehrt 90 km/h.\nWie weit in 40 Minuten?","antworten":{"A":"50 km","B":"55 km","C":"60 km","D":"65 km"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"15 x 4 - 18 / 3 = ?","antworten":{"A":"52","B":"54","C":"56","D":"58"},"richtig":"B","seq":"15 x 4  -  18 / 3  =  ?"},
    {"kategorie":"Konzentration","frage":"Umfang eines Quadrats mit Seite 7 cm?","antworten":{"A":"21 cm","B":"28 cm","C":"35 cm","D":"49 cm"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Monate haben 31 Tage?","antworten":{"A":"5","B":"6","C":"7","D":"8"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"8 x 7 + 6 - 5 = ?","antworten":{"A":"55","B":"57","C":"59","D":"61"},"richtig":"B","seq":"8 x 7 + 6 - 5 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viele Sekunden hat eine Stunde?","antworten":{"A":"1200","B":"2400","C":"3600","D":"4800"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"25% von 200 = ?","antworten":{"A":"25","B":"40","C":"50","D":"75"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Flaeche eines Rechtecks: 8 x 6 = ?","antworten":{"A":"42","B":"46","C":"48","D":"52"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Minuten hat ein Tag?","antworten":{"A":"720","B":"1440","C":"2880","D":"360"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"33 + 47 - 15 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"C","seq":"33 + 47 - 15 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viel ist 12 hoch 2?","antworten":{"A":"124","B":"134","C":"144","D":"154"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"50% von 50% von 100 = ?","antworten":{"A":"10","B":"20","C":"25","D":"50"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Ein Rechteck hat Laenge 12 und Breite 5.\nWas ist der Umfang?","antworten":{"A":"30","B":"34","C":"38","D":"60"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Stunden hat eine Woche?","antworten":{"A":"148","B":"158","C":"168","D":"178"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"9 x 9 - 9 / 9 = ?","antworten":{"A":"72","B":"78","C":"80","D":"81"},"richtig":"C","seq":"9 x 9 - 9 / 9 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viele Buchstaben hat das Alphabet?","antworten":{"A":"24","B":"25","C":"26","D":"27"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"75% von 80 = ?","antworten":{"A":"55","B":"60","C":"65","D":"70"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Tage hat ein Schaltjahr?","antworten":{"A":"364","B":"365","C":"366","D":"367"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"3 hoch 5 = ?","antworten":{"A":"125","B":"215","C":"243","D":"315"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Monate hat ein Jahr?","antworten":{"A":"10","B":"11","C":"12","D":"13"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"120 / 8 + 5 = ?","antworten":{"A":"18","B":"20","C":"22","D":"24"},"richtig":"B","seq":"120 / 8 + 5 = ?"},
    {"kategorie":"Konzentration","frage":"Ein Kreis hat Radius 7.\nWas ist die Flaeche? (Pi=3)","antworten":{"A":"100","B":"120","C":"147","D":"154"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Tage hat der Februar im Normaljahr?","antworten":{"A":"27","B":"28","C":"29","D":"30"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"17 x 3 - 11 = ?","antworten":{"A":"38","B":"40","C":"42","D":"44"},"richtig":"B","seq":"17 x 3 - 11 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viele Wochen hat ein Monat durchschnittlich?","antworten":{"A":"3","B":"4","C":"5","D":"6"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"500 - 125 x 2 = ?","antworten":{"A":"200","B":"250","C":"300","D":"375"},"richtig":"B","seq":"500 - 125 x 2 = ?"},
    {"kategorie":"Konzentration","frage":"Wie viele Grad hat ein rechter Winkel?","antworten":{"A":"45","B":"60","C":"90","D":"180"},"richtig":"C","seq":None},
    {"kategorie":"Konzentration","frage":"2 hoch 10 = ?","antworten":{"A":"512","B":"1024","C":"2048","D":"4096"},"richtig":"B","seq":None},
    {"kategorie":"Konzentration","frage":"Wie viele Stunden hat ein halber Tag?","antworten":{"A":"6","B":"10","C":"12","D":"14"},"richtig":"C","seq":None},
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
    pool = ALLE_FRAGEN.copy()
    random.shuffle(pool)
    fragen = []
    for i, f in enumerate(pool[:anzahl]):
        frage = f.copy()
        frage['level'] = i + 1
        fragen.append(frage)
    return fragen
