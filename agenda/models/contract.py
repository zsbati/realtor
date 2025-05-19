from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .visit import Visit

class Contract(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('signed', 'Assinado'),
        ('cancelled', 'Cancelado'),
        ('expired', 'Expirado')
    ]

    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True, verbose_name='Visita Relacionada')
    contract_number = models.CharField(max_length=50, unique=True, verbose_name='Número do Contrato')
    contract_date = models.DateField(verbose_name='Data do Contrato')
    client_name = models.CharField(max_length=200, verbose_name='Nome do Cliente')
    property_address = models.CharField(max_length=500, verbose_name='Morada do Imóvel')
    transaction_type = models.CharField(max_length=10, choices=Visit.TRANSACTION_TYPES, verbose_name='Tipo de Transação')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')
    signed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracts_signed', verbose_name='Assinado por')
    signature_date = models.DateField(null=True, blank=True, verbose_name='Data da Assinatura')
    notes = models.TextField(blank=True, null=True, verbose_name='Notas')
    documents = models.FileField(upload_to='contracts/', blank=True, null=True, verbose_name='Documentos')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='contracts_created', verbose_name='Criado por')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f"Contrato #{self.contract_number} - {self.client_name}"

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['-contract_date']
