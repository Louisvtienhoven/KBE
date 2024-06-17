# KBE Group 24: Rotor Burst Analysis
This app is used to perform the Particular Risk Assessment of a rotor burst of a turbine engine.
The app is developed to comply with [EASA CS-25 AMC-20-128A](https://www.easa.europa.eu/en/document-library/easy-access-rules/online-publications/easy-access-rules-acceptable-means?page=23).
By analyzing the risk zone formed per rotor fragment under different orientations, one can determine if EWIS channels in
the aircraft run the risk of being hit. With this app, one can determine if a redundant fuselage channel is available 
for every single rotor burst event.

To perform the analysis, the file ```main.py``` has to be ran with parapy installed locally.

## Model setup
The app consists of 4 modules to model the aircraft: 

```assembly```
```engine```
```fuselage```
```wiring```

### Internal analysis
The app has an internal analysis module ```rotorburst_analysis``` which allows the user to visualize the risk zone
per engine (left/right), per engine stage (fan/compressor etc.) and per rotation direction of the engine (CW/CCW). By varying
the release angle of the rotor burst fragment, one can determine which channels are being hit.

### External analysis
The app has an external analysis module ```matlab_files``` which is called from the ```MainAssembly``` class in ```main.py```
The external analysis makes use of a matlab engine and is used to document the overview of the critical release angles per
engine stage. The overview is presented to the user as uitable and saved in .xlsx format.

## Initialising the app
To initialize the app for a predefined wiring structure, one has to define the wiring in the ```EWIS``` class in ```EWIS.py```
Next, in ```evaluate_risk_zones.py``` set the ```hidden=True``` of ```@Part threshold```in line 117. Now run ```main.py```
and look in the tree for the ```pra_rotor_burst``` part. This part has a sequence of parts in ```threshold```,
check how many children this sequence has. The number of children specifies the number of intersected shapes
of the wiring part itself. When the risk volume of a rotor fragment hits a channel, additional intersections are created.

The determine threshold needs to be updated and adjusted in the part ```intersection_threshold``` in line 50 of ```evaluate_risk_zones.py```.