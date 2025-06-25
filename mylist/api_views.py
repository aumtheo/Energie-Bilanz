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
        
        # Extract building parameters
        laenge = float(params.get("laenge", 0))
        breite = float(params.get("breite", 0))
        geschosshoehe = float(params.get("geschosshoehe", 0))
        anz_geschosse = int(params.get("anz_geschosse", 0))
        
        # Calculate building data
        geb = berechne_gebaeudedaten(laenge, breite, geschosshoehe, anz_geschosse)
        
        # Extract energy parameters
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

@csrf_exempt
@require_http_methods(["POST"])
def api_save_project(request):
    """
    API endpoint to save project data
    """
    try:
        data = json.loads(request.body)
        
        # Here you would save the project data to the database
        # For now, we'll just return success
        
        return JsonResponse({
            "success": True,
            "message": "Project saved successfully",
            "project_id": 1  # Would be the actual saved project ID
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def api_climate_data(request):
    """
    API endpoint to get climate data for a specific location
    """
    try:
        location = request.GET.get('location', '')
        
        # Here you would query your climate data
        # For now, return sample data
        
        return JsonResponse({
            "success": True,
            "location": location,
            "temperature_data": {
                "jan": 2.1, "feb": 2.8, "mar": 5.4,
                "apr": 8.8, "mai": 13.1, "jun": 16.2,
                "jul": 18.0, "aug": 17.8, "sep": 14.8,
                "okt": 10.8, "nov": 6.2, "dez": 3.2,
                "jahreswert": 9.9
            }
        })
        
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)