# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2010-2011 OpenERP s.a. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#	Coded by: pat01822@gmail.com
#
##############################################################################


from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import api, models
import time


class anteproyecto(models.Model):
    _name = 'sspp.anteproyecto'

    _description = 'Formulario De Anteproyecto'

    _columns = {
     	'possibleTasks': fields.char('Posibles Tareas A Realizar', size=256 , requiered=True, help='Posibles trabajos a realizar'),
        #'fechainicio': fields.date('Fecha de inicio', requiered=True),
        #'fechafinal': fields.date('Fecha de fin', requiered=True),
        'actualTask': fields.char('Descripcion Del Trabajo A Realizar', size=256 , requiered=True, help='Trabajos a realizar durante el proyecto'),
        'generalObjetive': fields.char('Objetivo General Del Trabajo', size=256 , requiered=True, help='Objetivo general del proyecto'),
    	'specificObjective': fields.char('Objetivos Especificos', size=256 , requiered=True, help='Objetivos especificos para logra el objetivo'),
        'metodology': fields.char('Metodologia', size=256 , requiered=True, help='Describa la metodologia a utilizar'),
        'tools': fields.char('Tecnicas o Herramientas A Utilizar', size=256 , requiered=True, help='Herramientas a usar para lograr los objetivos'),
        #'categ_ids': fields.many2many('prof.category', string='Areas de estudio'), #, relation='professor_category_sspp_anteproyecto_rel'
        'state': fields.selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto'),
    }

    _defaults = {
    	'state': 'draft', 
    }
    



#class contacto_empresa_partner(models.Model): #osv.osv
#    _inherit = 'res.partner'
    #_name = 'contacto.partner' #decided skip this step during first iteration
    

#class asesor_empresa_partner(models.Model):
#    _inherit = 'res.partner'
    #_name = 'asesor.partner'

#    def create(self, values):
#        return super(User, self).create(values)
    

