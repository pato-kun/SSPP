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


from openerp.tools.translate import _
from openerp import api, models, fields
import time


class anteproyecto(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.anteproyecto'
	_description = 'Formulario De Anteproyecto'

	name = fields.Char('Nombre Del Proyecto', size=256 , requiered=True, help='Nombre del proyecto')
	student = fields.Many2one('res.users' ,  ondelete='set null', string="Estudiante", index=True ) #,default=lambda self: self.env.user )
	company = fields.Many2one('res.partner', 'Empresa',requiered=True)
	companyContact = fields.Many2one('res.partner', ondelete='set null', string="Contacto de la Empresa", index=True )
	companyAssesor = fields.Many2one('res.partner', ondelete='set null', string="Asesor en la Empresa", index=True )
	profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) 
		#, domain="[('asset_catg_id', '=',place)]"),
		#, read=['Anteproyectos.user_group_professor'] )
	possibleTasks = fields.Html('Posibles Trabajos a Realizar', requiered=True, help='Posibles trabajos a realizar')
	#'fechainicio': fields.date('Fecha de inicio', requiered=True),
	#'fechafinal': fields.date('Fecha de fin', requiered=True),
	actualTask = fields.Html('Descripcion Del Trabajo A Realizar',  requiered=True, help='Trabajos a realizar durante el proyecto')
	generalObjetive  = fields.Html('Objetivo General Del Trabajo',  requiered=True, help='Objetivo general del proyecto')
	specificObjective = fields.Html('Objetivos Especificos',  requiered=True, help='Objetivos especificos para logra el objetivo')
	metodology = fields.Html('Metodologia',  requiered=True, help='Describa la metodologia a utilizar')
	tools = fields.Html('Tecnicas o Herramientas A Utilizar', size=256 , requiered=True, help='Herramientas a usar para lograr los objetivos')
	topics = fields.Many2many('anteproyecto.topics', string='Areas de estudio',ondelete='cascade')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto', default= 'draft')

	

	@api.multi
	def action_draft(self):
		self.state = 'draft'
	@api.one
	def action_aprove(self):
		self.state = 'aprove'
	@api.one
	def action_reject(self):
		self.write({
	    'state': 'reject',
		})
		#self.state = 'reject'

	_defaults = {
		'student': lambda obj, cr, uid, context: uid,
		'state': 'draft', 
	}
	
	#@api.onchange(student)
	#def dynamic_student_domain(self):
    #  return {'domain': {'student': [('student.groups_id','in',['Anteproyectos.user_group_student'])]}}

	
#class res_users_student(osv.osv):
#    _inherit = 'res.users.user'
#    _name = 'student'
#    _columns = { 'categ_ids': fields.many2many('professor.category', string='Tags'), }
#    @api.model
#    def create(self, values):
#        return super(User, self).create(values)
    

class anteproyecto_tema(models.Model):
	""" Area que conocimiento que abarca """
	_name = 'anteproyecto.topics'
	_description = "Area de estudio o tema."
	name = fields.Char('Nombre', required=True, translate=True)
    
    # User can write on a few of his own fields (but not his groups for example)
    #SELF_WRITEABLE_FIELDS = ['name']
    # User can read a few of his own fields
    #SELF_READABLE_FIELDS = ['profAssesor'] 


#class contacto_empresa_partner(models.Model): #osv.osv
#    _inherit = 'res.partner'
    #_name = 'contacto.partner' #decided skip this step during first iteration
    

#class asesor_empresa_partner(models.Model):
#    _inherit = 'res.partner'
    #_name = 'asesor.partner'

#    def create(self, values):
#        return super(User, self).create(values)
    

