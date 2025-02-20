# Generated by Django 5.0 on 2024-09-11 23:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id_are', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_are', models.CharField(max_length=50, unique=True)),
                ('estado_are', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_area',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id_carg', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_carg', models.CharField(max_length=50)),
                ('estado_carg', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_cargo',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id_doc', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_doc', models.CharField(max_length=50)),
                ('estado_doc', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_documento',
            },
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id_est', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_est', models.CharField(max_length=50)),
                ('estado_est', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_estudio',
            },
        ),
        migrations.CreateModel(
            name='Fiscal',
            fields=[
                ('id_fis', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_fis', models.CharField(max_length=20, verbose_name='Nombre')),
                ('apellidoP_fis', models.CharField(default='S/n', max_length=30, verbose_name='ApellidoP')),
                ('estado_fis', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_fiscal',
            },
        ),
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id_par', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_par', models.CharField(max_length=30, verbose_name='Nombre')),
                ('estado_par', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_parentesco',
            },
        ),
        migrations.CreateModel(
            name='Profesion',
            fields=[
                ('id_prof', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_prof', models.CharField(max_length=50)),
                ('estado_prof', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_profesion',
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id_zon', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_zon', models.CharField(max_length=50)),
                ('estado_zon', models.PositiveIntegerField(default=1)),
            ],
            options={
                'db_table': 'admrrhh_zona',
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id_per', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_per', models.CharField(max_length=20, verbose_name='Nombre')),
                ('apellidoP_per', models.CharField(default='S/n', max_length=20, verbose_name='ApellidoP')),
                ('apellidoM_per', models.CharField(default='S/n', max_length=20, verbose_name='ApellidoM')),
                ('telf_per', models.CharField(max_length=10, verbose_name='Telefono')),
                ('sexo_per', models.CharField(max_length=20, verbose_name='Tipo de sexo')),
                ('numDoc_per', models.CharField(default='0', max_length=15, verbose_name='Numero de documento')),
                ('exteDoc_per', models.CharField(max_length=6, verbose_name='Extension de documento')),
                ('fechNac_per', models.CharField(max_length=10, verbose_name='Fecha de Nacimiento ')),
                ('venDoc_per', models.CharField(max_length=10, verbose_name='Fecha vencimiento de documento')),
                ('lugarNac_per', models.CharField(max_length=30, verbose_name='Lugar de nacimiento')),
                ('sangre_per', models.CharField(max_length=10, verbose_name='Tipo de sangre')),
                ('estCivil_per', models.CharField(max_length=20, verbose_name='Estado civil')),
                ('imagen_per', models.ImageField(default='S/n', null=True, upload_to='imagenesPer/', verbose_name='Imagen')),
                ('direccion_per', models.CharField(default='S/n', max_length=100, verbose_name='Direccion')),
                ('estado_per', models.PositiveIntegerField(default=1)),
                ('documento_per', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.documento')),
            ],
            options={
                'db_table': 'admrrhh_persona',
            },
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id_perl', models.AutoField(primary_key=True, serialize=False)),
                ('hijos_perl', models.PositiveIntegerField(default=0)),
                ('fechIngre_perl', models.CharField(max_length=10, verbose_name='Fecha de ingreso')),
                ('licCond_perl', models.CharField(max_length=2, verbose_name='Licencia de conducir')),
                ('tipoLic_perl', models.CharField(blank=True, max_length=5, null=True, verbose_name='Tipo de Licencia')),
                ('fechVenlic_perl', models.CharField(blank=True, max_length=10, null=True, verbose_name='Fecha vencimiento de licencia')),
                ('ctaBanc_perl', models.CharField(default='0', max_length=20, verbose_name='Cuenta Bancaria')),
                ('nua_perl', models.CharField(default='0', max_length=20, verbose_name='Cuenta Nua')),
                ('ctaAfp_perl', models.CharField(max_length=20, verbose_name='Cuenta Afp')),
                ('aseg_perl', models.CharField(default='0', max_length=20, verbose_name='Numero de seguro')),
                ('sueldo_perl', models.FloatField(default=0)),
                ('estado_perl', models.PositiveIntegerField(default=1)),
                ('area_perl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.area')),
                ('cargo_perl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.cargo')),
                ('estudio_perl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.estudio')),
                ('persona_perl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.persona')),
                ('profesion_perl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.profesion')),
            ],
            options={
                'db_table': 'admrrhh_personal',
            },
        ),
        migrations.CreateModel(
            name='Familiar',
            fields=[
                ('id_fam', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_fam', models.CharField(max_length=20, verbose_name='Nombre')),
                ('apellidoP_fam', models.CharField(max_length=30, verbose_name='ApellidoP')),
                ('telef_fam', models.CharField(max_length=10, verbose_name='Telefono')),
                ('nota_fam', models.CharField(default='S/n', max_length=100, verbose_name='nota')),
                ('estado_fam', models.PositiveIntegerField(default=1)),
                ('parentesco_fam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.parentesco')),
                ('personal_fam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.personal')),
            ],
            options={
                'db_table': 'admrrhh_familiar',
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id_proy', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_proy', models.CharField(max_length=20, verbose_name='Nombre')),
                ('grafo_proy', models.CharField(default='S/n', max_length=20, verbose_name='Grafo')),
                ('trafo_proy', models.CharField(default='S/n', max_length=20, verbose_name='Trafo')),
                ('ubicacion_proy', models.CharField(default='S/n', max_length=100, verbose_name='Ubicacion')),
                ('nota_proy', models.CharField(default='S/n', max_length=100, verbose_name='Nota')),
                ('fechaRecep_proy', models.CharField(max_length=10, verbose_name='Fecha de registro')),
                ('fechaDisen_proy', models.CharField(max_length=10, verbose_name='Fecha de diseño')),
                ('fechaConst_proy', models.CharField(max_length=10, verbose_name='Fecha de construccion')),
                ('estado_proy', models.PositiveIntegerField(default=1)),
                ('fiscal_proy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.fiscal')),
            ],
            options={
                'db_table': 'admrrhh_proyecto',
            },
        ),
        migrations.CreateModel(
            name='Ordent',
            fields=[
                ('id_ord', models.AutoField(primary_key=True, serialize=False)),
                ('nota_ord', models.CharField(default='S/N', max_length=100, verbose_name='Nota')),
                ('numero_ord', models.CharField(max_length=12, verbose_name='Numero de orden')),
                ('numeroCaj_ord', models.CharField(max_length=5, verbose_name='Numero de caja')),
                ('estado_ord', models.PositiveIntegerField(default=1)),
                ('proyecto_ord', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.proyecto')),
            ],
            options={
                'db_table': 'admrrhh_ordent',
            },
        ),
        migrations.CreateModel(
            name='Envio',
            fields=[
                ('id_env', models.AutoField(primary_key=True, serialize=False)),
                ('nota_env', models.CharField(default='S/N', max_length=100, verbose_name='nota')),
                ('fechaEnv_env', models.CharField(max_length=10, verbose_name='Fecha envio')),
                ('cronograma_env', models.BooleanField(default=False, verbose_name='Cronograma')),
                ('estacado_env', models.BooleanField(default=False, verbose_name='Hoja Estacado')),
                ('plano_env', models.BooleanField(default=False, verbose_name='Plano')),
                ('puntoPunto_env', models.BooleanField(default=False, verbose_name='Punto a punto')),
                ('manoObra_env', models.BooleanField(default=False, verbose_name='Mano de obra')),
                ('resplado_env', models.BooleanField(default=False, verbose_name='Respaldo')),
                ('estado_env', models.PositiveIntegerField(default=1)),
                ('proyecto_env', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.proyecto')),
            ],
            options={
                'db_table': 'admrrhh_envio',
            },
        ),
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id_asig', models.AutoField(primary_key=True, serialize=False)),
                ('nota_asig', models.CharField(default='S/n', max_length=100, verbose_name='Nota')),
                ('fechaIni_asig', models.CharField(max_length=10, verbose_name='Fecha inicio')),
                ('fechaFin_asig', models.CharField(blank=True, max_length=10, null=True, verbose_name='Fecha fin')),
                ('estado_asig', models.PositiveIntegerField(default=1)),
                ('personal_asig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.personal')),
                ('proyecto_asig', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.proyecto')),
            ],
            options={
                'db_table': 'admrrhh_asignacion',
            },
        ),
        migrations.AddField(
            model_name='fiscal',
            name='zona_fis',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admRrhh.zona'),
        ),
    ]
