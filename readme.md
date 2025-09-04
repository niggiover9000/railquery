# RailQuery - RIL100-Suchmaschine

Dieses Suchmaschine dient dazu, die Betriebsstellen zu finden, die sich hinter einer RIL-100-Abkürzung verbergen. Außerdem werden ergänzende Informationen zur Betriebsstelle angezeigt.

![image](https://github.com/user-attachments/assets/ef4c4c75-af26-46e0-a68c-41a0384e9ae5)

Nach einem Klick auf die Betriebsstelle werden weitere Details angezeigt.

![image](https://github.com/user-attachments/assets/8e6cccb4-ed73-49a8-9cc4-b5f824e9f5b8)

## Installation
- Die Datei ".env.example" in ".env" umbenennen
- ID und Secret Key für die API auf https://developers.deutschebahn.com/db-api-marketplace/apis/product/152577 erstellen und in der ".env"-Datei einfügen.
- Die Datei "personal_data.py.example" in "personal_data.py" umbenennen und die persönlichen Daten für das Impressum eintragen.
- Die neueste Excel-Datei für die Datenbank der Betriebsstellen kann unter https://www.dbinfrago.com/web/schienennetz/betrieb/allgemeine-betriebsinformationen/betriebsstellen-12592996 unter "Downloads" gefunden werden. Die Datei wird am Monatsende aktualisiert.
- `docker compose pull && docker compose up -d`

## To Do

- [ ] SEO-Optimierung
- [ ] Mehr Infos aus StaDa darstellen (z.B. Öffnungszeiten)
- [ ] Erklärung der Bahnhofs- und Preiskategorien
- [x] Optimierung der Suchgeschwindigkeit
- [ ] Tooltips durch Accordion ersetzen
- [ ] Tooltips zu Bahnhofs- und Preiskategorie, 3-S-Zentrale und Fahrplanzentrale hinzufügen
- [ ] Infrastrukturregister anbinden (über Koordinaten sollte das möglich sein)
- [ ] Link zur [Abfahrtstafel](https://iris.noncd.db.de) ausblenden wenn nicht verfügbar
- [ ] Definitionen zu Betriebsstellen hinzufügen (z.B. "Abzweigstellen sind Blockstellen der freien Strecke, wo Züge von einer Strecke auf eine andere Strecke übergehen können.")
- [ ] Link zu FAQ einfügen
- [ ] Captcha für Abfragen einfügen
- [ ] [FaSta](https://developers.deutschebahn.com/db-api-marketplace/apis/product/fasta) anbinden.
- [ ] ÖBB-Betriebsstellen hinzufügen
- [ ] personal_data.py durch sauberere Lösung ersetzen

Featurewünsche gerne per GitHub oder per [LinkedIn](https://www.linkedin.com/in/nicolas-bartels/) an mich!