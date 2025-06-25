from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import csv
import json
import os
from django.conf import settings

from .models import (
    BuildingProject, 
    Gebaeude, 
    Bauteil, 
    KlimaregionTemperatur,
    SolarStrahlungMonat,
    SonnenschutzFaktor,
    SonneneintragsKennwert,
    Temperaturkorrekturfaktor,
    DruckverlustBauteil
)

from .forms import (
    GebaeudeAllgForm,
    BauteilForm,
    BuildingProjectForm,
    PVForm,
    LueftungForm,
    BeleuchtungForm,
    WaermequellenForm,
    SDFForm,
    GWPForm
)

from .berechnungen import (
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
    # Load climate locations for dropdown
    klima_orte = []
    csv_path = os.path.join(settings.BASE_DIR, 'klimadaten_full.csv')
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            klima_orte = [row['referenzort'] for row in reader]
    except FileNotFoundError:
        pass
    
    if request.method == 'POST':
        form = GebaeudeAllgForm(request.POST)
        if form.is_valid():
            gebaeude = form.save()
            request.session['gebaeude_id'] = gebaeude.pk
            return redirect('baukrper')
    else:
        form = GebaeudeAllgForm()
    
    return render(request, 'allg_angaben.html', {
        'form': form,
        'orte': klima_orte
    })

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
    
    # Calculate energy needs if we have the data
    if daten:
        nf = daten.get('nf', 0)
        # Example values - in a real app these would come from previous steps
        jahres_hw_bedarf_kwh = 12500.0
        tw_kwh_pro_m2 = 30.0
        luftfoerderung_kwh_m2 = 15.0
        beleuchtung_kwh_m2 = 10.0
        nutzer_pro_m2 = 5.0
        
        ergebnis_ne = berechne_nutzenergiebedarf(
            nf,
            jahres_hw_bedarf_kwh,
            tw_kwh_pro_m2,
            luftfoerderung_kwh_m2,
            beleuchtung_kwh_m2,
            nutzer_pro_m2
        )
        
        context = {
            "daten": daten,
            "ne_absolut": ergebnis_ne["ne_absolut"],
            "ne_spezifisch": ergebnis_ne["ne_spezifisch"],
        }
    else:
        context = {"daten": {}}
    
    return render(request, 'einfach_ergebnis.html', context)

# 5) Ausführliche Bilanzierung (Platzhalter)
def ausfuehrlich(request):
    return render(request, 'ausfuehrlich.html')

def bauteile_bezugsgroessen(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('bauteile_aufbau')
    
    return render(request, 'bauteile_bezugsgroessen.html', {'gebaeude': gebaeude})

def bauteile_aufbau(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('bauteile_luftfoerderung')
    
    return render(request, 'bauteile_aufbau.html', {'gebaeude': gebaeude})

def bauteile_luftfoerderung(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('bauteile_photovoltaik')
    
    return render(request, 'bauteile_luftfoerderung.html', {'gebaeude': gebaeude})

def bauteile_photovoltaik(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('waerme_heizwaerme')
    
    return render(request, 'bauteile_photovoltaik.html', {'gebaeude': gebaeude})

# — Wärme —
def waerme_heizwaerme(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('waerme_waermequellen')
    
    return render(request, 'waerme_heizwaerme.html', {'gebaeude': gebaeude})

def waerme_waermequellen(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('waerme_waermeschutz')
    
    return render(request, 'waerme_waermequellen.html', {'gebaeude': gebaeude})

def waerme_waermeschutz(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('waerme_lichtwasser')
    
    return render(request, 'waerme_waermeschutz.html', {'gebaeude': gebaeude})

def waerme_lichtwasser(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('gwp_herstellung')
    
    return render(request, 'waerme_lichtwasser.html', {'gebaeude': gebaeude})

# — GWP —
def gwp_herstellung(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('gwp_waermequellen')
    
    return render(request, 'gwp_herstellung.html', {'gebaeude': gebaeude})

def gwp_waermequellen(request):
    gebaeude_id = request.session.get('gebaeude_id')
    if not gebaeude_id:
        return redirect('allg_angaben')
    
    try:
        gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
    except Gebaeude.DoesNotExist:
        return redirect('allg_angaben')
    
    if request.method == 'POST':
        # Process form data here
        # ...
        return redirect('ergebnis')
    
    return render(request, 'gwp_waermequellen.html', {'gebaeude': gebaeude})

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
    # Get data from session or database
    daten = request.session.get('daten', {})
    if not daten and 'gebaeude_id' in request.session:
        try:
            gebaeude = Gebaeude.objects.get(pk=request.session['gebaeude_id'])
            daten = {
                'laenge_ns': gebaeude.laenge_ns,
                'breite_ow': gebaeude.breite_ow,
                'geschosse': gebaeude.geschosse,
                'geschosshoehe': gebaeude.geschosshoehe,
                'hoehe': gebaeude.geschosse * gebaeude.geschosshoehe,
                'volumen': gebaeude.laenge_ns * gebaeude.breite_ow * gebaeude.geschosse * gebaeude.geschosshoehe,
                'bgf': gebaeude.laenge_ns * gebaeude.breite_ow * gebaeude.geschosse,
                'nf': gebaeude.laenge_ns * gebaeude.breite_ow * gebaeude.geschosse * 0.8,
            }
        except Gebaeude.DoesNotExist:
            daten = {}

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
        value = daten.get(key, '-')
        p.drawString(80, y, f"{label}: {value}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ergebnis.pdf"'
    return response

def baukrper(request):
    gebaeude_id = request.session.get('gebaeude_id')
    
    if request.method == 'POST':
        form = BauteilForm(request.POST)
        if form.is_valid():
            bauteil = form.save(commit=False)
            
            # Calculate building data
            gd = berechne_gebaeudedaten(
                bauteil.laenge,
                bauteil.breite,
                bauteil.geschosshoehe,
                bauteil.anz_geschosse
            )
            
            # Store calculated values
            bauteil.hoehe = gd['hoehe']
            bauteil.volumen = gd['volumen']
            bauteil.bgf = gd['bgf']
            bauteil.nf = gd['nf']
            
            bauteil.save()
            request.session['bauteil_id'] = bauteil.pk
            
            return redirect('bauteil')
    else:
        # Pre-fill form with data from Gebaeude if available
        initial_data = {}
        if gebaeude_id:
            try:
                gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
                initial_data = {
                    'laenge': gebaeude.laenge_ns,
                    'breite': gebaeude.breite_ow,
                    'geschosshoehe': gebaeude.geschosshoehe,
                    'anz_geschosse': gebaeude.geschosse,
                }
            except Gebaeude.DoesNotExist:
                pass
        
        form = BauteilForm(initial=initial_data)
    
    return render(request, 'baukrper.html', {'form': form})

def bauteil(request):
    bauteil_id = request.session.get('bauteil_id')
    
    if request.method == 'POST':
        # Process U-values
        if bauteil_id:
            try:
                bauteil = Bauteil.objects.get(pk=bauteil_id)
                bauteil.u_wand_nord = float(request.POST.get('u_wand_nord', 0))
                bauteil.u_wand_sued = float(request.POST.get('u_wand_sued', 0))
                bauteil.u_wand_west = float(request.POST.get('u_wand_west', 0))
                bauteil.u_wand_ost = float(request.POST.get('u_wand_ost', 0))
                bauteil.u_bodenplatte = float(request.POST.get('u_bodenplatte', 0))
                bauteil.u_dach = float(request.POST.get('u_dach', 0))
                bauteil.save()
            except Bauteil.DoesNotExist:
                pass
        
        return redirect('pv')
    
    # Get bauteil data if available
    bauteil_data = None
    if bauteil_id:
        try:
            bauteil_data = Bauteil.objects.get(pk=bauteil_id)
        except Bauteil.DoesNotExist:
            pass
    
    return render(request, "bauteil.html", {'bauteil': bauteil_data})

def pv(request):
    bauteil_id = request.session.get('bauteil_id')
    
    if request.method == 'POST':
        form = PVForm(request.POST)
        if form.is_valid():
            # Store PV data in session
            request.session['pv_data'] = {
                'pv_nord_fenster': form.cleaned_data.get('pv_nord_fenster'),
                'pv_nord_opak': form.cleaned_data.get('pv_nord_opak'),
                'pv_sued_fenster': form.cleaned_data.get('pv_sued_fenster'),
                'pv_sued_opak': form.cleaned_data.get('pv_sued_opak'),
                'pv_west_fenster': form.cleaned_data.get('pv_west_fenster'),
                'pv_west_opak': form.cleaned_data.get('pv_west_opak'),
                'pv_ost_fenster': form.cleaned_data.get('pv_ost_fenster'),
                'pv_ost_opak': form.cleaned_data.get('pv_ost_opak'),
                'wirkungsgrad': form.cleaned_data.get('wirkungsgrad'),
            }
            return redirect('lftung')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('pv_data', {})
        form = PVForm(initial=initial_data)
    
    return render(request, 'pv.html', {'form': form})

def lftung(request):
    if request.method == 'POST':
        form = LueftungForm(request.POST)
        if form.is_valid():
            # Store ventilation data in session
            request.session['lueftung_data'] = {
                'lueftungstyp': form.cleaned_data.get('lueftungstyp'),
                'luftwechselrate': form.cleaned_data.get('luftwechselrate'),
                'wrg_wirkungsgrad': form.cleaned_data.get('wrg_wirkungsgrad'),
                'raum_soll_temp': form.cleaned_data.get('raum_soll_temp'),
                'laufzeit_h_d': form.cleaned_data.get('laufzeit_h_d'),
                'laufzeit_d_a': form.cleaned_data.get('laufzeit_d_a'),
            }
            return redirect('beleuchtung')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('lueftung_data', {})
        form = LueftungForm(initial=initial_data)
    
    return render(request, 'lftung.html', {'form': form})

def beleuchtung(request):
    if request.method == 'POST':
        form = BeleuchtungForm(request.POST)
        if form.is_valid():
            # Store lighting data in session
            request.session['beleuchtung_data'] = {
                'beleuchtungsart_buero': form.cleaned_data.get('beleuchtungsart_buero'),
                'regelungsart_buero': form.cleaned_data.get('regelungsart_buero'),
                'e_soll_buero': form.cleaned_data.get('e_soll_buero'),
                'laufzeit_h_d_buero': form.cleaned_data.get('laufzeit_h_d_buero'),
                'laufzeit_d_a_buero': form.cleaned_data.get('laufzeit_d_a_buero'),
                'beleuchtungsart_wohnen': form.cleaned_data.get('beleuchtungsart_wohnen'),
                'regelungsart_wohnen': form.cleaned_data.get('regelungsart_wohnen'),
                'e_soll_wohnen': form.cleaned_data.get('e_soll_wohnen'),
                'laufzeit_h_d_wohnen': form.cleaned_data.get('laufzeit_h_d_wohnen'),
                'laufzeit_d_a_wohnen': form.cleaned_data.get('laufzeit_d_a_wohnen'),
            }
            return redirect('beleuchtung_2')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('beleuchtung_data', {})
        form = BeleuchtungForm(initial=initial_data)
    
    return render(request, 'beleuchtung.html', {'form': form})

def beleuchtung_2(request):
    if request.method == 'POST':
        # Process additional lighting data if needed
        return redirect('waermequellen')
    
    return render(request, 'beleuchtung_2.html')

def waermequellen(request):
    if request.method == 'POST':
        form = WaermequellenForm(request.POST)
        if form.is_valid():
            # Store heat sources data in session
            request.session['waermequellen_data'] = {
                'geraet1_anzahl': form.cleaned_data.get('geraet1_anzahl'),
                'geraet1_leistung': form.cleaned_data.get('geraet1_leistung'),
                'geraet1_betr_h_d': form.cleaned_data.get('geraet1_betr_h_d'),
                'geraet1_betr_d_a': form.cleaned_data.get('geraet1_betr_d_a'),
                'quelle1_anzahl': form.cleaned_data.get('quelle1_anzahl'),
                'quelle1_leistung': form.cleaned_data.get('quelle1_leistung'),
                'quelle1_betr_h_d': form.cleaned_data.get('quelle1_betr_h_d'),
                'quelle1_betr_d_a': form.cleaned_data.get('quelle1_betr_d_a'),
            }
            return redirect('sdf')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('waermequellen_data', {})
        form = WaermequellenForm(initial=initial_data)
    
    return render(request, 'wrmequellen.html', {'form': form})

def sdf(request):
    if request.method == 'POST':
        form = SDFForm(request.POST)
        if form.is_valid():
            # Store SDF data in session
            request.session['sdf_data'] = {
                'kritischer_raum': form.cleaned_data.get('kritischer_raum'),
                'fassadenorientierung': form.cleaned_data.get('fassadenorientierung'),
                'sonnenschutzart': form.cleaned_data.get('sonnenschutzart'),
                'verglasungsart': form.cleaned_data.get('verglasungsart'),
                'passive_kuehlung': form.cleaned_data.get('passive_kuehlung'),
                'fensterneigung': form.cleaned_data.get('fensterneigung'),
            }
            return redirect('gwp')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('sdf_data', {})
        form = SDFForm(initial=initial_data)
    
    return render(request, 'sdf.html', {'form': form})

def gwp(request):
    if request.method == 'POST':
        form = GWPForm(request.POST)
        if form.is_valid():
            # Store GWP data in session
            request.session['gwp_data'] = {
                'bauteil1_menge': form.cleaned_data.get('bauteil1_menge'),
                'bauteil1_co2': form.cleaned_data.get('bauteil1_co2'),
                'bauteil2_menge': form.cleaned_data.get('bauteil2_menge'),
                'bauteil2_co2': form.cleaned_data.get('bauteil2_co2'),
            }
            return redirect('ergebnis')
    else:
        # Pre-fill form with session data if available
        initial_data = request.session.get('gwp_data', {})
        form = GWPForm(initial=initial_data)
    
    return render(request, 'gwp.html', {'form': form})

def ergebnis(request):
    # Collect all data from session
    gebaeude_id = request.session.get('gebaeude_id')
    bauteil_id = request.session.get('bauteil_id')
    pv_data = request.session.get('pv_data', {})
    lueftung_data = request.session.get('lueftung_data', {})
    beleuchtung_data = request.session.get('beleuchtung_data', {})
    waermequellen_data = request.session.get('waermequellen_data', {})
    sdf_data = request.session.get('sdf_data', {})
    gwp_data = request.session.get('gwp_data', {})
    
    # Get building data
    gebaeude = None
    bauteil = None
    
    if gebaeude_id:
        try:
            gebaeude = Gebaeude.objects.get(pk=gebaeude_id)
        except Gebaeude.DoesNotExist:
            pass
    
    if bauteil_id:
        try:
            bauteil = Bauteil.objects.get(pk=bauteil_id)
        except Bauteil.DoesNotExist:
            pass
    
    # Calculate final results
    results = {}
    
    if bauteil:
        # Use bauteil data for calculations
        nf = bauteil.nf
        
        # Example values - in a real app these would come from previous steps
        jahres_hw_bedarf_kwh = 12500.0
        tw_kwh_pro_m2 = 30.0
        luftfoerderung_kwh_m2 = 15.0
        beleuchtung_kwh_m2 = 10.0
        nutzer_pro_m2 = 5.0
        
        ne = berechne_nutzenergiebedarf(
            nf,
            jahres_hw_bedarf_kwh,
            tw_kwh_pro_m2,
            luftfoerderung_kwh_m2,
            beleuchtung_kwh_m2,
            nutzer_pro_m2
        )
        
        sb = berechne_strombedarf(
            nf,
            tw_kwh_pro_m2,
            luftfoerderung_kwh_m2,
            beleuchtung_kwh_m2,
            nutzer_pro_m2
        )
        
        wb = berechne_waermebedarf(
            jahres_hw_bedarf_kwh,
            0,  # verteilungsverlust_kwh
            0,  # speicherverlust_kwh
            0   # warmwasserbedarf_kwh
        )
        
        ee = berechne_endenergiebedarf(nf, sb, wb)
        
        results = {
            'nutzenergie': ne,
            'strombedarf': sb,
            'waermebedarf': wb,
            'endenergie': ee,
        }
    
    return render(request, 'ergebnis.html', {
        'gebaeude': gebaeude,
        'bauteil': bauteil,
        'pv_data': pv_data,
        'lueftung_data': lueftung_data,
        'beleuchtung_data': beleuchtung_data,
        'waermequellen_data': waermequellen_data,
        'sdf_data': sdf_data,
        'gwp_data': gwp_data,
        'results': results,
    })

def baukoerper_kp(request):
    return render(request, 'baukrper_kp.html')

def baukrper_kp_2(request):
    return render(request, 'baukrper_kp_2.html')

def bauteil_kp(request):
    return render(request, 'bauteil_kp.html')

@csrf_exempt
def api_berechnung(request):
    """
    API endpoint for real-time building energy calculations
    """
    try:
        # Extract parameters from request
        if request.method == "GET":
            params = request.GET
        else:
            data = json.loads(request.body)
            params = data
        
        # Extract building parameters with defaults
        laenge = float(params.get("laenge", 0))
        breite = float(params.get("breite", 0))
        geschosshoehe = float(params.get("geschosshoehe", 0))
        anz_geschosse = int(params.get("anz_geschosse", 0))
        
        # Calculate building data
        geb = berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse)
        
        # Extract energy parameters with defaults
        nf = geb["nf"]
        heiz = float(params.get("jahres_heizbedarf", 0))
        ww = float(params.get("tw_pro_m2", 0))
        luft = float(params.get("lwt_pro_m2", 0))
        bel = float(params.get("bel_pro_m2", 0))
        nutz = float(params.get("nutzer_pro_m2", 0))
        
        # Calculate energy demands
        ne = berechne_nutzenergiebedarf(nf, heiz, ww, luft, bel, nutz)
        sb = berechne_strombedarf(nf, ww, luft, bel, nutz)
        wb = berechne_waermebedarf(
            heiz,
            float(params.get("verlust_verteilung", 0)),
            float(params.get("verlust_speicher", 0)),
            float(params.get("ww_warmwasser", 0))
        )
        ee = berechne_endenergiebedarf(nf, sb, wb)
        
        return JsonResponse({
            "success": True,
            "gebaeudedaten": geb,
            "nutzenergie": ne,
            "strombedarf": sb,
            "waermebedarf": wb,
            "endenergie": ee,
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)