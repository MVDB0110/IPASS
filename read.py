def readFile(mode):  # Functie aanmaken om bestand te lezen
    if mode == 0:  # Als argument 0 is zodat goede downloads worden gelezen
        okdown = []  # List aanmaken waar straks inhoud aan gegeven wordt
        with open('vsftpd.log', 'r') as logfile:  # Open bestand om te lezen
            for line in logfile:  # Elke lijn lezen in de file
                if "OK DOWNLOAD" in line:  # Filteren op goede downloads
                    okdown.append(line)  # Voeg gevonden lijnen tekst toe aan list
        return okdown  # Geef list terug
    if mode == 1:  # Als argument 1 is zodat gefaalde downloads gelezen worden
        faildown = []  # List aanmaken waar straks inhoud aan gegeven wordt
        with open('vsftpd.log', 'r') as logfile:  # Open bestand om te lezen
            for line in logfile:  # Elke lijn lezen in de file
                if "FAIL DOWNLOAD" in line:  # Filteren op gefaalde downloads
                    faildown.append(line)  # Voeg gevonden lijnen tekst toe aan list
        return faildown  # Geef list terug


def okDownload():  # Functie aanmaken voor top 10 downloads
    analyzedSuccess = []  # List aanmaken
    okdown = readFile(0)  # List van goede downloads opvragen
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
    return analyzedSuccess  # Geef totale list terug


def failDownload():  # Functie aanmaken voor onbekende bestanden
    analyzedFail = []
    faildown = readFile(1)
    okdown = readFile(0)
    for linelog in faildown:
        file = linelog.split(', ')[1]
        x = 0
        aanwezig = "0"
        for failedLine in faildown:
            if file in failedLine:
                x += 1
        for success in okdown:
            if file in success:
                aanwezig = "1"
        if aanwezig == "0":
            append = [x, file.replace('"', "")]
            if append not in analyzedFail:
                analyzedFail.append(append)
    analyzedFail.sort(reverse=True)
    return analyzedFail


def formatText(mode):
    if int(mode) == 0:
        okDown = okDownload()[:10]
        formattedText = "{:#^85s}\n".format("Top 10")
        formattedText += "{:10} {}\n".format("Pogingen", "Bestand")
        for line in okDown:
            formattedText += "{:<10} {}\n".format(line[0], line[1])
        print(formattedText)

    elif int(mode) == 1:
        failDown = failDownload()
        formattedText = "{:#^85s}\n".format("Niet gevonden bestanden")
        formattedText += "{:10} {}\n".format("Pogingen", "Bestand")
        for line in failDown:
            formattedText += "{:<10} {}\n".format(line[0], line[1])
        print(formattedText)


print("Selecteer de modus waarin het script opereert.\n")
print("0 voor top 10 downloads.")
print("1 voor mislukte downloads met het aantal keren dat het opgevraagd is.\n")
mode = input("Geef modus op: ")
modes = ('0', '1', '2')
while mode not in modes:
    mode = input("Geef modus op: ")

print("")
formatText(int(mode))
input("\nDruk op ENTER om af te sluiten.")
