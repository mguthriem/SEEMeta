from SEEmeta import *

#Example: A PE cell 

#first instantiate a ZTA anvil
ZTA = anvil(type="polycrystalline",
            material="ZTA",
            culetGeometry="single toroid",
            culetDiameter=10.0)

print("zta is type",type(ZTA))

#Then instantiate a PE cell using this
PE001 = opposedAnvilCell(type="paris-edinburgh",
                         model = "VX5",
                         material = "819AW",
                         anvils = [ZTA,ZTA], #need convention for order e.g. [piston, cylinder]
                         gasketMaterial = "TiZr",
                         gasketType="encapsulating",
                         loadAxis=[0,1,0] #mantid coord system
                         )

#add optional parameters: 
PE001.temperatureControl = "CCR-1"
PE001.comment = "standard mail in set-up" 

#serialise and write to disk as json
PE_001_dict = PE001.to_dict()

SEEMetaSaver(PE_001_dict,"PE001.json")

# test reloading from disk
reloaded = SEEMetaLoader("PE001.json")

#check that reloading works
print("these data were reloaded from file as a dictionary: \n")
for key in reloaded:

    print(key," : ",reloaded[key])

#check that conversion to string works
print("\nand then converted to this giant string:\n")
outputString = toString(reloaded) 
print("output is of type: ",type(outputString)," with value: ")
print(outputString)