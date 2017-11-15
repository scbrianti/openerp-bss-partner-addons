# -*- coding: utf-8 -*-
# Part of Split Partner Name.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging


class Partner(models.Model):
    _inherit = 'res.partner'
    _logger = logging.getLogger(_inherit)

    first_name = fields.Char("First Name", size=64, index=True)
    last_name = fields.Char("Last Name", size=64, index=True)

    @staticmethod
    def _full_name(first_name, last_name):
        """Private method to override if you want to change the computed name.
        """
        return u"{} {}".format(first_name, last_name)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            name = vals.pop('name')
            if not vals.get('first_name'):
                vals['first_name'] = name
        if vals.get('first_name') or vals.get('last_name'):
            if vals.get('is_company'):
                vals['name'] = vals.get('first_name')
                vals.pop('last_name', None)
            elif vals.get('last_name'):
                vals['name'] = self._full_name(vals.get('first_name'),
                                               vals.get('last_name'))
            else:
                vals['name'] = vals.get('first_name')

        return super(Partner, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('name'):
            if vals.get('first_name') or vals.get('last_name'):
                raise UserError(_("Name cannot be defined if "
                                  "first name or last name is defined!"))
            vals['first_name'] = vals.pop('name')
        res = super(Partner, self).write(vals)
        if vals.get('first_name') or vals.get('last_name'):
            super(Partner, self).write(vals)
            for p in self:
                n_vals = {}
                if p.is_company:
                    n_vals['name'] = p.first_name
                    n_vals['last_name'] = None
                elif p.last_name:
                    n_vals['name'] = self._full_name(p.first_name, p.last_name)
                else:
                    n_vals['name'] = p.first_name
                super(Partner, self).write(n_vals)
            return True
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
