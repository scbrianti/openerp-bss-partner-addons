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

from odoo import models, fields


class bss_partner_qualifier(models.Model):

    _name = 'bss.partner.qualifier'

    name = fields.Char('Name', size=64, translate=True, required=True)
    protected = fields.Boolean('Protected', default=False)


bss_partner_qualifier()


class bss_partner_qualified_contact_rel(models.Model):

    _name = 'bss.partner.qualified_contact.rel'

    parent_id = fields.Many2one('res.partner', "Parent")
    contact_id = fields.Many2one('res.partner', "Contact")
    qualifier_id = fields.Many2one('bss.partner.qualifier', "Qualifier")
    phone = fields.Char(related='contact_id.phone', string="Phone",
                        readonly=True,  store=False)
    mobile = fields.Char(related='contact_id.mobile', string="Mobile",
                         readonly=True, store=False)

    @api.v7
    def open_contact(self, cr, uid, ids, context=None):
        res_id = self.browse(cr, uid, ids[0], context).contact_id.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': res_id,
            'view_mode': 'form',
        }


bss_partner_qualified_contact_rel()


class bss_partner_qualified_contact(models.Model):

    _inherit = 'res.partner'

    qualified_contact_ids = fields.Many2many(
        'res.partner',
        'bss_partner_qualified_contact_rel',
        'parent_id', 'contact_id', 'Contacts'
    )
    qualified_contact_rel_ids = fields.One2many(
        'bss.partner.qualified_contact.rel',
        'parent_id', string="Contact Relations"
    )


bss_partner_qualified_contact()
