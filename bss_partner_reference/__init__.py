# -*- coding: utf-8 -*-
# Part of Automatic Partner Reference.
# See LICENSE file for full copyright and licensing details.

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
