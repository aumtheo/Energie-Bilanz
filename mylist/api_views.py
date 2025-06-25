from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .berechnungen import (
    berechne_gebaeudedaten,
    berechne_nutzenergiebedarf,
    berechne_strombedarf,
    berechne_waermebedarf,
    berechne_endenergiebedarf,
)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_berechnung(request):
    """
    API endpoint for real-time building energy calculations
    """
    try:
        if request.method == "GET":
            params = request.GET
        else:
            data = json.loads(request.body)
            params = data
        
        # Extract building parameters with defaults
        laenge = float(params.get("laenge", 0))
        breite = float(params.get("breite", 0))
        geschosshoehe = float(params.get("geschosshoehe", 2.7))
        anz_geschosse = int(params.get("anz_geschosse", 1))
        
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