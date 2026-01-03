import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render
from django.views.decorators.http import require_http_methods
from .models import Lead


@require_http_methods(["PATCH", "POST"])
def mover_lead(request, pk):

    lead = get_object_or_404(Lead, pk=pk)

    data = json.loads(request.body.decode("utf-8"))
    etapa = data.get("etapa_funil")

    etapas_validas = dict(Lead.EtapaFunil.choices)
    if etapa not in etapas_validas:
        return JsonResponse({"erro": "Etapa inválida"}, status=400)

    lead.etapa_funil = etapa
    lead.save(update_fields=["etapa_funil"])

    return JsonResponse({"ok": True, "id": lead.id, "etapa_funil": lead.etapa_funil})



def kanban_funil(request):
    ctx = {
        "novos": Lead.objects.filter(etapa_funil=Lead.EtapaFunil.NOVO),
        "negociacao": Lead.objects.filter(etapa_funil=Lead.EtapaFunil.NEGOCIACAO),
        "convertido": Lead.objects.filter(etapa_funil=Lead.EtapaFunil.CONVERTIDO),
    }
    return render(request, "crm/kanban.html", ctx)

def get_lead_details(request, lead_id):
    try:
        lead = Lead.objects.get(id=lead_id)
        data = {

            'name': lead.name,
            'email': lead.email,
            'number': lead.number,
            'curso': lead.curso,
            # adicione outros campos conforme necessário
        }
        return JsonResponse(data)
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead não encontrado'}, status=404)