#import blender
import bpy
import random
import math
import re
import bmesh
from bpy import context as C
                                                                                                                                                                                         
#determination des parametres de l'environnement
#def choixEnviron():
    #file = open("settings.txt", "r")
    #lines = file.readlines()
    #for line in lines :
        #line=float(line.split(": ")[1].split("#")[0])
    #return lines
def choixEnviron():
    print("Taille de l'environnement")
    envSize=50
    print("nombre de proteine dans l'environnement : concentration")
    nbProt=100
    print("rayon de la proteine")
    
    return envSize,nbProt

#classe grain biologique
class BiologicalGrain:
    def __init__(self, coordinatesP, coordinatesR,listOfNeighbours,associationProbability ):
        self.x, self.y, self.z = coordinatesP
        self.rotateX, self.rotateY, self.rotateZ = coordinatesR
        self.associationProb = associationProbability
        self.associatedNeighbours = listOfNeighbours
    def getCoordP(self):
        listCoord=[self.x,self.y,self.z]
        return listCoord
    def getNeighbours():
        return self.associatedNeighbours
        
#classe grain biologique
class SimulatedGrain:
    def __init__(self, bGrain,activesFace, grainName):
        self.BiologicalGrain = bGrain
        self.activesFaces =  activesFace      
        self.moved=False
        self.name=grainName
        self.attach=False
        
# initialisation de l'environnement en terme de coordonnees des objets
def initProteine(envSize,nbProt,scaleFactor,grainDiameter):
    listProt=[]
    for i in range(0,nbProt,1):
        caseEmpty=False
        while not caseEmpty:
            x=random.randrange(0,envSize,grainDiameter)
            x=float(x)/scaleFactor
            y=random.randrange(0,envSize,grainDiameter)
            y=float(y)/scaleFactor
            z=random.randrange(0,envSize,grainDiameter)
            z=float(z)/scaleFactor
            listCoord=[x,y,z]
            caseEmpty=caseIsEmpty(listProt,listCoord)
            if caseEmpty:
                drawProt(listProt,listCoord,scaleFactor,grainDiameter)
    return listProt

# dessiner le proteine dans l'environnement blender : rotation, faces d'interet (site de liaison)...
def drawProt(listProt,listCoord,scaleFactor,grainDiameter):
    x,y,z=listCoord
    #creation d'une sphere
    nameS="Sphere"+str(len(listProt))
    bpy.ops.mesh.primitive_ico_sphere_add(size=grainDiameter/(scaleFactor*2), view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nameS
    #creation des poles:
    proteinFaces(nameS)
    #appli d'une rotation aleatoire
    a,b,c=angleRotation()
    listRotate=[a,b,c]
    bpy.ops.transform.rotate(axis=(a, b, c))
    #creation des grains
    listNeighbours=[]
    protein=BiologicalGrain(listCoord,listRotate,listNeighbours,2)
    grain=SimulatedGrain(protein,1,nameS)
    listProt.append(grain)

# determination aleatoire de l'angle de rotation de la proteine
def angleRotation():
    a=random.randint(-360,360)
    a=a*(math.pi/180)
    b=random.randint(-360,360)
    b=b*(math.pi/180)
    c=random.randint(-360,360)
    c=c*(math.pi/180)
    return a,b,c

# verrification pour savoir si une case d'interet est vide
def caseIsEmpty(listProt,listCoord):
    for protToCheck in listProt:
        listCoordToCheck=protToCheck.BiologicalGrain.x,protToCheck.BiologicalGrain.y,protToCheck.BiologicalGrain.z
        if listCoordToCheck==listCoord:
            return False
    return True
  
# determination des faces correspondantes aux sites de liaison
def proteinFaces(objectName):
        #def obj + face a colorier et attribuer une propriete
    obj=bpy.data.objects[objectName]
    obj.select=True
    faces=obj.data.polygons
    obj.data.calc_tessface()
    faces=obj.data.tessfaces
    
    red = bpy.data.materials.new('Red')
    red.diffuse_color = (1,0,0)
    blue = bpy.data.materials.new('Blue')
    blue.diffuse_color = (0,0,1)
    yellow = bpy.data.materials.new('Yellow')
    yellow.diffuse_color = (1,1,0)
    grey = bpy.data.materials.new('Grey')
    grey.diffuse_color = (0.5,0.5,0.5)
    
    ob = bpy.context.object
    me = ob.data
    me.materials.append(grey)
    me.materials.append(red)
    me.materials.append(blue)
    me.materials.append(yellow)
    
  # Assign materials to faces
    for f in faces:
        #print(f.index)
        if f.index==78 or f.index==79:
            f.material_index=2
        elif f.index==10 or f.index==5:
            f.material_index=1
        elif f.index==0 or f.index==2:
            f.material_index=3
        else:
            f.material_index=0
        #f.material_index = f.index % 3
 
    # Set left half of sphere smooth, right half flat shading
   
# determiner les molecules attachees en fonction de la distance entre les sites de liaisons
def attacher(listProt,grainDiameter,scaleFactor):
    #trouver les spheres attachées
    #portLiees={}
    distance=grainDiameter/scaleFactor
    for i in range(len(listProt)-1):
        x1=listProt[i].BiologicalGrain.x
        y1=listProt[i].BiologicalGrain.y
        z1=listProt[i].BiologicalGrain.z
        for j in range(i+1,len(listProt)):
            x2=listProt[j].BiologicalGrain.x
            y2=listProt[j].BiologicalGrain.y
            z2=listProt[j].BiologicalGrain.z
            dx=x1-x2
            dy=y1-y2
            dz=z1-z2
            if (dx <distance and dx >-distance) and (dy <distance and dy >-distance) and (dz <distance and dz >-distance):
                print ("proteine attachee !!!!!!!!!!!!!",dx,dy,dz)
                listProt[i].BiologicalGrain.associatedNeighbours.append(listProt[j])
                listProt[j].BiologicalGrain.associatedNeighbours.append(listProt[i])

# determiner les coord de chaque molecules en fonction de chaque frame
def mouvementProt(listProt,envSize,scaleFactor,grainDiameter):
    envSize=envSize/scaleFactor
    frame_num =0#numero de la frame (pour le temps)
    # Verrif que le bool est false (pas encore deplace)
    attacher(listProt,grainDiameter,scaleFactor)
    nbDeplacement=26
    for position in range(nbDeplacement):
        indiceList=indice(listProt)
        while len(indiceList)!=0:
            # choix d'une molecule aleatoirement
            i=random.randint(0,len(indiceList)-1)
            ind=indiceList[i]
            prot=listProt[ind]
            # enregistrement des donnees sur la frame
            bpy.context.scene.frame_set(frame_num)
            mvtOK=False
            if prot.moved==True:
                mvtOK=True
                indiceList.pop(i)
            while mvtOK!=True:
                # calcul du mouvement
                x=random.randrange(-grainDiameter,grainDiameter,grainDiameter)
                x=x/scaleFactor
                y=random.randrange(-grainDiameter,grainDiameter,grainDiameter)
                y=y/scaleFactor
                z=random.randrange(-grainDiameter,grainDiameter,grainDiameter)
                z=z/scaleFactor
                move=[x,y,z]
                # tests pour controler le mouvement
                coordOfCurrentSphere = prot.BiologicalGrain.x,prot.BiologicalGrain.y,prot.BiologicalGrain.z
                listCoord=[coordOfCurrentSphere[0]+x,coordOfCurrentSphere[1]+y,coordOfCurrentSphere[2]+z]
                moveIsPossible=caseIsEmpty(listProt,listCoord)
                if moveIsPossible==True:
                    mvtOK=True
                    deplacePosition(prot, x, y, z, scaleFactor)
                    indiceList.pop(i)
        for prot in listProt:
            prot.moved=False
        frame_num+=10

def indice(listProt):
    indiceList=[]
    for i in range(len(listProt)):
        indiceList.append(i)
    return indiceList
           
# l'environnement est considere comme inifini
def deplacePosition(prot, x, y, z, scaleFactor):
    bProt=bpy.data.objects[prot.name]
    bProt.location[0]=bProt.location[0]+x
    bProt.location[1]=bProt.location[1]+y
    bProt.location[2]=bProt.location[2]+z
    if bProt.location[0]<0:
        bProt.location[0]=envSize/scaleFactor
    if bProt.location[1]<0:
        bProt.location[1]=envSize/scaleFactor
    if bProt.location[2]<0:
        bProt.location[2]=envSize/scaleFactor
    if bProt.location[0]>envSize/scaleFactor:
        bProt.location[0]=0
    if bProt.location[1]>envSize/scaleFactor:
        bProt.location[1]=0
    if bProt.location[2]>envSize/scaleFactor:
        bProt.location[2]=0
    bProt.keyframe_insert(data_path="location", index=-1)
    prot.BiologicalGrain.x,prot.BiologicalGrain.y,prot.BiologicalGrain.z=bProt.location[0],bProt.location[1],bProt.location[2]
    prot.moved=True

#supprimer tous les objets de l'environnement avant de refaire une simulation   
def clean():
    for obj in bpy.data.objects:
        currentName=obj.name
        #print(currentName)
        if("Cube" in currentName or "Sphere" in currentName):
            obj.select=True
            bpy.ops.object.delete(use_global=False)
 
 

#prog principal
bpy.ops.object.mode_set(mode='OBJECT')
clean()
scaleFactor = 10
grainDiameter = 2
#grainDiameter,envSize,nbProt,associationProb,nbRunPerFrame,sizeActiveSite,nbActivesSites=choixEnviron()
envSize,nbProt=choixEnviron()
bpy.context.scene.frame_set(0)
listProt=initProteine(envSize,nbProt,scaleFactor,grainDiameter)
mouvementProt(listProt,envSize,scaleFactor,grainDiameter)
#attacher(listProt,grainDiameter,scaleFactor)   

