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

from odoo import models, fields, api
from odoo.osv import osv

GENERATE_REFS = [('none', 'None'),
                 ('empty', 'For partners with empty references'),
                 ('all', 'For all existing partners')]


class bluestar_partner_reference(models.Model):

    _inherit = 'res.partner'
    _description = "Bluestar partner reference"

    ref = fields.Char('Reference', size=64, index=True, readonly=True)

    # TODO: manage defaults
    # _defaults = {
    #     'customer': lambda self, cr, uid, context:
    #     context['customer'] if context and 'customer' in context else 1,
    #     'supplier': lambda self, cr, uid, context:
    #     context['supplier'] if context and 'supplier' in context else 0,
    # }

    @api.v7
    def create(self, cr, uid, vals, context=None):
        if 'ref' not in vals:
            vals['ref'] = self.pool.get('ir.sequence'
                                        ).get(cr, uid, 'bluestar.partner.ref')
        return super(bluestar_partner_reference,
                     self).create(cr, uid, vals, context=context)


bluestar_partner_reference()


class bluestar_partner_reference_config(models.TransientModel):

    _name = 'bss.partner.reference.config'
    _inherit = 'res.config'

    generate_ref = fields.Selection(GENERATE_REFS, 'Generate references',
                                    required=True)

    @api.v7
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
