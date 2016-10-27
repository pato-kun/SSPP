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
	#status= fields.Selection([('onTrack','En Curso'),('suspended','Suspendido')]
	#	,'Estado del proyecto', default= 'onTrack')
	# comments= fields.Char('Comentarios', size=256 , requiered=True, help='Comentarios')
	# commentsCoord= fields.Char('Observaciones del Coordinador', size=256 , help='Observaciones del Coordinador')
	statusProgress = fields.Selection([('belated','Atrasado'),('onTime','A tiempo'),
		('ahead','Adelantado'),('suspended','Suspendido')],'Estado del anteproyecto', default= 'onTime')
	isActive = fields.Boolean()

	@api.multi
	def sendMailTarget(self, body, subject,target):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':target.email,
			'email_to': target.email,
			'subject': subject,
			'body_html': body,
			'state': 'outgoing',
			'type': 'email',
		}
		mail_id = mail_mail.create( mail_values)
		mail_mail.send([mail_id])

	@api.multi
	def sendMailAdmin(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		users = self.env['res.users'].search([('isAdmin','=',True)])
		for admins in users:

			mail_values  = {
				'email_from':admins.email,
				'email_to': admins.email,
				'subject': subject,
				'body_html': body,
				'state': 'outgoing',
				'type': 'email',
			}
			mail_id = mail_mail.create( mail_values)
			mail_mail.send([mail_id])

	@api.multi
	def action_suspend(self):
		self.write({
	    'statusProgress': 'suspended',
		})
		

	@api.multi
	def action_resume(self):
		self.write({
	    'statusProgress': 'onTime',
		})
		body  = '''
		<p></p>
		<p> La continuacion de su proyecto ''' "%s" % self.name + '''  ha sido aprobada.</p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Proyecto rehabilitado."
		self.sendMailTarget(body,subject,self.student)

	@api.multi
	def action_apeal(self):
		# self.write({
	 #    'statusProgress': 'onTime',
		# })
		body = '''
		<p></p>
		<p> El estudiante  ''' "%s" % self.student.name + ''' a cargo del proyecto ''' "%s" % self.name + '''  solicita una revision a la suspension de su proyecto.</p> 
		'''
		subject = "Solicitud de apelacion de proyecto suspendido."
		self.sendMailAdmin(body,subject)
		return {
				'warning': {
					'title': _('Aviso'),
					'message': _('El coordinador del curso ha sido notificado.')
				}
		}

	_defaults = {
		'isActive': True ,
	}

	
