from SEEmeta import *

#Example: A PE cell 

#first instantiate a ZTA anvil
anv = anvil(type="single-crystal",
            material="diamond",
            culetGeometry="flat",
            culetDiameter=0.8)

print("anvil is type",type(anv))

#Then instantiate a PE cell using this
cell = opposedAnvilCell(type="DAC",
                         model = "Mark IV",
                         material = "steel",
                         anvils = [anv,anv], #need convention for order e.g. [piston, cylinder]
                         gasketMaterial = "Re",
                         gasketType="flat",
                         loadAxis=[0,0,1] #mantid coord system
                         )

#add optional parameters: 
cell.temperatureControl = "none"
cell.comment = "SNAP DAC room temp" 

#serialise and write to disk as json
dict = cell.to_dict()

SEEMetaSaver(dict,"DAC001.json")

# test reloading from disk
reloaded = SEEMetaLoader("DAC001.json")

#check that reloading works
print("these data were reloaded from file as a dictionary: \n")
for key in reloaded:

    print(key," : ",reloaded[key])

#check that conversion to string works
print("\nand then converted to this giant string:\n")
outputString = toString(reloaded) 
print("output is of type: ",type(outputString)," with value: ")
print(outputString)