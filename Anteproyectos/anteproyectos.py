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
from openerp.api import Environment
import time


class anteproyecto(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.anteproyecto'
	_description = 'Formulario De Anteproyecto'

	name = fields.Char('Nombre Del Proyecto', size=256 , requiered=True, help='Nombre del proyecto')
	student = fields.Many2one('res.users' ,  ondelete='set null', string="Estudiante", index=True )
	carnet = fields.Integer()
	company = fields.Many2one('res.partner', 'Empresa',requiered=True)
	companyContact = fields.Many2one('res.partner', ondelete='set null', string="Contacto de la Empresa", index=True )
	companyAssesor = fields.Many2one('res.partner', ondelete='set null', string="Asesor en la Empresa", index=True )
	profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) 
	possibleTasks = fields.Html('Posibles Trabajos a Realizar', requiered=True, help='Posibles trabajos a realizar')
	actualTask = fields.Html('Descripcion Del Trabajo A Realizar',  requiered=True, help='Trabajos a realizar durante el proyecto')
	generalObjetive  = fields.Html('Objetivo General Del Trabajo',  requiered=True, help='Objetivo general del proyecto')
	specificObjective = fields.Html('Objetivos Especificos',  requiered=True, help='Objetivos especificos para logra el objetivo')
	#metodology = fields.Html('Metodologia',  requiered=True, help='Describa la metodologia a utilizar')
	#tools = fields.Html('Tecnicas o Herramientas A Utilizar', size=256 , requiered=True, help='Herramientas a usar para lograr los objetivos')
	topics = fields.Many2many('anteproyecto.topics', string='Areas de estudio',ondelete='cascade')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto', default= 'draft')
	comments = fields.Char('Comentarios', size=256 , help='Comentarios de Coordinación')
	isActive = fields.Boolean()
	#extraFile = fields.Binary("Documento", help="Subir aqui la documentación complementaria")
	extraFile= fields.Many2many("ir.attachment", string="Documento") 
	cronogram = fields.Binary("Cronograma", help="Subir aqui la imagen del cronograma")

	@api.onchange('student')
	def _set_carnet(self):
		self.carnet = self.student.carnet

	@api.multi
	def action_draft(self):
		self.state = 'draft'
	# @api.one
	# def action_aprove(self):
	# 	self.state = 'aprove'
	@api.one
	def action_reject(self):
		self.write({
	    'state': 'reject',
		})
		
		# body = '''
		# 	Dear ''' " %s," % (self.student.name) + '''
		# 	<p></p>
		# 	<p> Su proyecto ''' "%s" % self.name + '''  ha sido rechazdo
		# 	 ''' "%s" % self.student.email +''' su correo lol.</p> 
		# 	<p></p>
		# 	<p>Esto esta entre P's nerd </p> 
		# 	<p> </p>
		# 	<p>No responda este correo </p>
                            
		# 	<p>Saludos, </p> 
		# 	'''
		# mail_details = {'subject': "Proyeccto rechazado",
		# 	'body': body,
		# 	'partner_ids': [(self.student.email)]
		# 	}
		# mail = self.env['mail.thread']
  #       mail.message_post(type="notification", subtype="mt_comment", **mail_details)



	#here
	#@api.v8 
	#@api.multi
	#@api.depends('anteproyecto.topics')
	@api.one
	def action_aprove(self):
		self.state = 'aprove'
		tags = []
		if self.profAssesor.cantStudents > 0:
			for item in self.topics:
				tags.append(item.id)
			id_project = self.env['sspp.proyecto'].create({
				'name' : self.name,
				'student' : self.student.id,
				'carnet' : self.carnet,
				'company' : self.company.id,
				'companyContact' : self.companyContact.id,
				'companyAssesor' : self.companyAssesor.id,
				'profAssesor' : self.profAssesor.id,
				'possibleTasks' : self.possibleTasks,
				'actualTask' : self.actualTask,
				'generalObjetive' : self.generalObjetive,
				'specificObjective' : self.specificObjective,
				#'metodology' : self.metodology,
				#'tools' : self.tools,
				'topics' : [(6, 0, tags)],
				'state' : self.state,
				'comments' : self.comments
			})
			self.env.cr.commit()
			self.profAssesor.cantStudents -= 1
			
			mail_mail = self.env['mail.mail']
			body = '''
			Dear ''' " %s," % (self.student.name) + '''
			<p></p>
			<p> Su proyecto ''' "%s" % self.name + '''  ha sido aprobado
			 ''' "%s" % self.student.email +''' su correo lol.</p> 
			<p></p>
			<p>Esto esta entre P's </p> 
			<p> </p>
			<p>No responda este correo </p>
                            
			<p>Saludos, </p> 
			'''
			subject = "Proyecto aprobado"
			mail_values = {
			'email_from':self.student.email,
			'email_to': self.student.email,
			'subject': subject,
			'body_html': body,
			'state': 'outgoing',
			'type': 'email',
			}
			mail_id = mail_mail.create( mail_values)
			mail_mail.send([mail_id])
				#,auto_commit=True)
				#,force_send=True)


		else:

			return {
				'warning': {
					'title': " Aviso",
					'message': "El profesor asignado no tiene mas cupos disponibles.",
				},
			}
		




	_defaults = {
		'student': lambda obj, cr, uid, context: uid,
		'state': 'draft', 
		'isActive': True ,
	}
	    
# def sendMail(user,project):
# 		mail_mail = self.env('mail.mail')
# 		#this_context = context
# 		body = '''
# 			Dear ''' " %s," % (user.name) + '''
# 			<p></p>
# 			<p> Su proyecto ''' "%s" % project + '''  ha sido aprobado
# 			 ''' "%s" % user.email +''' su correo lol.</p> 
# 			<p></p>
# 			<p>Esto esta entre P's </p> 
# 			<p> </p>
# 			<p>No responda este correo </p>
                            
# 			<p>Saludos, </p> 
# 			'''
# 		subject = "Proyecto aprobado"
# 		print "Email to",user.name 
# 		mail_values = {
# 			'email_from':user.email,
# 			'email_to': user.email,
# 			'subject': subject,
# 			'body_html': body,
# 			'state': 'outgoing',
# 			'type': 'email',
# 			}
# 		mail_id = mail_mail.create( mail_values, context=this_context)
# 		mail_mail.send([mail_id],  auto_commit=True, context=this_context)

class anteproyecto_tema(models.Model):
	""" Area que conocimiento que abarca """
	_name = 'anteproyecto.topics'
	_description = "Area de estudio o tema."
	name = fields.Char('Nombre', required=True, translate=True)
    
    # User can write on a few of his own fields (but not his groups for example)
    #SELF_WRITEABLE_FIELDS = ['name']
    # User can read a few of his own fields
    #SELF_READABLE_FIELDS = ['profAssesor'] 

    

