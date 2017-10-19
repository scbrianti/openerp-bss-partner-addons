# -*- coding: utf-8 -*-
# Part of Qualified Contacts.
# See LICENSE file for full copyright and licensing details.

import unittest2
import odoo.tests.common as common
from odoo.netsvc import logging


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
        ben_id = self.partner.create(cr, uid, {
            'name': 'Obi-Wan Kenobi',
            'phone': '+1 5550110',
            'mobile': '+1 5550115',
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
        self.assertEqual(
            self.luke.qualified_contact_rel_ids[0].phone,
            '+1 5550110'
        )
        self.assertEqual(
            self.luke.qualified_contact_rel_ids[0].mobile,
            '+1 5550115'
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
