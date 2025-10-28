#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 11:08:58 2018

@author: cristini
"""

import gmsh
import csv
import numpy as np

gmsh.initialize()

gmsh.option.setNumber("General.Terminal", 1)
model = gmsh.model

# Choose factory
OCC = False

if OCC:
    factory = model.occ
else:
    factory = model.geo
#

# Initialize variables

xc = np.array([0,1500])
z0 = np.array([0,0])
z1 = np.array([40,40])
z2 = np.array([80,80])



#LC = longueur caractéristique

lc1 = 2     # eau
lc2 = 0.4          # sediment


#%%

pt_eau=[]
for ct in range(len(xc)):
    pt_eau.append(factory.addPoint(xc[ct], -z0[ct], 0., lc1)) #lcx = longueur carac du milieu de l'interface avec la + petite vitesse
    
pt_sed = []
for ct  in range(len(xc)):
    pt_sed.append(factory.addPoint(xc[ct], -z1[ct], 0., lc2)) #lcx = longueur carac du milieu de l'interface avec la + petite vitesse
    
pt_sed2=[]
for ct  in range(len(xc)):
    pt_sed2.append(factory.addPoint(xc[ct], -z2[ct], 0., lc2))


    
#%%
l_eau = factory.addSpline(pt_eau)  # l7
l_sed = factory.addSpline(pt_sed)  # l7
l_sed2 = factory.addSpline(pt_sed2)  # l7


H1, H2, L = -z1[0], -z1[-1], xc[-1]

H = -80

p1 = factory.addPoint(xc[0], 0., 0., lc1)
p2 = factory.addPoint(L,  0., 0., lc1)
p3 = factory.addPoint(L,  H,  .0, lc2)
p4 = factory.addPoint(xc[0], H,  .0, lc2)



l2 = factory.addLine(pt_eau[-1], pt_sed[-1])
l3 = factory.addLine(pt_sed[0], pt_eau[0])


l4 = factory.addLine(pt_sed[-1],  pt_sed2[-1])
l5 = factory.addLine(pt_sed2[0], pt_sed[0])



ll1  = factory.addCurveLoop([l_sed,-l2,-l_eau,-l3])
ll2  = factory.addCurveLoop([l_sed2,-l4,-l_sed,-l5])

eau  = factory.addPlaneSurface([ll1])
sed = factory.addPlaneSurface([ll2])


model.addPhysicalGroup(2, [eau], 1)
model.setPhysicalName(2, 1, 'M_1')

model.addPhysicalGroup(2, [sed], 2)
model.setPhysicalName(2, 2,'M_2')





#--------------------------------------------------------------
# Start Gmsh API
#gmsh.initialize('',False)

gmsh.option.setNumber("Geometry.MatchMeshTolerance", 1e-9)
gmsh.option.setNumber("Geometry.Tolerance", 1e-9)

gmsh.option.setNumber("Mesh.Algorithm", 8)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm",2)
#gmsh.option.setNumber("Mesh.SubdivisionAlgorithm",1)
gmsh.option.setNumber("Mesh.RecombineAll",1)
gmsh.option.setNumber("Mesh.Smoothing",40)
gmsh.option.setNumber("Mesh.MshFileVersion", 2.2)
gmsh.option.setNumber("Mesh.RecombineOptimizeTopology",5)
gmsh.option.setNumber("Mesh.CharacteristicLengthFactor",1)
#gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)

factory.synchronize()
# 1) Generate the 2D mesh
model.mesh.generate(2)

gmsh.option.setNumber("Mesh.QualityType", 0)   # 0 => Scaled Jacobian (typical)

# Create a quality post-processing view (colored by quality + histogram)
# (If your Gmsh has the MeshQuality plugin, this will create the view automatically.)
try:
    gmsh.plugin.setNumber("MeshQuality", "Dimension", 2)  # check 2D elements
    # If your build names the option differently, it will just ignore it.
    gmsh.plugin.setNumber("MeshQuality", "What", 0)       # match Mesh.QualityType above
    gmsh.plugin.run("MeshQuality")
except:
    # If plugin options differ in your version, the GUI's Tools>Statistics still works.
    pass


# (Optional) write mesh to file
gmsh.write("meshNya.msh")


gmsh.fltk.run()


gmsh.finalize()
