# ASF-NLogWulf v0.1a

ASF-NLogWulf ist eine Erweiterung für ArchiSteamFarm: einheitliche NLog-Ausgabe, deutsche Normalisierung bekannter Meldungen, konfigurierbare Retrowave-Farben für Konsole/WebUI und optionale IRC-, Discord-, Telegram- und Nova-Wulf-Relays. Das Projekt befindet sich in der Alpha-Phase und ist ein unabhängiges Drittanbieterplugin.

## Kompatibilität und Installation

Zielversion ist **ASF-generic 6.3.11.7** mit **.NET 10 Runtime**; der Linux-Ladesmoke lief mit .NET **10.0.14**. Für das fertige Plugin ist kein SDK erforderlich. ASF und seine Laufzeitabhängigkeiten werden getrennt installiert.

1. ASF kontrolliert beenden und die bestehende Installation sichern.
2. `NLogWulf-v0.1a.zip` und `SHA512SUMS` aus den Assets desselben [v0.1a-Releases](https://github.com/n-e-o-w-u-l-f/ASF-NlogWulf/releases/tag/v0.1a) in ein gemeinsames Verzeichnis laden.
3. Die SHA-512-Prüfsumme vor dem Entpacken vergleichen. Unter Linux im Downloadverzeichnis:

   ```sh
   sha512sum --check SHA512SUMS
   ```

   Unter PowerShell den Wert mit `SHA512SUMS` vergleichen:

   ```powershell
   (Get-FileHash ./NLogWulf-v0.1a.zip -Algorithm SHA512).Hash
   ```

4. Beide Dateien `NLogWulf.dll` und `NLogWulf.deps.json` in ein eigenes Unterverzeichnis `plugins/NLogWulf` der ASF-Installation entpacken. Bei einem Update die bisherige NLogWulf-Kopie ersetzen und doppelte Plugin-DLLs vermeiden. Das ZIP enthält keine ASF-/NLog-/OpenAPI-Host-DLLs.
5. ASF starten und die erfolgreiche NLogWulf-Lademeldung prüfen. Das Plugin benötigt Schreibrecht auf sein eigenes Verzeichnis, um die WebUI-Overlaydateien zu erzeugen. Relayziele benötigen eine gesonderte Konfiguration; der Ladesmoke verwendete keine Relay-Zugangsdaten.

## Nachgewiesener Stand

Am 16.11.2026 bestanden unter Linux/x64 die Übersetzungsprüfung, Debug-/Release-Builds, Smoke-Tests mit 100.000 Ereignissen sowie Publish-, ZIP- und Hashprüfungen. Die finale Buildprüfung meldete keine Warnungen oder Fehler; der damalige NuGet-Audit keine bekannten verwundbaren Pakete.

Die lokale Installation wurde über den installierten Launcher als unprivilegierter Benutzer mit isoliertem, kontenfreiem Zustand geprüft: NLogWulf und 53 weitere Plugins luden gemeinsam auf ASF-generic 6.3.11.7 / .NET 10.0.14 bis zur Initialisierung ohne Bots, mit 0 ERROR-Zeilen, 0 Exceptions und kontrolliertem Exit 0. Deutsche ASF-/NLogWulf-Ausgabe, ANSI-freies Dateilog und generierte WebUI-Overlaydateien wurden nachgewiesen.

Der Test belegt keine Steam-Anmeldung, Handels-/Kauf-/Authenticatorfunktionen, späteren Botbefehle, PeriodicGC-Zyklen, Browserdarstellung, IPC- oder Relayzustellung. Fremdplugintexte können unübersetzt bleiben. Windows wurde in diesem Durchlauf nicht ausgeführt. Details und bekannte Grenzen stehen in den [Release-Notes](Release-Notes.md).

## Paket und Prüfsumme

`NLogWulf-v0.1a.zip`: 120.384 Bytes, genau zwei Dateien. SHA-512:

```text
4e23690647bdfa2ef3d81346eb532e1ac7db1ff87340c992c0f0fdd02d0a5ff466af2d508393598b2d114288c41f64e77e02f367efd591bf2f545a2ef431d223
```

Metadatenkorrektur: Die geprüfte DLL trägt exakt die Informationsversion `0.1a`, ohne interne Quellreferenz. Der korrigierte Kandidat wurde neu gebaut, gezielt installiert und erneut mit 54 Plugins geladen. Begrenzte Nachprüfung und Veröffentlichung stehen noch aus.

Assemblyversion: `0.1.0.0`; Releasebezeichnung: `v0.1a` (Alpha). Lizenz: [Apache-2.0](LICENSE.txt).
