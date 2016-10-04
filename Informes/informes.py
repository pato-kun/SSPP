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
from openerp import api, models, fields, tools
import logging
import time
from openerp.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class informesprofesor(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.informesprofesor'
	_description = 'Formulario De Informes Profesor-coordinador'

	#name = fields.Char('Nombre Del Proyecto', size=256 , requiered=True, help='Nombre del proyecto')
	student = fields.Many2one('res.users', 'Estudiante', ondelete='set null', requiered=True)
		#,domain="[('isStudent2','=',True)]"  )
		#, domain=[(_get_students(self))]) #,default=lambda self: self.env.user )
	profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) #,domain=[('user.id')]) 
	project_id = fields.Many2one('sspp.anteproyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	dateFiled= fields.Date(string='Fecha')
	#fechafinal: fields.date('Fecha de fin', requiered=True),
	#tareasrealizadas: fields.char('Tareas realizadas', size=256 , requiered=True, help='Tareas realizadas en la semana'),
	description= fields.Char('Descripcion', size=256 , requiered=True, help='Descripcion del avance')
	status= fields.Selection([('belated','Atrasado'),('onTime','A tiempo'), ('ahead','Adelantado')],'Estado del proyecto', default= 'onTime')
	comments= fields.Char('Comentarios', size=256 , requiered=True, help='Comentarios')
	commentsCoord= fields.Char('Observaciones del Coordinador', size=256 , help='Observaciones del Coordinador')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto', default= 'draft')
	#sortField = fields.Boolean(compute='sort_index_groups')


	# @api.multi
	# def sort_index_groups(self):
	# 	#env = Environment(cr, uid, context)
	# 	recs = self.env['res.users']  
	# 	#recs = recs.search([Dominio con Condiciones para la Busqueda de Registros])
	# 	for user in recs:
	# 		if user.has_group('Anteproyectos.user_group_student'):
	# 			user.isStudent = True
	# 			_logger.warning('WARNING: entro! %s', user.name)
	# 		elif user.has_group('Anteproyectos.user_group_professor'):
	# 			user.isProfessor = True
	# 		else:
	# 			user.isStudent = False
	# 			_logger.warning('WARNING: no entro! %s', user.name)
	# 			user.isProfessor = False

	# @api.multi
	# def sort_index_groups(self, cr, uid, ids, context=None):
	# 	user_ids = self.search(cr, uid, [], context=context)
	# 	for user in self.browse(cr, uid, user_ids, context=context):
	# 		if user.has_group(cr, uid,'Anteproyectos.user_group_student'):
	#  			user.isStudent = True
	#  		elif user.has_group(cr, uid,'Anteproyectos.user_group_professor'):
	#  			user.isProfessor = True
	#  		else:
	#  			user.isStudent = False
	#  			user.isProfessor = False




	# @api.multi
	# def sort_index_groups(self):
	# 	all_users =self.pool.get('res.users')
		
	# 	for id2 in all_users.browse(cr, uid, uid, context=context):
	# 		user1=id2
	# 		if user1.has_group(cr, user1.id,'Anteproyectos.user_group_student'):
	# 			user1.isStudent = True
	# 		elif user1.has_group(cr, user1.id,'Anteproyectos.user_group_professor'):
	# 			user1.isProfessor = True
	# 		else:
	# 			user1.isStudent = False
	# 			user1.isProfessor = False

		
		# group = self.env['res.groups'].search([('category_id.name', '=', 'user_group_student')])
		# group2 = self.env['res.groups'].search([('category_id.name', '=', 'user_group_professor')])

		# for recipient in group.users:
		# 	for use in all_users:
		# 		if recipient.users.uid == all_users.groups_id.uid:
		# 			user.isStudent  = True
		
		# for recipient2 in group2.users:
		# 	recipient2.isProfessor = True	

		# def has_group2(self,cr,uid,group_ext_id):
  #        if '.' in group_ext_id:
  #             users_group1 = [x.id for x in self.pool['ir.model.data'].get_object(cr, uid, 'bms',  'Anteproyectos.user_group_student').users]
  #             users_group2 = [x.id for x in self.pool['ir.model.data'].get_object(cr, uid, 'bms',  'Anteproyectos.user_group_professor').users]

  #             if uid in users_group1:
  #                 return super(Users,self).has_group2(cr,uid,'Anteproyectos.user_group_student')
  #             elif uid in users_group2:
  #                 return super(Users,self).has_group2(cr,uid,'Anteproyectos.user_group_professor')
  #             else:
  #                 return super(Users,self).has_group2(cr,uid,'base.group_user')

  #        else:
  #            return super(Users,self).has_group(cr,uid,group_ext_id)
		
		
		    
	    

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
		#'student': lambda self, cr, uid, context:self._get_students(self),
		'state': 'draft', 
	}
	#@api.onchange(student)
	#def dynamic_student_domain(self):
    #  return {'domain': {'student': [('student.groups_id','in',['Anteproyectos.user_group_student'])]}}

		#try this: get_students; returns domain 
		#<field name="subject_id" domain="list_new" />
	#def _get_domain(self, cr, uid, ids, field_name, arg, context=None):
	#    record_id = ids[0] 
	#    # do some computations....
	#    return {record_id: YOUR DOMAIN} 

	#'list_new': fields.function(_get_domain, type='char', size=255, method=True, string="Domain"),