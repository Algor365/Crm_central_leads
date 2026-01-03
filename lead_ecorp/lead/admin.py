# app/admin.py
from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    # colunas que aparecem na listagem
    list_display = ("id", "name", "email", "number", "etapa_funil")

    # filtros na lateral
    list_filter = ("etapa_funil",)

    # barra de busca
    search_fields = ("name", "email", "number")

    # permite editar direto na tabela (sem abrir o registro)
    list_editable = ("etapa_funil",)

    # ordenação padrão
    ordering = ("-id",)

    # campos só leitura (opcional)
    readonly_fields = ("id",)

    # organização do formulário ao abrir o Lead
    fieldsets = (
        ("Dados do Lead", {"fields": ("name", "email", "number", "curso")}),
        ("Funil", {"fields": ("etapa_funil",)}),
    )
