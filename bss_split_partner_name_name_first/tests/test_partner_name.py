# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Bluestar Solutions Sàrl (<http://www.blues2.ch>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.gopher
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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
