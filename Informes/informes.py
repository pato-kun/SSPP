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
	#student = fields.Many2one('res.users', 'Estudiante', ondelete='set null', requiered=True)
		#,domain="[('isStudent2','=',True)]"  )
		#, domain=[(_get_students(self))]) #,default=lambda self: self.env.user )
	profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) #,domain=[('user.id')]) 
	project_id = fields.Many2one('sspp.proyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	dateFiled= fields.Date(string='Fecha')
	description= fields.Char('Descripcion', size=256 , requiered=True, help='Descripcion del avance')
	status= fields.Selection([('belated','Atrasado'),('onTime','A tiempo'), ('ahead','Adelantado'),('suspended','Suspender')],'Estado del proyecto', default= 'onTime')
	comments= fields.Char('Comentarios', size=256 , requiered=True, help='Comentarios')
	commentsCoord= fields.Char('Observaciones del Coordinador', size=256 , help='Observaciones del Coordinador')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del anteproyecto', default= 'draft')

	@api.multi
	def sendMailStudent(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':self.project_id.student.email,
			'email_to': self.project_id.student.email,
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
	def action_draft(self):
		self.state = 'draft'

	@api.one
	def action_aprove(self):
		self.state = 'aprove'
		body  = '''
		Dear ''' " %s," % (self.project_id.profAssesor.name) + '''
		<p></p>
		<p> El informe de avance del proyecto ''' "%s" % self.project_id.name + ''', creado el  
		''' "%s" % self.create_date + ''' a sido aprobado.</p> 
		<p>
		Comentarios del Coordinador:
		''' "%s" % self.commentsCoord + '''
		</p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Reporte de avance de" + " %s," % (self.project_id.name) + "aprobado."
		self.sendMailProfAssesor(body,subject)
		

	@api.one
	def action_reject(self):
		self.write({
	    'state': 'reject',
		})
		body  = '''
		Dear ''' " %s," % (self.project_id.profAssesor.name) + '''
		<p></p>
		<p> El informe de avance del proyecto ''' "%s" % self.project_id.name + ''', creado el  
		''' "%s" % self.create_date + ''' a sido rechazado.</p> 
		<p>
		Comentarios del Coordinador:
		''' "%s" % self.commentsCoord + '''
		</p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Reporte de avance de" + " %s," % (self.project_id.name) + "rechazado."
		self.sendMailProfAssesor(body,subject)

	@api.model
	def create(self, vals):
		rec = super(informesprofesor, self).create(vals)
		#When overriding default Create method, the self value becomes and empty
		#registry while vals contains a dictionary with values to create the reg with.
		#Assigning the creation to a var ensures the capability to use said reg values on other 
		#methods
		if rec.status == 'suspended':
			body  = '''
			Dear ''' " %s," % (rec.project_id.student.name) + '''
			<p></p>
			<p> Su profesor asesor del proyecto ''' "%s" % rec.project_id.name + '''  ha enviado un reporte de avance 
			la fecha ''' "%s" % rec.create_date + '''.</p> 
			<p></p>
			<p>Se ha decidido suspender el proyecto por las siguientes rasones:	</p> ''' "%s" % rec.comments + '''
			<p></p>
			<p>Si desea apelar esta desicion ingrese al sistema y solicite apelacion desde el apartado de proyectos de proyectos. </p> 
			<p></p>
			<p>No responda este correo </p>       
			<p>Saludos, Coordindacion del curso de Practica </p> 
			'''
			subject = "Proyecto suspendido" + " %s" % (rec.project_id.name)
			rec.sendMailStudent(body,subject)

		else:
			body  = '''
			Dear ''' " %s," % (rec.project_id.student.name) + '''
			<p></p>
			<p> Su profesor asesor del proyecto ''' "%s" % rec.project_id.name + '''  ha enviado un reporte de avance 
			la fecha ''' "%s" % rec.create_date + '''.</p> 
			<p></p>
			<p>Comentarios:	</p> ''' "%s" % rec.comments + '''
			<p></p>
			<p>No responda este correo </p>       
			<p>Saludos, Coordindacion del curso de Practica </p> 
			'''
			subject = "Reporte de avance del proyecto" + " %s" % (rec.project_id.name)
			rec.sendMailStudent(body,subject)

		bodyAdmin  = '''
		<p></p>
		<p> El profesor ''' " %s," % (rec.project_id.profAssesor.name) + ''' asesor del proyecto''' "%s" % rec.project_id.name + '''  ha enviado un reporte de avance 
		la fecha ''' "%s" % rec.create_date + '''.</p> 
		<p></p>
		<p>Esta pendiente su aprobacion. </p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subjectAdmin = "Reporte de avance del proyecto" + " %s" % (rec.project_id.name)

		
		rec.sendMailAdmin(bodyAdmin,subjectAdmin)	
		
		rec.project_id.statusProgress = rec.status 
		return rec

	@api.multi
	def write(self, vals):
		super(informesprofesor, self).write(vals)
		self.project_id.statusProgress = self.status 
		return True

	_defaults = {
		'profAssesor': lambda obj, cr, uid, context: uid,
		#'student': lambda self, cr, uid, context:self._get_students(self),
		'state': 'draft', 
	}


class informesestudiante(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.informesestudiante'
	_description = 'Formulario De Informes Estudiantes-Profesor'

	#student = fields.Many2one('res.users', 'Estudiante', ondelete='set null', requiered=True)
	#profAssesor = fields.Many2one('res.users', ondelete='set null', string="Profesor Asesor", index=True) #,domain=[('user.id')]) 
	project_id = fields.Many2one('sspp.proyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	dateStart= fields.Date(string='Fecha inicio')
	dateEnd= fields.Date(string='Fecha final')
	tareasPlaneadas = fields.Char('Actividades planeadas para este periodo', size=512, requiered=True, help='Tareas planeadas para este periodo')
	tareasRealizadasPlan = fields.Char('Actividades realizadas segun lo planeado', size=512, requiered=True, help='Tareas realizadas')
	tareasRealizadasNoPlan = fields.Char('Actividades realizadas que no estaban planeadas', size=512, requiered=True, help='Tareas Planeadas no planeadas')
	tareasARealizar = fields.Char('Actividades por realizar el próximo periodo', size=512, requiered=True, help='Tareas para el próximo periodo')
	comments= fields.Char('Comentarios ', size=256 , requiered=True, help='Comentarios')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado del informes', default= 'draft')
	

	@api.multi
	def sendMailStudent(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':self.project_id.student.email,
			'email_to': self.project_id.student.email,
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
	def action_draft(self):
		self.state = 'draft'

	@api.one
	def action_aprove(self):
		self.state = 'aprove'
		body  = '''
		Dear ''' " %s," % (self.project_id.student.name) + '''
		<p></p>
		<p> Su informe semanal del proyecto ''' "%s" % self.project_id.name + ''', creado el  
		''' "%s" % self.create_date + ''' a sido aprobado.</p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Reporte semanal de " + " %s," % (self.create_date) + "aprobado."
		self.sendMailStudent(body,subject)

	@api.one
	def action_reject(self):
		self.write({
	    'state': 'reject',
		})
		body  = '''
		Dear ''' " %s," % (self.project_id.student.name) + '''
		<p></p>
		<p> Su informe semanal del proyecto ''' "%s" % self.project_id.name + ''', creado el  
		''' "%s" % self.create_date + ''' a sido rechazado.</p> 
		<p>
		Comentarios del profesor:
		''' "%s" % self.comments + '''
		</p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Reporte semanal de " + " %s," % (self.create_date) + "rechazado."
		self.sendMailStudent(body,subject)

	@api.model
	def create(self, vals):
		rec = super(informesestudiante, self).create(vals)
		body  = '''
		Dear ''' " %s," % (rec.project_id.profAssesor.name) + '''
		<p></p>
		<p> El estudiante ''' "%s" % rec.project_id.student.name + ''' ha enviado un reporte semanal 
		del Proyecto  ''' "%s" % rec.project_id.name + '''.</p> 
		<p></p>
		<p>Esta pendiente su aprobacion. </p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Reporte semanal del proyecto" + " %s," % (rec.project_id.name)
		rec.sendMailProfAssesor(body,subject)
		#return ({'warning': {'title': _('Warning !'), 'message': _(str(vals))}})     
		return rec

	_defaults = {
	'state': 'draft', 
	}


class minutas(models.Model):
	#_inherit = 'prof.category'
	_name = 'sspp.minutas'
	_description = 'Formulario De Minutas'

	#student = fields.Many2one('res.users', 'Estudiante', ondelete='set null', requiered=True)
	author = fields.Many2one('res.users', ondelete='set null', string="Encargado", index=True) #,domain=[('user.id')]) 
	project_id = fields.Many2one('sspp.proyecto', 'Proyecto' ,ondelete='set null',requiered=True ) #, domain=[('profAssesor','=','uid')])
	otherMembers = fields.Char('Asistentes', size=256 , requiered=True, help='Asistentes de la reunión')
	#otherMembers = fields.Many2many('res.partner', ondelete='set null',string="Asistentes de la reunión",help='Los interesados recibiran una copia del reporte')
	#for future use, when the app is actually online
	meetingType = fields.Char('Tipo de Reunión', size=256 , requiered=True, help='Tipo de reunión, presencial, telefónica...')
	place = fields.Char('Lugar de Reunión', size=256 , requiered=True, help='Locacion de la reunión')
	dateDone= fields.Date(string='Fecha de reunión')
	pointers = fields.Html('Puntos tratados y acuerdos',  requiered=True, help='Acuerdos y puntos tratados')
	comments= fields.Char('Comentarios ', size=256 , requiered=True, help='Comentarios')
	state = fields.Selection([('draft','Borrador'),('aprove','Aprobado'), ('reject','Rechazado')],'Estado de la minuta', default= 'draft')


	@api.multi
	def sendMailStudent(self, body, subject):
		#Sends to Professor Assesor
		mail_mail = self.env['mail.mail']
		mail_values  = {
			'email_from':self.project_id.student.email,
			'email_to': self.project_id.student.email,
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
		#############here here##################
	@api.multi
	def action_draft(self):
		self.state = 'draft'

	@api.one
	def action_aprove(self):
		self.state = 'aprove'
		bodyAdmin  = '''
		<p></p>
		<p> La minuta de reunion efectuada el  ''' "%s" % self.create_date + '''del proyecto''' "%s" % self.project_id.name + '''  ha sido aprobada.</p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subjectAdmin = "Minuta de reunion aprobada."
		self.sendMailStudent(body,subject,self.author)

	@api.one
	def action_reject(self):
		self.write({
	    'state': 'reject',
		})
		#self.state = 'reject'

	@api.model
	def create(self, vals):
		rec = super(minutas, self).create(vals)
		body  = '''
		Dear ''' " %s," % (rec.project_id.student.name) + '''
		<p></p>
		<p> Minuta de reunion efectuada el ''' "%s," % rec.dateDone + ''' del proyecto ''' "%s," % rec.project_id.name + ''' creada por ''' "%s" % rec.author.name + '''.</p> 
		<p></p>
		<p>Esta pendiente su aprobacion. </p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subject = "Minuta de reunión, fecha  " + " %s" % (rec.dateDone)
		rec.sendMailStudent(body,subject)

		bodyAdmin  = '''
		<p> Minuta de reunion efectuada el ''' "%s," % rec.dateDone + ''' del proyecto ''' "%s," % rec.project_id.name + ''' creada por ''' "%s" % rec.author.name + '''.</p> 
		<p></p>
		<p>Esta pendiente su aprobacion. </p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''
		subjectAdmin = "Minuta de reunión, fecha" + " %s" % (rec.project_id.name)
		
		bodyProf  = '''
		Dear ''' " %s," % (rec.project_id.profAssesor.name) + '''
		<p></p>
		<p> Minuta de reunion efectuada el ''' "%s," % rec.dateDone + ''' del proyecto ''' "%s," % rec.project_id.name + ''' creada por ''' "%s" % rec.author.name + '''.</p> 
		<p></p>
		<p>Esta pendiente su aprobacion. </p> 
		<p></p>
		<p>No responda este correo </p>       
		<p>Saludos, Coordindacion del curso de Practica </p> 
		'''

		rec.sendMailTarget(bodyProf,subject,rec.profAssesor)
		rec.sendMailAdmin(body,subject)

		return rec

	_defaults = {
		'author': lambda obj, cr, uid, context: uid,
		#'student': lambda self, cr, uid, context:self._get_students(self),
		'state': 'draft', 
	}
