# SEE metadata
import json
import os

class anvil:
    #class to define a generic anvil

    def __init__(self,type,material,culetGeometry,culetDiameter):

        self.type = type
        self.material = material
        self.culetGeometry = culetGeometry
        self.culetDiameter = culetDiameter
        self.validate()

        #optional extra info
        self.cadFile = ""
        self.manufacturer = ""
        self.comment = ""
        self.UB = [] #aspirational, but could be included...

    def validate(self):

        assert self.type in ["polycrystalline", "single-crystal"]
        assert self.material in ["ZTA","WC","diamond","CBN","versimax"]
        assert self.culetGeometry in ["single toroid", "double toroid", "flat"]

    def to_dict(self):
        return {
            "type": self.type,
            "material": self.material,
            "culetGeometry": self.culetGeometry,
            "culetDiameter": self.culetDiameter,
            "cadFile": self.cadFile,
            "manufacturer": self.manufacturer,
            "comment": self.comment,
            "UB": self.UB
        }
    
    @classmethod
    def from_dict(cls, data):
        #instantiate class from data dictionary

        obj = cls(
            type=data["type"],
            material=data["material"],
            culetGeometry=data["culetGeometry"],
            culetDiameter=data["culetDiameter"]
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

        # optional info
        self.temperatureControl = None
        self.cadFile = ""
        self.manufacturer = ""
        self.comment = ""

        self.validate()

    def validate(self):

        assert self.type in ["paris-edinburgh","DAC"]
        if self.type == ["paris-edinburgh"]:
            assert self.model in ["VX1","VX3","VX5"]
        elif self.type == ["DAC"]:
            assert self.model in ["SNAP-DAC"]

        # assert self.material in [""] # not sure what these are
        if self.temperatureControl is not None:
            assert self.temperatureControl in ["CCR-1","CCR-2","Furnace"] #I made these up

        assert len(self.anvils) == 2 #make sure there are two anvils!

        assert self.gasketMaterial in ["TiZr","Re","W"]
        assert self.gasketType in ["encapsulating","flat"]

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

def SEEMetaLoader(filePath):
    #Loads SEEMeta json file as a dictionary
    
    with open(filePath, "r") as f:
        data = json.load(f)

    return data

def SEEMetaSaver(dict,filePath):
    #save SEEMeta dictionary to file.

    with open("PE001.json", "w") as f:
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


         