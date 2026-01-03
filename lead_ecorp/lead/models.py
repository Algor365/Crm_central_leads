from django.db import models


class Lead(models.Model):
    class EtapaFunil(models.TextChoices):
        NOVO = "novo", "Novo"
        NEGOCIACAO = "negociacao", "Negociação"
        CONVERTIDO = "convertido", "Convertido"

    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    number = models.CharField(max_length=20)
    curso = models.TextField(blank=True)

    etapa_funil = models.CharField(
        max_length=15,
        choices=EtapaFunil.choices,
        default=EtapaFunil.NOVO,
        db_index=True,
    )

    def __str__(self):
        return f"{self.name} - {self.get_etapa_funil_display()}"
