# mylist/forms.py

from django import forms
from .models import Gebaeude
from .models import Bauteil

class GebaeudeAllgForm(forms.ModelForm):
    """
    Formular für den ersten Wizard-Schritt: Allgemeine Gebäudedaten.
    """
    class Meta:
        model = Gebaeude
        fields = [
            'name',
            'laenge_ns',
            'breite_ow',
            'geschosshoehe',
            'geschosse',
        ]


class GebaeudeEnergieKennzahlenForm(forms.ModelForm):
    """
    Formular für den zweiten Wizard-Schritt:
    Eingabe der spezifischen kWh/m²-Werte (Warmwasser, Lüftung, Beleuchtung, Nutzer)
    sowie Heizwärmebedarf (jahres_heizwert).
    """
    class Meta:
        model = Gebaeude
        fields = [
            'jahres_heizwert',
            'tw_kwh_m2',
            'luft_kwh_m2',
            'bel_kwh_m2',
            'nutz_kwh_m2',
        ]


class GebaeudeVerlusteForm(forms.ModelForm):
    """
    Formular für den dritten Wizard-Schritt:
    Verteilungsverluste, Speicherverluste, thermischer Warmwasserbedarf.
    """
    class Meta:
        model = Gebaeude
        fields = [
            'verteilungsverlust_kwh',
            'speicherverlust_kwh',
            'warmwasserbedarf_kwh',
        ]

class BauteilForm(forms.ModelForm):
    class Meta:
        model = Bauteil
        # trage hier alle Felder ein, die Deine Form haben soll,
        # z.B. laenge, breite, geschosshoehe, anz_geschosse, usw.
        fields = [
            'laenge',
            'breite',
            'geschosshoehe',
            'anz_geschosse',
            # falls Du noch weitere Modell-Felder hast:
            # 'u_wert_wand_nord', 'u_wert_wand_sued', …, 'u_wert_dach'
        ]
        widgets = {
            'laenge':          forms.NumberInput(attrs={'step': '0.01'}),
            'breite':          forms.NumberInput(attrs={'step': '0.01'}),
            'geschosshoehe':   forms.NumberInput(attrs={'step': '0.01'}),
            'anz_geschosse':   forms.NumberInput(),
            # und so weiter …
        }