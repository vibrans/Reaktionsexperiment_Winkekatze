# This Python file uses the following encoding: utf-8
from psychopy import gui
import os
import sys
from psychopy import visual, event, core
import time
import io
import copy
import random
##############################################################################
# persönliche Daten in Datei packen
def DictAlsCsvSpeichern(bib, ID, Spaltentrennzeichen):
    info_Datei = "{}".format(ID) + u"_info" + u".csv"
    if os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + u"/Daten/" + info_Datei):
        sys.exit(u"Datei " + info_Datei + u" exisiert bereits!")
    pfad = os.path.dirname(os.path.abspath(__file__)) + "/Daten/" + info_Datei
    with open(pfad, 'w') as f:
        f.write(Spaltentrennzeichen.join(bib.keys()))
        f.write('\n')
        eintraege = [bib[i] for i in bib.keys()]
        f.write((Spaltentrennzeichen.join(eintraege)).encode('utf-8'))

# Erfragung Personendaten
# für diesen Rechner monitor="AcerMonitor" einstellen
def Personendaten_erfragen():
    win_background = visual.Window([1366,768], monitor="testMonitor", color='#000000', units='norm', colorSpace='rgb', fullscr=False, allowGUI=True)
    Dialog = gui.Dlg(title=u"Willkommen zum Experiment")
    Dialog.addField('ID:')
    Dialog.addField('Alter:')
    Dialog.addField('Gender:')
    Dialog.addField('Studienfach:')

    ok_data = Dialog.show()
    if Dialog.OK:
        print(Dialog.data)
    else:
        print('Abbruch')
        
    ID = int(Dialog.data[0])
    alter = Dialog.data[1]
    geschlecht = Dialog.data[2]
    fach = Dialog.data[3]

    info = {"ID": unicode(str(ID).encode('utf-8'), 'utf-8'), u"age": alter, u"gender": geschlecht, u"subject": fach}
    DictAlsCsvSpeichern(info, ID, ";")
    return win_background, ID


win_background, ID = Personendaten_erfragen()
#ID = 1
win = visual.Window([1366,768], monitor="testMonitor", color="#000000", units='norm', colorSpace='rgb', fullscr=False, allowGUI=False)
win_background.close()

###########################################################################
# Variablen, Objekte

#Pfeil_nach_links = visual.ShapeStim(win, units="norm", pos=[0, 0], vertices=[(-0.1, 0), (-0.03, 0.04), (-0.03, 0.02), (0.1, 0.02), (0.1, -0.02), (-0.03, -0.02), (-0.03, -0.04)])
Pfeil_nach_links = visual.ShapeStim(win, units="norm", pos=[0, 0], vertices=[(-0.03, 0), (0, 0.035), (-0.02, 0.005), (0.03, 0.005), (0.03, -0.005), (-0.02, -0.005), (0, -0.035)])
#Pfeil_nach_rechts = visual.ShapeStim(win, units="norm", pos=[0, 0], vertices=[(0.2, 0), (0.03, 0.04), (0.03, 0.02), (-0.2, 0.02), (-0.2, -0.02), (0.03, -0.02), (0.03, -0.04)])

linkesLabel = visual.TextStim(win, text=u"gelb", height=0.08, color='#FFFFFF', colorSpace='rgb', pos=[-0.7, -0.7])
rechtesLabel = visual.TextStim(win, text=u"blau", height=0.08, color='#FFFFFF', colorSpace='rgb', pos=[0.7, -0.7])

fixationskreuz = visual.TextStim(win, text=u"+", colorSpace='rgb', color='#FFFFFF', pos=[0, 0])

Z_Fixkreuz = 0.4
Z_nach_Fixkreuz = 0
keys =  ['space', 'escape']
limit = 1000        # in ms

########################################################################################################


# Reaktionszeitdaten in Datei packen
def ListeAlsCsvSpeichern(Liste, ID, Spaltentrennzeichen):
    RT_Datei = "{}".format(ID) + u"_RT" + u".csv"
    pfad = os.path.dirname(os.path.abspath(__file__)) + "/Daten/" + RT_Datei
    with open(pfad, 'a') as f:
        keyListe = Liste[0].keys()
        f.write(Spaltentrennzeichen.join(keyListe))
        f.write('\n')
        for j in xrange(len(Liste)):
            eintraege = []
            for k in xrange(len(keyListe)):
                eintraege.append(unicode(str(Liste[j][keyListe[k]]), 'utf-8'))
                #f.write(str(Liste[j][keyListe[k]]) + Spaltentrennzeichen)
            #print type(eintraege[6])
            f.write((Spaltentrennzeichen.join(eintraege)).encode('utf-8'))
            f.write('\n')
    f.close()


# Reaktionszeitdaten zur Datei hinzufügen ohne Spaltennamen
def ListeZuCsvHinzufuegen(Liste, ID, Spaltentrennzeichen):
    RT_Datei = "{}".format(ID) + u"_RT" + u".csv"
    pfad = os.path.dirname(os.path.abspath(__file__)) + "/Daten/" + RT_Datei
    with open(pfad, 'a') as f:
        keyListe = Liste[0].keys()
        for j in xrange(len(Liste)):
            eintraege = []
            for k in xrange(len(keyListe)):
                eintraege.append(unicode(str(Liste[j][keyListe[k]]), 'utf-8'))
                #f.write(str(Liste[j][keyListe[k]]) + Spaltentrennzeichen)
            #print type(eintraege[6])
            f.write((Spaltentrennzeichen.join(eintraege)).encode('utf-8'))
            f.write('\n')
    f.close()

###########################################################################
# Funktionen
def zeige_Botschaft(txt, keys=['space', 'escape'], c = "#FFFFFF", pos=[0, 0], Wartezeit=0.1):
    Botschaft = visual.TextStim(win, text=txt, height=0.08, wrapWidth=1.2, color=c, colorSpace='rgb')       #für diesen Rechner: wrapWidth=1.5
    Botschaft.draw()
    win.flip()
    core.wait(Wartezeit)            # Lesezeit garantieren
    if event.waitKeys(keyList=keys)[0] == 'escape':
        core.quit()
    win.flip()


def Stimuligenerierung(Pfad):
    dict = {u'ID': None, u'Trial': None, u'arrow_color': None, u'arrow_direction': None, u'condition': None, u'blockorder': None, u'cresp': None,
    u'RT': None,  u'accuracy': None, u'compatibility': None, u'responsecolor': None, u'duration_fixation': 400}
    Trials = []
    i = True
    with io.open(Pfad, 'r', encoding = 'utf-8') as Stimuliliste:
        for line in Stimuliliste:
            if i == True:
                i = False
                continue
            splitline = line.split(";")
            Kopie = copy.deepcopy(dict)
            Kopie[u'arrow_color'] = splitline[1][1:-1]
            Kopie[u'arrow_direction'] = splitline[2][1:-2]
            Trials.append(Kopie)
            random.shuffle(Trials)
    return Trials

# Rückmeldung für Inakkuratesse sowie für zu langsam und inakkurat sowie für schnell genug und inakkurat
def zeige_inakkurat(win, keys=['escape'], l=linkesLabel, r=rechtesLabel, Pfeil=Pfeil_nach_links):
    inakkurat = visual.TextStim(win, text=u'falsche Reaktion!', color='#cc0000', colorSpace='rgb', height=0.12, pos=(0, -0.2))
    Botschaft = visual.TextStim(win, text=u'nur auf {farbe} Pfeile reagieren!!!'.format(farbe="gelbe" if responsecolor=="yellow" else "blaue"), height=0.08, wrapWidth=1.5, color='#cc0000', colorSpace='rgb', pos=[0, -0.5])
    Pfeil.draw()
    inakkurat.draw()
    Botschaft.draw()
    win.flip()
    Tastendruck = event.waitKeys(maxWait=2, keyList=keys)
    if Tastendruck:
        if Tastendruck[0]=='escape':
            core.quit()


# Rückmeldung für zu langsam und korrekt
def zeige_zu_langsam(win, l=linkesLabel, r=rechtesLabel, Pfeil=Pfeil_nach_links, keys=['escape']):
    langsam = visual.TextStim(win, text=u'zu langsam', color='#cc0000', colorSpace='rgb', height=0.12, pos=(0, -0.2))
    Pfeil.draw()
    langsam.draw()
    win.flip()
    Tastendruck = event.waitKeys(maxWait=2, keyList=keys)
    if Tastendruck:
        if Tastendruck[0]=='escape':
            core.quit()

# Rückmeldung für verpasste Reaktion in go-Trials
def verpasste_Reaktion(win, keys=['escape', 'space']):
    verpasst = visual.TextStim(win, text=u'Fehler!\nDu hättest reagieren müssen!\n\n\nWeiter mit der Leertaste', color='#cc0000', colorSpace='rgb', height=0.12, pos=(0, -0.2))
    verpasst.draw()
    win.flip()
    Tastendruck = event.waitKeys(keyList=keys)
    if Tastendruck:
        if Tastendruck[0]=='escape':
            core.quit()




###############################################################################


def Ablauf_Uebung(liste):
    i = 1
    for d in liste:
        d[u'ID'] = ID        # Ergänzung ID
        d[u'condition'] = condition      # Ergänzung, dass Übung
        d[u'blockorder'] = u"practise"
        d[u'Trial'] = i
        i = i+1
        d[u'cresp'] = responsecolor
        Pfeil_nach_links.setOri(0)
        fixationskreuz.draw()
        win.flip()
        core.wait(Z_Fixkreuz)
        win.flip()
        if d[u'arrow_color']==u'yellow':
            Pfeil_nach_links.setLineColor('#FFFF00')
            Pfeil_nach_links.setFillColor('#FFFF00')
        elif d[u'arrow_color']==u'blue':
            Pfeil_nach_links.setLineColor('#0066CC')
            Pfeil_nach_links.setFillColor('#0066CC')
        if d[u'arrow_direction']==u'right':
            Pfeil_nach_links.setOri(240)
        elif d[u'arrow_direction']==u'left':
            Pfeil_nach_links.setOri(-60)
        if d[u'arrow_direction']==u'right' and d[u'arrow_color']==d[u'cresp'] or d[u'arrow_direction']==u'left' and d[u'arrow_color']!=d[u'cresp']:
            d[u'compatibility'] = u"compatible"
        else:
            d[u'compatibility'] = u"incompatible"
        Pfeil_nach_links.draw()
        win.flip()
        timer = core.Clock()
        Antwort = event.waitKeys(maxWait=1.5, keyList=['space', 'escape'], timeStamped=timer)
        if Antwort:
            Pfeil_nach_links.setLineColor('#FFFFFF')
            Pfeil_nach_links.setFillColor('#FFFFFF')
            Pfeil_nach_links.draw()
            win.flip()
            d[u'responsecolor'] = d[u'arrow_color']
            if Antwort[0][0] == 'escape':
                core.quit()
            d[u'RT'] = round(Antwort[0][1]*1000)
            if d[u'arrow_color']==d['cresp']:
                d['accuracy'] = 1
                if d[u'RT'] > limit:
                    zeige_zu_langsam(win)
            else:
                d[u'accuracy'] = 0
                zeige_inakkurat(win)
            if d[u'RT']<1500:
                core.wait((1500-d['RT'])/1000)
        elif d[u'arrow_color']==d['cresp']:
            d[u'accuracy'] == 0
            verpasste_Reaktion(win)
        else:
            d[u'accuracy'] = 1
        win.flip()
    return liste

def Ablauf_Experiment(liste):
    i = 1
    for d in liste:
        d[u'ID'] = ID        # Ergänzung ID
        d[u'condition'] = condition
        d[u'blockorder'] = blockreihenfolge
        d[u'Trial'] = i
        i = i+1
        d[u'cresp'] = responsecolor
        Pfeil_nach_links.setOri(0)
        fixationskreuz.draw()
        win.flip()
        core.wait(Z_Fixkreuz)
        win.flip()
        if d[u'arrow_color']==u'yellow':
            Pfeil_nach_links.setLineColor('#FFFF00')
            Pfeil_nach_links.setFillColor('#FFFF00')
        elif d[u'arrow_color']==u'blue':
            Pfeil_nach_links.setLineColor('#0066CC')
            Pfeil_nach_links.setFillColor('#0066CC')
        if d[u'arrow_direction']==u'right':
            Pfeil_nach_links.setOri(240)
        elif d[u'arrow_direction']==u'left':
            Pfeil_nach_links.setOri(-60)
        if d[u'arrow_direction']==u'right' and d[u'arrow_color']==d[u'cresp'] or d[u'arrow_direction']==u'left' and d[u'arrow_color']!=d[u'cresp']:
            d[u'compatibility'] = u"compatible"
        else:
            d[u'compatibility'] = u"incompatible"
        Pfeil_nach_links.draw()
        win.flip()
        timer = core.Clock()
        if d[u'arrow_color']==d[u'cresp']:
            Antwort = event.waitKeys(maxWait=1.5, keyList=['space', 'escape'], timeStamped=timer)
        else:
            Antwort = event.waitKeys(maxWait=1.5, keyList=['space', 'escape'], timeStamped=timer)
        if Antwort:
            Pfeil_nach_links.setLineColor('#FFFFFF')
            Pfeil_nach_links.setFillColor('#FFFFFF')
            Pfeil_nach_links.draw()
            win.flip()
            d[u'responsecolor'] = d[u'arrow_color']
            if Antwort[0][0] == 'escape':
                core.quit()
            d[u'RT'] = round(Antwort[0][1]*1000)
            if d[u'arrow_color']==d['cresp']:
                d[u'accuracy'] = 1
            else:
                d[u'accuracy'] = 0
            core.wait((1500-d['RT'])/1000)
        else:
            if d['arrow_color']==d['cresp']:
                d['accuracy'] = 0
            else:
                d[u'accuracy'] = 1
        win.flip()
    return liste
###########################################################################
# Instruktionen
def Uebungstrials_fuer_alle():
    zeige_Botschaft(txt=u'Lieber Proband,\n\n\
wir freuen uns, dass Du an unserem Experiment teilnimmst.\n\n\
In dem Experiment werden Dir gelbe und blaue Pfeile nacheinander präsentiert. Deine Aufgabe ist es, alle {nogofarbe} Pfeile zu ignorieren und \
auf alle {farbe} Pfeile mit Drücken der Leertaste zu reagieren.\n\n\n\
Es folgt nun eine detaillierte Beschreibung der Aufgabe. \n\
Solltest Du irgendwann eine Frage haben, wende Dich einfach an die Versuchsleitung.\n\n\
Bereit? So drücke die Leertaste.'.format(farbe=u"gelben" if responsecolor==u"yellow" else u"blauen", 
nogofarbe=u"blauen" if responsecolor==u"yellow" else "gelben"), keys=['space', 'escape'])

    zeige_Botschaft(txt=u'Das Experiment besteht aus einem Übungsblock und vier Experimentalblöcken, in welchen Dir nacheinander gelbe und blaue Pfeile präsentiert werden. \n\n\
Deine Aufgabe ist es, alle {nogofarbe} Pfeile zu ignorieren und auf alle {farbe} Pfeile mit Drücken der Leertaste zu reagieren.\n\n\
Nach jedem Block wird Dir eine Rückmeldung über Deine Leistung angezeigt. Außerdem wirst Du dazu aufgefordert, die Versuchsleitung zu informieren. \
Sie wird daraufhin den nächsten Block einleiten.\n\n\
Weiter kommst Du mit der Leertaste.'.format(farbe=u"gelben" if responsecolor==u"yellow" else u"blauen",
nogofarbe=u"blauen" if responsecolor==u"yellow" else u"gelben"), keys=['space', 'escape'])

    zeige_Botschaft(txt=u'Damit Du Dich mit der Aufgabe vertraut machen kannst, folgen nun ein paar Übungsdurchgänge.\n\n\
Lege dazu einen Zeigefinger auf die Leertaste.\n\
Reagiere so schnell und akkurat wie möglich:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste, wenn der Pfeil {farbe} ist.\n\n\n\
Zum Starten der Übungstrials drücke die Leertaste.'.format(farbe=u"gelb" if responsecolor==u"yellow" else u"blau", 
nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"), keys=['space', 'escape'])

#####################################################################################
def Berechnung_der_Rueckmeldung(liste, deadline):
    correctness_error = 0
    speed_failure = 0
    sum_speed = 0
    valid_trials = 0
    for d in liste:
        correctness_error = correctness_error + (1-d['accuracy'])
        if d[u'arrow_color']==d[u'cresp']:
            valid_trials = valid_trials + 1
            if d[u'RT'] > deadline:
                speed_failure = speed_failure + 1
            if d[u'RT']:
                sum_speed = sum_speed + d[u'RT']
    prozent_fehler = int(round(float(correctness_error)/len(liste)*100))
    prozent_geschwindigkeit = int(round(float(speed_failure)/valid_trials*100, 0))
    mean_speed = int(round(float(sum_speed)/valid_trials, 0))
    return prozent_fehler, prozent_geschwindigkeit, mean_speed

#####################################################################################
# Ablauf in Abhängigkeit von der ID festlegen: Farb- und Bedingungsreihenfolge

if ID%8==0:
    #CADB blau links, gelb rechts
    condition = 8
    blockreihenfolge = u"CADB"
    responsecolor = u"yellow"
elif ID%8==7:
    #BDAC blau links, gelb rechts
    condition = 7
    blockreihenfolge = u"BDAC"
    responsecolor = u"yellow"
elif ID%8==6:
    #DCBA blau links, gelb rechts
    condition = 6
    blockreihenfolge = u"DCBA"
    responsecolor = u"yellow"
elif ID%8==5:
    #ABCD blau links, gelb rechts
    condition = 5
    blockreihenfolge = u"ABCD"
    responsecolor = u"yellow"
elif ID%8==4:
    #CADB gelb links, blau rechts
    condition = 4
    blockreihenfolge = u"CADB"
    responsecolor = u"blue"
elif ID%8==3:
    #BDAC gelb links, blau rechts
    condition = 3
    blockreihenfolge = u"BDAC"
    responsecolor = u"blue"
elif ID%8==2:
    #DCBA gelb links, blau rechts
    condition = 2
    blockreihenfolge = u"DCBA"
    responsecolor = u"blue"
else:
    #ABCD gelb links, blau rechts
    condition = 1
    blockreihenfolge = u"ABCD"
    responsecolor = u"blue"





# nun je nach Bedingung (condition) den Experimentablauf gestalten
Uebungstrials_fuer_alle()

# Übungstrials
# werden wiederholt, wenn ein Proband in über 20% der Trials Fehler oder zu mehr als 1000ms Reaktionszeit hat.
Uebungsliste = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/uebung.csv")
Uebungsliste = Ablauf_Uebung(Uebungsliste)
ListeAlsCsvSpeichern(Uebungsliste, ID, u";")

prozent_fehler, prozent_geschwindigkeit, mean_speed = Berechnung_der_Rueckmeldung(Uebungsliste, deadline=1000)

if prozent_fehler > 20:
    if prozent_geschwindigkeit > 25:
        zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Leider hast Du mehr als 20% Fehler und hast in mehr als 25% der Durchgänge das Geschwindigkeitskritierium überschritten.\n\n\
Versuche es deshalb noch einmal. Reagiere schnell und korrekt auf die Pfeilfarbe:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des zweiten Übungsblockes drücke die Leertaste.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit, 
farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue", nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"))
    else:
        zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Leider hast Du mehr als 20% Fehler.\n\n\
Versuche es deshalb noch einmal. Reagiere schnell und korrekt auf die Pfeilfarbe:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des zweiten Übungsblockes drücke die Leertaste.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit, 
farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue", nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"))
    Uebungsliste = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/uebung.csv")
    Uebungsliste = Ablauf_Uebung(Uebungsliste)
    ListeZuCsvHinzufuegen(Uebungsliste, ID, u";")
    prozent_fehler, prozent_geschwindigkeit, mean_speed = Berechnung_der_Rueckmeldung(Uebungsliste, deadline=1000)
    zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Vielen Dank für die Bearbeitung dieser Übung:\n\n\n\
Bitte informiere die Versuchsleitung zum Starten des 1. Blockes.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit), keys=['escape', '0'])
elif prozent_geschwindigkeit > 25:
    zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Leider hast Du in mehr als 25% der Durchgänge das Geschwindigkeitskritierium von einer Sekunde überschritten.\n\n\
Versuche es deshalb noch einmal. Reagiere schnell und korrekt auf die Pfeilfarbe:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe}.\n\n\n\
Zum Starten des zweiten Übungsblockes drücke die Leertaste.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit, 
farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue", nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"))
    Uebungsliste = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/uebung.csv")
    Uebungsliste = Ablauf_Uebung(Uebungsliste)
    ListeZuCsvHinzufuegen(Uebungsliste, ID, u";")
    prozent_fehler, prozent_geschwindigkeit, mean_speed = Berechnung_der_Rueckmeldung(Uebungsliste, deadline=1000)
    zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Vielen Dank für die Bearbeitung dieser Übung:\n\n\n\
Bitte informiere die Versuchsleitung zum Starten des 1. Blockes.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit), keys=['escape', '0'])
else:
    zeige_Botschaft(txt=u'Fehleranteil: {fehler} %\n\
Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\
Vielen Dank für die Bearbeitung dieser Übung:\n\n\n\
Bitte informiere die Versuchsleitung zum Starten des 1. Blockes.'.format(fehler=prozent_fehler, langsamanteil=prozent_geschwindigkeit), keys=['escape', '0'])


zeige_Botschaft(txt=u'{block}'.format(block=blockreihenfolge[0]), keys=['escape', '0'])
###########################################################################
# Experimentestart
# 1. Block
zeige_Botschaft(txt=u'Das Experiment kann nun beginnen.\n\n\
Schaffst Du es, über alle folgenden Blöcke insgesamt weniger als 15 % Fehler zu machen und in mehr als in 75 % der Durchgänge \
das Geschwindigkeitskritierum von 750 ms einzuhalten, so erhälst Du am Ende des Experimentes eine Schokolade.\n\
Nach jedem Block erhälst Du eine Rückmeldung über Deine Leistung im letzten Block.\n\n\
Reagiere so schnell und akkurat wie möglich:\n\n\
    Ignoriere {nogofarbe} Pfeile\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des Experimentes drücke die Leertaste.'.format(farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue",
nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"), keys=['space', 'escape'])

# Liste
Trials = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/Liste.csv")
Trials = Ablauf_Experiment(Trials)

# Daten speichern
ListeZuCsvHinzufuegen(Trials, ID, u";")

# Rückmeldung und Überleitung zum 2. Block
prozent_fehler1, prozent_geschwindigkeit1, mean_speed1 = Berechnung_der_Rueckmeldung(Trials, deadline=750)
zeige_Botschaft(txt=u'Feedback für den letzten Block:\n\n\
    Fehleranteil: {fehler} %\n\
    Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\n\
Du hast den 1. Block geschafft. Es folgen nun noch drei weitere Blöcke.\n\n\
Bitte informiere die Versuchsleitung zum Starten des 2. Blockes'.format(fehler=prozent_fehler1, langsamanteil=prozent_geschwindigkeit1, farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue"), keys=['escape', '0'])

zeige_Botschaft(txt=u'{block}'.format(block=blockreihenfolge[1]), keys=['escape', '0'])
###########################################################################
# 2. Block
zeige_Botschaft(txt=u'Nun kommt der 2. Block. Reagiere so schnell und akkurat wie möglich:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des 2. Blockes drücke die Leertaste.'.format(farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue",
nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"), keys=['space', 'escape'])

Trials = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/Liste.csv")
Trials = Ablauf_Experiment(Trials)

# Daten speichern
ListeZuCsvHinzufuegen(Trials, ID, u";")

# Rückmeldung und Überleitung zum 3. Block
prozent_fehler2, prozent_geschwindigkeit2, mean_speed2 = Berechnung_der_Rueckmeldung(Trials, deadline=750)
zeige_Botschaft(txt=u'Feedback für den letzten Block:\n\n\
    Fehleranteil: {fehler} %\n\
    Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\n\
Du hast den 2. Block geschafft. Es folgen nun noch zwei weitere Blöcke.\n\n\
Bitte informiere die Versuchsleitung zum Starten des 3. Blockes'.format(fehler=prozent_fehler2, langsamanteil=prozent_geschwindigkeit2, farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue"), keys=['escape', '0'])

zeige_Botschaft(txt=u'{block}'.format(block=blockreihenfolge[2]), keys=['escape', '0'])
###########################################################################
# 3. Block
zeige_Botschaft(txt=u'Nun kommt der 3. Block. Reagiere so schnell und akkurat wie möglich:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des 3. Blockes drücke die Leertaste.'.format(farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue",
nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"), keys=['space', 'escape'])

Trials = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/Liste.csv")
Trials = Ablauf_Experiment(Trials)

# Daten speichern
ListeZuCsvHinzufuegen(Trials, ID, u";")

# Rückmeldung und Überleitung zum 4. Block
prozent_fehler3, prozent_geschwindigkeit3, mean_speed3 = Berechnung_der_Rueckmeldung(Trials, deadline=750)
zeige_Botschaft(txt=u'Feedback für den letzten Block:\n\n\
    Fehleranteil: {fehler} %\n\
    Anteil zu langsamer Reaktionen: {langsamanteil} %\n\n\n\
Du hast den 3. Block geschafft. Nun kommt der letzte Block.\n\n\
Bitte informiere die Versuchsleitung zum Starten des letzten Blockes'.format(fehler=prozent_fehler3, langsamanteil=prozent_geschwindigkeit3, farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue"), keys=['escape', '0'])

zeige_Botschaft(txt=u'{block}'.format(block=blockreihenfolge[3]), keys=['escape', '0'])
###########################################################################
# 4. Block
zeige_Botschaft(txt=u'Nun kommt der letzte Block. Reagiere so schnell und akkurat wie möglich:\n\n\
    Ignoriere {nogofarbe} Pfeile.\n\
    Drücke die Leertaste für {farbe} Pfeile.\n\n\n\
Zum Starten des letzten Blockes drücke die Leertaste.'.format(farbe=u"gelbe" if responsecolor==u"yellow" else u"blaue",
nogofarbe=u"blaue" if responsecolor==u"yellow" else u"gelbe"), keys=['space', 'escape'])

Trials = Stimuligenerierung(os.path.dirname(os.path.abspath(__file__))+u"/Liste.csv")
Trials = Ablauf_Experiment(Trials)

# Daten speichern
ListeZuCsvHinzufuegen(Trials, ID, u";")


# abschließende Rückmeldung und Bedankung für Teilnahme
prozent_fehler4, prozent_geschwindigkeit4, mean_speed4 = Berechnung_der_Rueckmeldung(Trials, deadline=750)

fehler_insgesamt = (prozent_fehler1 + prozent_fehler2 + prozent_fehler3 + prozent_fehler4)/4
geschwindigkeit_insgesamt = (prozent_geschwindigkeit1 + prozent_geschwindigkeit2 + prozent_geschwindigkeit3 + prozent_geschwindigkeit4)/4

if fehler_insgesamt < 15 and geschwindigkeit_insgesamt < 25:
    zeige_Botschaft(txt=u'Du hast es geschafft!\n\n\
Und Du hast insgesamt weniger als 15 % Fehler und warst in mehr als 75 % der Durchgänge schnell genug. Melde Dich nun bei der Versuchsleitung und \
hole Dir eine Schokolade ab.')
else:
    zeige_Botschaft(txt=u'Du hast es geschafft!\n\n\
Leider hast Du mehr als 15 % Fehler oder warst in weniger als 75 % der Durchgänge schnell genug. Melde Dich nun bei der Versuchsleitung.')
###########################################################################


