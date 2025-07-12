art = {
    "Abzw": "Abzweigstelle",
    "Anst": "Anschlussstelle",
    "Awanst": "Ausweichanschlussstelle",
    "Bf": "Bahnhof",
    "Bft": "Bahnhofsteil",
    "Bft Abzw": "Bahnhofsteil Abzweigstelle",
    "Bk": "Blockstelle",
    "Bush": "Bushaltestelle",
    "Dkst": "Deckungsstelle",
    "Est": "Einsatzstelle für Zugpersonal",
    "Fwst": "Fernwirkstelle",
    "Gp": "Grenzpunkt",
    "Hp": "Haltepunkt",
    "LGr": "Landesgrenze",
    "LW": "Laufweg",
    "Museum": "Museumsbahnhof",
    "PDGr": "Produktionsdurchführungsgrenze",
    "RBGr": "Regionalbereichsgrenze",
    "Sbk": "Selbsttätige Blockstelle",
    "Schstr": "Schutzstrecke",
    "Slst": "Schiffslandestelle",
    "Sp": "Schaltposten",
    "Strw": "Streckenwechsel",
    "Tp": "Tarifpunkt",
    "Urw": "Umrichterwerk",
    "Uw": "Unterwerk",
    "Üst": "Überleitstelle",
    "Zes": "Zentralschaltstelle"
}

region = {
    "A": "Hamburg",
    "B": "Berlin",
    "C": "Ausländische Örtlichkeiten von Schienengüterverkehrsunternehmen",
    "D": "Dresden",
    "E": "Essen",
    "F": "Frankfurt",
    "H": "Hannover",
    "I": "Ortsfeste und ortsveränderliche Energieanlagen der 16,7-Hertz-Energieversorgung",
    "J": "Ausländische Örtlichkeiten von Schienengüterverkehrsunternehmen",
    "K": "Köln",
    "L": "Halle",
    "M": "München",
    "N": "Nürnberg",
    "O": "Ausländische Örtlichkeiten in Ländern, die vollständig in das Europäische Fahrplanzentrum eingebunden sind",
    "P": "Ausländische Örtlichkeiten in Ländern, die vollständig in das Europäische Fahrplanzentrum eingebunden sind",
    "Q": "Örtlichkeiten von 50-Hertz-Anlagen",
    "R": "Karlsruhe",
    "S": "Saarbrücken",
    "T": "Stuttgart",
    "U": "Erfurt",
    "V": "Tankanlagen für Verbrennungsfahrzeuge",
    "W": "Schwerin",
    "X": "Ausland",
    "Y": "Streckenwechsel",
    "Z": "Ausland"}

sonderart = {
    "NE-": "Nichtbundeseigene Eisenbahn: ",
    "vp-": "verpachtet, "
}

''' 
Quelle: https://www.deutschebahn.com/resource/blob/5667426/c5a6eb32c2b78dc5b6c193e43add96ec/INBP_gueltig-ab-01-01-2021-data.pdf
Niedrigste Kategorie: 7
Höchste Kategorie: 1
Bahnhöfe einer höheren Kategorie weisen die Leistungen der niedrigeren Kategorien auf.
'''

bahnhofskategorien = {
    6: ["Sitzgelegenheit", "Wetterschutz"],
    5: ["Bahnhofsuhr/Zeitangabe", "Dynamische Reisendeninformation (visuell und/oder akustisch) mit Informationen zu Fahrplanabweichungen"],
    4: [],
    3: ["Dynamische Reisendeninformation (visuell und/oder akustisch) mit Informationen zum Fahrplan"],
    2: ["Servicemitarbeiter (auch zeitweise)", "Bahnsteigabschnittsmarkierung"],
    1: ["DB Information"]

}

betriebszustände = ["Planung", "Betrieb", "a.B. (außer Betrieb)", "ehemals", "Studie"]