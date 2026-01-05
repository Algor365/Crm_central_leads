import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render,redirect
from django.views.decorators.http import require_http_methods
from .models import Lead
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .forms import LeadForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@require_http_methods(["PATCH", "PUT"])
def editar_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"erro": "JSON inválido"}, status=400)

    # campos permitidos
    allowed = {"name", "email", "number", "curso", "etapa_funil"}

    for field, value in data.items():
        if field not in allowed:
            continue

        if field == "etapa_funil":
            etapas_validas = dict(Lead.EtapaFunil.choices)
            if value not in etapas_validas:
                return JsonResponse({"erro": "Etapa inválida"}, status=400)

        setattr(lead, field, value)

    lead.save()

    return JsonResponse({
        "ok": True,
        "lead": {
            "id": lead.id,
            "name": lead.name,
            "email": lead.email,
            "number": lead.number,
            "curso": lead.curso,
            "etapa_funil": lead.etapa_funil,
        }
    })


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect("kanban-funil")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("kanban-funil")

        messages.error(request, "Usuário ou senha inválidos.")

    return render(request, "crm/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@require_http_methods(["DELETE"])
def deletar_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    lead.delete()
    return JsonResponse({"ok": True, "deleted_id": pk})


def landing_lead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()

            # Se for requisição AJAX
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({
                    "success": True,
                    "lead": {
                        "id": lead.id,
                        "name": lead.name,
                        "number": lead.number,
                        "email": lead.email,
                        "curso": lead.curso,
                    }
                })

        # erro
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)

    # GET normal
    form = LeadForm()
    return render(request, "crm/landing_page.html", {"form": form})





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
    
def listar_leads(request):
    etapa = request.GET.get("etapa_funil")  # opcional: novo/negociacao/convertido

    qs = Lead.objects.all().order_by("-id")

    if etapa:
        qs = qs.filter(etapa_funil=etapa)

    data = list(qs.values("id", "name", "email", "number", "curso", "etapa_funil"))
    return JsonResponse(data, safe=False)
