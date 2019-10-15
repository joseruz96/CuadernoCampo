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
    lugar_ids = fields.One2many('cuaderno_campo.lugar','predio_id')
    almacenamiento_ids = fields.One2many('cuaderno_campo.almacenamiento','predio_id')
    formulario_ids = fields.One2many('cuaderno_campo.formulario', 'predio_id')

class Riesgo(models.Model):
    _name = 'cuaderno_campo.riesgo'
    _rec_name = 'proceso'
    _description = 'Identificación del riesgo'

    proceso = fields.Text(string='Proceso o Actividad')
    descripcion = fields.Text(string='Descrición del Riesgo')
    ocurrencia = fields.Selection([('b', 'B'), ('m', 'M'), ('a', 'A')], string='Probabilidad Ocurrencia / B=Bajo - M=Medio - A=Alto')
    severidad = fields.Selection([('b', 'B'), ('m', 'M'), ('a', 'A')],  string='Severidad / B=Bajo - M=Medio - A=Alto')
    peligro = fields.Selection([('sí', 'Si'), ('no', 'No')], string='Determine si el Peligro es Significativo')
    declaracion = fields.Text(string='Justifique Declaración')

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
    _rec_name = 'id'
    _description = 'Plan de acción respecto a la evaluación del riesgo'

    accion = fields.Text()

    evaluacion_id = fields.Many2one('cuaderno_campo.evaluacion_riesgo') 
    detalle_plan_accion_ids = fields.One2many('cuaderno_campo.detalle_plan_accion','plan_accion_id')

class Detalle_Plan_Accion(models.Model):
    _name = 'cuaderno_campo.detalle_plan_accion'
    _rec_name = 'id'
    _description = 'Detalle del plan de acción y los involucrados'

    plan_accion_id = fields.Many2one('cuaderno_campo.plan_accion')
    involucrado_id = fields.Many2one('cuaderno_campo.involucrado')
    responsabilidad = fields.Char(compute='_respon')
    fecha = fields.Datetime()
    
    @api.one
    @api.depends('involucrado_id')
    def _respon(self):
        for involucrado in self.involucrado_id:
            self.responsabilidad = involucrado.responsabilidad


class Involucrado(models.Model):
    _name = 'cuaderno_campo.involucrado'
    _rec_name = 'nombre'
    _description = 'Persona u empresa que está relacionado con el registro' 

    nombre = fields.Char()
    rut = fields.Char()
    responsabilidad = fields.Selection([('Verificador', 'Verificador'), ('Responsable', 'Responsable'), ('Presentador', 'Presentador'),('Empresa', 'Empresa')], string = 'Responsabilidad en el predio')

    calificacion_id = fields.Many2one('cuaderno_campo.calificacion')
    detalle_plan_accion_ids = fields.One2many('cuaderno_campo.detalle_plan_accion','involucrado_id')
    revision_equipo_ids = fields.One2many('cuaderno_campo.revision_equipo','involucrado_id')
    postcosecha_lote_ids = fields.One2many('cuaderno_campo.postcosecha_lote', 'involucrado_id')
    detalle_form_ids = fields.One2many('cuaderno_campo.detalle_form','involucrado_id')

class Calificacion(models.Model):
    _name = 'cuaderno_campo.calificacion'
    _rec_name = 'nombre'
    _description = 'Cargo del personal en la empresa'    

    nombre = fields.Char()

    involucrado_ids = fields.One2many('cuaderno_campo.involucrado', 'calificacion_id')



class Lugar(models.Model):
    _name = 'cuaderno_campo.lugar'
    _rec_name = 'nombre'
    _description = 'Identificar el lugar, ya sea Cuartel, Invernadero, etc.'

    tipo_lugar = fields.Selection([('cuartel','Cuartel'),('invernadero','Invernadero'),('sector','Sector')])
    nombre = fields.Char()
    superficie = fields.Integer()
    porta_injerto = fields.Char(string='Porta Injerto')
    polinizante = fields.Char()
    distancia = fields.Char(string='Distancia Plantación (m x m)')
    densidad = fields.Integer(string='Densidad de Plantación (N° Plantas)')
    año = fields.Char(string='Año de Plantación')
    sistema_c = fields.Char(string='Sistema de Conducción')
    sistema_r = fields.Char(string='Sistema de Riego')
    especie = fields.Char(compute='_especie')

    predio_id = fields.Many2one('cuaderno_campo.predio')
    variedad_id = fields.Many2one('cuaderno_campo.variedad')
    fecha_cosecha_ids = fields.One2many('cuaderno_campo.fecha_cosecha', 'variedad_id')
    embalaje_producto_ids = fields.One2many('cuaderno_campo.embalaje_producto', 'variedad_id')
   
    @api.one
    @api.depends('variedad_id')
    def _especie(self):
        for variedad in self.variedad_id:
            self.especie = variedad.especie_id.nombre

class Equipo(models.Model):
    _name = 'cuaderno_campo.equipo'
    _rec_name = 'nombre'
    _description = 'Equipo de protección para el personal'

    nombre = fields.Char()
    vida = fields.Char(string='Vida Útil')
    uso = fields.Selection([('siempre','Siempre'), ('a veces','A veces'),('nunca','Nunca')])
    respuesta = fields.Char(string='Cuando Responder')

    detalle_revision_equipo_ids = fields.One2many('cuaderno_campo.detalle_revision_equipo','equipo_id')

class Revision_Equipo(models.Model):
    _name = 'cuaderno_campo.revision_equipo'
    _rec_name = 'id'
    _description = 'Equipos que han sido revisados'

    fecha_revision = fields.Date()
    fecha_proxima = fields.Date()
    tipo_involucrado = fields.Char(compute='_respon', string='Tipo')

    detalle_revision_equipo_ids = fields.One2many('cuaderno_campo.detalle_revision_equipo','revision_equipo_id')
    involucrado_id = fields.Many2one('cuaderno_campo.involucrado')

    @api.one
    @api.depends('involucrado_id')
    def _respon(self):
        for involucrado in self.involucrado_id:
            self.tipo_involucrado = involucrado.responsabilidad

class Detalle_Revision_Equipo(models.Model):
    _name = 'cuaderno_campo.detalle_revision_equipo'
    _rec_name = 'id'
    _description = 'Detalle de la revisión de los equipos'

    reparacion = fields.Selection([('sí','Sí'), ('no','No')], string='¿Necesita Reparación?')
    cantidad_reponer = fields.Integer(string='Cantidad a Reponer')
    estado_revision = fields.Selection([('bueno','Bueno'), ('regular','Regular'),('malo','Malo')], string='Estado')
   
    equipo_id = fields.Many2one('cuaderno_campo.equipo')
    revision_equipo_id = fields.Many2one('cuaderno_campo.revision_equipo')


class Especie(models.Model):
    _name = 'cuaderno_campo.especie'
    _rec_name = 'nombre'
    _description = 'Especies tratadas en el predio'

    nombre = fields.Char(string='Especie')

    variedad_ids = fields.One2many('cuaderno_campo.variedad', 'especie_id')
    especie_procesar_ids = fields.One2many('cuaderno_campo.especie_procesar', 'especie_id')


class Variedad(models.Model):
    _name = 'cuaderno_campo.variedad'
    _rec_name = 'nombre'
    _description = 'Variedad correspondiente a una especie'

    nombre = fields.Char(string='Variedad')

    lugar_ids = fields.One2many('cuaderno_campo.lugar', 'variedad_id')
    especie_id = fields.Many2one('cuaderno_campo.especie')
    tratamiento_post_ids = fields.One2many('cuaderno_campo.tratamiento_postcosecha', 'variedad_id')
    fecha_cosecha_ids = fields.One2many('cuaderno_campo.fecha_cosecha', 'variedad_id')
    embalaje_producto_ids = fields.One2many('cuaderno_campo.embalaje_producto', 'variedad_id')
    despacho_producto_ids = fields.One2many('cuaderno_campo.despacho_producto', 'variedad_id')

class Carencia_LMR(models.Model):
    _name = 'cuaderno_campo.carencia_lmr'
    _rec_name = 'id'
    _description = 'Se especifica las carencias y LMR de pesticidas'


    fuente_info = fields.Char()
    ingrediente = fields.Char(compute='_ingrediente')


    especie_id = fields.Many2one('cuaderno_campo.especie')
    detalle_pais_ids = fields.One2many('cuaderno_campo.detalle_pais', 'carencia_lmr_id')
    agroquimico_id = fields.Many2one('cuaderno_campo.agroquimico')

    @api.one
    @api.depends('agroquimico_id')
    def _ingrediente(self):
        for agroquimico in self.agroquimico_id:
            self.ingrediente = agroquimico.ingrediente


class Pais(models.Model):
    _name = 'cuaderno_campo.pais' 
    _rec_name = 'nombre'
    _description = 'Mercado de destino de carencias y lmr'

    nombre = fields.Char()
    
    detalle_pais_ids = fields.One2many('cuaderno_campo.detalle_pais', 'pais_id')

class Detalle_Pais(models.Model):
    _name = 'cuaderno_campo.detalle_pais' 
    _description = 'Detalle de las carencias y lmr según mercado de destino'
    _rec_name = 'id'       

    lmr = fields.Integer(string='LMR (ppm)')
    carencia = fields.Integer(string='Carencia (días)')

    pais_id = fields.Many2one('cuaderno_campo.pais')
    carencia_lmr_id = fields.Many2one('cuaderno_campo.carencia_lmr')


class Agroquimico(models.Model):
    _name = 'cuaderno_campo.agroquimico' 
    _rec_name = 'nombre'
    _description = 'Agroquímicos usados en el predio'

    nombre = fields.Char(string='Nombre Comercial')
    ingrediente = fields.Char(string='Ingrediente Activo')
    nutriente = fields.Char(string='Contenido Nutrie')
    formulacion = fields.Char()
    registro = fields.Char()
    periodo_reingreso = fields.Char()
    accion = fields.Selection([('Acaricida','Acaricida'), ('Fungicida','Fungicida'),('Insecticida','Insecticida'), ('Herbicida','Herbicida'),('Nematicida','Nematicida'), ('Rodenticida','Rodenticida'),('Coadyuvante','Coadyuvante'),('Fetilizante','Fetilizante')], string='Acción')


    #agroquimico_equipo_ids = fields.One2many('cuaderno_campo.agroquimico_equipo', 'agroquimico_id')
    #accion_id = fields.Many2one('cuaderno_campo.accion')
    carencia_lmr_ids = fields.One2many('cuaderno_campo.carencia_lmr', 'agroquimico_id')
    tratamiento_post_ids = fields.One2many('cuaderno_campo.tratamiento_postcosecha', 'agroquimico_id')
  
class Aplicacion_Agroquimico(models.Model):
    _name = 'cuaderno_campo.aplicacion_agroquimico' 
    _rec_name = 'id'
    _description = 'Información acerca de la aplicació de los agroquímicos'

    superficie = fields.Integer(string='Superficie Tratada (hectáreas)')
    fecha = fields.Date(string="Fecha Aplicación")

# <-------------------------------------PENDIENTE DE VIEW---------------------------------------------->

class Tratamiento_Postcosecha(models.Model):
    _name = 'cuaderno_campo.tratamiento_postcosecha' 
    _rec_name = 'id'
    _description = ''

    objetivo = fields.Char(string='Objetivo del Control')
    descripcion = fields.Text(string='Descripción de Lotes')
    total_aplicado = fields.Integer()
    especie = fields.Char(compute='_especie')
    ingrediente = fields.Char(compute='_ingrediente')

    variedad_id = fields.Many2one('cuaderno_campo.variedad')
    agroquimico_id = fields.Many2one('cuaderno_campo.agroquimico')
    tipo_tratamiento_id = fields.Many2one('cuaderno_campo.tipo_tratamiento')
    packing_id = fields.Many2one('cuaderno_campo.packing')
    postcosecha_lote_ids = fields.One2many('cuaderno_campo.postcosecha_lote', 'tratamiento_post_id')

    @api.one
    @api.depends('variedad_id')
    def _especie(self):
        for variedad in self.variedad_id:
            self.especie = variedad.especie_id.nombre

    @api.one
    @api.depends('agroquimico_id')
    def _ingrediente(self):
        for agroquimico in self.agroquimico_id:
            self.ingrediente = agroquimico.ingrediente

class Tipo_Tratamiento(models.Model):
    _name = 'cuaderno_campo.tipo_tratamiento' 
    _rec_name = 'id'
    _description = ''

    nombre = fields.Char(string='Tipo de Tratamiento')

    tratamiento_post_ids = fields.One2many('cuaderno_campo.tratamiento_postcosecha', 'tipo_tratamiento_id')

class Packing(models.Model):
    _name = 'cuaderno_campo.packing' 
    _rec_name = 'nombre'
    _description = '' 

    nombre = fields.Char(string='Nombre del Packing')
    razon_social = fields.Char()
    rut = fields.Char()
    direccion = fields.Char(string='Dirección')
    comuna = fields.Char()
    region = fields.Char(string='Región')
    telefono = fields.Char(string='Teléfono')
    fax = fields.Char()
    email = fields.Char()
    representante = fields.Char(string='Representante')

    tratamiento_post_ids = fields.One2many('cuaderno_campo.tratamiento_postcosecha', 'packing_id')
    especie_procesar_ids = fields.One2many('cuaderno_campo.especie_procesar', 'packing_id')
    embalaje_producto_ids = fields.One2many('cuaderno_campo.embalaje_producto', 'packing_id')

class Lote(models.Model):
    _name = 'cuaderno_campo.lote' 
    _rec_name = 'id'
    _description = ''

    unidad = fields.Integer(string='Unidad de Embalaje')
    postcosecha_lote_ids = fields.One2many('cuaderno_campo.postcosecha_lote', 'lote_id')

class Postcosecha_Lote(models.Model):
    _name = 'cuaderno_campo.postcosecha_lote' 
    _rec_name = 'id'
    _description = ''

    fecha = fields.Date(string='Fecha de Tratamiento')
    dosis = fields.Char()
    cantidad_aplicado = fields.Integer()
    lote = fields.Char(compute='_lote', string='N° Unidades / Lote')


    tratamiento_post_id = fields.Many2one('cuaderno_campo.tratamiento_postcosecha')
    lote_id = fields.Many2one('cuaderno_campo.lote')
    involucrado_id = fields.Many2one('cuaderno_campo.involucrado')

    @api.one
    @api.depends('lote_id')
    def _lote(self):
        for lote in self.lote_id:
            self.lote = lote.unidad


class Fecha_Cosecha(models.Model):
    _name = 'cuaderno_campo.fecha_cosecha' 
    _rec_name = 'fecha'
    _description = ''

    fecha = fields.Date('Fecha de Cosehca')
    especie = fields.Char(compute='_especie')
    cantidad = fields.Integer(string='Cantidad Cosechada')
    guia_despacho = fields.Integer(string='N° Guía de Despacho')

    lugar_id = fields.Many2one('cuaderno_campo.lugar')
    variedad_id = fields.Many2one('cuaderno_campo.variedad')

    @api.one
    @api.depends('variedad_id')
    def _especie(self):
        for variedad in self.variedad_id:
            self.especie = variedad.especie_id.nombre

class Especie_Procesar(models.Model):
    _name = 'cuaderno_campo.especie_procesar' 
    _rec_name = 'id'
    _description = ''

    especie_id = fields.Many2one('cuaderno_campo.especie')
    packing_id = fields.Many2one('cuaderno_campo.packing')


class Embalaje_Producto(models.Model):
    _name = 'cuaderno_campo.embalaje_producto' 
    _rec_name = 'id'
    _description = ''

    fecha = fields.Date(string='Fecha de Embalaje')
    num_recepcion = fields.Integer(string='Número de Recepción')
    envase = fields.Char()
    cantidad = fields.Integer(string='Cantidad Envasada')
    observacion = fields.Text()
    especie = fields.Char(compute='_especie')

    variedad_id = fields.Many2one('cuaderno_campo.variedad')
    packing_id = fields.Many2one('cuaderno_campo.packing')
    lugar_id = fields.Many2one('cuaderno_campo.lugar')
    despacho_producto_id = fields.Many2one('cuaderno_campo.despacho_producto')

    @api.one
    @api.depends('variedad_id')
    def _especie(self):
        for variedad in self.variedad_id:
            self.especie = variedad.especie_id.nombre
        

class Despacho_Producto(models.Model):
    _name = 'cuaderno_campo.despacho_producto' 
    _rec_name = 'id'
    _description = ''

    unidad = fields.Integer(string='Unidad Embalaje')
    fecha = fields.Date(string='Fecha Despacho')
    destinatario = fields.Char()
    envase = fields.Char()
    observacion = fields.Text()

    variedad_id = fields.Many2one('cuaderno_campo.variedad')

class Almacenamiento(models.Model):
    _name = 'cuaderno_campo.almacenamiento' 
    _rec_name = 'nombre'
    _description = ''

    nombre = fields.Char()

    predio_id = fields.Many2one('cuaderno_campo.predio')
    control_temperatura_ids = fields.One2many('cuaderno_campo.control_temperatura', 'almacenamiento_id')

class Control_Temperatura(models.Model):
    _name = 'cuaderno_campo.control_temperatura' 
    _rec_name = 'id'
    _description = ''

    fecha = fields.Date(string='Fecha de Control')

    almacenamiento_id = fields.Many2one('cuaderno_campo.almacenamiento')
    detalle_control_ids = fields.One2many('cuaderno_campo.detalle_control', 'control_temperatura_id')

class Hora_Control(models.Model):
    _name = 'cuaderno_campo.hora_control' 
    _rec_name = 'hora'
    _description = ''

    hora = fields.Datetime(string='Hora del Control')

    detalle_control_ids = fields.One2many('cuaderno_campo.detalle_control', 'hora_control_id')


class Detalle_Control(models.Model):
    _name = 'cuaderno_campo.detalle_control' 
    _rec_name = 'id'
    _description = ''

    temperatura = fields.Float()
    humedad = fields.Float()

    control_temperatura_id = fields.Many2one('cuaderno_campo.control_temperatura')
    hora_control_id = fields.Many2one('cuaderno_campo.hora_control')

class Formulario(models.Model):
    _name = 'cuaderno_campo.formulario' 
    _rec_name = 'id'
    _description = ''

    fecha_presentacion = fields.Date()
    descripcion = fields.Text()
    causa = fields.Text()
    accion_reparadora = fields.Text()
    accion_correctiva = fields.Text()
    costo = fields.Text()
    fecha_aplicacion = fields.Date()
    fecha_cierre = fields.Date()
  
    predio_id = fields.Many2one('cuaderno_campo.predio')
    tipo_formulario_id = fields.Many2one('cuaderno_campo.tipo_formulario')
    detalle_form_ids = fields.One2many('cuaderno_campo.detalle_form','formulario_id')

class Tipo_Formulario(models.Model):
    _name = 'cuaderno_campo.tipo_formulario' 
    _rec_name = 'id'
    _description = ''

    nombre = fields.Char()

class Detalle_Form(models.Model):
    _name = 'cuaderno_campo.detalle_form' 
    _rec_name = 'id'
    _description = ''

    formulario_id = fields.Many2one('cuaderno_campo.formulario')
    involucrado_id = fields.Many2one('cuaderno_campo.involucrado')
