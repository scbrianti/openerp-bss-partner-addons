# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-2017 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

    _columns = {
        'first_name': fields.char('First Name', size=64, required=False,
                                  select=True),
        'last_name': fields.char('Last Name', size=64, required=False,
                                 select=True),
    }

    def _full_name(self, first_name, last_name):
        """Private method to override if you want to change the computed name.
        """
        return '%s %s' % (first_name, last_name)

    def create(self, cr, uid, vals, context=None):
        if vals.get('name'):
            if vals.get('first_name'):
                vals.pop('name')
            else:
                vals['first_name'] = vals.pop('name')
        if (vals.get('first_name') or vals.get('last_name') or
                vals.get('is_company')):
            if vals.get('is_company'):
                vals['name'] = vals.get('first_name')
                vals.pop('last_name', None)
            elif vals.get('last_name'):
                vals['name'] = self._full_name(vals.get('first_name'),
                                               vals.get('last_name'))
            else:
                vals['name'] = vals.get('first_name')

        return super(res_partner_split, self).create(cr, uid, vals,
                                                     context=context)

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('name'):
            if vals.get('first_name') or vals.get('last_name'):
                raise osv.except_osv('Error', 'name cannot be defined if '
                                     'first name or last name is defined')
            vals['first_name'] = vals.pop('name')
            return super(res_partner_split, self).write(cr, uid, ids, vals,
                                                        context=context)
        elif (vals.get('first_name') or vals.get('last_name') or
              vals.get('is_company')):
            super(res_partner_split, self).write(cr, uid, ids, vals,
                                                 context=context)
            for p in self.browse(cr, uid, ids, context=context):
                n_vals = {}
                if p.is_company:
                    n_vals['name'] = p.first_name
                    n_vals['last_name'] = None
                elif p.last_name:
                    n_vals['name'] = self._full_name(p.first_name, p.last_name)
                else:
                    n_vals['name'] = p.first_name
                super(res_partner_split, self).write(cr, uid, ids, n_vals,
                                                     context=context)
            return True
        else:
            return super(res_partner_split, self).write(cr, uid, ids, vals,
                                                        context=context)

    def _res_partner_split_install(self, cr, uid, ids=None, context=None):
        """Fill the first_name field with name value at install."""
        if ids is not None:
            raise NotImplementedError(
                "Ids is just there by convention! Please don't use it.")

        cr.execute("update res_partner set first_name = name")
        return True


res_partner_split()
