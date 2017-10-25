# -*- coding: utf-8 -*-
# Part of Automatic Partner Reference.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    ref = fields.Char('Reference', size=64, index=True, readonly=True)

    @api.model
    def create(self, vals):
        if 'ref' not in vals:
            vals['ref'] = self.env['ir.sequence'].get('bss.partner.ref')
        return super(Partner, self).create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
