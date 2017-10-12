# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2013 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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
    'name': 'Partner References',
    'version': '7.0.4.2',
    "category": 'Bluestar/Generic module',
    'complexity': "easy",
    'description': """
Automatic partner reference
===========================

With this module, the partner reference field becomes mandatory,
read-only and automatically filled at save from a customizable
sequence.

A configuration wizard can be used to reset all or empty reference
from existing partners.
    """,
    'author': 'Bluestar Solutions Sàrl',
    'website': 'http://www.blues2.ch',
    'depends': [],
    'update_xml': ['partner_sequence.xml',
                   'partner_view.xml'],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': ['images/customer_tree.png', ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
