# -*- coding: utf-8 -*-
from odoo import http

# class CuadernoCampo(http.Controller):
#     @http.route('/cuaderno_campo/cuaderno_campo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cuaderno_campo/cuaderno_campo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cuaderno_campo.listing', {
#             'root': '/cuaderno_campo/cuaderno_campo',
#             'objects': http.request.env['cuaderno_campo.cuaderno_campo'].search([]),
#         })

#     @http.route('/cuaderno_campo/cuaderno_campo/objects/<model("cuaderno_campo.cuaderno_campo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cuaderno_campo.object', {
#             'object': obj
#         })