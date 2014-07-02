#import blender
import bpy
import random
import math
import re
import bmesh
from bpy import context as C

def choixEnviron():
    print("Taille de l'environnement")
    envSize=50
    print("nombre de proteine dans l'environnement : concentration")
    nbProt=200
    print("rayon de la proteine")
    
    return envSize,nbProt


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
            #print("init x",x,"y",y,"z",z)
            listCoord=[x,y,z]
            caseEmpty=caseIsEmpty(listProt,listCoord)
            if caseEmpty:
                #print(listCoord)
                drawProt(listProt,listCoord,scaleFactor,grainDiameter)
    return listProt

def drawProt(listProt,listCoord,scaleFactor,grainDiameter):
    #print("i",i)
    x,y,z=listCoord
    #creation d'une sphere
    nameS="Sphere"+str(len(listProt))
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, size=grainDiameter/(scaleFactor*2), view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nameS
    obj=bpy.data.objects[nameS]
    ix=obj.location[0]
    iy=obj.location[1]
    iz=obj.location[2]
    print(nameS," x",ix,"y",iy,"z",iz)
    print("liste",listCoord)
    print("\n")
    #creation des poles:
    currentProt=[]
    listObjOfCurrentProt=poleProteine(nameS)
    currentProt.append(listObjOfCurrentProt)
    currentProt.append(listCoord)
    #appli d'une rotation aleatoire
    a,b,c=angleRotation()
    for i in range(2):
        currentPole=listObjOfCurrentProt[i]
        currentPole.select=True
        bpy.ops.transform.rotate(axis=(a, b, c))
    listProt.append(currentProt)

def angleRotation():
    a=random.randint(-360,360)
    a=a*(math.pi/180)
    b=random.randint(-360,360)
    b=b*(math.pi/180)
    c=random.randint(-360,360)
    c=c*(math.pi/180)
    return a,b,c

def caseIsEmpty(listProt,listCoord):
    for protToCheck in listProt:
        listCoordToCheck=protToCheck[1]
        #print("Coor a tester ",listCoord," coord deja existante ",listCoordToCheck)
        if listCoordToCheck==listCoord:
            #print("Danger")
            return False
    return True
  
def poleProteine(objectName):
    sphere=bpy.data.objects[objectName]
    sphere.select=True
    #besoin de passer en "edit" mode
    bpy.ops.object.mode_set(mode='EDIT')
    #passage en structure de pointeurs 
    bm = bmesh.from_edit_mesh(C.object.data)
    edges = []

    #coupe en 2 parallele a l'axe des y
    for i in range(-10, 10, 2):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(-1,0,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

    #met a jour les pointeurs
    bmesh.update_edit_mesh(C.object.data)
    #separe en 2 objets
    bpy.ops.mesh.separate(type='LOOSE')
    #repasse en mode objet
    bpy.ops.object.mode_set(mode='OBJECT')
    #selection objet
    pole1=bpy.data.objects[objectName]
    pole1.select=True
    #colorie en vert
    green = makeMaterial('Green', (0,1,0), (1,1,1), 1)
    pole1.data.materials.append(green)
    #setMaterial(bpy.context.object, green)
    #selection du pole 2
    namePole2=objectName+'.001'
    pole2=bpy.data.objects[namePole2]
    pole2.select=True
    #colorie en bleu
    blue = makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
    pole2.data.materials.append(blue)
    pole1.keyframe_insert(data_path="location", index=-1)
    pole2.keyframe_insert(data_path="location", index=-1)
    #bpy.ops.object.join()#pour joindre les deux demi-spheres
    return [pole1,pole2]

def makeMaterial(name, diffuse, specular, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.diffuse_shader = 'LAMBERT' 
    mat.diffuse_intensity = 1.0 
    mat.specular_color = specular
    mat.specular_shader = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha = alpha
    mat.ambient = 1
    return mat
 
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)
        
def voisin(x,y,z):
    caseVide=1
    for obj in bpy.data.objects:
        #obj=bpy.data.objects[i]
        ix=obj.location[0]
        iy=obj.location[1]
        iz=obj.location[2]
        if (x==ix and y==iy and z==iz):
            caseVide=0
    return caseVide

def attacher(listProt,grainDiameter,scaleFactor):
    #trouver les spheres attachées
    portLiees={}
    distance=grainDiameter/scaleFactor
    for i in range(len(listProt)-1):
        #print(len(listProt))
        #print("coucou")
        x1=listProt[i][1][0]
        y1=listProt[i][1][1]
        z1=listProt[i][1][2]
        for j in range(i+1,len(listProt)):
            x2=listProt[j][1][0]
            y2=listProt[j][1][1]
            z2=listProt[j][1][2]
            dx=x1-x2
            dy=y1-y2
            dz=z1-z2
            if (dx <distance and dx >-distance) and (dy <distance and dy >-distance) and (dz <distance and dz >-distance):
                print ("proteine attachee !!!!!!!!!!!!!",dx,dy,dz)

def mouvementProt(listProt,envSize,scaleFactor,grainDiameter):
    envSize=envSize/scaleFactor
    frame_num =10#numero de la frame (pour le temps)
    for position in range(1):
        bpy.context.scene.frame_set(frame_num)
        x=random.randint(-grainDiameter,grainDiameter)
        x=x/scaleFactor
        y=random.randint(-grainDiameter,grainDiameter)
        y=y/scaleFactor
        z=random.randint(-grainDiameter,grainDiameter)
        z=z/scaleFactor
        #1print("x",x,"y",y,"z",z)
        for prot in listProt:
            objectsOfCurrentSphere = prot[0]
            coordOfCurrentSphere = prot[1]
            listCoord=[coordOfCurrentSphere[0]+x,coordOfCurrentSphere[1]+y,coordOfCurrentSphere[2]+z]
            moveIsPossible=caseIsEmpty(listProt,listCoord)
            deplacePosition(prot, x, y, z,scaleFactor)
            coordOfCurrentSphere =listCoord
        frame_num+=10

def deplacePosition(prot, x, y, z,scaleFactor):
    objectsOfCurrentSphere = prot[0]
    for i in range(2):
        currentPole=objectsOfCurrentSphere[i]
        currentPole.location[0]=currentPole.location[0]+x
        currentPole.location[1]=currentPole.location[1]+y
        currentPole.location[2]=currentPole.location[2]+z
        if currentPole.location[0]<0:
            currentPole.location[0]=envSize/scaleFactor
        if currentPole.location[1]<0:
            currentPole.location[1]=envSize/scaleFactor
        if currentPole.location[2]<0:
            currentPole.location[2]=envSize/scaleFactor
        if currentPole.location[0]>envSize/scaleFactor:
            currentPole.location[0]=0
        if currentPole.location[1]>envSize/scaleFactor:
            currentPole.location[1]=0
        if currentPole.location[2]>envSize/scaleFactor:
            currentPole.location[2]=0
        currentPole.keyframe_insert(data_path="location", index=-1)
   
def clean():
    # remove mesh Cube and Sphere before new run
    for i in bpy.data.objects:
        print(i.name)
        if re.match(r'.*Sphere.*',i.name,re.M|re.I):
            obj=bpy.data.objects[i.name]
            obj.select=True
            bpy.ops.object.delete(use_global=False)
        if re.match(r'.*Cube.*',i.name,re.M|re.I):
            obj=bpy.data.objects[i.name]
            obj.select=True
            bpy.ops.object.delete(use_global=False)

def clean2():
    for obj in bpy.data.objects:
        currentName=obj.name
        #print(currentName)
        if("Cube" in currentName or "Sphere" in currentName):
            obj.select=True
            bpy.ops.object.delete(use_global=False)
 
 
#classe grain biologique
class biologicalGrain:
    def __init__(self, coordinates,listOfNeighbours,associationProbability ):
        self.x, slef.y, self.z = coordinates
        self.associationProb = associationProbability
        self.associatedNeighbours = listOfNeighbours
        
#classe grain biologique
class simulatedGrain:
    def __init__(self, bGrain,activesFace):
        self.biologicalGrain = bGrain
        self.activesFaces =  activesFace      
        self.moved=False

#prog principal
#filename = "testEnvirProteinV4.py"
#exec(compile(open(filename).read(), filename, 'exec'))

#print(bpy.ops.object.mode)
bpy.ops.object.mode_set(mode='OBJECT')
#clean()
clean2()
scaleFactor = 10
grainDiameter = 2
envSize,nbProt=choixEnviron()
bpy.context.scene.frame_set(0)
listProt=initProteine(envSize,nbProt,scaleFactor,grainDiameter)
print(listProt)
mouvementProt(listProt,envSize,scaleFactor,grainDiameter)
#attacher(listProt,grainDiameter,scaleFactor) 
        
for i in range(len(listProt)-1):
    protCoord=listProt[i][1]
    x1=protCoord[0]
    y1=protCoord[1]
    z1=protCoord[2]
    for j in range(i+1,len(listProt)):
        protTest=listProt[j][1]
        x2=protTest[0]
        y2=protTest[1]
        z2=protTest[2]
        if x1==x2 and y1==y2 and z1==z2:
            print("danger !!!!!!!!!!!!")                                                                                                                                                                                                                                                                         