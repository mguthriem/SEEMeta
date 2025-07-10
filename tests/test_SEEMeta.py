import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_instantiateCylinder():

    from SEEmeta import cylinder

    # Instantiate a Cylinder object
    cylinder = cylinder(material="NiCrAl",
                        chemicalFormula="(Li7)2-H-D2",
                        massDensity=3.797,
                        ID=5.0,
                        OD=10.0,
                        height=20.0)
