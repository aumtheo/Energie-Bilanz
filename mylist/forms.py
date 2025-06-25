from django import forms
from .models import Gebaeude, Bauteil, BuildingProject

class GebaeudeAllgForm(forms.ModelForm):
    """
    Form for general building data input
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
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gebäudename (optional)'
            }),
            'laenge_ns': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'laenge',
                'placeholder': 'z.B. 20.0'
            }),
            'breite_ow': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'breite',
                'placeholder': 'z.B. 15.0'
            }),
            'geschosshoehe': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'geschosshoehe',
                'placeholder': 'z.B. 2.7'
            }),
            'geschosse': forms.NumberInput(attrs={
                'class': 'form-control',
                'name': 'anz_geschosse',
                'placeholder': 'z.B. 2'
            }),
        }

class BauteilForm(forms.ModelForm):
    """
    Form for building component data
    """
    class Meta:
        model = Bauteil
        fields = [
            'laenge',
            'breite',
            'geschosshoehe',
            'anz_geschosse',
            'u_wand_nord',
            'u_wand_sued',
            'u_wand_west',
            'u_wand_ost',
            'u_bodenplatte',
            'u_dach',
        ]
        widgets = {
            'laenge': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'laenge'
            }),
            'breite': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'breite'
            }),
            'geschosshoehe': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'geschosshoehe'
            }),
            'anz_geschosse': forms.NumberInput(attrs={
                'class': 'form-control',
                'name': 'anz_geschosse'
            }),
            'u_wand_nord': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_wand_nord'
            }),
            'u_wand_sued': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_wand_sued'
            }),
            'u_wand_west': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_wand_west'
            }),
            'u_wand_ost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_wand_ost'
            }),
            'u_bodenplatte': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_bodenplatte'
            }),
            'u_dach': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'name': 'u_dach'
            }),
        }

class BuildingProjectForm(forms.ModelForm):
    """
    Form for building project data
    """
    class Meta:
        model = BuildingProject
        fields = [
            'standort',
            'laenge_ns',
            'breite_ow',
            'geschosshoehe',
            'geschosse',
            'fenster_nord',
            'fenster_sued',
            'fenster_ost',
            'fenster_west',
            'fenster_dach',
        ]
        widgets = {
            'standort': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'z.B. Berlin'
            }),
            'laenge_ns': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'laenge'
            }),
            'breite_ow': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'breite'
            }),
            'geschosshoehe': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'geschosshoehe'
            }),
            'geschosse': forms.NumberInput(attrs={
                'class': 'form-control',
                'name': 'anz_geschosse'
            }),
            'fenster_nord': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'fenster_nord'
            }),
            'fenster_sued': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'fenster_sued'
            }),
            'fenster_ost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'fenster_ost'
            }),
            'fenster_west': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'fenster_west'
            }),
            'fenster_dach': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'name': 'fenster_dach'
            }),
        }

class PVForm(forms.Form):
    """
    Form for PV system data
    """
    pv_nord_fenster = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_nord_fenster'
        })
    )
    pv_nord_opak = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_nord_opak'
        })
    )
    pv_sued_fenster = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_sued_fenster'
        })
    )
    pv_sued_opak = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_sued_opak'
        })
    )
    pv_west_fenster = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_west_fenster'
        })
    )
    pv_west_opak = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_west_opak'
        })
    )
    pv_ost_fenster = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_ost_fenster'
        })
    )
    pv_ost_opak = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'pv_ost_opak'
        })
    )
    wirkungsgrad = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'name': 'wirkungsgrad'
        })
    )

class LueftungForm(forms.Form):
    """
    Form for ventilation system data
    """
    lueftungstyp = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'lueftungstyp'
        })
    )
    luftwechselrate = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'luftwechselrate'
        })
    )
    wrg_wirkungsgrad = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'name': 'wrg_wirkungsgrad'
        })
    )
    raum_soll_temp = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'raum_soll_temp'
        })
    )
    laufzeit_h_d = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'laufzeit_h_d'
        })
    )
    laufzeit_d_a = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'laufzeit_d_a'
        })
    )

class BeleuchtungForm(forms.Form):
    """
    Form for lighting system data
    """
    beleuchtungsart_buero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'beleuchtungsart_buero'
        })
    )
    regelungsart_buero = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'regelungsart_buero'
        })
    )
    e_soll_buero = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'e_soll_buero'
        })
    )
    laufzeit_h_d_buero = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'laufzeit_h_d_buero'
        })
    )
    laufzeit_d_a_buero = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'laufzeit_d_a_buero'
        })
    )
    beleuchtungsart_wohnen = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'beleuchtungsart_wohnen'
        })
    )
    regelungsart_wohnen = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'regelungsart_wohnen'
        })
    )
    e_soll_wohnen = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'e_soll_wohnen'
        })
    )
    laufzeit_h_d_wohnen = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'laufzeit_h_d_wohnen'
        })
    )
    laufzeit_d_a_wohnen = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'laufzeit_d_a_wohnen'
        })
    )

class WaermequellenForm(forms.Form):
    """
    Form for heat sources data
    """
    geraet1_anzahl = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'geraet1_anzahl'
        })
    )
    geraet1_leistung = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'geraet1_leistung'
        })
    )
    geraet1_betr_h_d = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'geraet1_betr_h_d'
        })
    )
    geraet1_betr_d_a = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'geraet1_betr_d_a'
        })
    )
    quelle1_anzahl = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'quelle1_anzahl'
        })
    )
    quelle1_leistung = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'quelle1_leistung'
        })
    )
    quelle1_betr_h_d = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'quelle1_betr_h_d'
        })
    )
    quelle1_betr_d_a = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'name': 'quelle1_betr_d_a'
        })
    )

class SDFForm(forms.Form):
    """
    Form for SDF (Sommerlicher Wärmeschutz) data
    """
    kritischer_raum = forms.ChoiceField(
        choices=[('opt1', 'Option 1'), ('opt2', 'Option 2')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'kritischer_raum'
        })
    )
    fassadenorientierung = forms.ChoiceField(
        choices=[('nord', 'Nord'), ('sued', 'Süd'), ('west', 'West'), ('ost', 'Ost')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'fassadenorientierung'
        })
    )
    sonnenschutzart = forms.ChoiceField(
        choices=[('opt1', 'Option 1'), ('opt2', 'Option 2')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'sonnenschutzart'
        })
    )
    verglasungsart = forms.ChoiceField(
        choices=[('zweifach', 'zweifach'), ('dreifach', 'dreifach'), ('zweifach_sonnenschutz', 'zweifach Sonnenschutzglas')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'verglasungsart'
        })
    )
    passive_kuehlung = forms.ChoiceField(
        choices=[('ja', 'Ja'), ('nein', 'Nein')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'name': 'passive_kuehlung'
        })
    )
    fensterneigung = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '1',
            'name': 'fensterneigung'
        })
    )

class GWPForm(forms.Form):
    """
    Form for GWP (Global Warming Potential) data
    """
    bauteil1_menge = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'bauteil1_menge'
        })
    )
    bauteil1_co2 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'bauteil1_co2'
        })
    )
    bauteil2_menge = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'bauteil2_menge'
        })
    )
    bauteil2_co2 = forms.FloatField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'name': 'bauteil2_co2'
        })
    )