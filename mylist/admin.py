from django.contrib import admin
from .models import (
    BuildingProject,
    Gebaeude,
    Bauteil,
    KlimaregionTemperatur,
    DruckverlustLueftung,
    DruckverlustBauteil,
    SolarStrahlungMonat,
    SonnenschutzFaktor,
    SonneneintragsKennwert,
    Temperaturkorrekturfaktor
)

@admin.register(BuildingProject)
class BuildingProjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'standort', 'created')
    list_filter = ('created',)
    search_fields = ('standort',)
    ordering = ('-created',)

@admin.register(Gebaeude)
class GebaeudeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'laenge_ns', 'breite_ow', 'geschosse')
    search_fields = ('name',)
    fieldsets = (
        ('Geometrie', {
            'fields': ('name', 'laenge_ns', 'breite_ow', 'geschosshoehe', 'geschosse')
        }),
        ('Energiekennzahlen', {
            'fields': ('jahres_heizwert', 'tw_kwh_m2', 'luft_kwh_m2', 'bel_kwh_m2', 'nutz_kwh_m2')
        }),
        ('Verluste', {
            'fields': ('verteilungsverlust_kwh', 'speicherverlust_kwh', 'warmwasserbedarf_kwh')
        }),
    )

@admin.register(Bauteil)
class BauteilAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'laenge', 'breite', 'anz_geschosse')
    fieldsets = (
        ('Eingabedaten', {
            'fields': ('laenge', 'breite', 'geschosshoehe', 'anz_geschosse')
        }),
        ('U-Werte', {
            'fields': ('u_wand_nord', 'u_wand_sued', 'u_wand_west', 'u_wand_ost', 'u_bodenplatte', 'u_dach')
        }),
        ('Berechnungsergebnisse', {
            'fields': ('hoehe', 'volumen', 'bgf', 'nf', 'ne_absolut', 'ne_spez', 'sb_absolut', 'sb_spez', 'wb_absolut', 'ee_absolut', 'ee_spez')
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(KlimaregionTemperatur)
class KlimaregionTemperaturAdmin(admin.ModelAdmin):
    list_display = ('region', 'referenzort', 'jahreswert')
    search_fields = ('referenzort',)
    list_filter = ('region',)

@admin.register(DruckverlustLueftung)
class DruckverlustLueftungAdmin(admin.ModelAdmin):
    list_display = ('bauteil', 'druckverlust_normal')
    search_fields = ('bauteil',)

@admin.register(DruckverlustBauteil)
class DruckverlustBauteilAdmin(admin.ModelAdmin):
    list_display = ('bauteil', 'druckverlust_pa')
    search_fields = ('bauteil',)

@admin.register(SolarStrahlungMonat)
class SolarStrahlungMonatAdmin(admin.ModelAdmin):
    list_display = ('orientierung', 'neigung', 'jahreswert')
    list_filter = ('orientierung', 'neigung')

@admin.register(SonnenschutzFaktor)
class SonnenschutzFaktorAdmin(admin.ModelAdmin):
    list_display = ('zeile', 'sonnenschutzvorrichtung', 'f_c_g_le_0_40_zweifach')
    search_fields = ('zeile', 'sonnenschutzvorrichtung')

@admin.register(SonneneintragsKennwert)
class SonneneintragsKennwertAdmin(admin.ModelAdmin):
    list_display = ('typ', 'kennwert_key', 'beschreibung', 'bauart')
    list_filter = ('typ', 'bauart')
    search_fields = ('kennwert_key', 'beschreibung')

@admin.register(Temperaturkorrekturfaktor)
class TemperaturkorrekturfaktorAdmin(admin.ModelAdmin):
    list_display = ('bauteil', 'fx')
    search_fields = ('bauteil',)