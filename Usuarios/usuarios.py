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


class usuarios_users(models.Model): #osv.osv
	_inherit = 'res.users'
	_name = 'res.users'
	#_name = 'professor.users' #decided skip this step during first iteration
	topics = fields.Many2many( 'anteproyecto.topics' , 'id', 'name')#, string='Areas de Conocimineto')
	#role specific attributes

	cantStudents = fields.Integer()
	carnet = fields.Integer()
	

	isProfessor = fields.Boolean()
	isStudent = fields.Boolean()
	isAdmin = fields.Boolean()
	

	#probe if user belongs to a group
	def _get_flag(self):
		self.isStudent = self.pool.get('res.users').has_group(cr, uid, 'Anteproyectos.user_group_student') 

	_defaults = {
	'isStudent': True,
	'isProfessor': False,
	'isAdmin' : False
	}

	@api.onchange('isStudent')
	def dynamic_student_domain(self):
		if self.isStudent:
			self.isProfessor = False
		else:
			self.isStudent =False
			self.carnet = 0
			self.isProfessor = True

	@api.onchange('isProfessor')
	def dynamic_professor_domain(self):
		if self.isProfessor:
			self.isStudent = False
			self.carnet = 0
		# else:
		# 	self.isProfessor =False
		# 	self.isStudent = True

	@api.model
	def create(self, vals):
		rec = super(usuarios_users, self).create(vals)
		#user = self.env['res.users'].search([('isProfessor', '=', True)])
		rec.insertToGroup()
		return rec

	@api.one
	def insertToGroup(self):
		res_groups = self.env['res.groups']
		groupStudents = res_groups.search([('name', '=', 'Grupo Estudiantes')])
		groupProfessors = res_groups.search([('name', '=', 'Grupo Profesores')])
		groupCoord = res_groups.search([('name', '=', 'Technical Features')])

		if self.isProfessor:
			groupProfessors.write({ 'users': [(4, self.id, None)]})
		elif self.isStudent:
			groupStudents.write({ 'users': [(4, self.id, None)]})
		elif self.isAdmin:
			groupCoord.write({ 'users': [(4, self.id, None)]})
		else:
			return {
					'warning': {
						'title': _('Aviso'),
						'message': _('Seleccione un rol para el usuario.')
					}
			}

#class res_users_student(osv.osv):
#    _inherit = 'res.users.user'
#    _name = 'student'
#    _columns = { 'categ_ids': fields.many2many('professor.category', string='Tags'), }
#    @api.model
#    def create(self, values):
#        return super(User, self).create(values)


    
    

