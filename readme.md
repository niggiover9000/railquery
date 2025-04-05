# Bahninfo - RIL 100

Dieses Tool dient dazu, die Betriebsstellen zu finden, die sich hinter einer RIL-100-Abkürzung verbergen.
![image](https://github.com/user-attachments/assets/ef4c4c75-af26-46e0-a68c-41a0384e9ae5)

Nach einem Klick die Betriebsstelle werden weitere Details angezeigt.

![image](https://github.com/user-attachments/assets/8e6cccb4-ed73-49a8-9cc4-b5f824e9f5b8)

## Installation
- Die Datei ".env.example" in ".env" umbenennen
- ID und Secret Key für die API auf https://developers.deutschebahn.com/db-api-marketplace/apis/product/152577 erstellen und in der ".env"-Datei einfügen.
- Die neueste Excel-Datei für die Datenbank der Betriebsstellen kann unter https://www.dbinfrago.com/web/schienennetz/betrieb/allgemeine-betriebsinformationen/betriebsstellen-12592996 unter "Downloads" gefunden werden. Die Datei wird am Monatsende aktualisiert.
- `docker compose pull && docker compose up -d`

## To Do
- [ ] Debug-Mode remote deaktivieren
- [ ] Port-Settings in .env
- [ ] Wenn möglich Host-Settings (URL) in .env
- [ ] Karte in Website einbinden
- [ ] Spendenlink hinzufügen
- [ ] Werbung einbetten
- [ ] Link zu FAQ einfügen
- [ ] Link zu Github einfügen
- [ ] Abfragen, ob Gleisplan existiert, ansonsten Button ausblenden

Featurewünsche gerne per GitHub oder per LinkedIn an mich!