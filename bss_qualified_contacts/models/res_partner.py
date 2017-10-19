# -*- coding: utf-8 -*-
# Part of Qualified Contacts.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PartnerQualifier(models.Model):
    _name = 'bss.partner.qualifier'
    _description = "Partner Qualifier"

    name = fields.Char('Name', size=64, translate=True, required=True)
    protected = fields.Boolean('Protected', default=False)


class PartnerQualifiedContactRel(models.Model):
    _name = 'bss.partner.qualified_contact.rel'
    _description = "Partner Qualified Contact Relation"

    parent_id = fields.Many2one('res.partner', "Parent")
    contact_id = fields.Many2one('res.partner', "Contact")
    qualifier_id = fields.Many2one('bss.partner.qualifier', "Qualifier")
    phone = fields.Char("Phone", related='contact_id.phone', readonly=True)
    mobile = fields.Char(
        string="Mobile", related='contact_id.mobile', readonly=True)

    @api.multi
    def open_contact(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': self[0].contact_id.id,
            'view_mode': 'form',
        }


class Partner(models.Model):
    _inherit = 'res.partner'

    qualified_contact_ids = fields.Many2many(
        'res.partner', 'bss_partner_qualified_contact_rel',
        'parent_id', 'contact_id', 'Contacts')
    qualified_contact_rel_ids = fields.One2many(
        'bss.partner.qualified_contact.rel', 'parent_id', "Contact Relations")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
