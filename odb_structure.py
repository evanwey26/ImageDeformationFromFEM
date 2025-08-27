from odbAccess import *
from textRepr import *
from odbMaterial import *
from odbSection import *
from abaqusConstants import *
import csv

def makeCSV(odbname, csvname):
    odb = openOdb(path=odbname)
    field_csv = []
    reaction_forces_csv=[]
    frame_count=0
    for stepName in odb.steps.keys():
    	for frame in odb.steps[stepName].frames:
    		frame_count+=1
    		displacementALL=frame.fieldOutputs['U']
    		fieldValuesU=displacementALL.values
    		coordinates=odb.rootAssembly.nodeSets[' ALL NODES']
    		for i in range(len(coordinates.nodes[0])):
    			temp_dict={
    			'time': frame.frameValue, 
    			'id': coordinates.nodes[0][i].label, 
    			'x': coordinates.nodes[0][i].coordinates[0], 
    			'y': coordinates.nodes[0][i].coordinates[1],
    			'z': coordinates.nodes[0][i].coordinates[2],
    			'u': fieldValuesU[i].data[0],
    			'v': fieldValuesU[i].data[1],
    			'w': fieldValuesU[i].data[2],
    			}
    			field_csv.append(temp_dict)

    with open("C:\\EvanWey\\ImageDeformationPackage\\"+csvname+".csv", 'w', newline='') as csvfile:
        fieldnames = ['time', 'id', 'x', 'y', 'z', 'u', 'v', 'w']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(field_csv)
    
if __name__ == "__main__":
    odbname = sys.argv[1]
    csvname = sys.argv[2]
    makeCSV(odbname, csvname)