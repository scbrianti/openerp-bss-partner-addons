# -*- coding: utf-8 -*-
# Part of Marital Status.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class MaritalStatus(models.Model):
    _name = 'bss.marital_status'
    _description = "Marital status"

    name = fields.Char("Name", size=32, required=True, translate=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
