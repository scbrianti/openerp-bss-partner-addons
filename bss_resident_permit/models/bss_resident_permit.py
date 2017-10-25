# -*- coding: utf-8 -*-
# Part of Resident Permits.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class ResidentPermit(models.Model):
    _name = 'bss.resident_permit'
    _description = "Resident permit"

    name = fields.Char("Name", size=20, required=True, translate=True)
    description = fields.Char(
        "Description", size=200, required=True, translate=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
