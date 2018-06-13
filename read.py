import sys  # Importeer SYS voor het stoppen van het script wanneer configuratie niet klopt van het ini bestand
import configparser  # Ini file parser
import argparse  # Het doorgeven van command line arguments


def readFile(mode):  # Functie aanmaken om bestand te lezen
    global log  # Globale variabele gebruiken in plaats van lokale
    global filenotfounderror
    loglist = []  # List aanmaken waar straks inhoud aan gegeven wordt
    try:
        with open(str(log), 'r') as logfile:  # Open bestand om te lezen
            if mode == 0:  # Als argument 0 is zodat goede downloads worden gelezen
                for line in logfile:  # Elke lijn lezen in de file
                    if "OK DOWNLOAD" in line:  # Filteren op goede downloads
                        loglist.append(line)  # Voeg gevonden lijnen tekst toe aan list
            if mode == 1:  # Als argument 1 is zodat gefaalde downloads gelezen worden
                for line in logfile:  # Elke lijn lezen in de file
                    if "FAIL DOWNLOAD" in line:  # Filteren op gefaalde downloads
                        loglist.append(line)  # Voeg gevonden lijnen tekst toe aan list

    except FileNotFoundError:
        print(filenotfounderror + "\n")
        input("Druk op ENTER om te sluiten.")
        sys.exit()  # Afsluiten als het bestand niet gevonden kan worden
    return loglist  # Geef list terug


def okDownload():  # Functie aanmaken voor top 10 downloads
    global indexerror
    analyzedSuccess = []  # List aanmaken
    okdown = readFile(0)  # List van goede downloads opvragen
    try:
        for line in okdown:  # Elke lijn lezen van de goede downloads
            file = line.split(', ')[1]  # Haal de locatie van het bestand uit de lijn
            x = 0  # Statement voor tellen

            for download in okdown:  # Elke lijn lezen van de goede downloads om duplicaten te vinden
                if file in download:  # Filteren voor duplicaten
                    x += 1  # Als er een duplicaat is tel je één bij statement op

            append = [x, file.replace('"', "")]  # Maak list aan om toe te voegen

            if append not in analyzedSuccess:  # Kijk of list al toegevoegd is aan de list
                analyzedSuccess.append(append)  # Voeg statement met bestandslocatie toe als list aan de list

        analyzedSuccess.sort(reverse=True)  # Sorteer list zodat het aflopend is

    except IndexError:
        print(indexerror + "\n")
        input("Druk op ENTER om te sluiten.")
        sys.exit()  # Afsluiten als de gelezen lijnen van het bestand niet kunnen geanalyseerd worden door dit script.

    return analyzedSuccess  # Geef totale lijst terug


def failDownload():  # Functie aanmaken voor onbekende bestanden
    global indexerror
    analyzedFail = []  # Lijst aanmaken
    faildown = readFile(1)  # Lijst van gefaalde downloads opvragen
    okdown = readFile(0)  # Lijst van goede downloads opvragen
    try:
        for linelog in faildown:  # Elke lijn lezen van gefaalde downloads
            file = linelog.split(', ')[1]  # Haal de locatie van het bestand uit de lijn
            x = 0  # Statement voor tellen
            aanwezig = "0"  # Statement om lijn te identificeren in lijst van goede downloads

            for failedLine in faildown:  # Optellen bij tel statement
                if file in failedLine:  # Wanneer bestand voorkomt in de lijn
                    x += 1  # Een optellen

            for success in okdown:  # Voor elke lijn in goede downloads
                if file in success:  # Wanneer bestand voorkomt in lijst van goede downloads
                    aanwezig = "1"  # Zet aanwezigheid naar 1

            if aanwezig == "0":  # Als bestandslocatie niet aanwezig is in goede downloads
                append = [x, file.replace('"', "")]  # Voeg lijn toe aan onbekende bestanden lijst

                if append not in analyzedFail:  # Als lijn niet aanwezig is
                    analyzedFail.append(append)  # Voeg lijn toe

        analyzedFail.sort(reverse=True)  # Sorteer op aflopende downloads

    except IndexError:
        print(indexerror + "\n")
        input("Druk op ENTER om te sluiten.")
        sys.exit()  # Afsluiten als de gelezen lijnen van het bestand niet kunnen geanalyseerd worden door dit script.

    return analyzedFail  # Geef lijst terug


def formatText(mode):  # Functie aanmaken
    if int(mode) == 0:  # Als modus voor top 10 is
        global topdownloads  # Globale variabele gebruiken in plaats van lokale
        okDown = okDownload()[:topdownloads]  # Vraag de eerste 10 van gelukte downloads op
        formattedText = "{:#^85s}\n".format("Top 10")  # Tekst opmaken
        formattedText += "{:10} {}\n".format("Pogingen", "Bestand")  # Tekst opmaken
        for line in okDown:  # Voor elke gelukte downloads
            formattedText += "{:<10} {}\n".format(line[0], line[1])  # Voeg opgemaakte tekst toe aan geheel
        print(formattedText)  # Print uiteindelijke top 10

    elif int(mode) == 1:  # Als modus voor gefaalde downloads is
        failDown = failDownload()  # Vraag lijst op waarin onbekende bestanden staan
        formattedText = "{:#^85s}\n".format("Niet gevonden bestanden")  # Tekst opmaken
        formattedText += "{:10} {}\n".format("Pogingen", "Bestand")  # Tekst opmaken
        for line in failDown:  # Voor elk onbekend bestand
            formattedText += "{:<10} {}\n".format(line[0], line[1])  # Voeg opgemaakte tekst toe aan het geheel
        print(formattedText)  # Print onbekende bestanden


config = configparser.ConfigParser()  # Configparser aanroepen
config.read('conf.ini')  # Configparser configfile laten lezen
try:
    log = config['MAIN']['log']  # Logfile locatie proberen op te vragen
except:
    print("In het configfile staat geen verwijzing naar een bestand.\n")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als logfile niet opgegeven is

try:
    topdownloads = config['MAIN']['topdownloads']  # Topdownloads proberen op te vragen
    topdownloads = int(topdownloads)  # Proberen om te zetten naar getal
except:
    print("In het configfile staat geen getal voor hoe groot de top downloads moet zijn.\n")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als omzetten of opvragen niet lukt.

try:
    filenotfounderror = config['TEXT']['filenotfounderror']  # File not found error tekst opvragen
except:
    print("In het configuratiebestand staat geen string bij filenotfounderror\n")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als tekst niet gevonden kan worden

try:
    indexerror = config['TEXT']['indexerror']  # Index error tekst opvragen
except:
    print("In het configuratiebestand staat geen string bij indexerror\n")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als tekst niet gevonden kan worden


parser = argparse.ArgumentParser(description='Selecteer de modus waarin het script opereert.\n', add_help=True)  # Argumentparser aanroepen
parser.add_argument('--topdownloads', action='store_true', default=True,
                    dest='mode', help='Zie de topdownloads')  # Argument van topdownloads toevoegen

parser.add_argument('--ontbrekendebestanden', action='store_false', default=False,
                    dest='mode', help='Zie de ontbrekende bestanden')  # Argument van ontbrekendebestanden toevoegen

args = parser.parse_args()  # Doorgegeven argumenten opvragen

if args.mode == True:  # Als niets is doorgegeven of --topdownloads
    formatText(0)  # Laat top downloads zien

if args.mode == False:  # Als --ontbrekendebestanden is doorgegeven
    formatText(1)  # Laat ontbrekende bestanden zien

input("\nDruk op ENTER om af te sluiten.")  # Als script klaar is pas sluiten wanneer ENTER is ingedrukt
