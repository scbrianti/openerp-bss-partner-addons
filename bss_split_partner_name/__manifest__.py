# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

{
    'name': 'Split Partner Name',
    'version': '7.0.4.1',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Split Partner Name
==================

Add a first name and a last name fields on partner and keep the field name
synchronized with the concatenation of the first name and the last name.

Update standard views to use split name.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [],
    'data': ['views/res_partner_views.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
    'post_init_hook': '_auto_init',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
