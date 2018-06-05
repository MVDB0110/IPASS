import sys
import configparser


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
        print(filenotfounderror)
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
        print(indexerror)
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
        print(indexerror)
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
    print("In het configfile staat geen verwijzing naar een bestand.")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als logfile niet opgegeven is

try:
    topdownloads = config['MAIN']['topdownloads']  # Topdownloads proberen op te vragen
    topdownloads = int(topdownloads)  # Proberen om te zetten naar getal
except:
    print("In het configfile staat geen getal voor hoe groot de top downloads moet zijn.")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als omzetten of opvragen niet lukt.

try:
    filenotfounderror = config['TEXT']['filenotfounderror']  # File not found error tekst opvragen
except:
    print("In het configuratiebestand staat geen string bij filenotfounderror")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als tekst niet gevonden kan worden

try:
    indexerror = config['TEXT']['indexerror']  # Index error tekst opvragen
except:
    print("In het configuratiebestand staat geen string bij indexerror")
    input("Druk op ENTER om te sluiten.")
    sys.exit()  # Afsluiten als tekst niet gevonden kan worden


print("Selecteer de modus waarin het script opereert.\n")  # Instructie tekst
print("0 voor top " + str(topdownloads) + " downloads.")  # Instructie tekst
print("1 voor mislukte downloads met het aantal keren dat het opgevraagd is.\n")  # Instructie tekst
mode = input("Geef modus op: ")  # Instructie tekst
modes = ('0', '1')  # Tuple voor beschikbare modus

while mode not in modes:  # Als modus niet beschikbaar is
    mode = input("Geef modus op: ")  # Geef vraag opnieuw weer

print("")  # Opmaak
formatText(int(mode))  # Voer script uit met opgegeven modus
input("\nDruk op ENTER om af te sluiten.")  # Als script klaar is pas sluiten wanneer ENTER is ingedrukt
