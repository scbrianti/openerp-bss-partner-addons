# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-2013 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
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

GENERATE_REFS = [('none', 'None'),
                 ('empty', 'For partners with empty references'),
                 ('all', 'For all existing partners')]


class bluestar_partner_reference(osv.osv):

    _inherit = 'res.partner'
    _description = "Bluestar partner reference"

    _columns = {
        'ref': fields.char('Reference', size=64, select=1, readonly=True),
    }

    _defaults = {
        'customer': lambda self, cr, uid, context:
        context['customer'] if context and 'customer' in context else 1,
        'supplier': lambda self, cr, uid, context:
        context['supplier'] if context and 'supplier' in context else 0,
    }

    def create(self, cr, uid, vals, context=None):
        if not 'ref' in vals:
            vals['ref'] = self.pool.get('ir.sequence'
                                        ).get(cr, uid, 'bluestar.partner.ref')
        return super(bluestar_partner_reference,
                     self).create(cr, uid, vals, context=context)

bluestar_partner_reference()


class bluestar_partner_reference_config(osv.osv_memory):

    _name = 'bss.partner.reference.config'
    _inherit = 'res.config'

    _columns = {
        'generate_ref': fields.selection(GENERATE_REFS, 'Generate references',
                                         required=True),
    }

    def execute(self, cr, uid, ids, context=None):
        for config in self.read(cr, uid, ids, ['generate_ref']):
            partner_ids = []
            if config['generate_ref'] == 'all':
                partner_ids += self.pool.get('res.partner'
                                             ).search(cr, uid, [],
                                                      context=None)
            elif config['generate_ref'] == 'empty':
                partner_ids += self.pool.get('res.partner'
                                             ).search(cr,
                                                      uid,
                                                      ['|',
                                                       ('ref', '=', False),
                                                       ('ref', '=', '')
                                                       ], context=None)
            for partner_id in partner_ids:
                self.pool.get('res.partner').\
                    write(cr, uid, partner_id,
                          {'ref': self.pool.get('ir.sequence'
                                                ).get(cr, uid,
                                                      'bluestar.partner.ref')})

            partner_ids = []
            partner_ids += self.pool.get('res.partner'
                                         ).search(cr, uid,
                                                  [('ref', '=', False)],
                                                  context=None)
            partner_ids += self.pool.get('res.partner'
                                         ).search(cr, uid,
                                                  [('ref', '=', '')],
                                                  context=None)
            if partner_ids:
                raise osv.except_osv('Erreur', 'There is empty references !')

            duplicates = cr.execute("""
                SELECT COUNT(ref)
                FROM res_partner
                GROUP BY ref
                HAVING ( COUNT(ref) > 1 )
            """)
            if duplicates:
                raise osv.except_osv('Erreur',
                                     'There is duplicates references !')

        return True

bluestar_partner_reference_config()
