# test of building a cylider with materials
from SEEmeta import cylinder, material 
from sqlalchemy import create_engine

def test_cylinder_with_materials():

    # Connect to your DB
    engine = create_engine("sqlite:///../materials/materials.db")

    # Create a cylinder with a material
    mat = material(name="Aluminum", id=1, hasSpectra=False)
    cyl = cylinder.Cylinder(
        id=1,
        name="Test Cylinder",
        diameter=10.0,
        height=20.0,
        gasketType="encapsulating",
        materials=[mat]
    )
    
    # Check if the cylinder is created correctly
    assert cyl.id == 1
    assert cyl.name == "Test Cylinder"
    assert cyl.diameter == 10.0
    assert cyl.height == 20.0
    assert len(cyl.materials) == 1
    assert cyl.materials[0].name == "Aluminum"
    
    # Check if the gasket type is set correctly
    assert cyl.gasketType == "encapsulating"