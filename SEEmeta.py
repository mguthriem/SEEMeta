# SEE metadata
import json
import os
from sqlalchemy import create_engine, text

class anvil:
    #class to define a generic anvil

    def __init__(self,type,material,culetGeometry,culetDiameter,model):

        self.type = type
        self.material = material
        self.culetGeometry = culetGeometry
        self.culetDiameter = culetDiameter
        self.validate()

        #optional extra info
        self.model = model
        
        self.manufacturer = ""
        self.comment = ""
        self.UB = [] #aspirational, but could be included...

        self.stringDescriptor = self.buildStringDescriptor()
        self.cadFile = f"{self.stringDescriptor}.cad"

    def validate(self):

        assert self.type in ["polycrystalline", "single-crystal"]
        assert self.material in ["ZTA","WC","diamond","CBN","sintered diamond"]
        assert self.culetGeometry in ["single toroid", "double toroid", "flat"]
        assert type(self.culetDiameter) is float


    def to_dict(self):
        return {
            "type": self.type,
            "material": self.material,
            "culetGeometry": self.culetGeometry,
            "culetDiameter": self.culetDiameter,
            "model": self.model,
            "cadFile": self.cadFile,
            "manufacturer": self.manufacturer,
            "stringDescriptor": self.stringDescriptor,
            "comment": self.comment,
            "UB": self.UB
        }
    
    def buildStringDescriptor(self):

        # create a short string to represent instance

        if self.type == "single-crystal":
            stringDescriptor = f"anvil_SXL_{self.material}_culet_{self.culetDiameter}"
        elif self.type == "polycrystalline":
            stringDescriptor = f"anvil_{self.culetGeometry}_{self.model}_{self.material}"

        return stringDescriptor.replace(" ","_")

    @classmethod
    def from_dict(cls, data):
        #instantiate class from data dictionary

        obj = cls(
            type=data["type"],
            material=data["material"],
            culetGeometry=data["culetGeometry"],
            culetDiameter=data["culetDiameter"],
            model=data["model"]
        )
        obj.cadFile = data.get("cadFile", "") 
        obj.manufacturer = data.get("manufacturer", "")
        obj.comment = data.get("comment", "")
        obj.UB = data.get("UB", [])
        return obj

class opposedAnvilCell:
    #class to define a generic opposed anvil cell

    def __init__(self,type,model,material,anvils,gasketMaterial,gasketType,loadAxis):

        self.type = type
        self.model = model
        self.material = material
        self.anvils = anvils
        self.gasketMaterial = gasketMaterial
        self.gasketType = gasketType
        self.loadAxis = loadAxis

        self.stringDescriptor = self.buildStringDescriptor()
        self.cadFile = f"{self.stringDescriptor}.cad"

        # optional info
        self.temperatureControl = None
        self.manufacturer = ""
        self.comment = ""

        self.validate()

    def validate(self):

        assert self.type in ["paris-edinburgh","DAC"]
        if self.type == ["paris-edinburgh"]:
            assert self.model in ["VX1","VX3","VX5"]
        elif self.type == ["DAC"]:
            assert self.model in ["LEGACY","MARK-VI","MARK-VII"]

        # assert self.material in [""] # not sure what these are
        if self.temperatureControl is not None:
            assert self.temperatureControl in ["CCR-14",
                                               "CCR-21",
                                               "CCR-25",
                                               "CRYO-04",
                                               "PE-CRYO",
                                               "None"] 
        assert len(self.anvils) == 2 #make sure there are two anvils!
        assert self.gasketMaterial in ["TiZr","Re","W", "Zr", 
                                       "SS301", 
                                       "pyrophyllite","Al",
                                       "CuBe"]
        print(f"gasket type is {self.gasketType}")
        assert self.gasketType in ["encapsulating","non_encapsulating","flat","other"]

    def to_dict(self):
        return {
            "type": self.type,
            "model": self.model,
            "material": self.material,
            "anvils": [anvil.to_dict() for anvil in self.anvils],
            "gasketMaterial": self.gasketMaterial,
            "gasketType": self.gasketType,
            "loadAxis": self.loadAxis,
            "temperatureControl": self.temperatureControl,
            "cadFile": self.cadFile,
            "stringDescriptor": self.stringDescriptor,
            "manufacturer": self.manufacturer,
            "comment": self.comment
        }
    
    @classmethod
    def from_dict(cls, data):
        anvils = [anvil.from_dict(a) for a in data["anvils"]]
        obj = cls(
            type=data["type"],
            model=data["model"],
            material=data["material"],
            anvils=anvils,
            gasketMaterial=data["gasketMaterial"],
            gasketType=data["gasketType"],
            loadAxis=data["loadAxis"]
        )
        obj.temperatureControl = data.get("temperatureControl", "")
        obj.cadFile = data.get("cadFile", "")
        obj.manufacturer = data.get("manufacturer", "")
        obj.comment = data.get("comment", "")
        return obj
    
    def buildStringDescriptor(self):

        # create a short string to represent instance
        anvil = self.anvils[0] # this assumes anvils are the same

        if self.type == "paris-edinburgh":

            stringDescriptor = f"PE_{self.model}_{anvil.material}_{anvil.culetGeometry}"
        elif self.type == "DAC":
            stringDescriptor = f"DAC_{self.model}_{anvil.culetDiameter}mm_culet_{self.gasketMaterial}_gasket"
        else:
            raise ValueError(f"Unsupported type: {self.type}")

        return stringDescriptor.replace(" ","_")

    
    def makeFileName(self):
        # a standardised way to create a file name for the output json. The filename should
        # intelligibly describe the SEE, so should be build from it's core attributes. For
        # the save of brevity, these will be abbreviated.

        if self.type == "paris-edinburgh":
            abbrvType = "PE"
        else:
            abbrvType = self.type

        self.anvils[0].type
        
        self.filename = f"{abbrvType}_{self.anvils[0].culetGeometry}_{self.anvils[0].material}.json".replace(' ','_')
        
        print(self.filename)


def SEEMetaLoader(filePath):
    #Loads SEEMeta json file as a dictionary
    
    with open(filePath, "r") as f:
        data = json.load(f)

    return data

def SEEMetaSaver(dict,filePath):
    #save SEEMeta dictionary to file.

    with open(filePath, "w") as f:
        json.dump(dict, f, indent=4)

    print(f"successfully wrote: {filePath}")

def toString(data,compact=True):
    #converts data loaded from file as a dictionary to a string that can be added as a value to a pv
    #optionally can make a compact version with no indentation or whitespace
    
    if compact:
        jsonString = json.dumps(data, separators=(",",":"))
    else:
        jsonString = json.dumps(data, indent=4)

    return jsonString

class material:
    def __init__(self, db_engine, *, id=None, name=None):
        self.db_engine = db_engine

        if id is None and name is None:
            raise ValueError("Must provide either id or name.")

        with db_engine.connect() as conn:
            if id is not None:
                result = conn.execute(text("SELECT * FROM materials WHERE id = :id"), {"id": id}).fetchone()
            else:
                result = conn.execute(
                    text("SELECT * FROM materials WHERE LOWER(name) = LOWER(:name)"),
                    {"name": name}
                ).fetchone()

            if result is None:
                raise ValueError(f"Material not found for id={id} name={name}")

            # Populate attributes from row
            for key, value in result._mapping.items():
                setattr(self, key, value)

            # gather any spectra associated with this material
            
            self.get_spectra()

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"<Material {self.name} (ID: {self.id})>"

    @classmethod
    def load_all(cls, db_engine):
        with db_engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM materials")).fetchall()
            return [cls(db_engine, id=row.id) for row in result]
        
    def get_spectra(self):
        with self.db_engine.connect() as conn:
            result = conn.execute(text("""
                SELECT * FROM spectra WHERE material_id = :id
            """), {"id": self.id}).fetchall()

            self.spectra = [dict(row._mapping) for row in result]
            self.hasSpectra = len(self.spectra) > 0

            return self.spectra



         