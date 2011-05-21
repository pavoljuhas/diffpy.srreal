#!/usr/bin/env python

"""Unit tests for the PDFEnvelope class from diffpy.srreal.pdfcalculator
"""

# version
__id__ = '$Id$'

import os
import unittest
import cPickle

from diffpy.srreal.pdfcalculator import PDFEnvelope, makePDFEnvelope

##############################################################################
class TestPDFEnvelope(unittest.TestCase):

    def setUp(self):
        self.fstepcut = PDFEnvelope.createByType('stepcut')
        self.fstepcut.stepcut = 5
        self.fscale = PDFEnvelope.createByType('scale')
        return


    def tearDown(self):
        return


    def test___init__(self):
        """check PDFEnvelope.__init__()
        """
        self.assertEqual(1.0, self.fscale.scale)
        self.fscale._setDoubleAttr('scale', 2.0)
        self.assertEqual(2.0, self.fscale.scale)
        return


    def test___call__(self):
        """check PDFEnvelope.__call__()
        """
        # this is a virtual method in the base class
        self.assertRaises(RuntimeError, PDFEnvelope().__call__, 37)
        self.assertEqual(0.0, self.fstepcut(10))
        self.assertEqual(1.0, self.fstepcut(3.45))
        self.assertEqual(1.0, self.fscale(3.45))
        self.assertEqual(1.0, self.fscale(345))
        self.fscale.scale = -2
        self.assertEqual(-2.0, self.fscale(3.5))
        return


    def test_clone(self):
        """check PDFEnvelope.clone
        """
        # this is a virtual method in the base class
        self.assertRaises(RuntimeError, PDFEnvelope().clone)
        self.fstepcut.stepcut = 17
        e2 = self.fstepcut.clone()
        self.assertEqual('stepcut', e2.type())
        self.assertEqual(17.0, e2.stepcut)
        self.assertEqual(17.0, e2._getDoubleAttr('stepcut'))
        return


    def test_create(self):
        """check PDFEnvelope.create
        """
        # this is a virtual method in the base class
        self.assertRaises(RuntimeError, PDFEnvelope().create)
        self.assertEqual('stepcut', self.fstepcut.create().type())
        self.assertEqual('scale', self.fscale.create().type())
        self.fstepcut.stepcut = 17
        self.assertEqual(0.0, self.fstepcut.create().stepcut)
        return


    def test_type(self):
        """check PDFEnvelope.type
        """
        # this is a virtual method in the base class
        self.assertRaises(RuntimeError, PDFEnvelope().type)
        self.assertEqual('stepcut', self.fstepcut.type())
        self.assertEqual('scale', self.fscale.type())
        return


    def test_createByType(self):
        """check PDFEnvelope.createByType()
        """
        self.assertRaises(ValueError, PDFEnvelope.createByType, 'notregistered')
        return


    def test_getRegisteredTypes(self):
        """check PDFEnvelope.getRegisteredTypes
        """
        regtypes = PDFEnvelope.getRegisteredTypes()
        self.assertTrue(2 <= len(regtypes))
        self.assertTrue('stepcut' in regtypes)
        self.assertTrue('scale' in regtypes)
        return


    def test_pickling(self):
        '''check pickling and unpickling of PDFEnvelope.
        '''
        stp = self.fstepcut
        stp.foo = "qwer"
        stp.stepcut = 11
        stp2 = cPickle.loads(cPickle.dumps(stp))
        self.assertEqual('stepcut', stp2.type())
        self.assertEqual(11, stp2.stepcut)
        self.assertEqual(11, stp2._getDoubleAttr('stepcut'))
        self.assertEqual("qwer", stp2.foo)
        return


    def test_makePDFEnvelope(self):
        '''check the makePDFEnvelope wrapper.
        '''
        pbl = makePDFEnvelope('parabolaenvelope',
                parabola_envelope, a=1, b=2, c=3)
        self.assertEqual(3, pbl(0))
        self.assertEqual(6, pbl(1))
        self.assertEqual(11, pbl(2))
        pbl.b = 0
        self.assertEqual([7, 3, 28], map(pbl, [-2, 0, 5]))
        pbl2 = pbl.clone()
        self.assertEqual(1, pbl2.a)
        self.assertEqual(0, pbl2.b)
        self.assertEqual(3, pbl2.c)
        self.assertEqual([7, 3, 28], map(pbl2, [-2, 0, 5]))
        pbl3 = PDFEnvelope.createByType('parabolaenvelope')
        self.assertEqual(1, pbl3.a)
        self.assertEqual(2, pbl3.b)
        self.assertEqual(3, pbl3.c)
        return

# End of class TestPDFEnvelope

# function for wrapping by makePDFEnvelope

def parabola_envelope(x, a, b, c):
    return a * x**2 + b * x + c

if __name__ == '__main__':
    unittest.main()

# End of file