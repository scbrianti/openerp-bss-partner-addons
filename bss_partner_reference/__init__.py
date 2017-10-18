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

import models

from odoo import api, SUPERUSER_ID


def _auto_set_reference(cr, __):
    """Set a ref for all partners with empty one.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.partner'].with_context(active_test=True).search(
        [('ref', '=', False)]).write(
        {'ref': env['ir.sequence'].get('bss.partner.ref')})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
