#aide windows : file="C:/\\Users/\\Emilie/\\Desktop/\\IGEM/\\testEnvirProteinV10.py"
# exec(compile(open(file).read(),file,'exec'))


#import blender
import bpy
import random
import math
import re
import bmesh
from bpy import context as C

#grainDiameter,envSize,nbProt,associationProb,nbRunPerFrame,nbRun,sizeActiveSite,nbActivesSites,scaleFactor

#fenetre appellee pour rentrer les parametres :
class DialogOperator(bpy.types.Operator):
    bl_idname = "object.dialog_operator"
    bl_label = "Simple Dialog Operator"

    grainDiameter = bpy.props.FloatProperty(name="diametre du grain",default=2)
    envSize = bpy.props.FloatProperty(name="Taille de l'environnement",default=50)
    nbProt = bpy.props.IntProperty(name="nombre de proteine",default=100,min=0)
    associationProb = bpy.props.FloatProperty(name="proba asso ",default=0.5,min=0,max=1)
    nbRunPerFrame = bpy.props.IntProperty(name="nombre de run par frame",default=5,min=1)
    nbRun = bpy.props.IntProperty(name="nombre de run",default=10,min=1)
    sizeActiveSite=bpy.props.IntProperty(name="taille du site de liaison",default=2)
    nbActivesSites=bpy.props.IntProperty(name="nombre de site de liaison",default=2)
    scaleFactor=bpy.props.IntProperty(name="facteur d'ajustement",default=10)
    #temp = bpy.props.IntProperty(name="temperature",default=20)

    def execute(self, context):
        message = "Popup Values: %f,%f,%i, %f,%i,%i,%i,%i, %i" % (self.grainDiameter,self.envSize,self.nbProt,self.associationProb,self.nbRunPerFrame,self.nbRun,self.sizeActiveSite,self.nbActivesSites,self.scaleFactor)
        self.report({'INFO'}, message)
        infoParam=message.split(":")[1]
        tableauParam=infoParam.split(",")
        main(tableauParam)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

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
        self.activesSites =  [sizeActiveSite,nbActivesSites]
        self.moved=False
        self.objectBl=objGrain
        self.attach=False

##############################################################################################
# initialisation de l'environnement en terme de coordonnees des objets
def initProteine(envSize,nbProt,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites):
    listProt=[]
    facesList=[]
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
                drawProt(listProt,listCoord,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites,facesList)
    return listProt


# dessiner le proteine dans l'environnement blender : rotation, faces d'interet (site de liaison)...
def drawProt(listProt,listCoord,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites,facesList):
    x,y,z=listCoord
    #creation d'une sphere
    nameS="Sphere"+str(len(listProt))
    bpy.ops.mesh.primitive_ico_sphere_add(size=grainDiameter/(scaleFactor*2), view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nameS
    objectBl=bpy.data.objects[nameS]
    #creation des faces d'accroche:
    proteinFaces(nameS,sizeActiveSite,nbActivesSites,facesList)
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
def proteinFaces(objectName,sizeActiveSite,nbActivesSites,facesList):
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
        f.material_index=0
        for nbFace in range(nbActivesSites):
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
# calcul d'un tableau de valeur d'association avant le lancement du run, retourne un tableau de valeur
def tableauProbaAsso(nbProt,nbRun):
    tableauProba=[];
    for i in range(nbProt*nbRun):
        proba=random.randint(0,100)
        proba=proba/100
        tableauProba.append(proba)
    return tableauProba


# determiner les molecules attachees en fonction de la distance entre les sites de liaisons + proba
# probleme je ne m'interesse pas a la distance entre 2 faces mais entre les deux centres !!!!!
def attacher(listProt,grainDiameter,scaleFactor,tableauProba,associationProb):
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
                elem=tableauProba[0]
                tableauProba.remove(tableauProba[0])
                print("attacher ",len(tableauProba)," proba ",elem)
                if elem<=associationProb:
                    listProt[i].BiologicalGrain.associatedNeighbours.append(listProt[j])
                    listProt[j].BiologicalGrain.associatedNeighbours.append(listProt[i])



def sos(prot,listProt):
    boolSOS=True
    #for i in range(len(listProt)-1):
    list1=[prot.objectBl.location[0],prot.objectBl.location[1],prot.objectBl.location[2]]
    for j in range(0,len(listProt)):
        list2=[listProt[j].objectBl.location[0],listProt[j].objectBl.location[1],listProt[j].objectBl.location[2]]
        if (prot!=listProt[j] and list1==list2):#si meme proteine et meme coordonnees alors pb
            print("protein sup",prot.objectBl.name,listProt[j].objectBl.name)
            boolSOS=False
    return boolSOS


# determiner les coord de chaque molecules en fonction de chaque frame
def mouvementProt(listProt,envSize,scaleFactor,grainDiameter,nbRunPerFrame,nbRun,tableauProba,associationProb):
    debug=false
    frame_num =nbRunPerFrame#numero de la frame (pour le temps)
    for position in range(nbRun):
        attacher(listProt,grainDiameter,scaleFactor,tableauProba,associationProb)
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
                    deplacePosition(prot, x, y, z, scaleFactor,envSize)
                    if debug :
                        boolSos=sos(prot,listProt)
                        if not boolSos :
                            print("indicefail",len(indiceList),cpteur,x,y,z)
                            print(sphereCoor)
                            print(listCoord)
                            print(listCoord2)
                            print(prot.objectBl.location[0],prot.objectBl.location[1],prot.objectBl.location[2])
                    if len(prot.BiologicalGrain.associatedNeighbours)!=0:
                        test(prot, x, y, z, scaleFactor,envSize)
                    indiceList.pop(i)
        for prot in listProt:
            prot.moved=False
        frame_num+=nbRunPerFrame


def indice(listProt):
    #indiceList=[]
    #for i in range(len(listProt)):
    #    indiceList.append(i)
    return range(len(listProt))

# deplacer toutes les proteines attachees
def test(prot, x, y, z, scaleFactor,envSize):
    for assoProt in prot.BiologicalGrain.associatedNeighbours:
        if assoProt.moved==False:
            deplacePosition(assoProt, x, y, z, scaleFactor,envSize)
            test(assoProt, x, y, z, scaleFactor,envSize)


# l'environnement est considere comme infini (TOR)
def deplacePosition(prot, x, y, z, scaleFactor,envSize):
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

def findBindingSitesForBinding(prot1, prot2):
    #prot 1 et 2 sont des grains simules
    #1 -on prend le milieu des deux centres
    coordProt1=prot1.objectBl.location
    coordProt2=prot2.objectBl.location
    coordMilieu=[0,0,0]
    for i in range(3) :
        coordMilieu[i]=(coordProt1[i]+coordProt2[i])/2.0
    #2-pour chaque prot on cherche le site actif le plus proche du milieu et ses voisins
    for i in range(2):
        currentProt=prot1
        if i=1 :
            currentProt=prot2
        currentBindingSites=[] #a modif
        currentDist=[]
        for bindingSite in currentBindingSites:
            currentDist=getDistance(bindingSite.coord,coordMilieu)#a modif?
    #a continuer

#distance euclidienne dans un espace a n dimension
def getDistance(listCoord1, listCoord2):
    squareSum = 0
    for i in range(len(listCoord1)):
        currentCoord=listCoord1[i]-listCoord2[i]
        squareSum+=currentCoord*currentCoord
    return math.sqrt(squareSum)


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

def main(tableauParam):
    # reccup des param dans le popup
    grainDiameter,envSize,nbProt,associationProb,nbRunPerFrame,nbRun,sizeActiveSite,nbActivesSites,scaleFactor=tableauParam
    grainDiameter=float(grainDiameter)
    envSize=float(envSize)
    nbProt=int(nbProt)
    associationProb=float(associationProb)
    nbRunPerFrame=int(nbRunPerFrame)
    nbRun=int(nbRun)
    sizeActiveSite=int(sizeActiveSite)
    nbActivesSites=int(nbActivesSites)
    scaleFactor=int(scaleFactor)
    # creation d'un tableau de proba d'asso sans tenir compte de la valeur
    tableauProba=tableauProbaAsso(nbProt,nbRun)
    #initialisation des spheres
    bpy.context.scene.frame_set(0)
    listProt=initProteine(envSize,nbProt,scaleFactor,grainDiameter,associationProb,sizeActiveSite,nbActivesSites)
    #deplacement des proteines
    mouvementProt(listProt,envSize,scaleFactor,grainDiameter,nbRunPerFrame,nbRun,tableauProba,associationProb)
##############################################################################################



#prog principal
#bpy.ops.object.mode_set(mode='OBJECT')
clean()

#popup + main
bpy.utils.register_class(DialogOperator)
bpy.ops.object.dialog_operator('INVOKE_DEFAULT')
