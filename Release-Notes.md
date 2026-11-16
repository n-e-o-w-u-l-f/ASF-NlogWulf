# ASF-NLogWulf v0.1a – Release-Notes

Alpha-Version für **ASF-generic 6.3.11.7 / .NET 10**. Stand der Verifikation: 16.11.2026.

## Umfang

- Einheitliches NLog-Layout für Konsole und ASF-Standardprotokoll, deutsche Normalisierung bekannter Meldungen und konfigurierbare Retrowave-Farben.
- Generiertes WebUI-Overlay und optionale gefilterte IRC-, Discord-, Telegram- und Nova-Wulf-Relays.
- Korrigierte Redaktion von Authorization-Werten mit Bearer-/Bot-Schema; Regressionen für Geheimnisentfernung und Kontextbewahrung.
- Korrigierte binäre Informationsversion: exakt `0.1a`, ohne unbeabsichtigten Quellrevisionsanhang; Regression prüft die tatsächlichen DLL-/ZIP-Metadaten.
- Paket ausschließlich mit `NLogWulf.dll` und `NLogWulf.deps.json`; keine Hostabhängigkeiten enthalten. Die [Installationsanleitung](README.md#kompatibilität-und-installation) setzt ASF-generic 6.3.11.7 und die .NET-10-Laufzeit voraus.

## Verifikation

Die Linux/x64-Prüfung mit SDK 10.0.403 bestand Übersetzungsvalidierung, Debug-/Release-Builds ohne finale Warnungen/Fehler, Smoke-Tests einschließlich 100.000 Ereignissen sowie Publish-/ZIP-/SHA-512-Gates. SDK 10.0.114 reicht für den verifizierten ASF-Quellbuild nicht aus; Anwender des fertigen Plugins benötigen nur die Laufzeit. Der NuGet-Audit meldete am Prüftag keine bekannten verwundbaren Pakete; dies ist eine zeitpunktgebundene Aussage.

Die lokale Installation und ein kontrollierter Start über den installierten Launcher als unprivilegierter Benutzer mit isoliertem Zustand luden **54 Plugins**, darunter NLogWulf, gemeinsam auf **ASF-generic 6.3.11.7 / .NET 10.0.14**. Initialisierung bis zum erwarteten Zustand ohne Bots, **0 ERROR-Zeilen / 0 Exceptions**, kontrollierter Exit 0. Deutsche ASF-/NLogWulf-Konsole, ANSI-freies Dateilog und generierte WebUI-Overlaydateien wurden bestätigt. Source-/Build- und Installationsstufen erhielten unabhängige Spec-/Qualitätsreviews ohne blockierende Befunde; die Metadatenkorrektur wurde neu gebaut, gezielt installiert und mit allen 54 Plugins erneut geprüft. Die unabhängige begrenzte Nachprüfung hat die Metadatenkorrektur ohne neue blockierende Befunde bestätigt.

Die sechs ausdrücklich geprüften offiziellen Komponenten PeriodicGC, SignInWithSteam, ItemsMatcher, MobileAuthenticator, Monitoring und SteamTokenDumper luden jeweils als 6.3.11.7. Die 54 Plugins sind ein getesteter Katalogsnapshot, kein Gesamtverzeichnis aller GitHub-Plugins und kein Bestandteil dieses ZIPs. Elf Pluginpakete wurden ausgeschlossen: neun wegen entfernter ASF-Typen und ASFBatchCmd/ASFDailyExecute wegen Humanizer-Ladefehlern. Drei Nichtplugins wurden getrennt gezählt.

## Grenzen

Keine funktionale Abnahme von Steamkonten, Anmeldung, Handel, Kauf, Authenticator, späteren Botbefehlen, PeriodicGCs 60-Sekunden-Zyklus, Browserdarstellung, IPC oder Relayzustellung. Der Ladesmoke beweist keine erst später verwendeten API-Signaturen. Es wurden keine Konten oder Relay-Zugangsdaten eingerichtet.

Referenzversionswarnungen sowie deaktivierte ASFEnhance-Teilfunktionen ohne EULA-Zustimmung bleiben sichtbar. Einzelne Fremdpluginmeldungen bleiben englisch oder chinesisch. Für Windows liegt aus diesem Durchlauf keine Ausführung vor. Die konservative Geheimnisredaktion kann bei Nicht-Auth-Schlüsseln und Einzelwortwerten `Bot`/`Bearer` zusätzlich ein nachfolgendes Nichtgeheimniswort entfernen; dieser kleine Kontextverlust ist bekannt, ohne festgestellten Credential-Leak.

## Artefakt

`NLogWulf-v0.1a.zip`, 120.384 Bytes; Assemblyversion `0.1.0.0`, Alpha `v0.1a`. SHA-512 wie in `SHA512SUMS`:

```text
4e23690647bdfa2ef3d81346eb532e1ac7db1ff87340c992c0f0fdd02d0a5ff466af2d508393598b2d114288c41f64e77e02f367efd591bf2f545a2ef431d223
```

Lizenz: [Apache-2.0](LICENSE.txt). ASF und andere Plugins werden mit diesem Paket nicht mitgeliefert.
