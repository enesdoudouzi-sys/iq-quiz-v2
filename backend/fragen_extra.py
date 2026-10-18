"""Zusaetzliche Fragen in 8 neuen Kategorien.

Format je Zeile: (schwierigkeit, frage, richtige_antwort, [3 falsche], erklaerung)
schwierigkeit: 1=leicht, 2=mittel, 3=schwer

Die Antwort-Reihenfolge wird beim Laden deterministisch gemischt (pro Frage
immer gleich), reine Zahlenantworten werden aufsteigend sortiert.
"""
import random as _random
import re as _re

_NUM = _re.compile(r"^\s*(\d+(?:[.,]\d+)?)(.*)$")


def _build(kat, rows):
    out = []
    letters = "ABCD"
    for schw, frage, richtig, falsche, erkl in rows:
        opts = [richtig] + list(falsche)
        nums = [_NUM.match(o) for o in opts]
        # Nur sortieren, wenn alle Antworten Zahlen mit gleicher Einheit sind
        if all(nums) and len({m.group(2).strip() for m in nums}) == 1:
            opts.sort(key=lambda o: float(_NUM.match(o).group(1).replace(",", ".")))
        else:
            _random.Random(kat + "|" + frage).shuffle(opts)
        out.append({
            "kategorie": kat,
            "schwierigkeit": schw,
            "frage": frage,
            "antworten": {letters[i]: opts[i] for i in range(4)},
            "richtig": letters[opts.index(richtig)],
            "erklaerung": erkl,
            "seq": None,
        })
    return out


FILM_TV = [
    (1, "Welcher Regisseur drehte den Film „Titanic“ (1997)?", "James Cameron", ["Steven Spielberg", "Ridley Scott", "Christopher Nolan"], "James Cameron führte Regie bei „Titanic“, der elf Oscars gewann."),
    (1, "Wie heißt der kleine grüne Jedi-Meister aus „Star Wars“?", "Yoda", ["Chewbacca", "Obi-Wan", "Jabba"], "Yoda ist ein sehr alter und weiser Jedi-Meister."),
    (2, "Welcher Film gewann 2020 als erster nicht-englischsprachiger Film den Oscar als Bester Film?", "Parasite", ["Roma", "Joker", "1917"], "„Parasite“ von Bong Joon-ho aus Südkorea schrieb 2020 Oscar-Geschichte."),
    (2, "Wer führte Regie bei „Pulp Fiction“ (1994)?", "Quentin Tarantino", ["Martin Scorsese", "David Fincher", "Guy Ritchie"], "Quentin Tarantino gewann für „Pulp Fiction“ den Oscar für das beste Originaldrehbuch."),
    (1, "In welcher Stadt spielt die Serie „Friends“?", "New York", ["Los Angeles", "Chicago", "Boston"], "Die sechs Freunde leben in Manhattan, New York."),
    (2, "Wer spielte im Film „Forrest Gump“ die Hauptrolle?", "Tom Hanks", ["Tom Cruise", "Kevin Costner", "Bill Murray"], "Tom Hanks gewann für die Rolle 1995 seinen zweiten Oscar."),
    (3, "Welcher Film gilt als erster abendfüllender Tonfilm?", "Der Jazzsänger", ["Metropolis", "Citizen Kane", "Moderne Zeiten"], "„Der Jazzsänger“ (1927) gilt als erster langer Spielfilm mit synchronisiertem Ton."),
    (2, "Aus welchem Land stammt die Mysteryserie „Dark“?", "Deutschland", ["Schweden", "Dänemark", "Österreich"], "„Dark“ wurde von Baran bo Odar und Jantje Friese für Netflix in Deutschland produziert."),
    (1, "Welcher Schauspieler verkörperte den Joker in „The Dark Knight“ (2008)?", "Heath Ledger", ["Joaquin Phoenix", "Jared Leto", "Jack Nicholson"], "Heath Ledger erhielt für diese Rolle posthum den Oscar als bester Nebendarsteller."),
    (2, "Welcher Film erhielt 2004 elf Oscars und wurde bester Film?", "Der Herr der Ringe: Die Rückkehr des Königs", ["Chicago", "Master & Commander", "Mystic River"], "„Die Rückkehr des Königs“ gewann alle elf Kategorien, in denen er nominiert war."),
    (1, "Wie heißt Harry Potters bester Freund mit den roten Haaren?", "Ron Weasley", ["Draco Malfoy", "Neville Longbottom", "Seamus Finnigan"], "Ron Weasley ist Harrys bester Freund und Mitglied der Familie Weasley."),
    (3, "Welcher Regisseur drehte „2001: Odyssee im Weltraum“?", "Stanley Kubrick", ["Ridley Scott", "George Lucas", "Steven Spielberg"], "Stanley Kubrick drehte den Science-Fiction-Klassiker 1968."),
    (2, "In welcher fiktiven Stadt spielt die Zeichentrickserie „Die Simpsons“?", "Springfield", ["Quahog", "South Park", "Bedrock"], "Die Familie Simpson lebt in Springfield."),
    (3, "Welcher deutsche Film gewann 2007 den Oscar für den besten fremdsprachigen Film?", "Das Leben der Anderen", ["Die Fälscher", "Das Boot", "Good Bye, Lenin!"], "„Das Leben der Anderen“ von Florian Henckel von Donnersmarck gewann 2007."),
    (2, "Welche Fantasy-Serie basiert auf den Büchern von George R. R. Martin?", "Game of Thrones", ["Vikings", "The Witcher", "Shadow and Bone"], "„Game of Thrones“ basiert auf der Buchreihe „Das Lied von Eis und Feuer“."),
    (1, "Welches Tier ist Simba im Animationsfilm „Der König der Löwen“?", "Löwe", ["Tiger", "Leopard", "Gepard"], "Simba ist ein junger Löwe und Sohn von König Mufasa."),
    (3, "In welchem Jahr kam der erste „Star Wars“-Film in die Kinos?", "1977", ["1975", "1980", "1983"], "„Krieg der Sterne“ startete im Mai 1977 in den USA."),
    (2, "Wer spielte Jack Dawson in „Titanic“?", "Leonardo DiCaprio", ["Brad Pitt", "Johnny Depp", "Matt Damon"], "Leonardo DiCaprio spielte den mittellosen Künstler Jack."),
    (2, "In welcher Stadt findet das Filmfestival mit der „Goldenen Palme“ statt?", "Cannes", ["Venedig", "Berlin", "Locarno"], "Die Goldene Palme ist der Hauptpreis der Internationalen Filmfestspiele von Cannes."),
    (2, "Wie heißt der Hauptpreis der Berlinale?", "Goldener Bär", ["Goldener Löwe", "Goldene Palme", "Goldener Leopard"], "Der Goldene Bär ist der Hauptpreis der Internationalen Filmfestspiele Berlin."),
    (1, "Wie heißt der graue Zauberer, der Frodo in „Der Herr der Ringe“ begleitet?", "Gandalf", ["Dumbledore", "Merlin", "Radagast"], "Gandalf der Graue führt die Gefährten auf ihrer Reise."),
    (3, "Welche Schauspielerin gewann vier Oscars als beste Hauptdarstellerin?", "Katharine Hepburn", ["Meryl Streep", "Ingrid Bergman", "Bette Davis"], "Katharine Hepburn ist mit vier Hauptdarstellerinnen-Oscars Rekordhalterin."),
    (2, "Wie heißt die südkoreanische Netflix-Serie über tödliche Kinderspiele um ein Preisgeld?", "Squid Game", ["Alice in Borderland", "Kingdom", "Sweet Home"], "„Squid Game“ wurde 2021 zu einer der meistgesehenen Serien der Welt."),
    (1, "Welche Pille nimmt Neo in „Matrix“, um die Wahrheit zu erfahren?", "Die rote", ["Die blaue", "Die grüne", "Die gelbe"], "Die rote Pille führt Neo aus der Matrix in die Realität."),
    (2, "Wer komponierte die Musik zu „Star Wars“ und „Indiana Jones“?", "John Williams", ["Hans Zimmer", "Ennio Morricone", "Howard Shore"], "John Williams schrieb die Musik zu vielen bekannten Kinofilmen."),
    (2, "In welcher Stadt wird die Oscar-Verleihung abgehalten?", "Los Angeles", ["New York", "Las Vegas", "San Francisco"], "Die Oscars werden traditionell in Los Angeles verliehen."),
    (3, "Welcher Animationsfilm von Hayao Miyazaki gewann 2003 den Oscar?", "Chihiros Reise ins Zauberland", ["Prinzessin Mononoke", "Mein Nachbar Totoro", "Das wandelnde Schloss"], "„Chihiros Reise ins Zauberland“ gewann den Oscar als bester Animationsfilm."),
    (2, "Wie viele Filme umfasst die Hauptreihe von „Der Pate“?", "3", ["2", "4", "5"], "Die Trilogie von Francis Ford Coppola besteht aus drei Teilen."),
    (1, "Wie heißt die bekannte ARD-Krimireihe, die seit 1970 sonntags läuft?", "Tatort", ["Polizeiruf 110", "SOKO", "Der Alte"], "Der erste „Tatort“ lief am 29. November 1970."),
    (3, "In welchem Jahr wurde der Film „Metropolis“ von Fritz Lang uraufgeführt?", "1927", ["1919", "1931", "1933"], "„Metropolis“ feierte im Januar 1927 in Berlin Premiere."),
]

ESSEN_TRINKEN = [
    (1, "Aus welchem Land stammt die Pizza ursprünglich?", "Italien", ["Frankreich", "Griechenland", "Spanien"], "Die Pizza hat ihren Ursprung in Neapel, Italien."),
    (1, "Woraus wird Sauerkraut hergestellt?", "Weißkohl", ["Rotkohl", "Spitzkohl", "Wirsing"], "Sauerkraut ist fermentierter, fein geschnittener Weißkohl."),
    (2, "Welches Gewürz verleiht Curry seine typische gelbe Farbe?", "Kurkuma", ["Safran", "Paprika", "Ingwer"], "Kurkuma färbt viele Currymischungen gelb."),
    (2, "Welche Alge wird traditionell zum Einwickeln von Maki-Sushi verwendet?", "Nori", ["Wakame", "Kombu", "Dulse"], "Nori sind getrocknete, geröstete Algenblätter."),
    (1, "Aus welcher Frucht wird Wein hergestellt?", "Trauben", ["Äpfeln", "Pflaumen", "Kirschen"], "Wein entsteht durch die Gärung von Traubensaft."),
    (2, "Welches Land ist der größte Kaffeeproduzent der Welt?", "Brasilien", ["Vietnam", "Kolumbien", "Äthiopien"], "Brasilien liefert seit über 150 Jahren den meisten Kaffee."),
    (2, "Was ist die Hauptzutat von Guacamole?", "Avocado", ["Tomate", "Gurke", "Zucchini"], "Guacamole wird aus zerdrückten Avocados zubereitet."),
    (2, "Welches Gewürz gehört nach Gewicht zu den teuersten der Welt?", "Safran", ["Zimt", "Paprika", "Kümmel"], "Safran besteht aus den Stempelfäden der Krokusblüte und wird von Hand geerntet."),
    (2, "Aus welchem Land stammt die Paella?", "Spanien", ["Portugal", "Italien", "Mexiko"], "Die Paella stammt aus Valencia in Spanien."),
    (2, "Woraus wird schottischer Single Malt Whisky hergestellt?", "Gemälzter Gerste", ["Mais", "Reis", "Kartoffeln"], "Single Malt wird aus gemälzter Gerste gebrannt."),
    (1, "Aus welchem Land stammt Feta-Käse?", "Griechenland", ["Türkei", "Italien", "Bulgarien"], "Feta ist ein Salzlakenkäse und in der EU für Griechenland geschützt."),
    (3, "Welche dieser Früchte ist botanisch eine Beere?", "Banane", ["Erdbeere", "Himbeere", "Kirsche"], "Botanisch zählt die Banane zu den Beeren, Erdbeere und Himbeere nicht."),
    (2, "Aus welcher Pflanze wird Tofu hergestellt?", "Soja", ["Erbsen", "Linsen", "Mais"], "Tofu entsteht aus geronnener Sojamilch."),
    (2, "Was ist die Hauptzutat von Hummus?", "Kichererbsen", ["Linsen", "Bohnen", "Erbsen"], "Hummus wird aus pürierten Kichererbsen und Sesampaste hergestellt."),
    (1, "Welches Getränk wird aus Hopfen, Malz, Hefe und Wasser gebraut?", "Bier", ["Wein", "Met", "Cidre"], "Das sind die klassischen Zutaten des deutschen Reinheitsgebots."),
    (2, "Wie heißt das italienische Dessert mit Mascarpone und Löffelbiskuits?", "Tiramisu", ["Panna Cotta", "Cannoli", "Zabaione"], "Tiramisu bedeutet übersetzt „zieh mich hoch“."),
    (3, "In welchem Jahr wurde das bayerische Reinheitsgebot für Bier erlassen?", "1516", ["1618", "1871", "1415"], "Das Reinheitsgebot wurde 1516 in Ingolstadt verkündet."),
    (1, "Welche Käsesorte ist für ihre großen Löcher bekannt?", "Emmentaler", ["Gouda", "Camembert", "Parmesan"], "Die Löcher entstehen durch Gase bei der Reifung."),
    (2, "Was ist die Hauptzutat von Marzipan?", "Mandeln", ["Haselnüsse", "Erdnüsse", "Kokos"], "Marzipan besteht aus Mandeln und Zucker."),
    (1, "Woraus wird Schokolade hergestellt?", "Kakaobohnen", ["Kaffeebohnen", "Sojabohnen", "Haselnüssen"], "Kakaobohnen wachsen an Kakaobäumen in den Tropen."),
    (2, "Aus welcher Region stammt die Kartoffel ursprünglich?", "Anden in Südamerika", ["Irland", "Deutschland", "Indien"], "Die Kartoffel wurde in den Anden domestiziert."),
    (2, "Wie heißt das japanische alkoholische Getränk aus Reis?", "Sake", ["Soju", "Baijiu", "Matcha"], "Sake wird aus vergorenem Reis hergestellt."),
    (3, "Aus welcher Milch wird Roquefort-Käse hergestellt?", "Schafsmilch", ["Kuhmilch", "Ziegenmilch", "Büffelmilch"], "Roquefort reift in Höhlen und wird aus Schafsmilch gemacht."),
    (1, "Welches Gemüse bringt beim Schneiden oft zum Weinen?", "Zwiebel", ["Karotte", "Gurke", "Paprika"], "Beim Schneiden werden Stoffe frei, die die Augen reizen."),
    (2, "Wie heißt die kalte spanische Suppe aus Tomaten und Gemüse?", "Gazpacho", ["Minestrone", "Borschtsch", "Ratatouille"], "Gazpacho kommt aus Andalusien und wird kalt serviert."),
    (3, "Aus welcher Teigart besteht Baklava hauptsächlich?", "Filoteig", ["Hefeteig", "Mürbeteig", "Blätterteig"], "Baklava besteht aus vielen hauchdünnen Teigschichten mit Nüssen und Sirup."),
    (2, "Welche Beere gibt Gin seinen typischen Geschmack?", "Wacholderbeere", ["Preiselbeere", "Johannisbeere", "Brombeere"], "Wacholder ist die wichtigste Zutat im Gin."),
    (1, "Welches Gemüse wird zu Halloween traditionell ausgehöhlt und beleuchtet?", "Kürbis", ["Rübe", "Kohl", "Kartoffel"], "Der Kürbis ersetzte die ursprünglich verwendeten Rüben."),
    (2, "Aus welchem Land stammt Kimchi?", "Korea", ["Japan", "China", "Thailand"], "Kimchi ist fermentierter Kohl und ein koreanisches Nationalgericht."),
    (2, "Wie nennt man die fünfte Geschmacksrichtung neben süß, sauer, salzig und bitter?", "Umami", ["Scharf", "Fettig", "Herb"], "Umami bedeutet auf Japanisch „herzhaft“."),
]

TECHNIK_COMPUTER = [
    (1, "Wofür steht die Abkürzung „WLAN“?", "Wireless Local Area Network", ["World Large Area Net", "Wide Link Access Network", "Wired Local Access Node"], "WLAN bezeichnet ein drahtloses lokales Netzwerk."),
    (1, "Welches Unternehmen stellte 2007 das erste iPhone vor?", "Apple", ["Samsung", "Nokia", "Microsoft"], "Steve Jobs präsentierte das iPhone im Januar 2007."),
    (2, "Wer gilt als Erfinder des World Wide Web?", "Tim Berners-Lee", ["Bill Gates", "Steve Jobs", "Vint Cerf"], "Tim Berners-Lee entwickelte das Web 1989 am CERN."),
    (2, "Wofür steht die Abkürzung „USB“?", "Universal Serial Bus", ["Unified System Board", "Ultra Speed Byte", "Universal Storage Block"], "USB ist ein Standard zum Anschluss von Geräten."),
    (2, "Welche Programmiersprache trägt einen Kaffee-Begriff im Namen und stammt ursprünglich von Sun Microsystems?", "Java", ["Python", "Ruby", "Swift"], "Java wurde in den 1990er-Jahren bei Sun Microsystems entwickelt."),
    (2, "Wie viele Bit hat ein Byte?", "8", ["4", "16", "32"], "Ein Byte besteht aus acht Bit."),
    (2, "Wofür steht die Abkürzung „CPU“?", "Central Processing Unit", ["Computer Personal Unit", "Central Power Unit", "Core Program Utility"], "Die CPU ist der Hauptprozessor eines Computers."),
    (1, "Welche Taste löscht Zeichen links vom Cursor?", "Rücktaste", ["Entf", "Esc", "Tab"], "Mit der Rücktaste (Backspace) löscht man nach links."),
    (3, "In welchem Jahr wurde Google gegründet?", "1998", ["1995", "2001", "2004"], "Larry Page und Sergey Brin gründeten Google 1998."),
    (2, "Welches Betriebssystem wurde von Linus Torvalds begonnen?", "Linux", ["Unix", "Windows", "macOS"], "Linus Torvalds startete Linux 1991 als Student."),
    (2, "Wofür steht „HTML“?", "HyperText Markup Language", ["High Tech Machine Language", "Hyper Transfer Media Link", "Home Tool Markup Language"], "HTML beschreibt die Struktur von Webseiten."),
    (3, "Welche Dezimalzahl entspricht der Binärzahl 1010?", "10", ["8", "12", "14"], "1010 bedeutet 8 + 2 = 10."),
    (2, "Wie nennt man Schadsoftware, die Daten verschlüsselt und Lösegeld verlangt?", "Ransomware", ["Spyware", "Adware", "Phishing"], "Ransomware sperrt Daten bis zur Zahlung."),
    (1, "Welches Gerät verbindet dein Heimnetzwerk mit dem Internet?", "Router", ["Drucker", "Scanner", "Monitor"], "Der Router vermittelt zwischen Heimnetz und Internet."),
    (2, "Wer gründete Microsoft zusammen mit Paul Allen?", "Bill Gates", ["Steve Jobs", "Larry Page", "Elon Musk"], "Gates und Allen gründeten Microsoft 1975."),
    (2, "Wer gründete Apple zusammen mit Steve Wozniak?", "Steve Jobs", ["Bill Gates", "Tim Cook", "Larry Ellison"], "Jobs und Wozniak gründeten Apple 1976 in einer Garage."),
    (2, "Welche Firma entwickelt das Betriebssystem Android weiter?", "Google", ["Samsung", "Microsoft", "Nokia"], "Android gehört seit 2005 zu Google."),
    (3, "Was gibt die Einheit Hertz bei einem Prozessor an?", "Die Taktfrequenz", ["Die Speichergröße", "Den Stromverbrauch", "Die Temperatur"], "Hertz misst Schwingungen pro Sekunde."),
    (1, "Wofür steht „KI“ in der Technik?", "Künstliche Intelligenz", ["Kabellose Internetverbindung", "Kurze Information", "Kontrollierte Instanz"], "KI bezeichnet Computersysteme, die lernen und Aufgaben lösen."),
    (2, "Wie nennt man den Betrug, bei dem gefälschte Nachrichten Zugangsdaten abgreifen sollen?", "Phishing", ["Streaming", "Hosting", "Tracking"], "Phishing ist das „Angeln“ nach Passwörtern."),
    (1, "Welches Zeichen trennt in einer E-Mail-Adresse den Namen vom Anbieter?", "@", ["#", "&", "%"], "Das @-Zeichen wird „At“ oder „Klammeraffe“ genannt."),
    (3, "Welches Element ist der wichtigste Grundstoff für Computerchips?", "Silizium", ["Kupfer", "Eisen", "Kohlenstoff"], "Silizium ist ein Halbleiter und Grundlage der Chipherstellung."),
    (2, "Wofür steht die Abkürzung „GPS“?", "Global Positioning System", ["General Path Signal", "Global Phone Service", "Geo Planning System"], "GPS bestimmt Positionen über Satelliten."),
    (2, "Welchem Unternehmen gehört die Videoplattform YouTube?", "Google", ["Meta", "Microsoft", "Amazon"], "Google kaufte YouTube 2006."),
    (2, "Wofür steht „PDF“?", "Portable Document Format", ["Personal Data File", "Printed Document Form", "Public Digital Format"], "PDF-Dateien sehen auf allen Geräten gleich aus."),
    (1, "Wie nennt man ein Programm, das Webseiten anzeigt?", "Browser", ["Compiler", "Treiber", "Server"], "Beispiele für Browser sind Firefox, Chrome und Safari."),
    (3, "Welche Spielkonsole brachte Nintendo 2017 auf den Markt?", "Nintendo Switch", ["Wii U", "GameCube", "Wii"], "Die Switch ist eine Hybrid-Konsole für Fernseher und unterwegs."),
    (2, "Wie nennt man die kleinste Einheit eines digitalen Bildes?", "Pixel", ["Voxel", "Byte", "Vektor"], "Ein Bild besteht aus vielen einzelnen Pixeln."),
    (1, "Woraus bestehen Glasfaserkabel?", "Glas", ["Kupfer", "Aluminium", "Stahl"], "Glasfasern übertragen Daten mit Lichtimpulsen."),
    (3, "Welcher Wissenschaftler entwickelte das Modell der Turing-Maschine?", "Alan Turing", ["John von Neumann", "Charles Babbage", "Konrad Zuse"], "Alan Turing legte 1936 die Grundlagen der theoretischen Informatik."),
]

TIERE_NATUR = [
    (1, "Wie viele Beine hat ein Insekt?", "6", ["4", "8", "10"], "Insekten haben sechs Beine."),
    (1, "Welches ist das größte Tier der Welt?", "Blauwal", ["Elefant", "Giraffe", "Walhai"], "Der Blauwal wird bis zu 30 Meter lang."),
    (2, "Wie nennt man ein junges Pferd?", "Fohlen", ["Kalb", "Kitz", "Lamm"], "Junge Pferde heißen Fohlen."),
    (2, "Welches dieser Tiere ist ein Säugetier, das Eier legt?", "Schnabeltier", ["Igel", "Fledermaus", "Delfin"], "Das Schnabeltier gehört zu den eierlegenden Säugetieren."),
    (1, "Welcher flugunfähige Vogel lebt in der Antarktis?", "Pinguin", ["Strauß", "Kiwi", "Emu"], "Pinguine leben auf der Südhalbkugel."),
    (2, "Wie viele Herzen hat ein Oktopus?", "3", ["1", "2", "4"], "Ein Oktopus hat drei Herzen."),
    (1, "Welches Tier hält bei uns im Winter Winterschlaf?", "Igel", ["Reh", "Fuchs", "Hase"], "Igel schlafen von Herbst bis Frühling."),
    (2, "Wie nennt man Tiere, die Pflanzen und Fleisch fressen?", "Allesfresser", ["Pflanzenfresser", "Fleischfresser", "Aasfresser"], "Allesfresser sind zum Beispiel Menschen und Bären."),
    (1, "Wie nennt man eine Gruppe von Wölfen?", "Rudel", ["Herde", "Schwarm", "Schar"], "Wölfe leben in Rudeln."),
    (2, "In welchem Regenwald lebt das größte zusammenhängende tropische Waldgebiet der Erde?", "Amazonas-Regenwald", ["Kongo-Regenwald", "Daintree-Regenwald", "Borneo-Regenwald"], "Der Amazonas-Regenwald ist der größte tropische Regenwald."),
    (1, "Welches Tier hat den längsten Hals?", "Giraffe", ["Elefant", "Kamel", "Strauß"], "Der Hals einer Giraffe misst bis zu 2 Meter."),
    (2, "Welches dieser Tiere ist ein Wirbeltier?", "Frosch", ["Qualle", "Schnecke", "Spinne"], "Frösche haben eine Wirbelsäule."),
    (1, "Welches ist das größte lebende Landtier?", "Afrikanischer Elefant", ["Nashorn", "Nilpferd", "Giraffe"], "Der Afrikanische Elefant wiegt bis zu 6 Tonnen."),
    (3, "Von welchem Baum stammt Kork?", "Korkeiche", ["Buche", "Birke", "Kastanie"], "Kork wird aus der Rinde der Korkeiche gewonnen."),
    (2, "Welche Pflanze gehört zu den am schnellsten wachsenden Gräsern?", "Bambus", ["Weizen", "Mais", "Schilf"], "Bambus kann an einem Tag fast einen Meter wachsen."),
    (1, "Was stellen Bienen aus Nektar her?", "Honig", ["Wachs", "Zucker", "Sirup"], "Bienen verwandeln Nektar in Honig."),
    (2, "Wie nennt man die Verwandlung einer Raupe in einen Schmetterling?", "Metamorphose", ["Mutation", "Evolution", "Migration"], "Dabei durchläuft sie das Puppenstadium."),
    (2, "Wie nennt man den Vorgang, mit dem Pflanzen aus Licht Energie gewinnen?", "Fotosynthese", ["Verdauung", "Zellatmung", "Gärung"], "Dabei entstehen Zucker und Sauerstoff."),
    (3, "Welches Gas nehmen Pflanzen bei der Fotosynthese auf?", "Kohlendioxid", ["Sauerstoff", "Stickstoff", "Wasserstoff"], "Pflanzen binden Kohlendioxid und geben Sauerstoff ab."),
    (3, "Welches Säugetier kann aktiv fliegen?", "Fledermaus", ["Flughörnchen", "Gleitbeutler", "Riesengleiter"], "Nur Fledermäuse beherrschen den Flug mit Flügelschlag."),
    (1, "Wie nennt man Tiere, die vorwiegend nachts aktiv sind?", "Nachtaktiv", ["Tagaktiv", "Winteraktiv", "Standorttreu"], "Eulen und Fledermäuse sind nachtaktiv."),
    (3, "Welcher Vogel legt das größte Ei?", "Strauß", ["Albatros", "Emu", "Kondor"], "Das Straußenei ist das größte Vogelei."),
    (3, "Wie lange dauert die Tragzeit eines Elefanten ungefähr?", "22 Monate", ["9 Monate", "12 Monate", "36 Monate"], "Elefanten tragen fast zwei Jahre lang."),
    (2, "Welches Tier kann seine Hautfarbe zur Tarnung und Verständigung verändern?", "Chamäleon", ["Leguan", "Gecko", "Salamander"], "Chamäleons ändern ihre Farbe auch je nach Stimmung."),
    (3, "Wie heißt der größte Fisch der Welt?", "Walhai", ["Weißer Hai", "Mantarochen", "Hammerhai"], "Der Walhai wird bis zu 12 Meter lang und frisst Plankton."),
    (2, "Welches Tier ziert das deutsche Bundeswappen?", "Adler", ["Löwe", "Bär", "Falke"], "Der Bundesadler ist das Wappentier Deutschlands."),
    (2, "Welche Farbe hat der Pflanzenfarbstoff Chlorophyll?", "Grün", ["Gelb", "Rot", "Blau"], "Chlorophyll färbt Blätter grün."),
    (2, "Welches Gas ist am häufigsten in der Erdatmosphäre?", "Stickstoff", ["Sauerstoff", "Kohlendioxid", "Argon"], "Etwa 78 % der Luft bestehen aus Stickstoff."),
    (3, "Woraus besteht Honig überwiegend?", "Zucker", ["Wasser", "Fett", "Eiweiß"], "Honig besteht zu etwa 80 % aus Fruchtzucker und Traubenzucker."),
    (1, "Wie nennt man ein junges Schaf?", "Lamm", ["Kitz", "Kalb", "Ferkel"], "Junge Schafe heißen Lämmer."),
]

KUNST_LITERATUR = [
    (1, "Wer malte „Die Sternennacht“?", "Vincent van Gogh", ["Claude Monet", "Pablo Picasso", "Paul Cézanne"], "Van Gogh malte das Bild 1889."),
    (2, "Wer schrieb „Die Verwandlung“?", "Franz Kafka", ["Thomas Mann", "Hermann Hesse", "Bertolt Brecht"], "Die Erzählung erschien 1915."),
    (2, "Wer malte die Decke der Sixtinischen Kapelle?", "Michelangelo", ["Raffael", "Leonardo da Vinci", "Tizian"], "Michelangelo malte sie zwischen 1508 und 1512."),
    (2, "Wer schrieb „Die Leiden des jungen Werthers“?", "Johann Wolfgang von Goethe", ["Friedrich Schiller", "Heinrich Heine", "Theodor Fontane"], "Der Briefroman erschien 1774."),
    (2, "Welcher Künstler gilt als Mitbegründer des Kubismus?", "Pablo Picasso", ["Salvador Dalí", "Henri Matisse", "Paul Klee"], "Picasso begründete den Kubismus gemeinsam mit Georges Braque."),
    (1, "Wer schrieb die „Harry Potter“-Romane?", "J. K. Rowling", ["Astrid Lindgren", "Roald Dahl", "Cornelia Funke"], "Der erste Band erschien 1997."),
    (2, "Wer schrieb „Der kleine Prinz“?", "Antoine de Saint-Exupéry", ["Victor Hugo", "Albert Camus", "Jules Verne"], "Das Buch erschien 1943."),
    (3, "Wie heißt das berühmte Gemälde von Edvard Munch mit der verzweifelten Gestalt?", "Der Schrei", ["Die Angst", "Der Ruf", "Die Nacht"], "„Der Schrei“ entstand 1893 und ist ein Hauptwerk des Expressionismus."),
    (2, "In welchem Museum hängt die Mona Lisa?", "Louvre", ["Prado", "Uffizien", "British Museum"], "Die Mona Lisa hängt im Louvre in Paris."),
    (2, "Wer schrieb „Die Glocke“?", "Friedrich Schiller", ["Goethe", "Lessing", "Heine"], "Das „Lied von der Glocke“ stammt von Schiller."),
    (3, "Wer schrieb „Die Blechtrommel“?", "Günter Grass", ["Heinrich Böll", "Siegfried Lenz", "Martin Walser"], "Der Roman erschien 1959."),
    (2, "Welcher Autor schrieb das Drama „Hamlet“?", "William Shakespeare", ["Christopher Marlowe", "Charles Dickens", "Oscar Wilde"], "„Hamlet“ entstand um 1600."),
    (2, "Welcher Maler schuf „Das Mädchen mit dem Perlenohrring“?", "Jan Vermeer", ["Rembrandt", "Frans Hals", "Rubens"], "Vermeer malte das Bild um 1665."),
    (3, "Wie heißt der Kunststil, der nach einem Gemälde von Claude Monet benannt wurde?", "Impressionismus", ["Expressionismus", "Realismus", "Surrealismus"], "Der Name geht auf Monets „Impression, soleil levant“ zurück."),
    (2, "Wer schrieb den Roman „1984“?", "George Orwell", ["Aldous Huxley", "Ray Bradbury", "H. G. Wells"], "„1984“ erschien 1949."),
    (1, "Wer schrieb „Der Herr der Ringe“?", "J. R. R. Tolkien", ["C. S. Lewis", "J. K. Rowling", "George R. R. Martin"], "Das Buch erschien 1954 und 1955."),
    (3, "Welcher Autor schrieb „Krieg und Frieden“?", "Leo Tolstoi", ["Fjodor Dostojewski", "Anton Tschechow", "Maxim Gorki"], "Der Roman erschien 1869."),
    (1, "Welche Brüder sammelten deutsche Märchen?", "Brüder Grimm", ["Brüder Wright", "Brüder Mann", "Brüder Humboldt"], "Jacob und Wilhelm Grimm gaben die „Kinder- und Hausmärchen“ heraus."),
    (3, "Welcher Architekt entwarf die Sagrada Família in Barcelona?", "Antoni Gaudí", ["Le Corbusier", "Frank Lloyd Wright", "Norman Foster"], "Gaudí widmete ihr die letzten Jahrzehnte seines Lebens."),
    (2, "Welcher Künstler ist für seine Pop-Art-Bilder mit Suppendosen bekannt?", "Andy Warhol", ["Roy Lichtenstein", "Jackson Pollock", "Keith Haring"], "Warhol war ein Hauptvertreter der Pop-Art."),
    (3, "Wer schrieb die „Buddenbrooks“?", "Thomas Mann", ["Hermann Hesse", "Robert Musil", "Alfred Döblin"], "Mann erhielt 1929 den Nobelpreis für Literatur für dieses Werk."),
    (2, "Wie viele Zeilen hat ein klassisches Sonett?", "14", ["8", "12", "16"], "Ein Sonett besteht aus zwei Quartetten und zwei Terzetten."),
    (2, "Welcher deutsche Maler schuf „Der Wanderer über dem Nebelmeer“?", "Caspar David Friedrich", ["Albrecht Dürer", "Franz Marc", "Max Liebermann"], "Das Bild ist ein Hauptwerk der Romantik."),
    (3, "Wer schrieb „Don Quijote“?", "Miguel de Cervantes", ["Lope de Vega", "Federico García Lorca", "Gabriel García Márquez"], "Der Roman erschien in zwei Teilen 1605 und 1615."),
    (1, "Aus welchen zwei Farben mischt man Grün?", "Gelb und Blau", ["Rot und Blau", "Rot und Gelb", "Rot und Weiß"], "Gelb und Blau ergeben zusammen Grün."),
    (2, "Welcher niederländische Maler schuf „Die Nachtwache“?", "Rembrandt", ["Vermeer", "Van Gogh", "Rubens"], "Rembrandt malte das Gemälde 1642."),
    (3, "Welcher Maler schuf „Die Beständigkeit der Erinnerung“ mit den zerfließenden Uhren?", "Salvador Dalí", ["René Magritte", "Max Ernst", "Joan Miró"], "Das Gemälde von 1931 ist ein Hauptwerk des Surrealismus."),
    (1, "Welche Autorin schrieb „Pippi Langstrumpf“?", "Astrid Lindgren", ["Selma Lagerlöf", "Michael Ende", "Erich Kästner"], "Das Buch erschien 1945."),
    (3, "Wer schrieb den Roman „Im Westen nichts Neues“?", "Erich Maria Remarque", ["Ernst Jünger", "Stefan Zweig", "Carl Zuckmayer"], "Der Antikriegsroman erschien 1929."),
    (2, "Wer schrieb den „Struwwelpeter“?", "Heinrich Hoffmann", ["Wilhelm Busch", "Erich Kästner", "Otfried Preußler"], "Der Frankfurter Arzt Heinrich Hoffmann veröffentlichte das Buch 1845."),
]

WELTRAUM = [
    (1, "Welcher Planet ist der Sonne am nächsten?", "Merkur", ["Venus", "Mars", "Erde"], "Merkur ist der kleinste und sonnennächste Planet."),
    (1, "Welcher Planet wird „Roter Planet“ genannt?", "Mars", ["Venus", "Jupiter", "Merkur"], "Eisenoxid im Boden färbt den Mars rot."),
    (2, "Wer betrat 1969 als erster Mensch den Mond?", "Neil Armstrong", ["Buzz Aldrin", "Juri Gagarin", "Michael Collins"], "Neil Armstrong betrat den Mond im Juli 1969 bei der Mission Apollo 11."),
    (1, "Wie heißt die Galaxie, in der unser Sonnensystem liegt?", "Milchstraße", ["Andromeda", "Sombrero", "Whirlpool"], "Die Milchstraße ist eine Balkenspiralgalaxie."),
    (1, "Wie viele natürliche Monde hat die Erde?", "1", ["2", "3", "0"], "Die Erde hat nur den Mond."),
    (1, "Welcher Planet hat die auffälligsten Ringe?", "Saturn", ["Jupiter", "Mars", "Venus"], "Saturns Ringe bestehen aus Eis und Gestein."),
    (3, "Wie lange braucht das Licht von der Sonne zur Erde ungefähr?", "8 Minuten", ["8 Sekunden", "1 Stunde", "1 Tag"], "Das Sonnenlicht ist etwa acht Minuten unterwegs."),
    (2, "Wie hieß der erste Mensch im Weltall (1961)?", "Juri Gagarin", ["Neil Armstrong", "Alan Shepard", "Walentina Tereschkowa"], "Gagarin umrundete die Erde am 12. April 1961."),
    (3, "Wie heißt der größte Mond des Saturn?", "Titan", ["Europa", "Ganymed", "Io"], "Titan hat eine dichte Atmosphäre."),
    (2, "Wie nennt man die Explosion eines massereichen Sterns am Ende seines Lebens?", "Supernova", ["Nova", "Pulsar", "Quasar"], "Eine Supernova kann kurzzeitig so hell leuchten wie eine ganze Galaxie."),
    (3, "Welcher Stern ist der Sonne am nächsten?", "Proxima Centauri", ["Sirius", "Betelgeuse", "Polarstern"], "Proxima Centauri ist etwa 4,2 Lichtjahre entfernt."),
    (2, "Welcher Himmelskörper verlor 2006 seinen Planetenstatus?", "Pluto", ["Ceres", "Eris", "Makemake"], "Pluto gilt seit 2006 als Zwergplanet."),
    (2, "Wie hieß der erste künstliche Erdsatellit (1957)?", "Sputnik 1", ["Explorer 1", "Vostok 1", "Apollo 1"], "Die Sowjetunion startete Sputnik 1 am 4. Oktober 1957."),
    (3, "Welche Raumsonde verließ 2012 als erste den Einflussbereich der Sonne?", "Voyager 1", ["Pioneer 10", "Voyager 2", "New Horizons"], "Voyager 1 erreichte 2012 den interstellaren Raum."),
    (2, "Was ist eine Sternschnuppe?", "Ein verglühendes Staubkorn in der Atmosphäre", ["Ein sterbender Stern", "Ein kleiner Komet", "Ein Satellit"], "Winzige Teilchen verglühen beim Eintritt in die Erdatmosphäre."),
    (2, "Welcher Planet dreht sich fast auf der Seite liegend um die Sonne?", "Uranus", ["Neptun", "Saturn", "Merkur"], "Die Achse des Uranus ist um etwa 98 Grad geneigt."),
    (3, "In welchem Jahr wurde das Weltraumteleskop Hubble gestartet?", "1990", ["1980", "1995", "2000"], "Hubble startete im April 1990."),
    (3, "Wie hieß die Mondlandefähre von Apollo 11?", "Eagle", ["Columbia", "Odyssey", "Challenger"], "„Eagle“ landete am 20. Juli 1969 im Meer der Ruhe."),
    (2, "Wie nennt man eine Region im All, aus der selbst Licht nicht entkommen kann?", "Schwarzes Loch", ["Weißer Zwerg", "Nebel", "Komet"], "Die Gravitation ist dort extrem stark."),
    (1, "Wie heißt der Stern im Zentrum unseres Sonnensystems?", "Sonne", ["Sirius", "Polarstern", "Mond"], "Die Sonne enthält fast die gesamte Masse des Sonnensystems."),
    (2, "Welcher Planet hat den „Großen Roten Fleck“?", "Jupiter", ["Mars", "Saturn", "Neptun"], "Der Fleck ist ein riesiger Wirbelsturm."),
    (3, "Wer formulierte die drei Gesetze der Planetenbewegung?", "Johannes Kepler", ["Isaac Newton", "Galileo Galilei", "Nikolaus Kopernikus"], "Kepler beschrieb 1609 und 1619 die Bahnen der Planeten."),
    (2, "Wie nennt man die Strecke, die das Licht in einem Jahr zurücklegt?", "Lichtjahr", ["Parsec", "Lichtsekunde", "Astronomische Einheit"], "Ein Lichtjahr entspricht rund 9,46 Billionen Kilometern."),
    (2, "Welche Weltraumorganisation ist die europäische?", "ESA", ["NASA", "Roskosmos", "JAXA"], "Die ESA hat ihren Hauptsitz in Paris."),
    (3, "Wie heißt der Rover, der 2021 auf dem Mars landete?", "Perseverance", ["Curiosity", "Opportunity", "Spirit"], "Perseverance landete im Februar 2021 im Krater Jezero."),
    (3, "Wer war der erste Deutsche im Weltall (1978)?", "Sigmund Jähn", ["Ulf Merbold", "Alexander Gerst", "Thomas Reiter"], "Der DDR-Bürger Sigmund Jähn flog 1978 mit Sojus 31."),
    (2, "Welcher Planet ist der heißeste im Sonnensystem?", "Venus", ["Merkur", "Mars", "Jupiter"], "Die dichte Atmosphäre der Venus erzeugt einen extremen Treibhauseffekt."),
    (1, "Wie nennt man den Mond, wenn man von der Erde aus seine ganze beleuchtete Seite sieht?", "Vollmond", ["Neumond", "Halbmond", "Sichelmond"], "Beim Vollmond steht die Erde zwischen Sonne und Mond."),
    (2, "Was verursacht hauptsächlich Ebbe und Flut?", "Die Anziehungskraft des Mondes", ["Der Wind", "Die Erdrotation allein", "Die Sonnenwärme"], "Die Gravitation des Mondes zieht das Wasser der Meere an."),
    (3, "Wie hieß die erste Frau im Weltall (1963)?", "Walentina Tereschkowa", ["Sally Ride", "Swetlana Sawizkaja", "Jelena Kondakowa"], "Walentina Tereschkowa flog 1963 mit Wostok 6."),
]

DEUTSCHLAND_EUROPA = [
    (1, "Wie viele Bundesländer hat Deutschland?", "16", ["14", "15", "17"], "Deutschland besteht aus 16 Bundesländern."),
    (2, "Welches ist das flächenmäßig größte Bundesland?", "Bayern", ["Niedersachsen", "Baden-Württemberg", "Nordrhein-Westfalen"], "Bayern ist mit rund 70.500 km² das größte Bundesland."),
    (2, "Welcher Fluss ist in Deutschland am längsten?", "Rhein", ["Elbe", "Donau", "Main"], "Der Rhein hat in Deutschland etwa 865 Kilometer Länge."),
    (2, "Wie heißt der höchste Berg Deutschlands?", "Zugspitze", ["Watzmann", "Feldberg", "Brocken"], "Die Zugspitze misst 2.962 Meter."),
    (1, "Wie heißt die Hauptstadt von Bayern?", "München", ["Nürnberg", "Augsburg", "Würzburg"], "München ist die Landeshauptstadt Bayerns."),
    (2, "Wann wurde Deutschland wiedervereinigt?", "1990", ["1989", "1991", "1985"], "Die Wiedervereinigung erfolgte am 3. Oktober 1990."),
    (2, "Wie hieß die deutsche Währung vor dem Euro?", "D-Mark", ["Reichsmark", "Taler", "Gulden"], "Die D-Mark galt von 1948 bis 2001 als Bargeld."),
    (3, "Wer wählt in Deutschland den Bundeskanzler?", "Der Bundestag", ["Das Volk direkt", "Der Bundesrat", "Der Bundespräsident"], "Der Bundestag wählt den Kanzler auf Vorschlag des Bundespräsidenten."),
    (1, "Welche Farben hat die deutsche Flagge von oben nach unten?", "Schwarz, Rot, Gold", ["Rot, Weiß, Schwarz", "Schwarz, Weiß, Rot", "Rot, Gold, Schwarz"], "Die Bundesflagge ist Schwarz-Rot-Gold."),
    (2, "Welcher See liegt vollständig in Deutschland und ist dort der größte?", "Müritz", ["Bodensee", "Chiemsee", "Starnberger See"], "Die Müritz in Mecklenburg-Vorpommern ist der größte Binnensee Deutschlands."),
    (3, "In welcher Stadt hat das Bundesverfassungsgericht seinen Sitz?", "Karlsruhe", ["Berlin", "Frankfurt", "Leipzig"], "Das Gericht sitzt seit 1951 in Karlsruhe."),
    (3, "In welchem Jahr trat das Grundgesetz in Kraft?", "1949", ["1945", "1955", "1990"], "Das Grundgesetz wurde am 23. Mai 1949 verkündet."),
    (2, "Welche Stadt ist die Hauptstadt von Sachsen?", "Dresden", ["Leipzig", "Chemnitz", "Erfurt"], "Dresden ist die Landeshauptstadt Sachsens."),
    (1, "Welche Stadt hat in Deutschland die meisten Einwohner?", "Berlin", ["Hamburg", "München", "Köln"], "Berlin hat rund 3,7 Millionen Einwohner."),
    (1, "Welches dieser Länder grenzt nicht an Deutschland?", "Spanien", ["Dänemark", "Polen", "Österreich"], "Spanien hat keine gemeinsame Grenze mit Deutschland."),
    (3, "Wie viele Nachbarländer hat Deutschland?", "9", ["7", "8", "10"], "Deutschland grenzt an neun Staaten."),
    (2, "In welchem Jahr wurde die Berliner Mauer gebaut?", "1961", ["1949", "1953", "1968"], "Der Mauerbau begann am 13. August 1961."),
    (1, "Wie heißt das berühmte Münchner Volksfest?", "Oktoberfest", ["Cannstatter Wasen", "Kieler Woche", "Kölner Karneval"], "Das Oktoberfest findet seit 1810 auf der Theresienwiese statt."),
    (2, "Wer war der erste Bundeskanzler der Bundesrepublik Deutschland?", "Konrad Adenauer", ["Willy Brandt", "Ludwig Erhard", "Helmut Schmidt"], "Adenauer war von 1949 bis 1963 Kanzler."),
    (2, "Welcher Kanzler führte Deutschland 1990 in die Einheit?", "Helmut Kohl", ["Helmut Schmidt", "Gerhard Schröder", "Willy Brandt"], "Helmut Kohl war von 1982 bis 1998 Kanzler."),
    (1, "Wer war von 2005 bis 2021 Bundeskanzlerin?", "Angela Merkel", ["Ursula von der Leyen", "Annalena Baerbock", "Andrea Nahles"], "Angela Merkel war 16 Jahre im Amt."),
    (2, "Wie heißt das Staatsoberhaupt Deutschlands?", "Bundespräsident", ["Bundeskanzler", "Bundestagspräsident", "Ministerpräsident"], "Der Bundespräsident repräsentiert Deutschland."),
    (2, "Welche Stadt nennt man das „Tor zur Welt“?", "Hamburg", ["Bremen", "Rostock", "Lübeck"], "Hamburg besitzt den größten deutschen Seehafen."),
    (3, "Welche Stadt war von 1949 bis 1990 Hauptstadt der Bundesrepublik?", "Bonn", ["Frankfurt", "Köln", "Hannover"], "Bonn war Regierungssitz der alten Bundesrepublik."),
    (2, "Wie heißt die größte deutsche Insel?", "Rügen", ["Sylt", "Usedom", "Fehmarn"], "Rügen in der Ostsee hat eine Fläche von rund 926 km²."),
    (1, "Wie viele Sterne zeigt die Flagge der Europäischen Union?", "12", ["10", "15", "27"], "Die zwölf Sterne stehen für Einheit und Harmonie."),
    (2, "In welcher Stadt hat die Europäische Zentralbank ihren Sitz?", "Frankfurt am Main", ["Brüssel", "Luxemburg", "Straßburg"], "Die EZB sitzt seit 1998 in Frankfurt am Main."),
    (3, "Mit welchen Verträgen wurde 1957 die Europäische Wirtschaftsgemeinschaft gegründet?", "Römische Verträge", ["Maastrichter Verträge", "Lissabonner Vertrag", "Pariser Verträge"], "Die Römischen Verträge wurden am 25. März 1957 unterzeichnet."),
    (1, "Wie heißt die Währung, die in vielen EU-Ländern gilt?", "Euro", ["Franken", "Kronen", "Pfund"], "Der Euro wurde 1999 als Buchgeld und 2002 als Bargeld eingeführt."),
    (3, "Wie heißt das Parlament der Europäischen Union?", "Europäisches Parlament", ["Europarat", "Europäische Kommission", "Rat der EU"], "Das Parlament wird alle fünf Jahre direkt gewählt."),
    (2, "Welche Stadt ist die Hauptstadt von Nordrhein-Westfalen?", "Düsseldorf", ["Köln", "Dortmund", "Essen"], "Düsseldorf ist die Landeshauptstadt von Nordrhein-Westfalen."),
]

KOERPER_GESUNDHEIT = [
    (1, "Wie viele Zähne hat ein Erwachsener mit Weisheitszähnen?", "32", ["28", "30", "34"], "Das vollständige Erwachsenengebiss hat 32 Zähne."),
    (1, "Welches Organ pumpt das Blut durch den Körper?", "Herz", ["Leber", "Lunge", "Niere"], "Das Herz ist ein Hohlmuskel."),
    (2, "Welches ist das größte Organ des Menschen?", "Haut", ["Leber", "Lunge", "Darm"], "Die Haut bedeckt etwa 1,8 Quadratmeter."),
    (2, "Welches Vitamin bildet der Körper mit Hilfe von Sonnenlicht?", "Vitamin D", ["Vitamin A", "Vitamin C", "Vitamin K"], "Die Haut bildet Vitamin D unter UV-Strahlung."),
    (2, "Wie viele Chromosomen hat ein Mensch normalerweise?", "46", ["23", "44", "48"], "Der Mensch hat 23 Chromosomenpaare."),
    (2, "Welches Organ filtert das Blut und bildet den Urin?", "Niere", ["Leber", "Milz", "Bauchspeicheldrüse"], "Die Nieren reinigen täglich etwa 180 Liter Blutplasma."),
    (3, "Welches ist der längste Knochen im menschlichen Körper?", "Oberschenkelknochen", ["Schienbein", "Oberarmknochen", "Wadenbein"], "Der Oberschenkelknochen (Femur) ist der längste und stärkste Knochen."),
    (2, "Wie nennt man die Zuckerkrankheit medizinisch?", "Diabetes mellitus", ["Anämie", "Asthma", "Arthritis"], "Beim Diabetes ist der Blutzuckerspiegel dauerhaft erhöht."),
    (1, "Mit welchem Sinnesorgan hören wir?", "Ohr", ["Nase", "Auge", "Zunge"], "Das Ohr nimmt Schallwellen auf."),
    (3, "Welche Blutgruppe gilt als Universalspender für rote Blutkörperchen?", "0 negativ", ["AB positiv", "A positiv", "B negativ"], "Blutgruppe 0 negativ ist für alle Blutgruppen verträglich."),
    (1, "Welches Vitamin ist in Zitrusfrüchten besonders reichlich enthalten?", "Vitamin C", ["Vitamin B12", "Vitamin D", "Vitamin K"], "Orangen und Zitronen enthalten viel Vitamin C."),
    (2, "Welche Blutzellen transportieren den Sauerstoff?", "Rote Blutkörperchen", ["Weiße Blutkörperchen", "Blutplättchen", "Blutplasma"], "Der rote Blutfarbstoff Hämoglobin bindet den Sauerstoff."),
    (2, "Welcher Teil des Auges steuert die Größe der Pupille?", "Iris", ["Hornhaut", "Netzhaut", "Linse"], "Die Iris regelt den Lichteinfall."),
    (2, "Wie viele Rippen hat ein Mensch normalerweise?", "24", ["12", "20", "28"], "Der Mensch hat zwölf Rippenpaare."),
    (2, "Welches Hormon der Bauchspeicheldrüse senkt den Blutzucker?", "Insulin", ["Adrenalin", "Östrogen", "Cortisol"], "Insulin schleust Zucker aus dem Blut in die Zellen."),
    (3, "Wie heißt der größte Muskel des menschlichen Körpers?", "Großer Gesäßmuskel", ["Oberschenkelmuskel", "Bizeps", "Zwerchfell"], "Der große Gesäßmuskel (Gluteus maximus) ist der größte Muskel."),
    (2, "In welchem Teil des Ohres liegen Hammer, Amboss und Steigbügel?", "Mittelohr", ["Innenohr", "Außenohr", "Gehörgang"], "Die drei Gehörknöchelchen übertragen den Schall."),
    (1, "Welches Organ ist für die Atmung zuständig?", "Lunge", ["Herz", "Magen", "Leber"], "In der Lunge gelangt Sauerstoff ins Blut."),
    (2, "Welcher Nährstoff liefert pro Gramm die meiste Energie?", "Fett", ["Kohlenhydrate", "Eiweiß", "Ballaststoffe"], "Ein Gramm Fett liefert etwa 9 Kilokalorien."),
    (3, "Wie hoch ist der Wasseranteil im Körper eines Erwachsenen ungefähr?", "60 %", ["20 %", "40 %", "90 %"], "Der Körper eines Erwachsenen besteht zu etwa 55 bis 60 % aus Wasser."),
    (3, "Wer entwickelte 1796 die erste Pockenimpfung?", "Edward Jenner", ["Louis Pasteur", "Robert Koch", "Alexander Fleming"], "Der englische Arzt Edward Jenner impfte mit Kuhpocken."),
    (2, "Wer entdeckte 1928 das Penicillin?", "Alexander Fleming", ["Robert Koch", "Louis Pasteur", "Wilhelm Röntgen"], "Fleming entdeckte das erste Antibiotikum zufällig."),
    (3, "Welches Organ produziert die Gallenflüssigkeit?", "Leber", ["Gallenblase", "Bauchspeicheldrüse", "Magen"], "Die Galle wird in der Leber gebildet und in der Gallenblase gespeichert."),
    (2, "Wie viel Blut hat ein Erwachsener ungefähr?", "5 Liter", ["2 Liter", "8 Liter", "12 Liter"], "Das Blutvolumen beträgt etwa 4 bis 6 Liter."),
    (1, "Wie nennt man die Anzahl der Herzschläge pro Minute?", "Puls", ["Blutdruck", "Atemfrequenz", "Temperatur"], "Der Puls lässt sich am Handgelenk fühlen."),
    (3, "Welcher Hirnteil steuert vor allem Gleichgewicht und Bewegungskoordination?", "Kleinhirn", ["Großhirn", "Stammhirn", "Zwischenhirn"], "Das Kleinhirn koordiniert Bewegungen."),
    (2, "Ab welcher Körpertemperatur spricht man ungefähr von Fieber?", "38 °C", ["36 °C", "37 °C", "40 °C"], "Ab 38,0 °C spricht man von Fieber."),
    (3, "Welches Eiweiß macht Haare und Nägel fest?", "Keratin", ["Kollagen", "Insulin", "Hämoglobin"], "Keratin ist der Hauptbestandteil von Haaren und Nägeln."),
    (3, "In welchem Organ befinden sich die Lungenbläschen (Alveolen)?", "Lunge", ["Herz", "Leber", "Niere"], "In den Alveolen findet der Gasaustausch statt."),
    (2, "Wie viele Stunden Schlaf werden Erwachsenen im Durchschnitt empfohlen?", "7 bis 9 Stunden", ["4 bis 5 Stunden", "10 bis 12 Stunden", "12 bis 14 Stunden"], "Die meisten Erwachsenen brauchen sieben bis neun Stunden Schlaf."),
]

EXTRA_FRAGEN = (
    _build("Film & TV", FILM_TV)
    + _build("Essen & Trinken", ESSEN_TRINKEN)
    + _build("Technik & Computer", TECHNIK_COMPUTER)
    + _build("Tiere & Natur", TIERE_NATUR)
    + _build("Kunst & Literatur", KUNST_LITERATUR)
    + _build("Weltraum", WELTRAUM)
    + _build("Deutschland & Europa", DEUTSCHLAND_EUROPA)
    + _build("Körper & Gesundheit", KOERPER_GESUNDHEIT)
)
