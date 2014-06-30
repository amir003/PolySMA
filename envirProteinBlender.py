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
    print("nombre de proteine dans l'environnement")
    nbProt=50
    return envSize,nbProt


def initProteine(envSize,nbProt,scaleFactor):
    listProt=[]
    for i in range(0,nbProt,1):
        caseEmpty=False
        while !caseEmpty:
            x=random.randint(1,envSize)
            x=float(x)/scaleFactor
            y=random.randint(1,envSize)
            y=float(y)/scaleFactor
            z=random.randint(1,envSize)
            z=float(z)/scaleFactor
            listCoord=[x,y,z]
            caseEmpty=caseIsEmpty(listProt,listCoord)
            if caseEmpty:
                drawProt()
    return listProt

def drawProt(listProt,listCoord,scaleFactor):
    i=len(listProt)
    #creation d'une sphere
    nameS="Sphere"+str(i)
    currentSphere=bpy.ops.mesh.primitive_uv_sphere_add(segments=16, size=0.5/scaleFactor, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    bpy.context.object.name = nameS
    #creation des poles:
    currentProt=[]
    listObjOfCurrentProt=poleProteine(obj,nameS)
    currentProt.append(listObjOfCurrentProt)
    currentProt.append(listCoord)
    #appli d'une rotation aleatoire
    a,b,c=angleRotation()
    for i in range(2):
        currentPole=listObjOfCurrentProt[i]
        cuyrrentPole.select=True
        bpy.ops.transform.rotate(axis=(a, b, c))

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
        if listTest==listCoord:
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
        

def colorMat():
    # Create two materials
    red = makeMaterial('Red', (1,0,0), (1,1,1), 1)
    blue = makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
 
    # Create red cube
    bpy.ops.mesh.primitive_cube_add(location=origin) #creer un cube a l'origine
    setMaterial(bpy.context.object, red)
    # and blue sphere
    bpy.ops.mesh.primitive_uv_sphere_add(location=origin) #creer une sphere a l'origine
    bpy.ops.transform.translate(value=(1,0,0))
    setMaterial(bpy.context.object, blue)

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

def attacher():
    print("coucou")

def mouvementProt(envSize):
    envSize=envSize/10
    frame_num =0
    for position in range(0,20,1):
        x=random.randint(-1,1)
        x=x/10
        y=random.randint(-1,1)
        y=y/10
        z=random.randint(-1,1)
        z=z/10
        print("x",x,"y",y,"z",z)
        bpy.context.scene.frame_set(frame_num)
        for prot in bpy.data.objects:
            
            bool=voisin(prot.location[0]+x,prot.location[1]+y,prot.location[2]+z)
            
            prot.location[0]=prot.location[0]+x
            prot.location[1]=prot.location[1]+y
            prot.location[2]=prot.location[2]+z
            if prot.location[0]<1:
                prot.location[0]=envSize
            if prot.location[1]<1:
                prot.location[1]=envSize
            if prot.location[2]<1:
                prot.location[2]=envSize
            if prot.location[0]>envSize:
                prot.location[0]=1
            if prot.location[1]>envSize:
                prot.location[1]=1
            if prot.location[2]>envSize:
                prot.location[2]=1
            prot.keyframe_insert(data_path="location", index=-1)
        frame_num+=10
       
def clean():
    # remove mesh Cube and Sphere before new run
    for i in bpy.data.objects:
        if re.match(r'.*Sphere.*',i.name,re.M|re.I):
            obj=bpy.data.objects[i.name]
            obj.select=True
            bpy.ops.object.delete(use_global=False)
        if re.match(r'.*Cube.*',i.name,re.M|re.I):
            obj=bpy.data.objects[i.name]
            obj.select=True
            bpy.ops.object.delete(use_global=False)

#prog principal
print(bpy.ops.object.mode)
bpy.ops.object.mode_set(mode='OBJECT')
clean()
scaleFactor=10
envSize,nbProt=choixEnviron()
listProt=initProteine(envSize,nbProt,scaleFactor)
mouvementProt(listProt,envSize)                                                                                                                                                                                                                                                                                 