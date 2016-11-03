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
##############################################################################


from openerp.tools.translate import _
from openerp import api, models, fields, tools
import logging
import datetime
from openerp.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class eventos(models.Model):
	_name = 'sspp.eventos'
	_description = 'Administracion de eventos automaticos'

	semesterStart= fields.Date('Date')
	name = fields.Char(required=True)
	weeks = fields.Integer()
	currentSemester = fields.Boolean()

    #this method will be called from automated actions, when the time is right it will initiate the week count
	@api.model
	def startCount(self):
		
		for dates in self.search([('currentSemester','=',True)]) :
			idk = dates.semesterStart

		weekStart = datetime.datetime.strptime(idk, '%Y-%m-%d').date()
		weekStart2 = weekStart.isocalendar()[1]
		currentWeek = datetime.date.today().isocalendar()[1]
		#_logger.critical('executed action weekstart %s', weekStart)

		#semana 5, primer reporte
		if (currentWeek - weekStart2) == 5:

			body  = '''
			Estimado estudiante, 
			<p>En el transcurso de esta semana debe entregar el primer reporte de avance. </p>
			<p>No responda este correo </p>       
			<p>Saludos, </p>
			<p>Coordindacion del curso de Practica </p> 
			'''
			subject = "Semana 5, Primer Reporte de Avance"

			self.mailAllStudents(body, subject)
			
			_logger.critical('Recordatorio de avance 1 enviado de y currentWeek %s',(currentWeek - weekStart2))
		
		#semana 9, segundo reporte
		elif (currentWeek - weekStart2) == 9:

			body  = '''
			Estimado estudiante, 
			<p>En el transcurso de esta semana debe entregar el segundo reporte de avance. </p>
			<p>No responda este correo </p>       
			<p>Saludos, </p>
			<p>Coordindacion del curso de Practica </p> 
			'''
			subject = "Semana 9, Segundo Reporte de Avance"

			self.mailAllStudents(body, subject)
			
			_logger.critical('Recordatorio de avance 2 enviado de y currentWeek %s',(currentWeek - weekStart2))

		#semana 13, ultima semana de permanencia del estudiante en la empresa
		elif (currentWeek - weekStart2) == 13:

			body  = '''
			Estimado estudiante, 
			<p>En el transcurso de esta semana debe entregar el primer reporte de avance. </p>
			<p>No responda este correo </p>       
			<p>Saludos, </p>
			<p>Coordindacion del curso de Practica </p> 
			'''
			subject = "Semana 13, ultima semana en la empresa"

			self.mailAllStudents(body, subject)
			
			_logger.critical('ultima semana de permanencia del estudiante en la empresa y currentWeek %s',(currentWeek - weekStart2))

		#semana 14, Informe Final 
		elif (currentWeek - weekStart2) == 14:

			body  = '''
			Estimado estudiante, 
			<p>En el transcurso de esta semana debe entregar el primer reporte de avance. </p>
			<p>No responda este correo </p>       
			<p>Saludos, </p>
			<p>Coordindacion del curso de Practica </p> 
			'''
			subject = "Semana 14, Informe Final"

			self.mailAllStudents(body, subject)
			
			_logger.critical('Informe Final y currentWeek %s',(currentWeek - weekStart2))

		#semana 15, Informe Final Revision
		elif (currentWeek - weekStart2) == 15:

			body  = '''
			Estimado estudiante, 
			<p>En el transcurso de esta semana debe entregar el primer reporte de avance. </p>
			<p>No responda este correo </p>       
			<p>Saludos, </p>
			<p>Coordindacion del curso de Practica </p> 
			'''
			subject = "Semana 15, Revision de Informe Final "

			self.mailAllStudents(body, subject)
			
			_logger.critical('Informe Final Revision y currentWeek %s',(currentWeek - weekStart2))

		else:
			_logger.critical('You are not prepared.. its just been %s Weeks',(currentWeek - weekStart2))


	# @api.model
	# def create(self, vals):
	# 	rec = super(eventos, self).create(vals)
	# 	#rec.startCount()
	# 	return rec


	@api.multi
	def endSemester(self):
		self.currentSemester = False


	@api.multi
	def mailAllStudents(self, body, subject):
		mail_mail = self.env['mail.mail']
		users = self.env['res.users'].search([('isStudent','=',True)])
		for student in users:
			mail_values  = {
				'email_from':'ssppitcr@gmail.com',
				'email_to': student.email,
				'subject': subject,
				'body_html': body,
				'state': 'outgoing',
				'type': 'email',
			}
			mail_id = mail_mail.create( mail_values)
			mail_mail.send([mail_id])


	@api.multi
	def mailAllProfessors(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		users = self.env['res.users'].search([('isProfessor','=',True)])
		for profs in users:

			mail_values  = {
				'email_from':'ssppitcr@gmail.com',
				'email_to': profs.email,
				'subject': subject,
				'body_html': body,
				'state': 'outgoing',
				'type': 'email',
			}
			mail_id = mail_mail.create( mail_values)
			mail_mail.send([mail_id])


	_defaults = {
		'currentSemester': True ,
	}