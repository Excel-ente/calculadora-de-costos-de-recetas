from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0003_alter_configuracion_tipo_de_cambio'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracion',
            name='redondeo_segunda_moneda',
            field=models.DecimalField(
                decimal_places=2,
                default=2,
                max_digits=5,
                help_text='Decimales para mostrar en segunda moneda. Usá 2 para centavos, 0 para enteros, -2 para redondear a centenas.',
            ),
        ),
    ]
