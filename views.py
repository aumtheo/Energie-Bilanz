from django.shortcuts import render, redirect
#from .forms import BuildingProjectForm
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .berechnungen import berechne_nutzenergiebedarf
from .forms import GebaeudeAllgForm
from django.http import JsonResponse
import csv
from django.conf import settings
import os
from .forms              import BauteilForm
from .berechnungen       import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf
)


# 1) Startseite – nur GET, leitet per Button auf allg_angaben weiter
def startseite(request):
    return render(request, 'startseite.html')

# 2) Schritt 1: Allgemeine Angaben (live JS-Berechnung)
def allg_angaben(request):
    return render(request, 'allg_angaben.html')

# 3) Einfache Bilanzierung – mit POST-Handling und Session-Storage
def einfach(request):
    if request.method == 'POST':
        # Eingabewerte aus dem Formular
        laenge_ns       = float(request.POST.get('laenge_ns'))
        breite_ow       = float(request.POST.get('breite_ow'))
        geschosse       = int(request.POST.get('geschosse'))
        geschosshoehe   = float(request.POST.get('geschosshoehe'))

        # Berechnungen
        hoehe   = geschosse * geschosshoehe
        volumen = laenge_ns * breite_ow * hoehe
        bgf     = laenge_ns * breite_ow * geschosse
        nf      = bgf * 0.8  # Nutzfläche als 80 %

        # Ergebnisse in Session speichern
        request.session['daten'] = {
            'laenge_ns':        laenge_ns,
            'breite_ow':        breite_ow,
            'geschosse':        geschosse,
            'geschosshoehe':    geschosshoehe,
            'hoehe':            round(hoehe, 2),
            'volumen':          round(volumen, 2),
            'bgf':              round(bgf, 2),
            'nf':               round(nf, 2),
        }

        # Zur Ergebnis-Seite weiterleiten
        return redirect('einfach_ergebnis')

    # GET-Request zeigt das Eingabe-Formular
    return render(request, 'einfach.html')

# 4) Ergebnis-View der einfachen Bilanzierung
def einfach_ergebnis(request):
    daten = request.session.get('daten', {})
    return render(request, 'einfach_ergebnis.html', {'daten': daten})

# 5) Ausführliche Bilanzierung (Platzhalter)
def ausfuehrlich(request):
    return render(request, 'ausfuehrlich.html')

def bauteile_bezugsgroessen(request):
    return render(request, 'bauteile_bezugsgroessen.html')

def bauteile_aufbau(request):
    return render(request, 'bauteile_aufbau.html')

def bauteile_luftfoerderung(request):
    return render(request, 'bauteile_luftfoerderung.html')

def bauteile_photovoltaik(request):
    return render(request, 'bauteile_photovoltaik.html')

def gwp(request):
    return render(request, 'gwp.html')

def ergebnis(request):
    return render(request, 'ergebnis.html')

# — Wärme —
def waerme_heizwaerme(request):
    return render(request, 'waerme_heizwaerme.html')

def waerme_waermequellen(request):
    return render(request, 'waerme_waermequellen.html')

def waerme_waermeschutz(request):
    return render(request, 'waerme_waermeschutz.html')

def waerme_lichtwasser(request):
    return render(request, 'waerme_lichtwasser.html')


# — GWP —
def gwp_herstellung(request):
    return render(request, 'gwp_herstellung.html')

def gwp_waermequellen(request):
    return render(request, 'gwp_waermequellen.html')

def allg_angaben(request):
    if request.method == 'POST':
        form = GebaeudeAllgForm(request.POST)
        if form.is_valid():
            gebaeude = form.save()
            request.session['project_id'] = gebaeude.pk
            return redirect('bauteile_bezugsgroessen')
    else:
        form = GebaeudeAllgForm()

    return render(request, 'allg_angaben.html', {
        'form': form
    })

def grundriss(request):
    return render(request, 'grundriss.html')   

def raumkonfigurator(request):
    return render(request, 'raumkonfigurator.html')

def floorplanner(request):
    return render(request, 'floorplanner.html')

def wandaufbau(request):
    return render(request, 'wandaufbau.html')

def uber_tool(request):
    return render(request, "uber_tool.html")

def entwicklerteam(request):
    return render(request, 'entwicklerteam.html')

def kontakt(request):
    return render(request, 'kontakt.html')

def hilfe(request):
    return render(request, 'hilfe.html')

def einfach_ergebnis_pdf(request):
    # Beispiel-Daten; Du holst Dir natürlich Deine echten daten aus dem Kontext
    daten = {
        'laenge_ns': 20,
        'breite_ow': 15,
        'geschosse': 2,
        'geschosshoehe': 2.7,
        'hoehe': 5.4,
        'volumen': 1620,
        'bgf': 300,
        'nf': 280,
    }

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Überschrift
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 80, "Ergebnis Deiner Eingaben")

    # Inhalt
    p.setFont("Helvetica", 12)
    y = height - 120
    for key, label in [
        ('laenge_ns', 'Länge Nord/Süd (m)'),
        ('breite_ow', 'Breite Ost/West (m)'),
        ('geschosse', 'Anzahl Geschosse'),
        ('geschosshoehe', 'Geschosshöhe (m)'),
        ('hoehe', 'Gebäudehöhe (m)'),
        ('volumen', 'Volumen (m³)'),
        ('bgf', 'BGF (m²)'),
        ('nf', 'NF (m²)')
    ]:
        p.drawString(80, y, f"{label}: {daten[key]}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ergebnis.pdf"'
    return response

def ergebnis_view(request):
    #  – die Parameter müssen natürlich aus dem Kontext kommen,
    #    z.B. aus der Datenbank oder aus POST-Daten (Formular):
    nf_m2                    = 128.0   # Beispielwert, aus Berechnung Pro Raum
    jahres_hw_bedarf_kwh     = 12500.0 # Beispiel: Summe aller Heizmonate
    tw_kwh_pro_m2            = 30.0    # Beispiel: Tabelle Warmwasserbedarf
    luftfoerderung_kwh_m2    = 15.0    # Beispiel: Lüftung (korrigiert)
    beleuchtung_kwh_m2       = 10.0    # Beispiel: Beleuchtung
    nutzer_pro_m2            = 5.0     # Beispiel: Prozess-Energie

    ergebnis_ne = berechne_nutzenergiebedarf(
        nf_m2,
        jahres_hw_bedarf_kwh,
        tw_kwh_pro_m2,
        luftfoerderung_kwh_m2,
        beleuchtung_kwh_m2,
        nutzer_pro_m2
    )

    context = {
        "ne_absolut":    ergebnis_ne["ne_absolut"],
        "ne_spezifisch": ergebnis_ne["ne_spezifisch"],
        # … später ggf. weitere Ergebnisse (Endenergie, Primärenergie etc.)
    }

    return render(request, "einfach_ergebnis.html", context)

def baukrper(request):
    return render(request, 'baukrper.html')

def bauteil(request):
    return render(request, "bauteil.html")

def pv(request):
    return render(request, 'pv.html')

def lftung(request):
    return render(request, 'lftung.html')

def beleuchtung(request):
    return render(request, 'beleuchtung.html')

def beleuchtung_2(request):
    return render(request, 'beleuchtung_2.html')

def waermequellen(request):
    return render(request, 'wrmequellen.html')

def sdf(request):
    return render(request, 'sdf.html')

def gwp(request):
    return render(request, 'gwp.html')

def ergebnis(request):
    return render(request, 'ergebnis.html')

def baukoerper_kp(request):
    return render(request, 'baukrper_kp.html')


def baukrper_kp_2(request):
    return render(request, 'baukrper_kp_2.html')

def bauteil_kp(request):
    return render(request, 'bauteil_kp.html')

from .berechnungen import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf,
)

def api_berechnung(request):
    laenge = float(request.GET.get("laenge", 0))
    breite = float(request.GET.get("breite", 0))
    geschosshoehe = float(request.GET.get("geschosshoehe", 0))
    anz_geschosse = int(request.GET.get("anz_geschosse", 0))

    geb = berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse)

    # Beispiel: Nutzenergiebedarf
    nf = geb["nf"]
    heiz = float(request.GET.get("jahres_heiz", 0))
    ww = float(request.GET.get("trinkwarm", 0))
    luft = float(request.GET.get("lueftung", 0))
    bel = float(request.GET.get("beleuchtung", 0))
    nutz = float(request.GET.get("nutzer", 0))

    ne = berechne_nutzenergiebedarf(nf, heiz, ww, luft, bel, nutz)
    sb = berechne_strombedarf(nf, ww, luft, bel, nutz)
    wb = berechne_waermebedarf(heiz)
    ee = berechne_endenergiebedarf(nf, sb, wb)

    return JsonResponse({
        "gebaeudedaten": geb,
        "nutzenergie": ne,
        "strom": sb,
        "waerme": wb,
        "endenergie": ee,
    })


from .berechnungen import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf,
)

def api_berechnung(request):
    # 1) Parameter aus den GET-Parametern auslesen
    laenge    = float(request.GET.get("laenge", 0))
    breite    = float(request.GET.get("breite", 0))
    geschossh = float(request.GET.get("geschosshoehe", 0))
    geschosse = int(request.GET.get("anz_geschosse", 0))

    # 2) Erst Gebäude­daten rechnen
    geb = berechne_gebaeudedaten(laenge, breite, geschossh, geschosse)

    # 3) Dann Nutzenergie, Strom, Wärme, Endenergie
    ne = berechne_nutzenergiebedarf(
        geb["nf"],
        float(request.GET.get("jahres_heizbedarf", 0)),
        float(request.GET.get("tw_pro_m2", 0)),
        float(request.GET.get("lwt_pro_m2", 0)),
        float(request.GET.get("bel_pro_m2", 0)),
        float(request.GET.get("nutzer_pro_m2", 0)),
    )
    sb = berechne_strombedarf(
        geb["nf"],
        float(request.GET.get("tw_pro_m2", 0)),
        float(request.GET.get("lwt_pro_m2", 0)),
        float(request.GET.get("bel_pro_m2", 0)),
        float(request.GET.get("nutzer_pro_m2", 0)),
    )
    wb = berechne_waermebedarf(
        float(request.GET.get("jahres_heizbedarf", 0)),
        float(request.GET.get("verlust_verteilung", 0)),
        float(request.GET.get("verlust_speicher", 0)),
        float(request.GET.get("ww_warmwasser", 0)),
    )
    ee = berechne_endenergiebedarf(geb["nf"], sb, wb)

    # 4) JSON zusammenpacken und zurückgeben
    return JsonResponse({
        "gebaeudedaten": geb,
        "nutzenergie":   ne,
        "strombedarf":   sb,
        "waermebedarf":  wb,
        "endenergie":    ee,
    })
    

# settings.BASE_DIR ist das Verzeichnis, in dem manage.py liegt
CSV_PATH = os.path.join(settings.BASE_DIR, 'klimadaten_full.csv')

# Lies die Orte beim Start einmalig ein
KLIMA_ORTE = []
try:
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Wir nehmen an, die Spalte mit den Ortsnamen heißt 'referenzort'
        KLIMA_ORTE = [row['referenzort'] for row in reader]
except FileNotFoundError:
    # Nur zur Diagnose in der Konsole
    print(f"❌ Datei nicht gefunden: {CSV_PATH}")

def allg_angaben(request):
    return render(request, 'allg_angaben.html', {
        'orte': KLIMA_ORTE,
    })

def bauteil_eingabe(request):
    if request.method == 'POST':
        form = BauteilForm(request.POST)
        if form.is_valid():
            bauteil = form.save(commit=False)

            # 1) Gebäudedaten
            gd = berechne_gebaeudedaten(
                laenge=bauteil.laenge,
                breite=bauteil.breite,
                geschosshoehe=bauteil.geschosshoehe,
                anz_geschosse=bauteil.anz_geschosse
            )
            bauteil.hoehe   = gd['hoehe']
            bauteil.volumen = gd['volumen']
            bauteil.bgf     = gd['bgf']
            bauteil.nf      = gd['nf']

            # 2) Nutzenergiebedarf
            ne = berechne_nutzenergiebedarf(
                nf_m2=bauteil.nf,
                jahres_heizwaermebedarf_kwh=0,         # hier ggf. eigenes Feld
                trinkwarmwasser_kwh_pro_m2=0,          #
                luftfoerderung_kwh_pro_m2=0,           #
                beleuchtung_kwh_pro_m2=0,              #
                nutzer_pro_m2=0                        #
            )
            bauteil.ne_absolut = ne['ne_absolut']
            bauteil.ne_spez    = ne['ne_spezifisch']

            # 3) Strombedarf
            sb = berechne_strombedarf(
                nf_m2=bauteil.nf,
                trinkwarmwasser_kwh_pro_m2=0,
                luftfoerderung_kwh_pro_m2=0,
                beleuchtung_kwh_pro_m2=0,
                nutzer_pro_m2=0
            )
            bauteil.sb_absolut = sb['sb_absolut']
            bauteil.sb_spez    = sb['sb_spezifisch']

            # 4) Wärmebedarf
            wb = berechne_waermebedarf(
                jahres_heizwaermebedarf_kwh=0,
                verteilungsverlust_kwh=0,
                speicherverlust_kwh=0,
                warmwasserbedarf_kwh=0
            )
            bauteil.wb_absolut = wb['wb_absolut']

            # 5) Endenergie
            ee = berechne_endenergiebedarf(
                nf_m2=bauteil.nf,
                ergebnis_strom=sb,
                ergebnis_waerme=wb
            )
            bauteil.ee_absolut = ee['ee_absolut']
            bauteil.ee_spez    = ee['ee_spezifisch']

            # speichern
            bauteil.save()
            return redirect('ergebnis_seite', pk=bauteil.pk)
    else:
        form = BauteilForm()

    return render(request, 'bauteil_eingabe.html', {'form': form})