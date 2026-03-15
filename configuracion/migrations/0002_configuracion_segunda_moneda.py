from django.db import migrations, models
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='habilitar_segunda_moneda',
            field=models.BooleanField(
                default=False,
                help_text='Activá esta opción para mostrar precios en dos monedas en todo el sistema.',
            ),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='segunda_moneda',
            field=models.CharField(
                blank=True,
                default='USD',
                max_length=10,
                help_text='Símbolo o código de la segunda moneda (ej: USD, €, BTC).',
            ),
        ),
        migrations.AddField(
            model_name='configuracion',
            name='tipo_de_cambio',
            field=models.DecimalField(
                decimal_places=6,
                default=Decimal('1'),
                max_digits=18,
                help_text='Cuántas unidades de moneda principal equivalen a 1 unidad de segunda moneda. Ej: si 1 USD = 1000 $, ingresá 1000.',
            ),
        ),
    ]
