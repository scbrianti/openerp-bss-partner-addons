# -*- coding: utf-8 -*-
# Part of Split Partner Name - Name First.
# See LICENSE file for full copyright and licensing details.

from odoo import models


class Parter(models.Model):
    _inherit = 'res.partner'

    def _full_name(self, first_name, last_name):
        return '%s %s' % (last_name, first_name)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
