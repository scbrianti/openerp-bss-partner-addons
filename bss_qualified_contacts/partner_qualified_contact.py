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

from openerp.osv import osv, fields


class bss_partner_qualifier(osv.osv):

    _name = 'bss.partner.qualifier'

    _columns = {
        'name': fields.char('Name', size=64, translate=True, required=True),
    }

bss_partner_qualifier()


class bss_partner_qualified_contact_rel(osv.osv):

    _name = 'bss.partner.qualified_contact.rel'

    _columns = {
        'parent_id': fields.many2one('res.partner', 'Parent'),
        'contact_id': fields.many2one('res.partner', 'Contact'),
        'qualifier_id': fields.many2one('bss.partner.qualifier', 'Qualifier'),
        'phone': fields.related('contact_id', 'phone', type="char",
                                readonly=True, string="Phone", store=False),
        'mobile': fields.related('contact_id', 'mobile', type="char",
                                readonly=True, string="Mobile", store=False),
    }

    def open_contact(self, cr, uid, ids, context=None):
        res_id = self.browse(cr, uid, ids[0], context).contact_id.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'res_id': res_id,
            'view_mode': 'form',
        }

bss_partner_qualified_contact_rel()


class bss_partner_qualified_contact(osv.osv):

    _inherit = 'res.partner'

    _columns = {
        'qualified_contact_ids': fields.many2many(
            'res.partner',
            'bss_partner_qualified_contact_rel',
            'parent_id', 'contact_id', 'Contacts'
        ),
        'qualified_contact_rel_ids': fields.one2many(
            'bss.partner.qualified_contact.rel',
            'parent_id'
        ),
    }

bss_partner_qualified_contact()
