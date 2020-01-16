# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    ('Inicio', False, URL('default', 'index'), []),
    ('Encuestas', False, URL('default', 'encuestas'), []),
    ('Reportes', False, URL('default', 'reportes'), []),
]