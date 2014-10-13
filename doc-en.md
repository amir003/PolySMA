PolySMA : Modeling of proteins and theirs self-binding in a 3D environment
=====================================================================================

Introduction
------------

This software is done for IGEM 2014 and more precisely for the project Elasticoli. This project aims to artificially produce elastic proteins by the bacterium Escherichia coli. These elastic proteins, also called ELP (stands for Elastine Like Protein), are able to binding to each other and may form aggregates (and even strings in particular conditions).

PolySMA aims to better understand how this proteins bind to each other. Indeed, the software will model this proteins and their interaction in a 3D environment.

Analysis
--------

In this case, we only want modelize one protein type. The software need to model several proteins in a 3D environment, then these proteins will be moved and  possibly binding to each other.

**Proteins modeling**

To easily model a protein, it could be represented by a spherical form when she is alone (no-binding with other proteins). In laboratory, it was observed that, after binding, the resultant aggregate has a volume lower than the initial volumes of each element sum together. Indeed, the volume of a 100 proteins aggregates makes about 1,5 times the one of the isolated protein. So, the initial spherical form of the protein could changed according to the bindings number and will takes a smaller volume when binds.

**Bindings and move rules**

To know if proteins bind each other, we need to take in consideration several elements. Firstly the meeting probability, to consider it the software need to simulate protein movements in a 3D space (that can be a cell for example). However, the information that a protein has been at the location A and then in B is not sufficient, we also need to know where it will be between this two points because it will not move in a straight line.

To consider this meeting probability, we choose to move proteins by small movements. Each movement is randomly generated and is smaller (or equal) the protein size, so we have all the information that we need.

If two proteins are close enough, the software must decide if they are binding together. Given the binding reaction occurs with a certain probability, we need to include an association probability. If the binding doesn't occur, the proteins will repulse each other (attraction-repulsion phenomena).

The temperature could be modified in the simulated model. Temperature effect is to increase the binding reaction by an increase of the meeting probability. Indeed, this probability is mdoified by the thermic agitation. So, it can be model by an increase of the protein speed and so an increase of the distance traveled for the same time step.

Finally, when a protein is moved, we need to decide what happens when it goes to an edge of the simulated environement.

**State of the art of 3D modeling softwares**
