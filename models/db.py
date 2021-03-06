# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig()

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
from custom_form import custom_formstyle
response.formstyle = custom_formstyle
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)
from widget import datetime_widget, time_widget

db.define_table('evento',
    Field('nombre', 'string'),
)

db.define_table('comisaria',
    Field('nombre', 'string'),
)

db.define_table('reclamo',
    Field('at_created', 'date', writable=False, readable=True, default=request.now, label='Fecha Creación'),
    Field('numero_ticket', 'integer', label='N° de Ticket'),
    Field('horario_llamada', 'datetime', widget=datetime_widget, label='Fecha y Horario de la Llamada', requires=IS_DATETIME(format=T('%d/%m/%Y %H:%M'))),
    Field('evento', 'string', requires=IS_IN_DB(db, 'evento.nombre', '%(nombre)s'), label='Tipo de Evento'),
    Field('direccion_hecho', 'string', label='Dirección del Hecho de Robo'),
    Field('jurisdiccion_hecho', 'string', requires=IS_EMPTY_OR(IS_IN_DB(db, 'comisaria.nombre', '%(nombre)s')), label='Jurisdicción del Hecho de Robo'),
    Field('area', 'integer', requires=IS_IN_SET([1, 2, 3, 4]), label='Área'),
    Field('despacho_llamada', 'datetime', widget=datetime_widget, label='Horario de Despacho de Llamada por parte del Móvil Policial', requires=IS_DATETIME(format=T('%d/%m/%Y %H:%M'))),
    Field('atencion_telefonica', 'string', requires=IS_IN_SET(['Mala', 'Regular', 'Buena', 'Muy Buena', 'Excelente']), label='Atención Telefónica'),
    Field('observacion_operador', 'string', label='Observaciones de Operadores', 
            requires=IS_IN_SET([
                'Telefonista durmiendo',
                'Telefonista con falta de ubicación',
                'Falta de respeto',
                'Falta de atención',
                'Desinterés',
                'Sin comentarios',
            ])), #estrellas
    Field('llego_movil', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['Si', 'No', 'N/S'])), widget=SQLFORM.widgets.radio.widget, label='¿Llegó el Móvil?'), # Si, No, N/S
    Field('observacion_movil', 'string', label='Observaciones de Móviles',
            requires=IS_IN_SET([
                'Falta de atención ciudadana',
                'Falta de respeto',
                'Agresión verbal',
                'Agresión física',
                'Falta de profesionalismo',
                'Falta de ubicación',
                'Demora en móvil',
                'Sin comentarios',
            ])),
    Field('persepcion_general_sistema', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['Mala', 'Regular', 'Buena', 'Muy Buena', 'Excelente'])), label='Percepción general del Sistema'), #estrellas
    Field('observacion_sistema', 'string', label='Observaciones del Sistema', 
            requires=IS_IN_SET([
                'Presencia en zona 1',
                'Presencia en zona 2',
                'Presencia en zona 3',
                'Presencia en zona 4',
                'Falta de profesionalismo en GU',
                'Falta de profesionalismo en Cria.',
                'Falta de nafta en móvil',
                'Sin comentarios',
            ])),
    Field('hizo_denuncia', 'string', requires=IS_IN_SET(['Si', 'No', 'N/S']), widget=SQLFORM.widgets.radio.widget, label='¿Hizo la Denuncia?'), #Si, No, N/S
    Field('denuncia_comisaria', 'string', requires=IS_EMPTY_OR(IS_IN_DB(db, 'comisaria.nombre', '%(nombre)s')), label='¿Cuál fue la Comisaría?'),
    Field('tomaron_denuncia', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['Si', 'No'])), widget=SQLFORM.widgets.radio.widget, label='¿Le tomaron la denuncia?'), #Si, No, N/S
    Field('atencion_comisaria', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['Mala', 'Regular', 'Buena', 'Muy Buena', 'Excelente'])), label='¿Cómo fue la Atención?'),
    Field('observacion_comisaria', 'string', label='Observaciones de Comisaría',
            requires=IS_EMPTY_OR(IS_IN_SET([
                    'Falta de atención ciudadana',
                    'No tenía papel',
                    'No habia personal',
                    'No tenían combustible',
                    'No le quisieron dar una copia',
                    'Cobro indebido',
                    'Falta de respeto',
                    'Vinculación de Droga',
                    'Vinculación con Ladrones',
                    'No responden los telefonos',
                    'Sin comentarios',
            ]))),
)
