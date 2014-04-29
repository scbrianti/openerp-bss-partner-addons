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
#    GNU Affero General Public License for more details.gopher
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import unittest2
import openerp.tests.common as common
from openerp.netsvc import logging


class test_partner_qualified_contact(common.TransactionCase):

    @classmethod
    def setUpClass(self):
        super(test_partner_qualified_contact, self).setUpClass()
        self.partner = self.registry('res.partner')
        self.qualifier = self.registry('bss.partner.qualifier')
        self.qualified_contact_rel = \
            self.registry('bss.partner.qualified_contact.rel')
        self._logger = logging.getLogger(__name__)

    def setUp(self):
        super(test_partner_qualified_contact, self).setUp()
        cr, uid = self.cr, self.uid

        # I create partners
        luke_id = self.partner.create(cr, uid, {
            'name': 'Luke Skywalker',
        })
        self.luke = self.partner.browse(cr, uid, luke_id)
        # I create partners
        ben_id = self.partner.create(cr, uid, {
            'name': 'Obi-Wan Kenobi',
        })
        self.ben = self.partner.browse(cr, uid, ben_id)

        # I create qualifiers
        jedi_master_id = self.qualifier.create(cr, uid, {
            'name': 'Jedi Master'
        })
        self.jedi_master = self.qualifier.browse(cr, uid, jedi_master_id)
        padawan_id = self.qualifier.create(cr, uid, {
            'name': 'Padawan'
        })
        self.padawan = self.qualifier.browse(cr, uid, padawan_id)

    def test_bidirectional(self):
        """I test add a qualified contact"""
        cr, uid = self.cr, self.uid

        # I create link
        self.qualified_contact_rel.create(cr, uid, {
            'parent_id': self.luke.id,
            'contact_id': self.ben.id,
            'qualifier_id': self.jedi_master.id,
        })

        # I create inverse link
        self.qualified_contact_rel.create(cr, uid, {
            'parent_id': self.ben.id,
            'contact_id': self.luke.id,
            'qualifier_id': self.padawan.id,
        })

        # I retrieve updated partners
        self.luke = self.partner.browse(cr, uid, self.luke.id)
        self.ben = self.partner.browse(cr, uid, self.ben.id)

        # I check partners values
        self.assertEqual(
            self.luke.qualified_contact_rel_ids[0].contact_id.name,
            'Obi-Wan Kenobi'
        )
        self.assertEqual(
            self.luke.qualified_contact_rel_ids[0].qualifier_id.name,
            'Jedi Master'
        )
        self.assertEqual(self.luke.qualified_contact_ids[0].name,
                         'Obi-Wan Kenobi')
        self.assertEqual(
            self.ben.qualified_contact_rel_ids[0].contact_id.name,
            'Luke Skywalker'
        )
        self.assertEqual(
            self.ben.qualified_contact_rel_ids[0].qualifier_id.name,
            'Padawan'
        )
        self.assertEqual(self.ben.qualified_contact_ids[0].name,
                         'Luke Skywalker')


if __name__ == '__main__':
    unittest2.main()
