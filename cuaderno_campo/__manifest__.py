# -*- coding: utf-8 -*-
{
    'name': "CuadernoCampo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
        'views/predio.xml',
        'views/riesgo.xml',
        'views/tipo_evaluacion.xml',
        'views/evaluacion_riesgo.xml',
        'views/plan_accion.xml',
        'views/lugar.xml',
        'views/calificacion.xml',
        'views/involucrado.xml',
        'views/detalle_plan_accion.xml',
        'views/equipo.xml',
        'views/revision_equipo.xml',
        'views/detalle_revision_equipo.xml',
        'views/especie.xml',
        'views/variedad.xml',
        'views/carencia_lmr.xml',
        'views/pais.xml',
        'views/detalle_pais.xml',
        'views/agroquimico.xml',
        'views/tratamiento_postcosecha.xml',
        'views/tipo_tratamiento.xml',
        'views/packing.xml',
        'views/lote.xml',
        'views/postcosecha_lote.xml',
        'views/fecha_cosecha.xml',
        'views/especie_procesar.xml',
        'views/embalaje_producto.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}