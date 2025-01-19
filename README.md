# AD2Template (English)

`AD2Template` is a Python script that generates files from Jinja2 templates using attributes from Active Directory (AD).

## Features

- Fetches user attributes from Active Directory.
- Renders Jinja2 templates with AD attributes.
- Replace variables in templates file- and folder names with AD attributes.
- Configurable template and output folders.
- Supports cleanup of the output folder before generating new files.

## Use Cases

- Automatically generate email signatures via login script.
- Create personalized documents for users based on AD attributes.
- Generate configuration files for applications using user-specific data from AD.

## Requirements

- Python 3.x
- `pyad` library
- `jinja2` library

## Installation

### Option 1: Clone the repository and install dependencies

1. Clone the repository:
    ```sh
    git clone https://github.com/WinTeach/AD2Template.git
    cd ad2template
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### Option 2: Download precompiled binary

1. Go to the [Releases](https://github.com/WinTeach/AD2Template/releases) page.
2. Download the latest precompiled binary for your operating system.
3. Extract the downloaded file to your desired location.
4. Run the binary directly from the extracted folder.

## Configuration

Modify the `config.ini` file in the project directory for your needs. The configuration file contains the following settings:

```ini
[CONFIG]
# Folder where the output files will be saved
output_folder=%appdata%\Microsoft\Signatures
# Whether to clean up the output folder before generating new files
cleanup_output_folder=false
# Folder where the Jinja2 templates are located
template_folder=templates
# Whether to print Active Directory attributes to the console
print_ad_attributes=false
# Logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_level=ERROR
```

It is possible to use UNC paths and environment variables in the `output_folder` and `template_folder` settings.

## Usage

The script will fetch the AD attributes of the current user, render the Jinja2 templates located in the `templates` 
folder, and write the output files to the specified `output_folder`. Non-template files and folders in the `templates` 
folder will be copied to the output folder as well.
All folder, file, and template names can contain variables (e.g.: #variable#_my_file.txt) that will be replaced by the AD attributes.
Demo Jinja templates, files and folders are available in the `templates` folder.

A fully explained example about using this tool for generating email signatures can be found at [https://winteach.de](https://www.winteach.de/windows-server/active-directory/e-mail-signaturen-aus-ad-daten-generieren-ad2template/) (German only). 

### Option 1: Without precompiled binary
Run the script using the following command:

```sh
python __main__.py
```
### Option 2: With precompiled binary
Run the binary directly.

```sh
ad2template.exe
```
## Logging

The script logs its operations to the console. The log level can be configured in the `config.ini` file.

## Reporting Bugs and Feature Requests

To report bugs or request new features, please use the GitHub [Issues](https://github.com/WinTeach/AD2Template/issues) function.

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the `LICENSE` file for details.

## Author

Tobias Wintrich, [https://winteach.de](https://winteach.de)

---

# AD2Template (Deutsch)

`AD2Template` ist ein Python-Skript, das Dateien aus Jinja2-Vorlagen unter Verwendung von Attributen aus Active Directory (AD) generiert.

## Funktionen

- Ruft Benutzerattribute aus Active Directory ab.
- Rendert Jinja2-Vorlagen mit AD-Attributen.
- Ersetzt Variablen in Datei- und Ordnernamen in Vorlagen durch AD-Attribute.
- Konfigurierbare Vorlagen- und Ausgabeverzeichnisse.
- Unterstützt das Bereinigen des Ausgabeverzeichnisses vor dem Generieren neuer Dateien.

## Anwendungsfälle

- Automatisches Generieren von E-Mail-Signaturen über ein Login-Skript.
- Erstellen personalisierter Dokumente für Benutzer basierend auf AD-Attributen.
- Generieren von Konfigurationsdateien für Anwendungen unter Verwendung benutzerspezifischer Daten aus AD.

## Anforderungen

- Python 3.x
- `pyad` Bibliothek
- `jinja2` Bibliothek

## Installation

### Option 1: Repository klonen und Abhängigkeiten installieren

1. Klone das Repository:
    ```sh
    git clone https://github.com/WinTeach/AD2Template.git
    cd ad2template
    ```

2. Installiere die erforderlichen Python-Pakete:
    ```sh
    pip install -r requirements.txt
    ```

### Option 2: Vorgefertigtes Binary herunterladen

1. Gehe zur [Releases](https://github.com/WinTeach/AD2Template/releases) Seite.
2. Lade das neueste vorgefertigte Binary für dein Betriebssystem herunter.
3. Entpacke die heruntergeladene Datei an den gewünschten Ort.
4. Führe das Binary direkt aus dem entpackten Ordner aus.

## Konfiguration

Passe die `config.ini` Datei im Projektverzeichnis nach deinen Bedürfnissen an. Die Konfigurationsdatei enthält die folgenden Einstellungen:

```ini
[CONFIG]
# Verzeichnis, in dem die Ausgabedateien gespeichert werden
output_folder=%appdata%\Microsoft\Signatures
# Ob das Ausgabeverzeichnis vor dem Generieren neuer Dateien bereinigt werden soll
cleanup_output_folder=false
# Verzeichnis, in dem sich die Jinja2-Vorlagen befinden
template_folder=templates
# Ob Active Directory-Attribute in der Konsole ausgegeben werden sollen
print_ad_attributes=false
# Protokollierungsstufe (z.B. DEBUG, INFO, WARNING, ERROR, CRITICAL)
log_level=ERROR
```

Es ist möglich, UNC-Pfade und Umgebungsvariablen in den Einstellungen `output_folder` und `template_folder` zu verwenden.

## Nutzung

Das Skript ruft die AD-Attribute des aktuellen Benutzers ab, rendert die im `templates`-Ordner 
befindlichen Jinja2-Vorlagen und schreibt die Ausgabedateien in das angegebene `output_folder`.
Nicht-Vorlagen-Dateien und -Ordner im `templates`-Ordner werden ebenfalls in das Ausgabeverzeichnis kopiert.
Alle Ordner-, Datei- und Vorlagennamen können Variablen enthalten (z.B.: #variable#_meine_datei.txt), die durch die AD-Attribute ersetzt werden.
Demo Jinja-Vorlagen, Dateien und Ordner sind im `templates`-Ordner verfügbar.

Ein ausführliches Beispiel zur Verwendung dieses Tools zur Generierung von E-Mail-Signaturen findet ihr unter [https://winteach.de](https://www.winteach.de/windows-server/active-directory/e-mail-signaturen-aus-ad-daten-generieren-ad2template/).

### Option 1: Ohne vorgefertigtes Binary
Führe das Skript mit folgendem Befehl aus:

```sh
python __main__.py
```
### Option 2: Mit vorgefertigtem Binary
Führe das Binary direkt aus.

```sh
ad2template.exe
```
## Protokollierung

Das Skript protokolliert seine Operationen in der Konsole. Die Protokollierungsstufe kann in der `config.ini` Datei konfiguriert werden.

## Fehler melden und Feature-Anfragen

Um Fehler zu melden oder neue Funktionen anzufordern, benutze bitte die GitHub [Issues](https://github.com/WinTeach/AD2Template/issues) Funktion.

## Lizenz

Dieses Projekt ist unter der GNU GENERAL PUBLIC LICENSE lizenziert. Siehe die `LICENSE` Datei für Details.

## Autor

Tobias Wintrich, [https://winteach.de](https://winteach.de)