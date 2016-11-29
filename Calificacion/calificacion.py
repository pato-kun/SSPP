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

class calificacion(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.calificacion'
	_description = 'Formulario De Calificacion de Proyecto'

	#project_id = fields.Many2one('sspp.proyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	student = fields.Many2one('res.users' ,  ondelete='set null', string="Estudiante", index=True )
	carnet = fields.Integer()

	firstReportProf = fields.Integer()
	secondReportProf = fields.Integer()
	finalReportProf = fields.Integer()

	firstReportComp = fields.Integer()
	secondReportComp = fields.Integer()
	finalReportComp = fields.Integer()

	finalPresentation = fields.Integer()

	#score = fields.Integer(compute='compute_total')
	score = fields.Integer()
	#comments= fields.Text('Comentarios', size=256 , help='Comentarios adicionales')
	
	#approvedBy = fields.Many2one('res.users', 'Aprobado por', ondelete='set null', requiered=False)

	@api.onchange('firstReportProf', 'secondReportProf','finalReportProf','firstReportComp','secondReportComp','finalReportComp','finalPresentation')
	def onchange_field(self):
		if self.firstReportProf or self.secondReportProf or self.finalReportProf or self.firstReportComp or self.secondReportComp or self.finalReportComp or self.finalPresentation :
			self.score = self.firstReportProf + self.secondReportProf + self.finalReportProf + self.firstReportComp + self.secondReportComp + self.finalReportComp + self.finalPresentation

	# @api.depends('firstReportProf', 'secondReportProf','finalReportProf','firstReportComp','secondReportComp','finalReportComp','finalPresentation')
	# @api.one
	# #@api.depends('sspp.valoresCalificacion.firstReportProf', 'sspp.valoresCalificacion.secondReportProf','sspp.valoresCalificacion.finalReportProf','sspp.valoresCalificacion.firstReportComp','sspp.valoresCalificacion.secondReportComp','sspp.valoresCalificacion.finalReportComp','sspp.valoresCalificacion.finalPresentation')
	# # @api.onchange('finalPresentation','valoresCalificacion.finalPresentation')
	# def compute_total(self):
	# 	instanciaValues = self.env['sspp.valorescalificacion']
	# 	reg = instanciaValues.search([('id', '!=', 69)])
	# 	r1 = (self.firstReportProf * (reg.firstReportProfValue / 100)) + (self.firstReportComp * (reg.firstReportCompValue / 100))
	# 	r2 = (self.secondReportProf * (reg.secondReportProfValue / 100)) + (self.secondReportComp * (reg.secondReportCompValue / 100))
	# 	r3 = (self.finalReportProf * (reg.finalReportProfValue / 100)) + (self.finalReportComp * (reg.finalReportCompValue / 100))
	# 	p = self.finalPresentation * (reg.finalPresentation / 100)
	# 	#p = self.finalPresentation * (valoresCalificacion.finalPresentation / 100)
	# 	#r1 = (self.firstReportProf * sspp.valoresCalificacion.firstReportProfValue) + (self.firstReportComp * sspp.valoresCalificacion.firstReportCompValue)
	# 	#r2 = (self.secondReportProf * sspp.valoresCalificacion.secondReportProfValue) + (self.secondReportComp * sspp.valoresCalificacion.secondReportCompValue)
	# 	#r3 = (self.finalReportProf * sspp.valoresCalificacion.finalReportProfValue) + (self.finalReportComp * sspp.valoresCalificacion.finalReportCompValue)
	# 	#p = self.finalPresentation * sspp.valoresCalificacion.finalPresentationValue

	# 	#x = r1 + r2 + r3 + p 

	# 	self.score = r1 + r2 + r3 + p 
	# 	#self.score = p 

	# def compute_total(self):
	# 	#instanciaValues = self.env['sspp.valorescalificacion']
	# 	#reg = instanciaValues.search([('id', '!=', 69)])
	# 	r1 = self.firstReportProf #* (reg.firstReportProfValue / 100)) + (self.firstReportComp * (reg.firstReportCompValue / 100))
	# 	r2 = self.secondReportProf #* (reg.secondReportProfValue / 100)) + (self.secondReportComp * (reg.secondReportCompValue / 100))
	# 	r3 = self.finalReportProf #* (reg.finalReportProfValue / 100)) + (self.finalReportComp * (reg.finalReportCompValue / 100))
		
	# 	p = self.finalPresentation #* (reg.finalPresentation / 100)
		
	# 	r4 = self.firstReportComp + secondReportComp +finalReportComp + firstReportProf + secondReportProf + finalReportProf + finalPresentation
	# 	r5 = self.secondReportComp
	# 	r6 =  self.secondReportComp
	# 	#p = self.finalPresentation * (valoresCalificacion.finalPresentation / 100)
	# 	#r1 = (self.firstReportProf * sspp.valoresCalificacion.firstReportProfValue) + (self.firstReportComp * sspp.valoresCalificacion.firstReportCompValue)
	# 	#r2 = (self.secondReportProf * sspp.valoresCalificacion.secondReportProfValue) + (self.secondReportComp * sspp.valoresCalificacion.secondReportCompValue)
	# 	#r3 = (self.finalReportProf * sspp.valoresCalificacion.finalReportProfValue) + (self.finalReportComp * sspp.valoresCalificacion.finalReportCompValue)
	# 	#p = self.finalPresentation * sspp.valoresCalificacion.finalPresentationValue

	# 	#x = r1 + r2 + r3 + p 

	# 	self.score = r1 + r2 + r3 + p + r4 + r5 + r6
	# 	#self.score = p 



	@api.multi
	def sendMailStudent(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':self.student.email,
			'email_to': self.student.email,
			'subject': subject,
			'body_html': body,
			'state': 'outgoing',
			'type': 'email',
		}
		mail_id = mail_mail.create( mail_values)
		mail_mail.send([mail_id])

	@api.multi
	def sendMailProfAssesor(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':self.project_id.profAssesor.email,
			'email_to': self.project_id.profAssesor.email,
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
	def write(self, vals):
		_logger.critical(' vals %s', vals)
		#vals['score'] =  int(vals['firstReportComp']) + int(vals['secondReportComp']) + int(vals['finalReportComp']) + int(vals['firstReportProf']) + int(vals['secondReportProf']) + int(vals['finalReportProf']) + int(vals['finalPresentation'])
		#c = 0
		#x = 0
		#for val in vals:

		#	x += val[c][1]
		#	c += 1

		#vals['score'] =  self.firstReportComp + self.secondReportComp + self.finalReportComp + self.firstReportProf + self.secondReportProf + self.finalReportProf + self.finalPresentation + self.score
		#vals['score'] =  x
		super(calificacion, self).write(vals)
		#super(calificacion, self).write(vals)
		#''' " %s," % (rec.project_id.student.name) + '''
		#self.score = self.firstReportProf
		body  = '''
			Estimado estudiante
			<p></p>
			<p> Su nota del curso se ha actualizado a: ''' "%s" % self.score + '''  .</p> 
			<p></p>

			<p>Esto es un mensaje automatico, favor no responder. </p>      
			<p>Saludos, Coordindacion del curso de Practica </p> 
			'''
		subject = "Nota del curso actualizada"
		self.sendMailStudent(body,subject)
		_logger.critical(' vals %s', self.score)
		#self.score = self.firstReportProf
			#rec.sendMailProfAssesor(body,subject)

		return True


	


	_defaults = {
		#'profAssesor': lambda obj, cr, uid, context: uid,
		'firstReportProf' : 0,
		'secondReportProf' : 0,

		'finalReportProf' : 0,
		'firstReportComp' : 0,

		'secondReportComp' : 0,
		'finalReportComp' : 0 ,

		'finalPresentation' : 0 ,
		'score' : 0,
	}

class valoresCalificacion(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.valorescalificacion'
	_description = 'Valores porcentuales De Calificacion de Proyecto'

	name = fields.Char('Nombre Del Proyecto', size=256 )
	firstReportProfValue = fields.Integer()
	secondReportProfValue = fields.Integer()
	finalReportProfValue = fields.Integer()

	firstReportCompValue = fields.Integer()
	secondReportCompValue = fields.Integer()
	finalReportCompValue = fields.Integer()
	#finalReportCompValue = fields.Integer()
	finalPresentation = fields.Integer()

	_defaults = {
		'name' : 'lol',
		'firstReportProfValue' : 14,
		'secondReportProfValue' : 10,

		'finalReportProfValue' : 14,
		'firstReportCompValue' : 10,

		'secondReportCompValue' : 22,
		'finalReportCompValue' : 10 ,

		'finalPresentation' : 20,
	}
