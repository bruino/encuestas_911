# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    response.flash = 'Bienvenido'
    return dict()

@auth.requires_login()
def encuestas():
    if request.args(1) and request.args(1) == 'new':
        redirect(URL('nueva_encuesta'))

    fields = [
        db.reclamo.horario_llamada,
        db.reclamo.numero_ticket,
        db.reclamo.evento,
        db.reclamo.area,
        db.reclamo.persepcion_general_sistema,
    ]

    grid = SQLFORM.smartgrid(
        db.reclamo,
        breadcrumbs_class='breadcrumb',
        showbuttontext=True,
        fields=fields,
        csv=False,
        orderby=dict(reclamo=~db.reclamo.id),
        advanced_search=False,
        )
    return dict(grid=grid)

@auth.requires_login()
def nueva_encuesta():
    form = SQLFORM.factory(db.reclamo, submit_button='Enviar')
    if form.accepts(request.vars):
        id_reclamo = db.reclamo.insert(
            at_created=request.now,
            numero_ticket=form.vars.numero_ticket,
            horario_llamada=form.vars.horario_llamada,
            evento=form.vars.evento,
            direccion_hecho=form.vars.direccion_hecho,
            jurisdiccion_hecho=form.vars.jurisdiccion_hecho,
            area=form.vars.area,
            despacho_llamada=form.vars.despacho_llamada,
            atencion_telefonica=form.vars.atencion_telefonica,
            observacion_operador=form.vars.observacion_operador,
            llego_movil=form.vars.llego_movil,
            observacion_movil=form.vars.observacion_movil,
            persepcion_general_sistema=form.vars.persepcion_general_sistema,
            observacion_sistema=form.vars.observacion_sistema,
            hizo_denuncia=form.vars.hizo_denuncia,
            denuncia_comisaria=form.vars.denuncia_comisaria,
            tomaron_denuncia=form.vars.tomaron_denuncia,
            atencion_comisaria=form.vars.atencion_comisaria,
            observacion_comisaria=form.vars.observacion_comisaria,
        )
        redirect(URL('encuestas'))
    return dict(form=form)

@auth.requires_login()
def reportes():
    from widget import date_widget
    form = SQLFORM.factory(
        Field('desde', 'string', requires=IS_NOT_EMPTY()),#, widget=date_widget),
        Field('hasta', 'string', requires=IS_NOT_EMPTY())#, widget=date_widget),
    )

    if form.accepts(request.vars):
        redirect(URL('default', 'reportes', args=[form.vars.desde, form.vars.hasta]))
        
    return dict(
        form=form,
        )

def satisfaccion():
    query_satisfactorio = (db.reclamo.atencion_telefonica == 'Buena') | (db.reclamo.atencion_telefonica == 'Muy Buena') | (db.reclamo.atencion_telefonica == 'Excelente')
    query_no_satisfactorio = (db.reclamo.atencion_telefonica == 'Mala') | (db.reclamo.atencion_telefonica == 'Regular')
    satisfactorio = db(query_satisfactorio).count()
    no_satisfactorio = db(query_no_satisfactorio).count()
    return dict(satisfactorio=satisfactorio, no_satisfactorio=no_satisfactorio)

#Arreglado!
def calificacion_llamada():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1])

    cantidad_llamadas_calificacion_mala = db((db.reclamo.atencion_telefonica == 'Mala') & query_desde_hasta).count()
    cantidad_llamadas_calificacion_regular = db((db.reclamo.atencion_telefonica == 'Regular') & query_desde_hasta).count()
    cantidad_llamadas_calificacion_bueno = db((db.reclamo.atencion_telefonica == 'Buena') & query_desde_hasta).count()
    cantidad_llamadas_calificacion_muy_bueno = db((db.reclamo.atencion_telefonica == 'Muy Buena') & query_desde_hasta).count()
    cantidad_llamadas_calificacion_excelente = db((db.reclamo.atencion_telefonica == 'Excelente') & query_desde_hasta).count()

    cantidades = [
        cantidad_llamadas_calificacion_mala,
        cantidad_llamadas_calificacion_regular,
        cantidad_llamadas_calificacion_bueno,
        cantidad_llamadas_calificacion_muy_bueno,
        cantidad_llamadas_calificacion_excelente,
    ]
    return dict(cantidades=cantidades)

def solicitud_de_presencia_policial():
    query_desde_hasta = (db.reclamo.at_created >= request.args[0]) & (db.reclamo.at_created <= request.args[1])

    cantidad_zona_1 = db(db.reclamo.observacion_sistema == 'Presencia en zona 1').count()
    cantidad_zona_2 = db(db.reclamo.observacion_sistema == 'Presencia en zona 2').count()
    cantidad_zona_3 = db(db.reclamo.observacion_sistema == 'Presencia en zona 3').count()
    cantidad_zona_4 = db(db.reclamo.observacion_sistema == 'Presencia en zona 4').count()
    """ 
    comisarias = []
    cantidades = []
    for comisaria in db().select(db.comisaria.nombre):
        cantidad = db((db.reclamo.denuncia_comisaria == comisaria.nombre) & query_desde_hasta).count()
        comisarias.append(comisaria.nombre)
        cantidades.append(cantidad)

    from gluon.serializers import json """
    return dict(
        cantidad_zona_1=cantidad_zona_1,
        cantidad_zona_2=cantidad_zona_2,
        cantidad_zona_3=cantidad_zona_3,
        cantidad_zona_4=cantidad_zona_4,
    )

# Arreglado!
def eventos():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1])

    eventos = {}
    for evento in db().select(db.evento.nombre):
        cantidad = db((db.reclamo.evento == evento.nombre) & query_desde_hasta).count()
        eventos[evento.nombre] = cantidad

    import operator
    eventos_mayores = sorted(eventos.items(), key=operator.itemgetter(1), reverse=True)

    lista_eventos = []
    lista_cantidad = []
    for item in range(5):
        lista_eventos.append(eventos_mayores[item][0])
        lista_cantidad.append(eventos_mayores[item][1])

    # Promedio de Tiempo de Espera
    lista_moda_espera = []
    for evento in lista_eventos:
        rows = db((db.reclamo.evento == evento) & query_desde_hasta).select(db.reclamo.horario_llamada, db.reclamo.despacho_llamada)
        from datetime import datetime
        from statistics import mode
        diferencias_totales = []
        for row in rows:
            if row.horario_llamada is not None and row.despacho_llamada is not None:
                i = row.horario_llamada
                f = row.despacho_llamada
                diferencia = i - f
                diferencias_totales.append(int(-diferencia.total_seconds()/60))
        moda = mode(diferencias_totales)
        lista_moda_espera.append(moda)
    return dict(eventos=lista_eventos, cantidades=lista_cantidad, promedios=lista_moda_espera)

#Arreglado!
def fue_a_comisaria():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1]) & (db.reclamo.evento == 'Robo')
    cantidad_si = db((db.reclamo.hizo_denuncia == 'Si') & query_desde_hasta).count()
    cantidad_no = db((db.reclamo.hizo_denuncia == 'No') & query_desde_hasta).count()
    cantidad_ns = db((db.reclamo.hizo_denuncia == 'N/S') & query_desde_hasta).count()
    return dict(
        cantidad_si=cantidad_si,
        cantidad_no=cantidad_no,
        cantidad_ns=cantidad_ns,
        )

# Arreglado!
def cantidad_eventos_area():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1])
    areas_eventos_cantidades = []
    for area in [1, 2, 3, 4]:
        eventos = {}
        for evento in db().select(db.evento.nombre):
            cantidad = db((db.reclamo.area == area) & (db.reclamo.evento == evento.nombre) & query_desde_hasta).count()
            eventos[evento.nombre] = cantidad

        import operator
        eventos_mayores = sorted(eventos.items(), key=operator.itemgetter(1), reverse=True)
        lista_eventos = []
        lista_cantidad = []
        for item in range(5):
            lista_eventos.append(eventos_mayores[item][0])
            lista_cantidad.append(eventos_mayores[item][1])
        from gluon.serializers import json
        areas_eventos_cantidades.append([str(area), json(lista_eventos), json(lista_cantidad)])
    return dict(areas_eventos_cantidades=areas_eventos_cantidades)

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def grafico_calificacion_sistema():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1])
    
    cantidad_calificacion_sistema_mala = db((db.reclamo.persepcion_general_sistema == 'Mala') & query_desde_hasta).count()
    cantidad_calificacion_sistema_regular = db((db.reclamo.persepcion_general_sistema == 'Regular') & query_desde_hasta).count()
    cantidad_calificacion_sistema_bueno = db((db.reclamo.persepcion_general_sistema == 'Buena') & query_desde_hasta).count()
    cantidad_calificacion_sistema_muy_bueno = db((db.reclamo.persepcion_general_sistema == 'Muy Buena') & query_desde_hasta).count()
    cantidad_calificacion_sistema_excelente = db((db.reclamo.persepcion_general_sistema == 'Excelente') & query_desde_hasta).count()

    cantidades = [
        cantidad_calificacion_sistema_mala,
        cantidad_calificacion_sistema_regular,
        cantidad_calificacion_sistema_bueno,
        cantidad_calificacion_sistema_muy_bueno,
        cantidad_calificacion_sistema_excelente,
    ]
    return dict(cantidades=cantidades)

def grafico_atencion_comisaria():
    query_desde_hasta = (db.reclamo.horario_llamada >= request.args[0]) & (db.reclamo.horario_llamada <= request.args[1])
    
    cantidad_atencion_comisaria_mala = db((db.reclamo.atencion_comisaria == 'Mala') & query_desde_hasta).count()
    cantidad_atencion_comisaria_regular = db((db.reclamo.atencion_comisaria == 'Regular') & query_desde_hasta).count()
    cantidad_atencion_comisaria_bueno = db((db.reclamo.atencion_comisaria == 'Buena') & query_desde_hasta).count()
    cantidad_atencion_comisaria_muy_bueno = db((db.reclamo.atencion_comisaria == 'Muy Buena') & query_desde_hasta).count()
    cantidad_atencion_comisaria_excelente = db((db.reclamo.atencion_comisaria == 'Excelente') & query_desde_hasta).count()

    cantidades = [
        cantidad_atencion_comisaria_mala,
        cantidad_atencion_comisaria_regular,
        cantidad_atencion_comisaria_bueno,
        cantidad_atencion_comisaria_muy_bueno,
        cantidad_atencion_comisaria_excelente,
    ]
    return dict(cantidades=cantidades)
