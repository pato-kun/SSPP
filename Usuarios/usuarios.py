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

	#categ_ids = fields.Many2many(related='anteproyecto.topics', string='Areas de Conocimineto',ondelete='cascade')

#class res_users_student(osv.osv):
#    _inherit = 'res.users.user'
#    _name = 'student'
#    _columns = { 'categ_ids': fields.many2many('professor.category', string='Tags'), }
#    @api.model
#    def create(self, values):
#        return super(User, self).create(values)


    
    

