from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Contract(models.Model):
    CONTRACT_TYPES = [
        ('buy', 'Compra'),
        ('rent', 'Arrendamento'),
        ('lease', 'Aluguer'),
        ('sell', 'Venda')
    ]

    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('signed', 'Assinado'),
        ('cancelled', 'Cancelado')
    ]

    title = models.CharField(max_length=200, default='Contrato Imobiliário', verbose_name='Título')
    contract_type = models.CharField(max_length=10, choices=CONTRACT_TYPES, default='buy', verbose_name='Tipo de Contrato')
    client_name = models.CharField(max_length=200, verbose_name='Nome do Cliente')
    property_address = models.CharField(max_length=500, verbose_name='Morada da Propriedade')
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Criado por')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    comment = models.TextField(blank=True, null=True, verbose_name='Comentários')
    signing_date = models.DateField(blank=True, null=True, verbose_name='Data de Assinatura')

    def __str__(self):
        return f"{self.title} - {self.get_contract_type_display()}"

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-created_at']
