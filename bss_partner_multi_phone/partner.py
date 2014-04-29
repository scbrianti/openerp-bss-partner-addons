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


class bss_partner_multi_phone(osv.osv):

    _inherit = 'res.partner'

    def _get_phone_field(self, cr, uid, ids, cat_id,
                         field_name, arg, context=None):
        result = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        for partner in self.browse(cr, uid, ids, context):
            for phone in partner.phone_ids:
                if phone.category_id.id == cat_id:
                    result[partner.id] = phone.number
                    break
        return result

    def _set_phone_field(self, cr, uid, ids, cat_id,
                         name, value, context=None):
        phone_obj = self.pool.get('bss.partner.phone')

        if not value:
            return False

        if isinstance(ids, (int, long)):
            ids = [ids]

        for partner in self.browse(cr, uid, ids, context):
            update_mode = False
            for phone in partner.phone_ids:
                if phone.category_id.id == cat_id:
                    phone_obj.write(cr, uid, phone.id, {'number': value},
                                    context)
                    update_mode = True
                    break
            if not update_mode:
                phone_obj.create(cr, uid, {
                    'category_id': cat_id,
                    'number': value,
                    'partner_id': partner.id,
                }, context)
        return True

    def _get_category_id(self, cr, uid, xml_sub_name):
        """Return the category id from the sub name of an xml id"""

        m = self.pool.get('ir.model.data')
        return m.get_object(
            cr, uid,
            'bss_partner_multi_phone',
            'phone_category_%s' % xml_sub_name
        ).id

    def _get_phone(self, cr, uid, ids, field_name, arg, context=None):
        return self._get_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'phone'),
                                    field_name, arg, context)

    def _set_phone(self, cr, uid, ids, name, value, arg, context=None):
        return self._set_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'phone'),
                                    name, value, context)

    def _get_fax(self, cr, uid, ids, field_name, arg, context=None):
        return self._get_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'fax'),
                                    field_name, arg, context)

    def _set_fax(self, cr, uid, ids, name, value, arg, context=None):
        return self._set_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'fax'),
                                    name, value, context)

    def _get_mobile(self, cr, uid, ids, field_name, arg, context=None):
        return self._get_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'mobile'),
                                    field_name, arg, context)

    def _set_mobile(self, cr, uid, ids, name, value, arg, context=None):
        return self._set_comm_field(cr, uid, ids,
                                    self._get_category_id(cr, uid, 'mobile'),
                                    name, value, context)

    _columns = {
        'phone_ids': fields.one2many(
            'bss.partner.phone', 'partner_id', 'Phones', reorderable=True
        ),

        'phone': fields.function(_get_phone, fnct_inv=_set_phone,
                                 type='char', store=True, multi=False),
        'fax': fields.function(_get_fax, fnct_inv=_set_fax,
                               type='char', store=True, multi=False),
        'mobile': fields.function(_get_mobile, fnct_inv=_set_mobile,
                                  type='char', store=True, multi=False),
    }

bss_partner_multi_phone()
