# -*- coding: utf-8 -*-
# Part of Split Partner Name.
# See LICENSE file for full copyright and licensing details.

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
