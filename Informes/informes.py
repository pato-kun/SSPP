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
	_name = 'sspp.informesprofesor'
	_description = 'Formulario De Informes Profesor-coordinador'

	#name = fields.Char('Nombre Del Proyecto', size=256 , requiered=True, help='Nombre del proyecto')
	#student = fields.Many2one('Anteproyectos.user_group_student' ,  ondelete='set null', string="Estudiante", index=True ) #,default=lambda self: self.env.user )
	profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) #,domain=[('user.id')]) 
	project_id = fields.Many2one('sspp.anteproyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	dateFiled= fields.Date(string='Fecha')
	#fechafinal: fields.date('Fecha de fin', requiered=True),
	#tareasrealizadas: fields.char('Tareas realizadas', size=256 , requiered=True, help='Tareas realizadas en la semana'),
	description= fields.Char('Descripcion', size=256 , requiered=True, help='Descripcion')
	status= fields.Selection([('belated','Atrasado'),('onTime','A tiempo'), ('ahead','Adelantado')],'Estado del proyecto', default= 'onTime')
	comments= fields.Char('Comentarios', size=256 , requiered=True, help='Comentarios')
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
		'profAssesor': lambda obj, cr, uid, context: uid,
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
    

