from SEEmeta import *

#Example: A PE cell 

#first instantiate a ZTA anvil
anvil = anvil(type="polycrystalline",
            material="CBN",
            culetGeometry="single toroid",
            culetDiameter=10.0)

#Then instantiate a PE cell using this
cell = opposedAnvilCell(type="paris-edinburgh",
                         model = "VX3",
                         material = "819AW",
                         anvils = [anvil,anvil], #need convention for order e.g. [piston, cylinder]
                         gasketMaterial = "TiZr",
                         gasketType="encapsulating",
                         loadAxis=[0,1,0] #mantid coord system
                         )

#add optional parameters: 
cell.temperatureControl = "none"
cell.comment = "standard mail in set-up" 

#serialise and write to disk as json
dict = cell.to_dict()

SEEMetaSaver(dict,"PE002.json")

# test reloading from disk
reloaded = SEEMetaLoader("PE002.json")

#check that reloading works
print("these data were reloaded from file as a dictionary: \n")
for key in reloaded:

    print(key," : ",reloaded[key])

#check that conversion to string works
print("\nand then converted to this giant string:\n")
outputString = toString(reloaded) 
print("output is of type: ",type(outputString)," with value: ")
print(outputString)