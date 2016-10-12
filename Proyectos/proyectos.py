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

class proyecto(models.Model):
	_inherit = 'sspp.anteproyecto'
	_name = 'sspp.proyecto'
	_description = 'Estado del Proyecto'
	# profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) 
	# project_id = fields.Many2one('sspp.anteproyecto', 'Proyecto' ,ondelete='set null',requiered=True ) 
	# dateFiled= fields.Date(string='Fecha')
	# description= fields.Char('Descripcion', size=256 , requiered=True, help='Descripcion del avance')
	#status= fields.Selection([('belated','Atrasado'),('onTime','A tiempo'), ('ahead','Adelantado')],'Estado del proyecto', default= 'onTime')
	# comments= fields.Char('Comentarios', size=256 , requiered=True, help='Comentarios')
	# commentsCoord= fields.Char('Observaciones del Coordinador', size=256 , help='Observaciones del Coordinador')
	# state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto', default= 'draft')

	

	
