#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

# Dateiname der .p12-Datei abfragen
read -p "Dateiname der .p12-Datei: " P12_FILE
if [ ! -f "$P12_FILE" ]; then
    echo "Datei '$P12_FILE' nicht gefunden." >&2
    exit 1
fi

# Passwort abfragen (ohne Anzeige)
read -s -p "Passwort für $P12_FILE: " P12_PASS
echo
export P12_PASS

# Extrahieren Sie das Zertifikat (.crt.pem Datei)
openssl pkcs12 -in "$P12_FILE" -clcerts -nokeys -passin env:P12_PASS -out MobilithekCertificate.crt.pem
# Extrahieren Sie den privaten Schlüssel (.key.pem Datei)
openssl pkcs12 -in "$P12_FILE" -nocerts -nodes -passin env:P12_PASS -out MobilithekPrivatekey.key.pem

unset P12_PASS
echo "Fertig: MobilithekCertificate.crt.pem und MobilithekPrivatekey.key.pem erstellt."
