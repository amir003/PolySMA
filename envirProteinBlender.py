#import blender
import bpy
import random
import math
import re
import bmesh
from bpy import context as C
                                                                                                                                                                                         
#determination des parametres de l'environnement
def choixEnviron():
    print("Donnez le nom du fichier")
    #fileName=raw_input()
    file = open("param.txt", "r")
    lines = file.readlines()
    paramList=[]
    for line in lines :
        line=float(line.split(":")[1].split("#")[0])
        paramList.append(line)
    return paramList

#classe grain biologique
class BiologicalGrain:
    def __init__(self, coordinatesR,listOfNeighbours,associationProbability ):
        self.rotateX, self.rotateY, self.rotateZ = coordinatesR
        self.associationProb = associationProbability
        self.associatedNeighbours = listOfNeighbours

        
#classe grain biologique
class SimulatedGrain:
    def __init__(self, bGrain,sizeActiveSite,nbActivesSites, objGrain):
        self.BiologicalGrain = bGrain
        self.nbActivesSites =  nbActivesSites  
        self.sizeActiveSite = sizeActiveSite
        self.moved=False
        self.objectBl=objGrain
        self.attach=False
  
##############################################################################################  
# initialisation de l'environnement en terme de coordonnees des objets
def initProteine(envSize,nbProt,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites):
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
            caseEmpty=caseIsEmpty(listProt,listCoord,envSize,scaleFactor,grainDiameter)
            if caseEmpty:
                drawProt(listProt,listCoord,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites)
    return listProt


# dessiner le proteine dans l'environnement blender : rotation, faces d'interet (site de liaison)...
def drawProt(listProt,listCoord,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites):
    x,y,z=listCoord
    #creation d'une sphere
    nameS="Sphere"+str(len(listProt))
    bpy.ops.mesh.primitive_ico_sphere_add(size=grainDiameter/(scaleFactor*2), view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nameS
    objectBl=bpy.data.objects[nameS]
    #creation des poles:
    proteinFaces(nameS)
    #appli d'une rotation aleatoire
    a,b,c=angleRotation()
    listRotate=[a,b,c]
    bpy.ops.transform.rotate(axis=(a, b, c))
    #creation des grains
    listNeighbours=[]
    protein=BiologicalGrain(listRotate,listNeighbours,associationProb)
    grain=SimulatedGrain(protein,sizeActiveSite,nbActivesSites,objectBl)
    listProt.append(grain)
    objectBl.keyframe_insert(data_path="location", index=-1)


# determination aleatoire de l'angle de rotation de la proteine
def angleRotation():
    a=random.randint(-360,360)
    a=a*(math.pi/180)
    b=random.randint(-360,360)
    b=b*(math.pi/180)
    c=random.randint(-360,360)
    c=c*(math.pi/180)
    return a,b,c


# determination des faces correspondantes aux sites de liaison
def proteinFaces(objectName):
    #def obj + face a colorier et attribuer une propriete
    obj=bpy.data.objects[objectName]
    obj.select=True
    #faces=obj.data.polygons
    obj.data.calc_tessface()
    faces=obj.data.tessfaces
    
    red = bpy.data.materials.new('Red')
    red.diffuse_color = (1,0,0)
    blue = bpy.data.materials.new('Blue')
    blue.diffuse_color = (0,0,1)
    yellow = bpy.data.materials.new('Yellow')
    yellow.diffuse_color = (1,1,0)
    green = bpy.data.materials.new('Green')
    green.diffuse_color = (0,1,0)
    turquoise = bpy.data.materials.new('Turquoise')
    turquoise.diffuse_color = (0,1,1)
    grey = bpy.data.materials.new('Grey')
    grey.diffuse_color = (0.5,0.5,0.5)
    
    ob = bpy.context.object
    me = ob.data
    me.materials.append(grey)
    me.materials.append(red)
    me.materials.append(blue)
    me.materials.append(yellow)
    me.materials.append(green)
    me.materials.append(turquoise)
    
  # Assign materials to faces
    for f in faces:
        if f.index==78 or f.index==79:
            f.material_index=2
        elif f.index==10 or f.index==5:
            f.material_index=1
        elif f.index==0 or f.index==2:
            f.material_index=3
        else:
            f.material_index=0

##############################################################################################  

# verification pour savoir si une case d'interet est vide
def caseIsEmpty(listProt,listCoord,envSize,scaleFactor,grainDiameter):
    #non déplacement non autorisé
    epsilon=grainDiameter/(scaleFactor*2)
    for i in range(len(listCoord)):
        if (listCoord[i]<0):
            listCoord[i]+=envSize/scaleFactor
        #if ( ( (listCoord[i]*scaleFactor)-envSize )>0.0 ):
        if listCoord[i]>envSize/scaleFactor :
           # print(listCoord[i],scaleFactor,float(envSize),(listCoord[i]*scaleFactor)-float(envSize)) 
            listCoord[i]-=envSize/scaleFactor
    x1,y1,z1=listCoord
    for protToCheck in listProt:
        x2,y2,z2=protToCheck.objectBl.location[0],protToCheck.objectBl.location[1],protToCheck.objectBl.location[2]
        #print(listCoord,listCoordToCheck)
        if (x1>x2-epsilon and x1<x2+epsilon) and (y1>y2-epsilon and y1<y2+epsilon) and (z1>z2-epsilon and z1<z2+epsilon):
            return False
    return True
  
##############################################################################################  
  
  
# determiner les molecules attachees en fonction de la distance entre les sites de liaisons
def attacher(listProt,grainDiameter,scaleFactor):
    distance=grainDiameter/scaleFactor
    for i in range(len(listProt)-1):
        x1=listProt[i].objectBl.location[0]
        y1=listProt[i].objectBl.location[1]
        z1=listProt[i].objectBl.location[2]
        for j in range(i+1,len(listProt)):
            x2=listProt[j].objectBl.location[0]
            y2=listProt[j].objectBl.location[1]
            z2=listProt[j].objectBl.location[2]
            dx=x1-x2
            dy=y1-y2
            dz=z1-z2
            if (dx <distance and dx >-distance) and (dy <distance and dy >-distance) and (dz <distance and dz >-distance):
                listProt[i].BiologicalGrain.associatedNeighbours.append(listProt[j])
                listProt[j].BiologicalGrain.associatedNeighbours.append(listProt[i])


def sos(prot,listProt):
    boolSOS=True
    #for i in range(len(listProt)-1):
    list1=[prot.objectBl.location[0],prot.objectBl.location[1],prot.objectBl.location[2]]
    for j in range(0,len(listProt)):
        list2=[listProt[j].objectBl.location[0],listProt[j].objectBl.location[1],listProt[j].objectBl.location[2]]
        if (prot!=listProt[j] and list1==list2):
            print("protein sup",prot.objectBl.name,listProt[j].objectBl.name)
            boolSOS=False
    return boolSOS


# determiner les coord de chaque molecules en fonction de chaque frame
def mouvementProt(listProt,envSize,scaleFactor,grainDiameter):
    frame_num =5#numero de la frame (pour le temps)
    nbDeplacement=40
    for position in range(nbDeplacement):
        attacher(listProt,grainDiameter,scaleFactor)
        print("new frame",position)
        indiceList=indice(listProt)
        cpteur=0
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
            while not mvtOK:
                # calcul du mouvement
                x=random.randrange(-grainDiameter,grainDiameter+1,grainDiameter)
                x=x/scaleFactor
                y=random.randrange(-grainDiameter,grainDiameter+1,grainDiameter)
                y=y/scaleFactor
                z=random.randrange(-grainDiameter,grainDiameter+1,grainDiameter)
                z=z/scaleFactor
                move=[x,y,z]
                # tests pour controler le mouvement
                sphereCoor = [float(prot.objectBl.location[0]),float(prot.objectBl.location[1]),float(prot.objectBl.location[2])]
                listCoord=[float(sphereCoor[0]+x),float(sphereCoor[1]+y),float(sphereCoor[2]+z)]
                listCoord2=listCoord.copy()
                moveIsPossible=caseIsEmpty(listProt,listCoord2,envSize,scaleFactor,grainDiameter)
                if moveIsPossible:
                    #print("nia")
                    mvtOK=True
                    cpteur+=1
                    deplacePosition(prot, x, y, z, scaleFactor)
                    boolSos=sos(prot,listProt)
                    if not boolSos :
                        print("indicefail",len(indiceList),cpteur,x,y,z)
                        print(sphereCoor)
                        print(listCoord)
                        print(listCoord2)
                        print(prot.objectBl.location[0],prot.objectBl.location[1],prot.objectBl.location[2])
                    if len(prot.BiologicalGrain.associatedNeighbours)!=0:
                        test(prot, x, y, z, scaleFactor)
                    indiceList.pop(i)
        for prot in listProt:
            prot.moved=False
        frame_num+=5


def indice(listProt):
    indiceList=[]
    for i in range(len(listProt)):
        indiceList.append(i)
    return indiceList

# deplacer toutes les proteines attachees
def test(prot, x, y, z, scaleFactor):
    for assoProt in prot.BiologicalGrain.associatedNeighbours:
        if assoProt.moved==False:
            deplacePosition(assoProt, x, y, z, scaleFactor)
            test(assoProt, x, y, z, scaleFactor)


# l'environnement est considere comme inifini
def deplacePosition(prot, x, y, z, scaleFactor):
    obProt=prot.objectBl
    obProt.location[0]=obProt.location[0]+x
    obProt.location[1]=obProt.location[1]+y
    obProt.location[2]=obProt.location[2]+z
    for i in range(3):
        if obProt.location[i]<0:
            obProt.location[i]+=envSize/scaleFactor
            
        if  obProt.location[i]>envSize/scaleFactor:
            obProt.location[i]-=envSize/scaleFactor
            
    obProt.keyframe_insert(data_path="location", index=-1)
    prot.moved=True

##############################################################################################  

#supprimer tous les objets de l'environnement avant de refaire une simulation   
def clean():
    for obj in bpy.data.objects:
        currentName=obj.name
        #print(currentName)
        if("Cube" in currentName or "Sphere" in currentName):
            obj.select=True
            bpy.ops.object.delete(use_global=False)
 
 
##############################################################################################  

#prog principal
bpy.ops.object.mode_set(mode='OBJECT')
clean()
#lecture du fichier de parametres
grainDiameter,envSize,nbProt,associationProb,nbRunPerFrame,nbRun,sizeActiveSite,nbActivesSites,scaleFactor=choixEnviron()
nbProt=int(nbProt)
nbActivesSites=int(nbActivesSites)
#initialisation des spheres
bpy.context.scene.frame_set(0)
listProt=initProteine(envSize,nbProt,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites)
#deplacement des proteines
mouvementProt(listProt,envSize,scaleFactor,grainDiameter)
