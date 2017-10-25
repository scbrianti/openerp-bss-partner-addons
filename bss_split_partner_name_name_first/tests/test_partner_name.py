# -*- coding: utf-8 -*-
# Part of Split Partner Name - Name First.
# See LICENSE file for full copyright and licensing details.

import unittest2
import odoo.tests.common as common
from odoo.netsvc import logging


class test_partner_name(common.TransactionCase):

    @classmethod
    def setUpClass(self):
        super(test_partner_name, self).setUpClass()
        self.partner = self.registry('res.partner')
        self._logger = logging.getLogger(__name__)

    def test_create(self):
        """I test create a partner"""
        cr, uid = self.cr, self.uid

        # I create a new partner
        luke_id = self.partner.create(cr, uid, {
            'first_name': 'Luke',
            'last_name': 'Skywalker',
        })

        # I retrieve the created partner
        luke = self.partner.browse(cr, uid, luke_id)

        # I check partner values
        self.assertEqual(luke.first_name, 'Luke')
        self.assertEqual(luke.last_name, 'Skywalker')
        self.assertEqual(luke.name, 'Skywalker Luke')

    def test_create_company(self):
        """I test create a company partner"""
        cr, uid = self.cr, self.uid

        # I create a new partner
        jedi_order_id = self.partner.create(cr, uid, {
            'first_name': 'The Jedi Order',
        })

        # I retrieve the created partner
        jedi_order = self.partner.browse(cr, uid, jedi_order_id)

        # I check partner values
        self.assertEqual(jedi_order.first_name, 'The Jedi Order')
        self.assertEqual(jedi_order.name, 'The Jedi Order')

    def test_create_old_way(self):
        """I test create a partner with name field (for compatibility)"""
        cr, uid = self.cr, self.uid

        # I create a new partner
        darth_vader_id = self.partner.create(cr, uid, {
            'name': 'Darth Vader',
        })

        # I retrieve the created partner
        darth_vader = self.partner.browse(cr, uid, darth_vader_id)

        # I check partner values
        self.assertEqual(darth_vader.first_name, 'Darth Vader')
        self.assertEqual(darth_vader.name, 'Darth Vader')


if __name__ == '__main__':
    unittest2.main()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
