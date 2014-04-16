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

class res_partner_split(osv.osv):

    _inherit = 'res.partner'
    _description = "Partner with split name"

    # Because of default_focus attribute in views cannot be dynamic, we choose
    # first_name to be required and to store the company name. In this way
    # first_name is always visible and has always the default focus.

    def _get_full_name(self, cr, uid, ids, field_name, arg, context):
        result = {}
        for p in self.browse(cr, uid, ids, context):
            if p.is_company:
                result[p.id] = p.first_name
            elif p.last_name:
                result[p.id] = '%s %s' % (p.first_name, p.last_name)
            else:
                result[p.id] = p.first_name

        return result

    def _set_full_name(self, cr, uid, ids, name, value, arg, context=None):
        if not value:
            return False
        self.write(cr, uid, ids, {'first_name': value}, context)
        return True

    _columns = {
        'name': fields.function(_get_full_name, fnct_inv=_set_full_name,
                                type="char", multi=False,
                                method=True, store=True, string='Name'),
        'first_name': fields.char('First Name', size=64, required=False,
                                  select=True),
        'last_name': fields.char('Last Name', size=64, required=False,
                                 select=True),
    }

    def _res_partner_split_install(self, cr, uid, ids=None, context=None):
        """Fill the first_name field with name value at install."""
        if ids is not None:
            raise NotImplementedError(
                    "Ids is just there by convention! Please don't use it.")

        cr.execute(" update res_partner set first_name = name ")
        return  True

res_partner_split()
