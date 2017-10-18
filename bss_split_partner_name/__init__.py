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

import models

from odoo import api, SUPERUSER_ID


def _auto_init(cr, registry):
    _auto_set_first_name(cr, registry)
    _auto_set_admin_last_name(cr, registry)


def _auto_set_first_name(cr, __):
    """Fill the first_name field with name for partners without one.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute(
        "update res_partner set first_name = name "
        "where coalesce(first_name, '') = ''")


def _auto_set_admin_last_name(cr, __):
    """Fill the last_name for admin user.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['res.users'].with_context(active_test=True).search([
        ('id', '=', SUPERUSER_ID), ('last_name', '=', False)
    ]).write({'last_name': "System"})


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
