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
#   Coded by: pat01822@gmail.com
#
##############################################################################

{
    'name': 'Modulo de Usuarios',
    'version': '1',
    'category': 'usuarios',
    'description': """Modulo de usuarios del sistema SSPP.""",
    'author': 'JCAS',
    'maintainer': 'JCAS',
    'website': 'http://www.facebook.com/patotec',
    'licenses' : 'AGPL-3',
    'depends': ['Anteproyectos','base','mail','email_template'],
    'init_xml' : [],
    'demo_xml' : ['demo.xml'],
    'data': [
                    'usuarios_view.xml',
                    ],
    'installable': True,
    'auto_install': True,
    'active': False,
    'application': True,

 }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
