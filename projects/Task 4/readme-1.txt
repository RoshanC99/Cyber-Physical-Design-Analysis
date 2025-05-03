About the script:
The script optimizes the SCSM config. 
It solves Question 1 (optimzing camera module OV07962-E62A) 
& Question 2 (comparing it with other two camera modules OV07690-R202A & OVM9724-RYDA-ND for cost-effectiveness)


Running the script:
- make sure you have python version 3.6 or above (This script was written in python verion 3.10.12 (default wsl ubuntu 22.04))
- make sure you have required libraries installed:
  pip install numpy scipy 

- download and save the script to preferred directory as optimization_script.py 
- run script using the following command in a terminal:
    python optimization_script.py    
    or
    python3 optimization_script.py 


Goals of the script:
- For Question 1, it finds optimal camera height (h) and pitch angle theta that maximizes the (v) line position for nearby obstacle
    using OV07962-E62A camera module 

- For Question 2, it repeats the optimization for 2 other camera modules including the one from Question 1 
    and determines which provides the best value based on constraint whether it's worth spending a dollar more only if 
    v can be improved by at least 2 pixels 


inputs of the script:
- 3 camera modules with their own specs (focal length, tu pixel size, price) 
- camera constraints (height and camera pitch angle theta bounds)
- obstacle positions for nearby at 15m, distant at 60m 
- detection constraints (v >= 350 pixels for distant obstacles, v<= 460 pixels for nearby obstacles)

- no user inputs required when script compiles 


output of the script:
- for Question 1:
    - optimal v value for camera moduel OV07962-E62A
    - optimal camera height and pitch angle 
    - determining if all constraints are met

- for Question 2: 
    - optimization results for all 3 camera bundles 
    - cost information for each camera module 