#import blender
import bpy
import random
import math
import re
import bmesh
from bpy import context as C


#print("coucou")
print(bpy.ops.object.mode)
bpy.ops.object.mode_set(mode='OBJECT')

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

#gerer ca en dehors de blender
#gros pb avec les redirections des sorties standards
#print ("taille de l'environnement")
#a=input()

#stocker dans une liste les coord
#verrifier que 2 coord sont bien differentes
#puis travailler sur les interactions
def choixEnviron():
    print("Taille de l'environnement")
    envSize=50
    print("nombre de proteine dans l'environnement")
    nbProt=50
    return envSize,nbProt


def initProteine(envSize,nbProt):
    dicoProt={}
    for i in range(0,nbProt,1):
        caseLibre=0
        while caseLibre==0:
            listCoord=[]
            x=random.randint(1,envSize)
            x=float(x)/10
            y=random.randint(1,envSize)
            y=float(y)/10
            z=random.randint(1,envSize)
            z=float(z)/10
            listCoord=[x,y,z]
            caseLibre=voisinInit(dicoProt,listCoord)
            if caseLibre==1:
                #creation d'une sphere
                nameS="Sphere"+str(i)
                dicoProt[nameS]=listCoord
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, size=0.05, view_align=False, enter_editmode=False, location=(x, y, z), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                bpy.context.object.name = nameS
                #creation des poles:
                obj=bpy.data.objects[nameS]
                obj.select=True
                poleProteine(obj,nameS)
                #appli d'une rotation aleatoire
                a,b,c=angleRotation()
                obj=bpy.data.objects[nameS]
                obj.select=True
                bpy.ops.transform.rotate(axis=(a, b, c))
    return dicoProt

def angleRotation():
    a=random.randint(-360,360)
    a=a*(math.pi/180)
    b=random.randint(-360,360)
    b=b*(math.pi/180)
    c=random.randint(-360,360)
    c=c*(math.pi/180)
    return a,b,c

def voisinInit(dicoProt,listCoord):
    caseLibre=1
    for key in dicoProt:
        listTest=dicoProt[key]
        if listTest==listCoord:
            caseLibre=0  
            break
    return caseLibre
  
def poleProteine(obj,name):
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(C.object.data)
    edges = []

    #coupe parallele a l'axe des y
    for i in range(-10, 10, 2):
        ret = bmesh.ops.bisect_plane(bm, geom=bm.verts[:]+bm.edges[:]+bm.faces[:], plane_co=(i,0,0), plane_no=(-1,0,0))
        bmesh.ops.split_edges(bm, edges=[e for e in ret['geom_cut'] if isinstance(e, bmesh.types.BMEdge)])

    bmesh.update_edit_mesh(C.object.data)
    
    bpy.ops.mesh.separate(type='LOOSE')
    
    bpy.ops.object.mode_set(mode='OBJECT')
    obj=bpy.data.objects[name]
    obj.select=True
    red = makeMaterial('Green', (0,1,0), (1,1,1), 1)
    setMaterial(bpy.context.object, red)
    
    nameS=name+'.001'
    #print(nameS)
    blue = makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
    obj=bpy.data.objects[nameS]
    obj.select=True
    me = obj.data
    #me.materials.append(red)
    me.materials.append(blue)
    #sme.materials.append(yellow)
    #blue = makeMaterial('BlueSemi', (0,0,1), (0.5,0.5,0), 0.5)
    #setMaterial(bpy.context.object, red)
    #bpy.ops.object.delete(use_global=False)
    bpy.ops.object.join()



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
        
    #positions = (0,0,2),(0,1,2),(3,2,1),(3,4,1),(1,2,1)
    
    #start_pos = (0,0,0)
    #bpy.ops.mesh.primitive_uv_sphere_add(segments=32, size=0.3, location=start_pos)
    #bpy.ops.object.shade_smooth()
    #obj=bpy.data.objects["Sphere1"]
    #obj.select=True
    
    #ob = bpy.context.active_object

    #frame_num = 0
 
#    for position in positions:
#        bpy.context.scene.frame_set(frame_num)
#        ob.location = position
#        ob.keyframe_insert(data_path="location", index=-1)
#        frame_num += 10

envSize,nbProt=choixEnviron()
dico=initProteine(envSize,nbProt)
mouvementProt(envSize)
                                                                                                                                                                                                                                                                                  