# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class cuaderno_campo(models.Model):
#     _name = 'cuaderno_campo.cuaderno_campo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Predio(models.Model):
    _name = 'cuaderno_campo.predio'
    _rec_name = 'nombre'
    _description = 'Datos del predio'

    razon_social = fields.Char()
    rut = fields.Char()
    nombre = fields.Char(string='Nombre del Predio')
    direccion = fields.Char(string='Dirección')
    comuna = fields.Char()
    region = fields.Char(string='Región')
    telefono = fields.Char(string='Teléfono')
    fax = fields.Char()
    email = fields.Char()
    representante = fields.Char(string='Representante')
    superficie_total = fields.Integer()
    superficie_plantada = fields.Integer()
    encargado = fields.Char(string='Encargado Cuaderno de Campo')
    reemplazante = fields.Char(string='Reempazante del Encargado Cuaderno de Campo')

    evaluacion_riesgo_ids = fields.One2many('cuaderno_campo.evaluacion_riesgo', 'predio_id')


class Riesgo(models.Model):
    _name = 'cuaderno_campo.riesgo'
    _rec_name = 'proceso'
    _description = 'Identificación del riesgo'

    proceso = fields.Char(string='Proceso o Actividad')
    descripcion = fields.Char(string='Descrición del Riesgo')
    ocurrencia = fields.Selection([('b', 'B'), ('m', 'M'), ('a', 'A')], string='Probabilidad Ocurrencia / B=Bajo - M=Medio - A=Alto')
    severidad = fields.Selection([('b', 'B'), ('m', 'M'), ('a', 'A')],  string='Severidad / B=Bajo - M=Medio - A=Alto')
    peligro = fields.Selection([('sí', 'Si'), ('no', 'No')], string='Determine si el Peligro es Significativo')
    declaracion = fields.Char(string='Justifique Declaración')

    evaluacion_riesgo_ids = fields.One2many('cuaderno_campo.evaluacion_riesgo', 'riesgo_id')


class Tipo_Evaluacion(models.Model):
    _name = 'cuaderno_campo.tipo_evaluacion'
    _rec_name = 'nombre'
    _description = 'Tipo de evaluación de riesgo'

    nombre = fields.Char()
    
    evaluacion_riesgo_ids = fields.One2many('cuaderno_campo.evaluacion_riesgo', 'tipo_evaluacion_id')

class Evaluacion_Riesgo(models.Model):
    _name = 'cuaderno_campo.evaluacion_riesgo'
    _rec_name = 'id'
    _description = 'Evaluación del riesgo seleccionado'

    ubicacion = fields.Char(compute='_select_ubicacion')
    fecha = fields.Datetime()
    informacion = fields.Text(string='Ingrese información sobre el tipo de evaluación a realizar')
    
    predio_id = fields.Many2one('cuaderno_campo.predio')
    riesgo_id = fields.Many2one('cuaderno_campo.riesgo')
    tipo_evaluacion_id = fields.Many2one('cuaderno_campo.tipo_evaluacion')
    
    @api.one
    @api.depends('predio_id')
    def _select_ubicacion(self):
        for predio in self.predio_id:
            self.ubicacion = predio.direccion

class Plan_Accion(models.Model):
    _name = 'cuaderno_campo.plan_accion'
    _description = 'Plan de acción respecto a la evaluación del riesgo'

    accion = fields.Text()
    fecha = fields.Datetime(string='Fecha de Implementación')
    fecha_verificacion = fields.Datetime(string='Fecha de Verificación')

    evaluacion_id = fields.Many2one('cuaderno_campo.evaluacion_riesgo')  
