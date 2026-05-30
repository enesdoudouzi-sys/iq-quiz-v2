def get_random_fragen(anzahl=15, kategorie='alle'):
    if kategorie == 'alle':
        pool = ALLE_FRAGEN.copy()
    else:
        pool = [f for f in ALLE_FRAGEN if f['kategorie'] == kategorie]
        if len(pool) < anzahl:
            pool = ALLE_FRAGEN.copy()
    random.shuffle(pool)
    fragen = []
    for i, f in enumerate(pool[:anzahl]):
        frage = f.copy()
        frage['level'] = i + 1
        fragen.append(frage)
    return fragen
