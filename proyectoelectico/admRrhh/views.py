from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import os
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from .models import  Area, Cargo, Documento, Estudio, Profesion, Persona, Personal, Zona, Fiscal, Proyecto, Asignacion,Parentesco, Familiar, Envio, Ordent
from django.db.models import Q, F
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from django.template import Context
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.utils import timezone
from django.db.models import Count
from datetime import datetime
from io import BytesIO
from django.contrib.auth.hashers import make_password
from django import template
from xhtml2pdf import pisa
from django.template.loader import get_template

def iniciar(resquest):
    return render(resquest, 'registration/login_ini.html')
@login_required
def base(resquest):
    return render(resquest, 'index.html')
def user_login(resquest):
    if resquest.method == 'POST':
        username = resquest.POST.get('username')
        password = resquest.POST.get('password')
        user = authenticate(resquest, username=username, password=password)
        if  user is not None:
            login(resquest, user)
            return redirect('base') 
        else:
            return render(resquest, 'registration/login.html')
    return render(resquest, 'registration/login.html')

def logout_view(resquest):
    logout(resquest)
   
    return redirect('iniciar')
#///////Area
@login_required
def areLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_area'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    areas= Area.objects.filter(estado_are =1).order_by('-id_are') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        areas = Area.objects.filter(
            Q(nombre_are__icontains=busqueda)
        ).distinct()

    elementos_por_pagina = 12
    paginator = Paginator(areas, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        areas = paginator.page(page)
    except PageNotAnInteger:
        areas = paginator.page(1)
    except EmptyPage:
        
        areas = paginator.page(paginator.num_pages)
    return render(resquest, 'area/lista.html', {'areas': areas})

def areCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_area'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'area/crear.html')

def areGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_are"]
        if Area.objects.filter(nombre_are__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'area/crear.html',context)
        areas = Area.objects.create(nombre_are=nombre.capitalize())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('areLista')
    else:
            return redirect('areLista')  
   
def areGuardarM(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_are"]
        if Area.objects.filter(nombre_are__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")

            return redirect('perlCrear')
        areas = Area.objects.create(nombre_are=nombre.capitalize())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('perlCrear')
    else:
        return redirect('perlLista')  
def areEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_area'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Area.objects.get(id_are=id)
    return render(resquest, 'area/editar.html', {'codigo': codigo})
def areActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_are"]
        area = Area.objects.get(id_are=id)
        if Area.objects.exclude(id_are=id).filter(nombre_are__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('areEditar', area.id_are)

        area.nombre_are = nuevo_nombre.capitalize()
        area.save()
        messages.success(resquest, "Se actualizó correctamente el área.")
        return redirect('areLista')
    else:
        return render(resquest, 'area/editar.html', {'area': area})

def areEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_area'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    area = Area.objects.get(id_are=id)
    area.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('areLista')
#///////Cargo
@login_required
def cargLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_cargo'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    cargos = Cargo.objects.filter(estado_carg=1)
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        cargos = Cargo.objects.filter(
            Q(nombre_carg__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(cargos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        cargos = paginator.page(page)
    except PageNotAnInteger:
        cargos = paginator.page(1)
    except EmptyPage:
        cargos = paginator.page(paginator.num_pages)
    return render(resquest,'cargo/lista.html', {'cargos':cargos})
def cargCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_cargo'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'cargo/crear.html')
def cargGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_carg"]
        if Cargo.objects.filter(nombre_carg__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'cargo/crear.html',context)
        cargos = Cargo.objects.create(nombre_carg=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('cargLista')
    else:
        return redirect('cargLista')  
def cargGuardarM(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_carg"]
        if Cargo.objects.filter(nombre_carg__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")

            return redirect('perlCrear')
        cargos = Cargo.objects.create(nombre_carg=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('perlCrear')
    else:
        return redirect('perlLista') 
def cargEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_cargo'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Cargo.objects.get(id_carg=id)
    return render(resquest, 'cargo/editar.html', {'codigo': codigo})
def cargActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_carg"]
        cargo = Cargo.objects.get(id_carg=id)
        if Cargo.objects.exclude(id_carg=id).filter(nombre_carg__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('cargEditar', cargo.id_carg)
        cargo.nombre_carg = nuevo_nombre.title()
        cargo.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('cargLista')
    else:
        return render(resquest, 'cargo/editar.html',{'cargo': cargo})
def cargEliminar(resquest,id):
    if not resquest.user.has_perm('admRrhh.delete_cargo'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    cargo = Cargo.objects.get(id_carg=id)
    cargo.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('cargLista')
# DOCUMENTO/////////////////////////////////////////////////////////
@login_required
def docLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_documento'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    try:
        documentos = Documento.objects.filter(estado_doc=1).order_by('-id_doc')
        busqueda = resquest.GET.get("buscar")
        if busqueda:
            documentos = Documento.objects.filter(
                Q(nombre_doc__icontains=busqueda)
            ).distinct()
        elementos_por_pagina = 12
        paginator = Paginator(documentos, elementos_por_pagina)
        page = resquest.GET.get("page", 1)

        try:
            documentos = paginator.page(page)
        except PageNotAnInteger:
            documentos = paginator.page(1)
        except EmptyPage:
            documentos = paginator.page(paginator.num_pages)

        usuario_actual = resquest.user
        return render(resquest, 'documento/lista.html', {'documentos': documentos})
    except PermissionDenied:
        return render(resquest, 'base.html')
def docCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_documento'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'documento/crear.html')
def docGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_doc"]
        if Documento.objects.filter(nombre_doc__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'documento/crear.html',context)
        documentos = Documento.objects.create(nombre_doc=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('docLista')
    else:
        return redirect('docLista')  
def docEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_documento'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Documento.objects.get(id_doc=id)
    return render(resquest, 'documento/editar.html', {'codigo': codigo})
def docActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_doc"]
        documentos = Documento.objects.get(id_doc=id)
        if Documento.objects.exclude(id_doc=id).filter(nombre_doc__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('docEditar', documentos.id_doc)
        documentos.nombre_doc = nuevo_nombre.title()
        documentos.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('docLista')
    else:
        return render(resquest, 'documento/editar.html', {'documentos': documentos})
def docEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_documento'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    docum = Documento.objects.get(id_doc=id)
    docum.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('docLista')
# ESTUDIO/////////////////////////////////////////////////////////
@login_required
def estLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_estudio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    estudios = Estudio.objects.filter(estado_est = 1).order_by('-id_est') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        estudios = Estudio.objects.filter(
            Q(nombre_est__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(estudios, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         estudios = paginator.page(page)
    except PageNotAnInteger:
        estudios = paginator.page(1)
    except EmptyPage:
        estudios = paginator.page(paginator.num_pages)
    return render(resquest, 'estudio/lista.html', {'estudios': estudios})
    
def estCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_estudio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'estudio/crear.html')
def estGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_est"]
        if Estudio.objects.filter(nombre_est__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'estudio/crear.html',context)
        estudios = Estudio.objects.create(nombre_est=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('estLista')
    else:
        return redirect('estLista') 
def estEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_estudio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Estudio.objects.get(id_est=id)
    return render(resquest, 'estudio/editar.html', {'codigo': codigo})
def estActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_est"]
        estudios = Estudio.objects.get(id_est=id)
        if Estudio.objects.exclude(id_est=id).filter(nombre_est__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('estEditar', estudios.id_est)

        estudios.nombre_est = nuevo_nombre.title()
        estudios.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('estLista')
    else:
        return render(resquest, 'estudio/editar.html', {'estudios': estudios})
def estEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_estudio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    estudio = Estudio.objects.get(id_est=id)
    estudio.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('estLista')
#PROFESION/////////////////////////////////////////////////////////
@login_required
def profLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_profesion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 

    profesiones = Profesion.objects.filter(estado_prof = 1).order_by('-id_prof') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        profesiones = Profesion.objects.filter(
            Q(nombre_prof__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(profesiones, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         profesiones = paginator.page(page)
    except PageNotAnInteger:
        profesiones = paginator.page(1)
    except EmptyPage:
        profesiones = paginator.page(paginator.num_pages)
    return render(resquest, 'profesion/lista.html', {'profesiones': profesiones})
def profCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_profesion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'profesion/crear.html')
def profGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_prof"]
        if Profesion.objects.filter(nombre_prof__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'profesion/crear.html',context)
        profesiones = Profesion.objects.create(nombre_prof=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('profLista')
    else:
        return redirect('profLista')  
def profGuardarM(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_prof"]
        if Profesion.objects.filter(nombre_prof__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")

            return redirect('perlCrear')
        profesiones = Profesion.objects.create(nombre_prof=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('perlCrear')
    else:
            
            return redirect('perlLista')  
def profEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_profesion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Profesion.objects.get(id_prof=id)
    return render(resquest, 'profesion/editar.html', {'codigo': codigo})
def profActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_prof"]
        profesiones = Profesion.objects.get(id_prof=id)
        if Profesion.objects.exclude(id_prof=id).filter(nombre_prof__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('profEditar', profesiones.id_prof)

        profesiones.nombre_prof = nuevo_nombre.title()
        profesiones.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('profLista')
    else:
        return render(resquest, 'profesion/editar.html', {'profesiones': profesiones})
def profEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_profesion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    profes = Profesion.objects.get(id_prof=id)
    profes.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('profLista')
# PARENTESCO/////////////////////////////////////////////////////////
@login_required
def parLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_parentesco'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    parentescos = Parentesco.objects.filter(estado_par = 1).order_by('-id_par') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        parentescos = Parentesco.objects.filter(
            Q(nombre_par__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(parentescos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        parentescos = paginator.page(page)
    except PageNotAnInteger:
        parentescos = paginator.page(1)
    except EmptyPage:
        parentescos = paginator.page(paginator.num_pages)
    return render(resquest, 'parentesco/lista.html', {'parentescos': parentescos})
def parCrear(resquest):
    if not resquest.user.has_perm('admRrhh.view_parentesco'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'parentesco/crear.html')
def parGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_par"]
        if Parentesco.objects.filter(nombre_par__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'parentesco/crear.html',context)
        parentescos = Parentesco.objects.create(nombre_par=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('parLista')
    else:
            return redirect('parLista') 
def parEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_parentesco'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Parentesco.objects.get(id_par=id)
    return render(resquest, 'parentesco/editar.html', {'codigo': codigo})
def parActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_par"]
        parentescos= Parentesco.objects.get(id_par=id)
        if Parentesco.objects.exclude(id_par=id).filter(nombre_par__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('parEditar', parentescos.id_par)
        parentescos.nombre_par = nuevo_nombre.title()
        parentescos.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('parLista')
    else:
        return render(resquest, 'parentesco/editar.html', {'parentescos': parentescos})
def parEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_parentesco'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    parentesco = Parentesco.objects.get(id_par=id)
    parentesco.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('parLista')
# FAMILIA/////////////////////////////////////////////////////////
@login_required
def famLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_familiar'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personas = Persona.objects.all()
    personales = Personal.objects.all()
    familiares = Familiar.objects.filter(estado_fam = 1).order_by('-id_fam') 
    parentescos = Parentesco.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        familiares = Familiar.objects.filter(
            Q(nombre_fam__icontains=busqueda) |
            Q(personal_fam__persona_perl__nombre_per__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(familiares, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        familiares = paginator.page(page)
    except PageNotAnInteger:
        familiares = paginator.page(1)
    except EmptyPage:
        familiares = paginator.page(paginator.num_pages)
    return render(resquest, 'familiar/lista.html', {'familiares': familiares,'personas': personas,'personales': personales,'parentescos': parentescos})
def famCrear(resquest):
    if not resquest.user.has_perm('admRrhh.view_familiar'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    familiares = Familiar.objects.all()
    proyectos = Proyecto.objects.all()
    personas = Persona.objects.all()
    personales = Personal.objects.all()
    parentescos = Parentesco.objects.all()
    return render(resquest, 'familiar/crear.html', {'familiares': familiares, 'proyectos': proyectos, 'personas': personas,'parentescos': parentescos,'personales': personales})
def famGuardar(resquest):
    nombre= resquest.POST["nombre_fam"]
    apellidoP = resquest.POST["apellidoP_fam"]
    telef = resquest.POST["telef_fam"]
    nota = resquest.POST["nota_fam"]
    idpersona = resquest.POST["personal_fam"]
    idparentesco = resquest.POST["parentesco_fam"]
    familiares = Familiar.objects.create(
    nombre_fam=nombre.title(),
    apellidoP_fam=apellidoP.title(),
    telef_fam=telef,
    nota_fam=nota.capitalize(),
    personal_fam_id=idpersona,
    parentesco_fam_id=idparentesco)
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('famLista')
def famEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_familiar'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.all()
    personas = Persona.objects.all()
    personales = Personal.objects.all()
    parentescos = Parentesco.objects.filter(estado_par=1)
    codigo = Familiar.objects.get(id_fam=id)
    return render(resquest, 'familiar/editar.html', {'codigo': codigo, 'proyectos': proyectos, 'personas': personas, 'personales': personales, 'parentescos': parentescos})
def famActualizar(resquest, id):
    nombre= resquest.POST["nombre_fam"]
    apellidoP = resquest.POST["apellidoP_fam"]
    telef = resquest.POST["telef_fam"]
    nota = resquest.POST["nota_fam"]
    idpersona = resquest.POST["personal_fam"]
    idparentesco = resquest.POST["parentesco_fam"]
    if Familiar.objects.exclude(id_fam=id).filter(nombre_fam__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('famEditar', familiar.id_fam)
    familiar = Familiar.objects.get(id_fam=id)
    familiar.nombre_fam=nombre.title()
    familiar.apellidoP_fam=apellidoP.title()
    familiar.telef_fam=telef
    familiar.nota_fam=nota.capitalize()
    familiar.personal_fam_id=idpersona
    familiar.parentesco_fam_id=idparentesco
    familiar.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('famLista')
def famEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_familiar'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    familiar = Familiar.objects.get(id_fam=id)
    familiar.estado_fam = 0
    familiar.save()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('famLista')
# PERSONA/////////////////////////////////////////////////////////
@login_required
def perLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_persona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personas = Persona.objects.filter(estado_per = 1).order_by('-id_per') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        personas = Persona.objects.filter(
            Q(nombre_per__icontains=busqueda)|
            Q(apellidoP_per__icontains=busqueda)|
            Q(apellidoM_per__icontains=busqueda)| 
            Q(direccion_per__icontains=busqueda) 
        ).distinct()
    elementos_por_pagina = 10
    paginator = Paginator(personas, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
        personas = paginator.page(page)
    except PageNotAnInteger:
        personas = paginator.page(1)
    except EmptyPage:
        personas = paginator.page(paginator.num_pages)
    return render(resquest, 'persona/lista.html', {'personas': personas})
def perCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_persona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personas = Persona.objects.all()
    documentos = Documento.objects.filter(estado_doc = 1)
    return render(resquest, 'persona/crear.html', {'personas': personas, 'documentos': documentos})
def perGuardar(resquest):
    if resquest.method == 'POST':
        idocumento = resquest.POST["doc_per"]
        nombreP = resquest.POST["nombre_per"]
        apellidoP = resquest.POST["apellidoP_per"]
        apellidoM = resquest.POST["apellidoM_per"]
        telefono = resquest.POST["telf_per"]
        sexo = resquest.POST["sexo_per"]
        numDoc = resquest.POST["numDoc_per"]
        fechNac = resquest.POST["fechNac_per"]
        venDoc = resquest.POST["venDoc_per"]
        exteDoc = resquest.POST["exteDoc_per"]
        lugarNac = resquest.POST["lugarNac_per"]
        sangre = resquest.POST["sangre_per"]
        estCivil = resquest.POST["estCivil_per"]
        foto = resquest.FILES.get("foto_per")
        direccion = resquest.POST["direccion_per"]
        if Persona.objects.filter(nombre_per=nombreP, apellidoP_per=apellidoP).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'persona/crear.html',context)
        personas = Persona.objects.create(nombre_per=nombreP.title(),
                                        apellidoP_per=apellidoP.capitalize(),
                                        apellidoM_per=apellidoM.capitalize(),
                                        telf_per=telefono,
                                        sexo_per=sexo.capitalize(),
                                        numDoc_per=numDoc,
                                        fechNac_per=fechNac,
                                        venDoc_per=venDoc,
                                        exteDoc_per=exteDoc.upper(),
                                        lugarNac_per=lugarNac.capitalize(),
                                        sangre_per=sangre.upper(),
                                        estCivil_per=estCivil.capitalize(),
                                        imagen_per=foto,
                                        direccion_per=direccion.capitalize(),
                                        documento_per_id=idocumento)
           
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('perLista')
    else:
        return redirect('perLista') 

def perEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_persona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    documentos = Documento.objects.all()
    codigo = Persona.objects.get(id_per=id)
    return render(resquest, 'persona/editar.html', {'codigo': codigo, 'documentos': documentos})
def perTarjeta(resquest, id):
    documentos = Documento.objects.all()
    codigo = Persona.objects.get(id_per=id)
    return render(resquest, 'persona/tarjeta.html', {'codigo': codigo, 'documentos': documentos})
def perActualizar(resquest, id):
    if resquest.method == 'POST':
        nombreP = resquest.POST["nombre_per"]
        idocumento = resquest.POST["doc_per"]
        apellidoP = resquest.POST["apellidoP_per"]
        apellidoM = resquest.POST["apellidoM_per"]
        telf = resquest.POST["telf_per"]
        sexo = resquest.POST["sexo_per"]
        numDoc = resquest.POST["numDoc_per"]
        fechNac = resquest.POST["fechNac_per"]
        venDoc = resquest.POST["venDoc_per"]
        exteDoc = resquest.POST["exteDoc_per"]
        lugarNac = resquest.POST["lugarNac_per"]
        sangre = resquest.POST["sangre_per"]
        estCivil = resquest.POST["estCivil_per"]
        foto = resquest.FILES.get("foto_per")
        direccion = resquest.POST["direccion_per"]
        personas = Persona.objects.get(id_per=id)
        existe_persona = Persona.objects.exclude(id_per=id).filter(nombre_per=nombreP, apellidoP_per=apellidoP).exists()
        if existe_persona:
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('perEditar', personas.id_per)
        personas.nombre_per = nombreP.title()
        personas.apellidoP_per = apellidoP.capitalize()
        personas.apellidoM_per = apellidoM.capitalize()
        personas.telf_per = telf
        personas.sexo_per = sexo.capitalize()
        personas.numDoc_per = numDoc
        personas.venDoc_per = venDoc
        personas.fechNac_per = fechNac
        personas.exteDoc_per = exteDoc.upper()
        personas.lugarNac_per = lugarNac.capitalize()
        personas.sangre_per = sangre.upper()
        personas.estCivil_per = estCivil.capitalize()
        personas.imagen_per = foto
        personas.direccion_per = direccion.capitalize()
        personas.documento_per_id = idocumento
        personas.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('perLista')
    else:
        return render(resquest, 'persona/editar.html', {'personas': personas})
def perEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_persona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    persona = Persona.objects.get(id_per=id)
    persona.estado_per = 0
    persona.save()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('perLista')
def perActivar(resquest, id):
    persona = Persona.objects.get(id_per=id)
    persona.estado_per = 1
    persona.save()
    messages.success(resquest, " REGISTRO ACTIVADO ")
    return redirect('perLista')
def perLista_noactivo(resquest):
    if not resquest.user.has_perm('admRrhh.view_persona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personas = Persona.objects.filter(estado_per = 0)
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        personas = Persona.objects.filter(
            Q(nombre_per__icontains=busqueda)|
            Q(apellidoP_per__icontains=busqueda)|
            Q(apellidoM_per__icontains=busqueda)| 
            Q(direccion_per__icontains=busqueda) 
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(personas, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
        personas = paginator.page(page)
    except PageNotAnInteger:
        personas = paginator.page(1)
    except EmptyPage:
        personas = paginator.page(paginator.num_pages)
    return render(resquest, 'persona/listaPers_inactiva.html', {'personas': personas})
# PERSONAL/////////////////////////////////////////////////////////
@login_required
def perlLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_personal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personales = Personal.objects.filter(estado_perl = 1).order_by('-id_perl') 
    personas = Persona.objects.all()
    areas = Area.objects.all()
    cargos = Cargo.objects.all()
    estudios = Estudio.objects.all()
    profesiones = Profesion.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        personales = Personal.objects.filter(
            Q(sueldo_perl__icontains=busqueda) |
            Q(persona_perl__nombre_per__icontains=busqueda) |
            Q(persona_perl__apellidoP_per__icontains=busqueda) |
            Q(area_perl__nombre_are__icontains=busqueda) |
            Q(cargo_perl__nombre_carg__icontains=busqueda) |
            Q(estudio_perl__nombre_est__icontains=busqueda) |
            Q(profesion_perl__nombre_prof__icontains=busqueda) 
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(personales, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
        personales = paginator.page(page)
    except PageNotAnInteger:
        personales = paginator.page(1)
    except EmptyPage:
        personales = paginator.page(paginator.num_pages)
    return render(resquest, 'personal/lista.html', {'personales': personales, 'personas': personas, 'areas': areas, 'cargos': cargos, 'estudios': estudios, 'profesiones': profesiones})
def perlCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_personal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personales = Personal.objects.filter(estado_perl = 1)
    personas = Persona.objects.filter(estado_per = 1)
    areas = Area.objects.filter(estado_are = 1)
    cargos = Cargo.objects.filter(estado_carg = 1)
    estudios = Estudio.objects.filter(estado_est = 1)
    profesiones = Profesion.objects.filter(estado_prof = 1)
    personas_no_encontradas = filtrar_personas(personales, personas)
    return render(resquest, 'personal/crear.html', {'personas_no_encontradas': personas_no_encontradas, 'personas': personas, 'areas': areas, 'cargos': cargos, 'estudios': estudios, 'profesiones': profesiones})
def filtrar_personas(personales, personas):
    personas_no_encontradas = []
    for persona in personas:
        encontrada = False
        for personal in personales:
            if personal.persona_perl_id == persona.id_per:
                encontrada = True
                break
        if not encontrada:
            personas_no_encontradas.append(persona)
    return personas_no_encontradas
def perlGuardar(resquest):
    idpersona = resquest.POST["persona_perl"]
    idarea = resquest.POST["area_perl"]
    idcargo = resquest.POST["cargo_perl"]
    idestudio = resquest.POST["estudio_perl"]
    idprofesion = resquest.POST.get("profesion_perl")
    hijos = resquest.POST["hijos_perl"]
    fechIngre = resquest.POST["fechIngre_perl"]
    licCond = resquest.POST["licCond_perl"]
    tipoLic = resquest.POST.get("tipoLic_perl")
    fechVenlic = resquest.POST.get("fechVenlic_perl")
    ctaBanc = resquest.POST["ctaBanc_perl"]
    nua = resquest.POST["nua_perl"]
    aseg = resquest.POST["aseg_perl"]
    ctaAfp = resquest.POST["ctaAfp_perl"]
    sueldo = resquest.POST["sueldo_perl"]
    personales = Personal.objects.create( persona_perl_id=idpersona,
        area_perl_id=idarea,
        cargo_perl_id=idcargo,
        estudio_perl_id=idestudio,
        profesion_perl_id=idprofesion,
        hijos_perl=hijos,
        fechIngre_perl=fechIngre,
        licCond_perl=licCond.capitalize(),
        tipoLic_perl=tipoLic,
        fechVenlic_perl=fechVenlic,
        ctaBanc_perl=ctaBanc,
        nua_perl=nua,
        aseg_perl=aseg,
        ctaAfp_perl=ctaAfp.capitalize(),
        sueldo_perl=sueldo)
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('perlLista') 
def perlEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_personal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personales = Personal.objects.filter(estado_perl = 1)
    personas = Persona.objects.filter(estado_per = 1)
    areas = Area.objects.all()
    cargos = Cargo.objects.all()
    estudios = Estudio.objects.all()
    profesiones = Profesion.objects.all()
    codigo = Personal.objects.get(id_perl=id)
    personas_no_encontradas = filtrar_personas(personales, personas)
    return render(resquest, 'personal/editar.html', {'codigo': codigo, 'personas_no_encontradas': personas_no_encontradas, 'personas': personas, 'areas': areas, 'cargos': cargos, 'estudios': estudios, 'profesiones': profesiones})
def perlActualizar(resquest, id):
    idpersona = resquest.POST["persona_perl"]
    idarea = resquest.POST["area_perl"]
    idcargo = resquest.POST["cargo_perl"]
    idestudio = resquest.POST["estudio_perl"]
    idprofesion = resquest.POST["profesion_perl"]
    hijos = resquest.POST["hijos_perl"]
    fechIngre = resquest.POST["fechIngre_perl"]
    licCond = resquest.POST["licCond_perl"]
    tipoLic = resquest.POST["tipoLic_perl"]
    fechVenlic = resquest.POST["fechVenlic_perl"]
    ctaBanc = resquest.POST["ctaBanc_perl"]
    nua = resquest.POST["nua_perl"]
    aseg = resquest.POST["aseg_perl"]
    ctaAfp = resquest.POST["ctaAfp_perl"]
    sueldo = resquest.POST["sueldo_perl"]
    personal = Personal.objects.get(id_perl=id)
    personal.persona_perl_id = idpersona
    personal.area_perl_id = idarea
    personal.cargo_perl_id = idcargo
    personal.estudio_perl_id = idestudio
    personal.profesion_perl_id = idprofesion
    personal.hijos_perl = hijos
    personal.fechIngre_perl = fechIngre
    personal.licCond_perl = licCond.capitalize()
    personal.tipoLic_perl = tipoLic.upper()
    personal.fechVenlic_perl = fechVenlic
    personal.ctaBanc_perl = ctaBanc
    personal.nua_perl = nua
    personal.aseg_perl = aseg
    personal.sueldo_perl = sueldo
    personal.ctaAfp_perl = ctaAfp.capitalize()
    personal.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('perlLista')
def perlEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_personal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personal = Personal.objects.get(id_perl=id)
    personal.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('perlLista')
# PROYECTO/////////////////////////////////////////////////////////
@login_required
def proyLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_proyecto'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.filter(estado_proy = 1).order_by('-id_proy') 
    fiscales = Fiscal.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        proyectos = Proyecto.objects.filter(
            Q(nombre_proy__icontains=busqueda)|
            Q(ubicacion_proy__icontains=busqueda)|
            Q(fiscal_proy__apellidoP_fis__icontains=busqueda)|
            Q(fiscal_proy__nombre_fis__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(proyectos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
         proyectos = paginator.page(page)
    except PageNotAnInteger:
        proyectos = paginator.page(1)
    except EmptyPage:
        proyectos = paginator.page(paginator.num_pages)
    return render(resquest, 'proyecto/lista.html', {'proyectos': proyectos, 'fiscales': fiscales})

def proyCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_proyecto'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.all()
    fiscales = Fiscal.objects.all()
    zonas = Zona.objects.all()
    return render(resquest, 'proyecto/crear.html',{'proyectos': proyectos, 'zonas': zonas, 'fiscales': fiscales})
def proyGuardar(resquest):
    if resquest.method == 'POST':
        proyecto = resquest.POST["nombre_proy"]
        idfiscal = resquest.POST["fiscal_proy"]
        grafo = resquest.POST["grafo_proy"]
        trafo = resquest.POST["trafo_proy"]
        ubicacion = resquest.POST["ubicacion_proy"]
        nota = resquest.POST["nota_proy"]
        fechaRecep = resquest.POST["fechaRecep_proy"]
        fechaDisen = resquest.POST["fechaDisen_proy"]
        fechaConst = resquest.POST["fechaConst_proy"]
        if Proyecto.objects.filter(nombre_proy__iexact=proyecto).exists():
            messages.error(resquest, "Ya existe un proyecto con este nombre.")
            return redirect('proyCrear')
        proyectos = Proyecto.objects.create(nombre_proy=proyecto.upper(),
                                        grafo_proy=grafo,
                                        trafo_proy=trafo.upper(),
                                        ubicacion_proy=ubicacion.title(),
                                        nota_proy=nota.capitalize(),
                                        fechaRecep_proy=fechaRecep,
                                        fechaDisen_proy=fechaDisen,
                                        fechaConst_proy=fechaConst,
                                        fiscal_proy_id=idfiscal)
        proyecto_id=proyectos.id_proy
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('proyEditar',proyecto_id)
def proyEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_proyecto'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    fiscales = Fiscal.objects.all()
    personas = Persona.objects.all()
    asignaciones = Asignacion.objects.all()
    proyectos = Proyecto.objects.all()
    cargos = Cargo.objects.filter(nombre_carg__in=obtener_cargos_disenio())
    personales = Personal.objects.all()
    fiscales = Fiscal.objects.all()
    codigo = Proyecto.objects.get(id_proy=id)
    return render(resquest, 'proyecto/editar.html', {'personas': personas,'cargos': cargos,'personales': personales,'codigo': codigo, 'fiscales': fiscales,'asignaciones': asignaciones, 'proyectos': proyectos })
def obtener_cargos_disenio():
    # Obtiene los nombres de los cargos únicos de las personas en el área 'Diseño'
    cargos = Personal.objects.filter(area_perl__nombre_are='Diseño').values_list('cargo_perl__nombre_carg', flat=True).distinct()
    return list(cargos)
def proyActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_proy"]
        idfiscal = resquest.POST["fiscal_proy"]
        grafo = resquest.POST["grafo_proy"]
        trafo = resquest.POST["trafo_proy"]
        ubicacion = resquest.POST["ubicacion_proy"]
        nota = resquest.POST["nota_proy"]
        fechaRecep = resquest.POST["fechaRecep_proy"]
        fechaDisen = resquest.POST["fechaDisen_proy"]
        fechaConst = resquest.POST["fechaConst_proy"]
        proyectos = Proyecto.objects.get(id_proy=id)
        if Proyecto.objects.exclude(id_proy=id).filter(nombre_proy__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un proyecto con este nombre.")
            return redirect('proyEditar', proyectos.id_proy)
        proyectos.nombre_proy = nuevo_nombre.upper()
        proyectos.grafo_proy=grafo
        proyectos.trafo_proy=trafo.upper()
        proyectos.ubicacion_proy=ubicacion.title()
        proyectos.nota_proy=nota.capitalize()
        proyectos.fechaRecep_proy=fechaRecep
        proyectos.fechaDisen_proy=fechaDisen
        proyectos.fechaConst_proy=fechaConst
        proyectos.fiscal_proy_id=idfiscal
        proyectos.save()
        messages.success(resquest, "Se actualizó correctamente el dato.")
        return redirect('proyLista')
    else:
        return redirect('proyLista')
def proyEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_proyecto'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyecto = Proyecto.objects.get(id_proy=id)
    proyecto.estado_proy = 0
    proyecto.save()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('proyLista')
def proyActivar(resquest, id):
    proyecto = Proyecto.objects.get(id_proy=id)
    proyecto.estado_proy = 1
    proyecto.save()
    messages.success(resquest, " REGISTRO ACTIVADO ")
    return redirect('proyLista')
def proyLista_noactivo(resquest):
    if not resquest.user.has_perm('admRrhh.view_proyecto'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.filter(estado_proy = 0).order_by('-id_proy') 
    fiscales = Fiscal.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        proyectos = Proyecto.objects.filter(
            Q(nombre_proy__icontains=busqueda)|
            Q(fiscal_proy__nombre_fis__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(proyectos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
         proyectos = paginator.page(page)
    except PageNotAnInteger:
        proyectos = paginator.page(1)
    except EmptyPage:
        proyectos = paginator.page(paginator.num_pages)
    return render(resquest, 'proyecto/listaProy_inactiva.html', {'proyectos': proyectos, 'fiscales': fiscales})
# ASIGNACION/////////////////////////////////////////////////////////
@login_required
def asigLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_asignacion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig') 
    proyectos = Proyecto.objects.filter(estado_proy = 1)
    personales = Personal.objects.filter(estado_perl = 1)
    personas = Persona.objects.filter(estado_per = 1)
    cargos = Cargo.objects.filter(estado_carg = 1)
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        asignaciones = Asignacion.objects.filter(
            Q(nota_asig__icontains=busqueda)|
            Q(proyecto_asig__nombre_proy__icontains=busqueda)|
            Q(personal_asig__persona_perl__nombre_per__icontains=busqueda)|
            Q(personal_asig__cargo_perl__nombre_carg__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(asignaciones, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
     asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    return render(resquest, 'asignacion/lista.html', {'asignaciones': asignaciones,'cargos': cargos, 'proyectos': proyectos, 'personales': personales,'personas': personas})
def asigCrear(resquest):
    if not resquest.user.has_perm('admRrhh.view_asignacion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    asignaciones = Asignacion.objects.all()
    personales = Personal.objects.all()
    proyectos = Proyecto.objects.all()
    personas =Persona.objects.all()
    cargos = Cargo.objects.filter(nombre_carg__in=['Estacador','Dibujante','Digitador'])
    proyectos_no_encontrados = filtrar_proyAsig(asignaciones, proyectos)
    return render(resquest, 'asignacion/crear.html', {'proyectos': proyectos,'cargos': cargos, 'personas': personas, 'personales': personales, 'proyectos_no_encontrados': proyectos_no_encontrados})
def filtrar_proyAsig(asignaciones, proyectos):
    proyectos_no_encontrados = []
    for proyecto in proyectos:
        encontrada = False
        for asignacion in asignaciones:
            if asignacion.proyecto_asig_id == proyecto.id_proy:
                encontrada = True
                break
        if not encontrada:
            proyectos_no_encontrados.append(proyecto)
    return proyectos_no_encontrados 
def asigGuardar(resquest):
    nota = resquest.POST["nota_asig"]
    fechaIni = resquest.POST["fechaIni_asig"]
    fechaFin = resquest.POST["fechaFin_asig"]
    idproyecto = resquest.POST["proyecto_asig"]
    idpersonal = resquest.POST["personal_asig"]
    asignaciones = Asignacion.objects.create(
    nota_asig=nota.capitalize(),
    fechaIni_asig=fechaIni,
    fechaFin_asig=fechaFin,
    proyecto_asig_id=idproyecto,
    personal_asig_id=idpersonal)
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('asigLista')
def asigEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_asignacion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    asignaciones = Asignacion.objects.all()
    proyectos = Proyecto.objects.all()
    personas = Persona.objects.all()
    personales = Personal.objects.all()
    codigo = Asignacion.objects.get(id_asig=id)
    proyectos_no_encontrados = filtrar_proyAsig(asignaciones, proyectos)
    return render(resquest, 'asignacion/editar.html', {'codigo': codigo, 'proyectos_no_encontrados': proyectos_no_encontrados, 'proyectos': proyectos, 'personas': personas,'personales': personales})
def asigActualizar(resquest, id):
    nota = resquest.POST["nota_asig"]
    imagen = resquest.FILES.get("imagen_asig")
    fechaIni = resquest.POST["fechaIni_asig"]
    fechaFin = resquest.POST["fechaFin_asig"]
    idpersonal = resquest.POST["personal_asig"]
    idproyecto = resquest.POST["proyecto_asig"]
    fechaInicial = datetime.strptime(fechaIni, "%Y-%m-%d")
    asignaciones = Asignacion.objects.get(id_asig=id)
    if fechaFin:
        fechaFinal = datetime.strptime(fechaFin, "%Y-%m-%d")
        if fechaFinal < fechaInicial:
                messages.error(resquest, "La fecha de finalización no puede ser menor que la fecha de inicio.")
                return redirect('asigEditar',asignaciones.id_asig)
    else:
        fechaFin = None

   
    asignaciones.nota_asig = nota.capitalize()
    asignaciones.imagen_asig =imagen
    asignaciones.fechaIni_asig = fechaIni
    asignaciones.fechaFin_asig = fechaFin
    asignaciones.personal_asig_id= idpersonal
    asignaciones.proyecto_asig_id= idproyecto
    asignaciones.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('proyEditar',asignaciones.proyecto_asig.id_proy)
def asigEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_asignacion'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    asignacion = Asignacion.objects.get(id_asig=id)
    asignacion.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('asigLista')
def asigRespaldo(resquest, id):
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig') 
    proyecto = Proyecto.objects.get(id_proy=id)
    
    personales = Personal.objects.filter(estado_perl = 1)
    personas = Persona.objects.filter(estado_per = 1)
    cargos = Cargo.objects.filter(estado_carg = 1)
    return render(resquest, 'asignacion/respaldo.html', {'asignaciones': asignaciones,'cargos': cargos, 'proyecto': proyecto, 'personales': personales,'personas': personas})
# ZONA/////////////////////////////////////////////////////////
@login_required
def zonLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_zona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    zonas = Zona.objects.filter(estado_zon = 1).order_by('-id_zon') 
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        zonas = Zona.objects.filter(
            Q(nombre_zon__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(zonas, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         zonas = paginator.page(page)
    except PageNotAnInteger:
        zonas = paginator.page(1)
    except EmptyPage:
        zonas = paginator.page(paginator.num_pages)
    return render(resquest, 'zona/lista.html', {'zonas': zonas})
def zonCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_zona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    return render(resquest, 'zona/crear.html')
def zonGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_zon"]
        if Zona.objects.filter(nombre_zon__iexact=nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return render(resquest, 'zona/crear.html',context)
        zonas = Zona.objects.create(nombre_zon=nombre.title())
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('zonLista')
    else:
            return redirect('zonLista')  
def zonEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_zona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    codigo = Zona.objects.get(id_zon=id)
    return render(resquest, 'zona/editar.html', {'codigo': codigo})
def zonActualizar(resquest, id):
    if resquest.method == 'POST':
        nuevo_nombre = resquest.POST["nombre_zon"]
        zona = Zona.objects.get(id_zon=id)
        if Zona.objects.exclude(id_zon=id).filter(nombre_zon__iexact=nuevo_nombre).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            return redirect('zonEditar', zona.id_zon)

        zona.nombre_zon = nuevo_nombre.title()
        zona.save()
        messages.success(resquest, "Se actualizó correctamente el área.")
        return redirect('zonLista')
    else:
        return render(resquest, 'zona/editar.html', {'zona': zona})
def zonEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_zona'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    zona = Zona.objects.get(id_zon=id)
    zona.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('zonLista')
# FISCAL/////////////////////////////////////////////////////////
@login_required
def fisLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_fiscal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 

    fiscales = Fiscal.objects.filter(estado_fis = 1).order_by('-id_fis') 
    zonas = Zona.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        fiscales = Fiscal.objects.filter(
            Q(nombre_fis__icontains=busqueda)|
            Q(apellidoP_fis__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(fiscales, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         fiscales = paginator.page(page)
    except PageNotAnInteger:
        fiscales = paginator.page(1)
    except EmptyPage:
        fiscales = paginator.page(paginator.num_pages)
    return render(resquest, 'fiscal/lista.html', {'fiscales': fiscales, 'zonas': zonas})
def fisCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_fiscal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    zonas = Zona.objects.all()
    return render(resquest, 'fiscal/crear.html', {'zonas': zonas})
def fisGuardar(resquest):
    if resquest.method == 'POST':
        nombreF = resquest.POST["nombre_fis"]
        apellidoP = resquest.POST["apellidoP_fis"]
        number= resquest.POST["zona_fis"]
        if Fiscal.objects.filter(nombre_fis=nombreF, apellidoP_fis=apellidoP).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return redirect( 'fisCrear')
        fiscales = Fiscal.objects.create(nombre_fis=nombreF.title(),
                                        apellidoP_fis=apellidoP.title(),
                                        zona_fis_id=number)
        messages.success(resquest, "SE REGISTRO CORRECTAMENTE ")
        return redirect('fisLista')
    else:

            return redirect('fisLista')  
def fisEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_fiscal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    zonas = Zona.objects.all()
    codigo = Fiscal.objects.get(id_fis=id)
    return render(resquest, 'fiscal/editar.html', {'codigo': codigo, 'zonas': zonas})
def fisActualizar(resquest, id):
    if resquest.method == 'POST':
        nombre = resquest.POST["nombre_fis"]
        idzona = resquest.POST["zona_fis"]
        apellidoP = resquest.POST["apellidoP_fis"]
        fiscal = Fiscal.objects.get(id_fis=id)
        if Fiscal.objects.exclude(id_fis=id).filter(nombre_fis=nombre, apellidoP_fis=apellidoP).exists():
            messages.error(resquest, "Ya existe un dato con este nombre.")
            context = {
             'messages': messages.get_messages(resquest),
            }
            return redirect( 'fisEditar', fiscal.id_fis)
        fiscal.nombre_fis = nombre.title()
        fiscal.apellidoP_fis = apellidoP.title()
        fiscal.zona_fis_id = idzona
        fiscal.save()
        messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('fisLista')
def fisEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_fiscal'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    fiscal = Fiscal.objects.get(id_fis=id)
    fiscal.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('fisLista')
# ENVIO/////////////////////////////////////////////////////////
@login_required
def envLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_envio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    envios = Envio.objects.filter(estado_env=2).order_by('-id_env') 
    proyectos = Proyecto.objects.all()
    asignaciones = Asignacion.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        envios = Envio.objects.filter(
            Q(proyecto_env__nombre_proy__icontains=busqueda)
            
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(envios, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         envios = paginator.page(page)
    except PageNotAnInteger:
        envios = paginator.page(1)
    except EmptyPage:
        envios = paginator.page(paginator.num_pages)
    return render(resquest, 'envio/lista.html', {'envios': envios, 'proyectos': proyectos,'asignaciones': asignaciones})
def envCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_envio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.filter(estado_proy=1)
    envios = Envio.objects.filter(estado_env=2)
    proyectos_no_encontrados = filtrar_proyectos(proyectos,envios)
    return render(resquest, 'envio/crear.html', {'proyectos_no_encontrados': proyectos_no_encontrados,'proyectos': proyectos})
def filtrar_proyectos(proyectos, envios):
    envio_no_encontradas = []
    for proyecto in proyectos:
        encontrado = False
        for envio in envios:
            if envio.proyecto_env_id == proyecto.id_proy:
                encontrado = True
                break
        if not encontrado:
            envio_no_encontradas.append(proyecto)
    return envio_no_encontradas
def envGuardar(resquest):
    if resquest.method == 'POST':
        fechaIn = resquest.POST["fechaEnv_env"]
        nota = resquest.POST["nota_env"]
        monto = resquest.POST["monto_env"]
        idproyecto = resquest.POST["proyecto_id"]
        crono = int(resquest.POST.get("cronograma",0))
        estacado = int(resquest.POST.get("estacado",0))
        plano = int(resquest.POST.get("plano",0))
        punto = int(resquest.POST.get("punto",0))
        mano = int(resquest.POST.get("mano",0))
        respaldo = int(resquest.POST.get("respaldo",0))
        envios = Envio.objects.create(fechaEnv_env=fechaIn,
                                        nota_env=nota.capitalize(),
                                        monto_env= monto,
                                        proyecto_env_id=idproyecto,
                                        cronograma_env=crono,
                                        estacado_env =estacado,
                                        plano_env=plano,
                                        puntoPunto_env=punto,
                                        manoObra_env =mano,
                                        resplado_env =respaldo,
                                        estado_env =2)                                   
                   
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('envLista')
def envEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_envio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    envios = Envio.objects.filter(estado_env=2)
    proyectos = Proyecto.objects.filter(estado_proy=1)
    proyectos_no_encontrados = filtrar_proyectos(proyectos,envios)
    codigo = Envio.objects.get(id_env=id)
    return render(resquest, 'envio/editar.html', {'proyectos': proyectos,'codigo': codigo, 'proyectos_no_encontrados': proyectos_no_encontrados})
def envActualizar(resquest, id):
    fechaIn = resquest.POST["fechaEnv_env"]
    nota = resquest.POST["nota_env"]
    monto = resquest.POST["monto_env"]
    idproyecto = resquest.POST["proyecto_id"]
    crono = int(resquest.POST.get("cronograma",0))
    estacado = int(resquest.POST.get("estacado",0))
    plano = int(resquest.POST.get("plano",0))
    punto = int(resquest.POST.get("punto",0))
    mano = int(resquest.POST.get("mano",0))
    respaldo = int(resquest.POST.get("respaldo",0))
    envio = Envio.objects.get(id_env=id)
    envio.fechaEnv_env=fechaIn
    envio.nota_env=nota.capitalize()
    envio.monto_env=monto
    envio.proyecto_env_id=idproyecto
    envio.cronograma_env=crono
    envio.estacado_env =estacado
    envio.plano_env=plano
    envio.puntoPunto_env=punto
    envio.manoObra_env =mano
    envio.resplado_env =respaldo
    envio.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('envLista')
def envEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_envio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    envio = Envio.objects.get(id_env=id)
    envio.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('envLista')
def filtrar_envios(proyectos, envios):
    envios_no_encontrados = []
    for envio in envios:
        encontrado = False
        for proyecto in proyectos:
            if proyecto.proyecto_envio_id == envio.id_env:
                encontrado = True
                break
        if not encontrado:
            envios_no_encontrados.append(envio)
    
    return envios_no_encontrados
# Ordent/////////////////////////////////////////////////////////
@login_required
def ordLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_ordent'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    ordenes = Ordent.objects.filter(estado_ord = 1).order_by('-id_ord') 
    proyectos = Proyecto.objects.all()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        ordenes = Ordent.objects.filter(
            Q(numero_ord__icontains=busqueda)|
            Q(proyecto_ord__nombre_proy__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(ordenes, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         ordenes = paginator.page(page)
    except PageNotAnInteger:
        ordenes = paginator.page(1)
    except EmptyPage:
        ordenes = paginator.page(paginator.num_pages)
    return render(resquest, 'ordent/lista.html', {'ordenes': ordenes, 'proyectos': proyectos})
def ordCrear(resquest):
    if not resquest.user.has_perm('admRrhh.add_ordent'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.all()
    ordenes = Ordent.objects.all()
    orden_no_encontrados = filtrar_proyect(proyectos,ordenes)
    return render(resquest, 'ordent/crear.html', {'orden_no_encontrados': orden_no_encontrados,'proyectos': proyectos,'ordenes': ordenes})
def filtrar_proyect(proyectos, ordenes):
    orden_no_encontrados = []
    for proyecto in proyectos:
        encontrado = False
        for orden in ordenes:
            if orden.proyecto_ord_id == proyecto.id_proy:
                encontrado = True
                break
        if not encontrado:
            orden_no_encontrados.append(proyecto)
    return orden_no_encontrados
def ordGuardar(resquest):
    if resquest.method == 'POST':
        idproyecto = resquest.POST["proyecto_ord"]
        numero = resquest.POST["numero_ord"]
        numeroCaj = resquest.POST["numeroCaj_ord"]
        nota = resquest.POST["nota_ord"]
        ordenes = Ordent.objects.create(numero_ord=numero,
                                            numeroCaj_ord=numeroCaj,
                                            nota_ord=nota.capitalize(),
                                            proyecto_ord_id=idproyecto)
        messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
        return redirect('ordLista')
def ordEditar(resquest, id):
    if not resquest.user.has_perm('admRrhh.change_ordent'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    proyectos = Proyecto.objects.all()
    codigo = Ordent.objects.get(id_ord=id)
    return render(resquest, 'ordent/editar.html', {'codigo': codigo, 'proyectos': proyectos})
def ordActualizar(resquest, id):
    idproyecto = resquest.POST["proyecto_ord"]
    numero = resquest.POST["numero_ord"]
    numeroCaj = resquest.POST["numeroCaj_ord"]
    nota = resquest.POST["nota_ord"]
    orden = Ordent.objects.get(id_ord=id)
    orden.numero_ord=numero
    orden.numeroCaj_ord=numeroCaj
    orden.nota_ord=nota.capitalize()
    orden.proyecto_ord_id=idproyecto
    orden.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('ordLista')
def ordEliminar(resquest, id):
    if not resquest.user.has_perm('admRrhh.delete_ordent'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    ordent = Ordent.objects.get(id_ord=id)
    ordent.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('ordLista')
# MAESTRO DETALLE/////////////////////////////////////////////////////////
def proyEditarDetall(resquest, id):
    datocarg = Cargo.objects.all()
    proyectos = Proyecto.objects.all()
    personas =Persona.objects.all()
    asignaciones = Asignacion.objects.all().order_by('-id_asig')
    cargos = Cargo.objects.filter(nombre_carg__in=['Estacador','Dibujante','Digitador'])
    personales = Personal.objects.all()
    fiscales = Fiscal.objects.all()
    codigo = Proyecto.objects.get(id_proy=id)
    return render(resquest, 'proyecto/detalleM.html', {'codigo': codigo,'datocarg': datocarg, 'personales': personales, 'personas': personas,'fiscales': fiscales,'cargos': cargos,'proyectos': proyectos,'asignaciones': asignaciones})
def asigGuardetalle(resquest):
    nota = resquest.POST["nota_asig"]
    fechaIni = resquest.POST["fechaIni_asig"]
    idproyecto = resquest.POST["proyecto_asig"]
    idpersonal = resquest.POST["personal_asig"]
    asignaciones = Asignacion.objects.create(
    nota_asig=nota.capitalize(),
    fechaIni_asig=fechaIni,
    proyecto_asig_id=idproyecto,
    personal_asig_id=idpersonal)
    asignacion_id=asignaciones.proyecto_asig_id
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('proyEditar', asignacion_id)
def proyDetalleM(resquest, id):
    cargos = Cargo.objects.all()
    personales = Personal.objects.select_related('persona', 'cargo').all()
    proyectos = Proyecto.objects.all()
    personas =Persona.objects.all()
    asignaciones = Asignacion.objects.all().order_by('-id_asig')
    cargos = Cargo.objects.filter(nombre_carg__in=['Estacador','Dibujante','Digitador'])
    personales = Personal.objects.all()
    fiscales = Fiscal.objects.all()
    codigo = Proyecto.objects.get(id_proy=id)
    return render(resquest, 'proyecto/detalleM.html', {'codigo': codigo, 'personales': personales, 'personas': personas,'fiscales': fiscales,'cargos': cargos,'proyectos': proyectos,'asignaciones': asignaciones})
def asigEliminarD(resquest, id):
    asignacion = get_object_or_404(Asignacion, id_asig=id)
    proyecto_id = asignacion.proyecto_asig_id  # Obtener el ID del proyecto antes de eliminar la asignación
    asignacion.delete()
    messages.success(resquest, "REGISTRO ELIMINADO")
    return redirect('proyEditar', proyecto_id)
# USUARIO/////////////////////////////////////////////////////////
@login_required
def usuLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_user'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    usuarios = User.objects.filter(is_active = 1).order_by('-id')
    if usuarios:
        grupos = usuarios[0].groups.all()
        busqueda = resquest.GET.get("buscar")
        if busqueda:
            usuarios = User.objects.filter(
                Q(username__icontains=busqueda)
            ).distinct()
        elementos_por_pagina = 12
        paginator = Paginator(usuarios, elementos_por_pagina)
        page = resquest.GET.get("page", 1)
        try:
            usuarios = paginator.page(page)
        except PageNotAnInteger:
            usuarios = paginator.page(1)
        except EmptyPage:
            usuarios = paginator.page(paginator.num_pages)
    return render(resquest, 'usuario/lista.html', {'usuarios': usuarios})
def usuCrear(resquest):
    personas = Persona.objects.all()
    usuarios = User.objects.all()
    proyectos = Proyecto.objects.all()
    personales = Personal.objects.filter(area_perl__nombre_are__in=['Administracion', 'Diseño', 'Contabilidad', 'Almacen'])
    resultados = []
    for personal in personales:
        nombre_completo = f"{personal.persona_perl.nombre_per} {personal.persona_perl.apellidoP_per}"
        if not usuarios.filter(username=nombre_completo).exists():
            resultados.append(personal)
    for resultado in resultados:
        print(f"Nombre: {resultado.persona_perl.nombre_per}, Apellido: {resultado.persona_perl.apellidoP_per}")
    return render(resquest, 'usuario/crear.html', {
        'personales': personales,
        'personas': personas,
        'proyectos': proyectos,
        'resultados': resultados
    })
def usuGuardar(resquest):
    if resquest.method == 'POST':
        nombre = resquest.POST["persona_usu"]
        password = resquest.POST["password_usu"]
        superusu = int(resquest.POST.get('super_usu', '0')) 
        correo = resquest.POST["mail_usu"]
        password_cifrada = make_password(password)
        if User.objects.filter(username=nombre).exists():
            messages.error(resquest, "Ya existe un dato registrado con este nombre.")
            return redirect('usuCrear')
        usuario = User.objects.create(
            username=nombre.title(),
            password=password_cifrada,
            is_superuser= superusu,
            email=correo,
            is_active=1
        )
        usu_id=usuario.id
        messages.success(resquest, "SE REGISTRÓ CORRECTAMENTE")
        return redirect('usuEditar',usu_id)
def usuEditar(resquest, id):
    grupos = Group.objects.all()
    usuarios = User.objects.filter(is_active = 1).order_by('-id')
    personales= Personal.objects.filter(area_perl__nombre_are__in=['Administracion','Diseño','Contabilidad','Almacen'])
    codigo = User.objects.get(id=id)
    return render(resquest, 'usuario/editar.html', {'grupos': grupos,'codigo': codigo,'usuarios': usuarios,'personales': personales})
def usuActualizar(resquest, id):
    if resquest.method == 'POST':
        nombre = resquest.POST["persona_usu"]
        password = resquest.POST["password_usu"]
        superusu = int(resquest.POST.get('super_usu', '0')) 
        correo = resquest.POST["mail_usu"]
        password_cifrada = make_password(password)
        usuario = User.objects.get(id=id)
        if User.objects.exclude(id=id).filter(username=nombre).exists():
            messages.error(resquest, "Ya existe un dato registrado con este nombre.")
            return redirect('usuEditar', usuario.id)
        usuario.username= nombre.title()
        usuario.password= password_cifrada
        usuario.is_superuser= superusu
        usuario.email=correo
        usuario.is_active=1
        usuario.save()
        messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE LOS DATOS ")
        return redirect('usuLista')
def usuEliminar(resquest, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    messages.success(resquest, " REGISTRO ELIMINADO ")
    return redirect('usuLista')
#///////
def userRolEliminar(resquest, usuario_id, grupo_id):
    try:
        usuario = User.objects.get(id=usuario_id)
        grupo = Group.objects.get(id=grupo_id)
        grupo.user_set.remove(usuario)
        return redirect('usuEditar', usuario_id)
    except User.DoesNotExist:
        print(f"Usuario con id {usuario.id} no encontrado.")
    except Group.DoesNotExist:
        print(f"Grupo con id {grupo.id} no encontrado.")

    return redirect('usuEditar', usuario.id)
    #//////PERMDETALLE
def permEditarDetall(resquest, id):
    permisos = Permission.objects.all() 
    personas =Persona.objects.all()
    userpermisos = Group.objects.filter(permissions__isnull=False).distinct()
    grupos =Group.objects.all()
    codigo = Group.objects.get(id=id)
    return render(resquest, 'rol/detalleRol.html', {'userpermisos': userpermisos,'codigo': codigo, 'personas': personas,'grupos': grupos,'permisos': permisos})
#////////////////PERMISOS
@login_required
def permLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_permission'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    personas = Persona.objects.all()
    usuarios = User.objects.all() 
    permisos = Permission.objects.all()
    permisoss = permisos_formato()
    elementos_por_pagina = 100
    paginator = Paginator(permisos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        permisos = paginator.page(page)
    except PageNotAnInteger:
        permisos = paginator.page(1)
    except EmptyPage:
        permisos = paginator.page(paginator.num_pages)
    usuarios = User.objects.all() 
    return render(resquest, 'permiso/lista.html', {'personas': personas,'usuarios':usuarios,'permisos':permisos,'permisoss':permisoss })
def permCrear(resquest):
    personas = Persona.objects.all()
    permisos = Permission.objects.all() 
    return render(resquest, 'permiso/crear.html',{'personas': personas,'permisos': permisos})
def permGuardar(resquest):
    nombre = resquest.POST["usuario_perm"]
    permiso = resquest.POST["permiso_perm"]
    roles = Permission.objects.create(user_id = nombre, permission_id = permiso)
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('permLista')
def permEditar(resquest, id):
    personas = Persona.objects.all()
    usuarios = User.objects.all() 
    codigo = Permission.objects.get(id=id)
    return render(resquest, 'permiso/editar.html', {'codigo': codigo,'usuarios': usuarios,'personas': personas})
def permActualizar(resquest, id):
    nombre = resquest.POST["usuario_perm"]
    permiso = resquest.POST["permiso_perm"]
    permisos = Permission.objects.get(id=id)
    permisos.user_id = nombre
    permisos.permission_id = permiso
    permisos.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('permLista')
    #///////////////USERPERMISOS
def userPermLista(resquest):
    personas = Persona.objects.all()
    usuarios = User.objects.all() 
    permisos = Permission.objects.all() 
    userpermisos = User.objects.filter(user_permissions__isnull=False).distinct()
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        permisos = User.objects.filter( 
            Q(username__icontains=busqueda)
        ).distinct()
    
    elementos_por_pagina = 12
    paginator = Paginator(permisos, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        permisos = paginator.page(page)
    except PageNotAnInteger:
        permisos = paginator.page(1)
    except EmptyPage:
        permisos = paginator.page(paginator.num_pages)
    usuarios = User.objects.all() 
    return render(resquest, 'permiso/lista.html', {'userpermisos': userpermisos,'permisos': permisos,'personas': personas,'usuarios':usuarios })
#///////////////////////GUARDAR ROL Y PERMISO
def rolPermGuardar(resquest):
    if resquest.method == 'POST':
        nombre_grupo = resquest.POST.get('rol_perm')
        nombre_permiso = resquest.POST.get('permiso_rol')
        grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
        try:
            permiso = Permission.objects.get(codename=nombre_permiso)
        except Permission.DoesNotExist:
            return HttpResponse("El permiso especificado no existe.")
        grupo.permissions.add(permiso)
        return redirect('rolEditar', grupo.id if creado else grupo.id)
#////////////ROL
@login_required
def rolLista(resquest):
    if not resquest.user.has_perm('admRrhh.view_group'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    grupos_y_permisos = obtener_grupos_y_permisos()
    roles =  Group.objects.all()
    roles_con_permisos = []
    for grupo in roles:
        permisos = grupos_y_permisos.get(grupo, [])
        roles_con_permisos.append({
            'grupo': grupo,
            'permisos': permisos
    })
    busqueda = resquest.GET.get("buscar")
    if busqueda:
        roles =  Group.objects.filter(
            Q(name__icontains=busqueda)
        ).distinct()
    elementos_por_pagina = 12
    paginator = Paginator(roles, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        
        roles = paginator.page(page)
    except PageNotAnInteger:
        roles = paginator.page(1)
    except EmptyPage:
        
        roles = paginator.page(paginator.num_pages)
    return render(resquest, 'rol/lista.html', {'roles_con_permisos': roles_con_permisos})
def rolCrear(resquest):
    return render(resquest, 'rol/crear.html')
def rolGuardar(resquest):
    nombre = resquest.POST["nombre_rol"]
    roles =  Group.objects.create(name=nombre.capitalize())
    rol_id= roles.id
    messages.success(resquest, " SE REGISTRO CORRECTAMENTE ")
    return redirect('rolEditar', rol_id)
def permDetalle(resquest,id):
    userpermisos = Group.objects.filter(permissions__isnull=False).distinct()
    permisos= Permission.objects.all()
    codigo = Group.objects.get(id=id)
    return render(resquest, 'rol/detalleRol.html', {'userpermisos': userpermisos,'codigo': codigo, 'permisos': permisos})
def rolEditar(resquest, id):
    grupos_y_permisos = obtener_grupos_y_permisos()
    userpermisos= Group.objects.all()
    permisos = permisos_formato()
    codigo =  Group.objects.get(id=id)
    return render(resquest, 'rol/editar.html', {'codigo': codigo, 'permisos': permisos,'grupos_y_permisos': grupos_y_permisos})
def rolActualizar(resquest, id):
    nombre = resquest.POST["nombre_rol"]
    rol =  Group.objects.get(id=id)
    rol.name = nombre.capitalize()
    rol.save()
    messages.success(resquest, " SE ACTUALIZO CORRECTAMENTE EL ARCHIVO ")
    return redirect('rolLista')
def rolPermEliminar(resquest, grupo_id, permiso_id):
    try:
        grupo = Group.objects.get(id=grupo_id)
        permiso = Permission.objects.get(id=permiso_id)
        # Remover el permiso del usuario
        grupo.permissions.remove(permiso)
        print(" se elimino ")
        return redirect('rolEditar', grupo.id)
    except permiso.DoesNotExist:
        print(f"Permiso con id {permiso_id} no encontrado.")
def rolEditarDetall(resquest, id):
    permisos = Permission.objects.all() 
    personas =Persona.objects.all()
    userpermisos = User.objects.filter(user_permissions__isnull=False).distinct()
    usuarios = User.objects.all()
    codigo = User.objects.get(id=id)
    return render(resquest, 'usuario/detallePerm.html', {'userpermisos': userpermisos,'codigo': codigo, 'personas': personas,'usuarios': usuarios,'permisos': permisos})
def rolDetalleM(resquest, id):
    todogrupos = Group.objects.all() 
    usuarios =User.objects.all()
    codigo = User.objects.get(id=id)
    grupos = []
    if usuarios:
        grupos = usuarios[0].groups.all()
    return render(resquest, 'usuario/detallePerm.html', {'codigo': codigo,'usuarios': usuarios,  'grupos': grupos, 'todogrupos':todogrupos})
#////////ROL-USUARIO
def userRolGuardar(resquest):
    if resquest.method == 'POST':
        nombre_grupo = resquest.POST.get('rol_perm')
        nombre_usuario = resquest.POST.get('usuario_per')
        grupo, creado = Group.objects.get_or_create(name=nombre_grupo)
        usuario, creado_usuario = User.objects.get_or_create(username=nombre_usuario)
        grupo.user_set.add(usuario)
        return redirect('usuEditar', usuario.id)
def permDetalleM(resquest, id):
    todogrupos = Group.objects.all() 
    usuarios =User.objects.all()
    codigo = User.objects.get(id=id)
    grupos = []
    if usuarios:
        grupos = usuarios[0].groups.all()
    return render(resquest, 'usuario/detallePerm.html', {'usuarios': usuarios,'codigo': codigo,'usuarios': usuarios,  'grupos': grupos, 'todogrupos':todogrupos})
#//////////////REPORTES
def reproyLista(resquest):
    asignaciones_inicio = repinicio(resquest)
    asignaciones_estacado = repestacado(resquest)
    asignaciones_digitacion = repdigitacion(resquest)
    asignaciones_plano = repplano(resquest)
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    busqueda = resquest.GET.get("buscar")
    
    elementos_por_pagina = 15
    paginator = Paginator(asignaciones, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
        asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    return render(resquest, 'reporte/lista.html', {
    'asignaciones_inicio': asignaciones_inicio,'asignaciones_estacado': asignaciones_estacado,'asignaciones_digitacion': asignaciones_digitacion,'asignaciones_plano': asignaciones_plano,'asignaciones': asignaciones})
def repListapdf(resquest):    #probando
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig')
    datofech = datetime.now()
    vacios = Asignacion.objects.all()
    elementos_por_pagina = 10
    paginator = Paginator(asignaciones, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
     asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    return render(resquest, 'reporte/listainiciopdf.html', {'asignaciones':asignaciones,'datofech':datofech,'vacios':vacios})
def export_pdf2(resquest):
    datofech = datetime.now()
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig')
    vacios = Asignacion.objects.all()
    asignaciones_con_contador = []
    icon=  (settings.STATIC_URL,'img/logosercre.png')
    context = {'datofech': datofech, 'asignaciones': asignaciones,'vacios': vacios,'icon': icon}
    template_path = 'reporte/listapdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    return response
#FUNCIONES DE COMPARACION
def repinicio(resquest): 
    proyectos = Proyecto.objects.filter(estado_proy=1)
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    proyecto_sin = proyectos_asignados(resquest)
    ids_proyectos_asignados = set(asignacion.proyecto_asig_id for asignacion in asignaciones)
    proyectos_sin_asignacion = [
        proyecto for proyecto in proyecto_sin
        if proyecto.id_proy not in ids_proyectos_asignados
    ]
    return proyectos_sin_asignacion
def proyectos_asignados(resquest):
    proyectos = Proyecto.objects.filter(estado_proy=1)
    # envios = Envio.objects.filter(estado_env=1)
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    proyecto_sin_envio= []
    for proyecto in proyectos:
        encontrada= False
        for asignacion in asignaciones:
            if asignacion.proyecto_asig_id == proyecto.id_proy:
                encontrada= True
                break
        if not encontrada:
            proyecto_sin_envio.append(proyecto)
    return proyecto_sin_envio
def repetapas(resquest):
    asignaciones_destacadas = Asignacion.objects.filter(estado_asig= 1, fechaFin_asig__isnull=True)
    return asignaciones_destacadas
def repestacado(resquest):
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    asignaciones_estacado = []
    for asignacion in asignaciones:
        if not asignacion.fechaFin_asig and asignacion.fechaIni_asig and asignacion.personal_asig.cargo_perl.nombre_carg == "Estacador":
            asignaciones_estacado.append(asignacion)
    return asignaciones_estacado
def repdigitacion(resquest):
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    asignaciones_digitacion = []
    for asignacion in asignaciones:
        if not asignacion.fechaFin_asig and asignacion.fechaIni_asig  and asignacion.personal_asig.cargo_perl.nombre_carg == "Digitador":
            asignaciones_digitacion.append(asignacion)
    return asignaciones_digitacion
def repplano(resquest):
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    asignaciones_planos = []
    for asignacion in asignaciones:
        if not asignacion.fechaFin_asig and asignacion.fechaIni_asig  and asignacion.personal_asig.cargo_perl.nombre_carg == "Dibujante":
            asignaciones_planos.append(asignacion)
    return asignaciones_planos
def repenvio(resquest):
    if not resquest.user.has_perm('admRrhh.view_envio'):
        messages.error(resquest, "No tienes permiso para esta opcion, ponte en contacto con el administrador (TI).")
        return redirect('grafana_etapas') 
    envios = Envio.objects.filter(estado_env=2).order_by('-id_env') 
    proyectos = Proyecto.objects.all()
    asignaciones = Asignacion.objects.all()
    busqueda = resquest.GET.get("buscar")
    fecha_inicio = resquest.GET.get("fecha_inicio")
    fecha_fin = resquest.GET.get("fecha_fin")
    if busqueda:
        envios = Envio.objects.filter(
            Q(fechaEnv_env__icontains=busqueda)|
            Q(proyecto_env__nombre_proy__icontains=busqueda)|
            Q(proyecto_env__ubicacion_proy__icontains=busqueda)|
            Q(proyecto_env__fiscal_proy__apellidoP_fis__icontains=busqueda)|
            Q(proyecto_env__fiscal_proy__nombre_fis__icontains=busqueda)
            
        ).distinct()
    if fecha_inicio and fecha_fin:
        try:
            # Convertimos a formato de fecha
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

            # Aplicamos el filtro
            envios = envios.filter(fechaEnv_env__range=(fecha_inicio, fecha_fin))
        except ValueError:
            pass  # En caso de error de conversión, ignoramos el filtro
    elementos_por_pagina = 12
    paginator = Paginator(envios, elementos_por_pagina)
    page = resquest.GET.get("page", 1)

    try:
         envios = paginator.page(page)
    except PageNotAnInteger:
        envios = paginator.page(1)
    except EmptyPage:
        envios = paginator.page(paginator.num_pages)
    return render(resquest, 'reporte/listaenvio.html', {'envios': envios, 'proyectos': proyectos,'asignaciones': asignaciones})

def repersonal(resquest):
    personales = Personal.objects.filter(estado_perl = 1).order_by('-id_perl')
    elementos_por_pagina = 15
    paginator = Paginator(personales, elementos_por_pagina)
    page = resquest.GET.get("page", 1)
    try:
         personales = paginator.page(page)
    except PageNotAnInteger:
        personales = paginator.page(1)
    except EmptyPage:
        personales = paginator.page(paginator.num_pages)
    return render(resquest, 'reporte/listapersonal.html', {'personales':personales})

#///////EXPORT PDF REPORTES
def reproyecto_pdf2(resquest):
    datofech = datetime.now()
    asignaciones_inicio = repinicio(resquest)
    asignaciones_estacado = repestacado(resquest)
    asignaciones_digitacion = repdigitacion(resquest)
    asignaciones_plano = repplano(resquest)
    icon=  (settings.STATIC_URL,'img/logosercre.png')
    context = {'datofech': datofech, 'asignaciones_inicio': asignaciones_inicio,'asignaciones_estacado': asignaciones_estacado, 'asignaciones_digitacion': asignaciones_digitacion,'asignaciones_plano': asignaciones_plano,'icon': icon, 'user': resquest.user}
    template_path = 'reporte/listaproyectopdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    return response
def repenvio_pdf2(resquest):
    datofech = datetime.now()
    proyectos = Proyecto.objects.filter(estado_proy = 1).order_by('-id_proy')
    envios = Envio.objects.filter(estado_env = 2).order_by('-id_env')
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig')
    vacios = Asignacion.objects.all()
    icon=  (settings.STATIC_URL,'img/logosercre.png')
    context = {'datofech': datofech, 'asignaciones': asignaciones,'envios': envios,'vacios': vacios,'icon': icon, 'user': resquest.user}
    template_path = 'reporte/listaenviopdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    return response
def repersonal_pdf2(resquest):
    datofech = datetime.now()
    personales = Personal.objects.filter(estado_perl = 1).order_by('-id_perl')
    icon=  (settings.STATIC_URL,'img/logosercre.png')
    context = {'datofech': datofech, 'personales': personales,'icon': icon, 'user': resquest.user}
    template_path = 'reporte/listapersonalpdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    return response
#//////pdf1
def proyListapdf(resquest, id):
    datofech = datetime.now()
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig') 
    proyectos = Proyecto.objects.all()
    personales = Personal.objects.all()
    personas = Persona.objects.all()
    cargos = Cargo.objects.all()
    codigo = Proyecto.objects.get(id_proy=id)
    return render(resquest, 'proyecto/listapdf.html', {'datofech': datofech, 'asignaciones': asignaciones,'cargos': cargos, 'proyectos': proyectos, 'personales': personales,'personas': personas,'codigo': codigo})
def export_pdf(resquest):
    areas = Area.objects.all()
    context = {'areas': areas}
    template_path = 'area/listapdf.html'
    template = get_template(template_path)
    html = template.render(context)
    pdf_buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf_buffer)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="generarlm.pdf"'
    pdf_buffer.seek(0)
    response.write(pdf_buffer.read())
    return response
def export_pdf1(resquest, id):
    datofech = datetime.now()
    asignaciones = Asignacion.objects.filter(estado_asig = 1).order_by('-id_asig') 
    proyectos = Proyecto.objects.all()
    personales = Personal.objects.all()
    personas = Persona.objects.all()
    cargos = Cargo.objects.all()
    codigo = Proyecto.objects.get(id_proy=id)
    icon=  (settings.STATIC_URL,'img/logosercre.png')
    context = {'datofech': datofech, 'asignaciones': asignaciones,'cargos': cargos, 'proyectos': proyectos, 'personales': personales,'personas': personas,'codigo': codigo,'icon': icon,'user': resquest.user}
    template_path = 'proyecto/listapdf.html'
    template = get_template(template_path)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    return response
#////INSERTA IMAGENESW AL PDF
def link_callback(uri, rel):
     # Convertir rutas locales a rutas de sistema de archivos
    sUrl = settings.STATIC_URL      
    sRoot = settings.STATIC_ROOT    
    mUrl = settings.MEDIA_URL       
    mRoot = settings.MEDIA_ROOT     
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri
    if not os.path.isfile(path):
            raise Exception('Archivo no encontrado en link_callback: %s' % (sUrl, mUrl))
    return path
#//////GRAFANA
def grafana_etapas(resquest):
    counter_inicio = len(proyectos_asignados(resquest))
    counter_estacado = len(repestacado(resquest))
    counter_digitacion = len(repdigitacion(resquest))
    counter_plano = len(repplano(resquest))
    fecha_actual = datetime.now()
    fechaactuales = fecha_actual.strftime("%Y-%m-%d")
    envios = Envio.objects.filter(estado_env=2)
    asignaciones = Asignacion.objects.filter(estado_asig=1)
    proyectos = Proyecto.objects.filter(estado_proy=1)
    resultados = []
    counters = {
        'inicio': counter_inicio ,
        'Estacador': counter_estacado,
        'Digitador': counter_digitacion,
        'Dibujante': counter_plano,
    }
    for proyecto in proyectos:
        proyecto_agregado = False
        
        for envio in envios:
            if envio.proyecto_env_id == proyecto.id_proy:
                break
        else:
            fecha_diseno = datetime.strptime(proyecto.fechaDisen_proy, '%Y-%m-%d').date()
            # Calcula la diferencia en días entre la fecha de diseño y la fecha actual
            diferencia = (fecha_diseno - fecha_actual.date()).days
            
            # Asegurarse de que la diferencia no sea negativa, si es negativa tomar el valor absoluto
            diferencia = abs(diferencia)
            
            resultados.append({'proyecto': proyecto, 'diferencia': diferencia})
            proyecto_agregado = True
        if not proyecto_agregado:
            resultados.append({'proyecto': proyecto, 'diferencia': None})
    return render(resquest, 'index.html', {
        'counters': counters,
        'fecha_actual': fecha_actual,
        'fechaactuales': fechaactuales,
        'resultados': resultados,
        
    })

#///formato de cambio de permiso
def permisos_formato():
    permisos = Permission.objects.filter(
        content_type__app_label='admRrhh', 
        content_type__model__in=['Area', 'Cargo', 'Documento', 'Estudio', 'Profesion', 'Persona', 'Personal', 'Zona', 'Fiscal', 'Proyecto', 'Asignacion', 'Parentesco', 'Familiar', 'Envio', 'Ordent'],
    )
    acciones = {'add': 'adicionar_', 'change': 'actualizar_', 'delete': 'eliminar_', 'view': 'vista_'}
    permisos_modificados = [perm.codename.replace('add_', acciones['add']).replace('change_', acciones['change']).replace('delete_', acciones['delete']).replace('view_', acciones['view']) for perm in permisos]
    return zip(permisos, permisos_modificados)    
def obtener_grupos_y_permisos():
    grupos = Group.objects.all()
    grupos_con_permisos = {}
    for grupo in grupos:
        # Obtener los permisos asociados a este grupo
        permisos = grupo.permissions.all()
        permisos_modificados = []
        for permiso in permisos:
            nombre_permiso = permiso.codename
            # Reemplazar prefijos en el nombre del permiso
            nombre_permiso = nombre_permiso.replace('add_', 'adicionar ')
            nombre_permiso = nombre_permiso.replace('change_', 'actualizar ')
            nombre_permiso = nombre_permiso.replace('delete_', 'eliminar ')
            nombre_permiso = nombre_permiso.replace('view_', 'vista ')
            permisos_modificados.append((nombre_permiso, permiso.id))
        grupos_con_permisos[grupo] = permisos_modificados
    return grupos_con_permisos
def rolEliminar(resquest, id):
    grupo = Group.objects.get(id=id)
    grupo.delete()
    messages.success(resquest, "REGISTRO ELIMINADO")
    return redirect('rolLista')

