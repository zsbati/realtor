from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Visit(models.Model):
    VISIT_TYPES = [
        ('visit', 'Visita Presencial'),
        ('phone', 'Telefone'),
        ('email', 'Email')
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('forgotten', 'Esquecido')
    ]

    title = models.CharField(max_length=200, verbose_name='Título')
    name = models.CharField(max_length=200, verbose_name='Nome')
    address = models.CharField(max_length=500, verbose_name='Morada', blank=True, null=True)
    description = models.TextField(verbose_name='Descrição', blank=True, null=True)
    visit_type = models.CharField(max_length=10, choices=VISIT_TYPES, default='visit', verbose_name='Tipo de Visita')
    scheduled_date = models.DateTimeField(verbose_name='Data/Hora Agendada')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='Status')
    email = models.EmailField(verbose_name='Email', blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name='Telefone', blank=True, null=True)
    comment = models.TextField(verbose_name='Comentários', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Criado por')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Criado em')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Atualizado em')
    price = models.CharField(max_length=100, verbose_name='Preço', blank=True, null=True, help_text='Exemplo: 750-800 euros')
    TRANSACTION_TYPES = [
        ('vender', 'Vender'),
        ('arrendar', 'Arrendar'),
        ('alugar', 'Alugar'),
        ('comprar', 'Comprar')
    ]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, verbose_name='Tipo de Transação')

    def __str__(self):
        return f"{self.title} - {self.name} ({self.get_visit_type_display()})"

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'
        ordering = ['-scheduled_date']
    
    def save(self, *args, **kwargs):
        # Ensure scheduled_date is timezone-aware
        if self.scheduled_date:
            if timezone.is_naive(self.scheduled_date):
                # If naive, make it aware using the current timezone
                self.scheduled_date = timezone.make_aware(
                    self.scheduled_date,
                    timezone.get_current_timezone()
                )
            # Ensure it's in the current timezone
            self.scheduled_date = timezone.localtime(self.scheduled_date)
        
        # Update updated_at timestamp with timezone-aware datetime
        self.updated_at = timezone.now()
        
        try:
            super().save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(f"Error saving visit: {str(e)}")
