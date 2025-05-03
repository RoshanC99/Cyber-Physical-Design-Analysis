import math 
#from math import sin, cos 
from scipy.optimize import minimize 

# given values from page 2 & 3
H_c = 480           # sensor height 480 in pixels, from resultion: 640(W) x 480 (H) 
v0 = H_c/2          # projection of the optical center in the image  240 


h_min = 0.40        # camera height with respect to ground bound 40 cm in m
h_max = 0.80        # camera height with respect to ground bound 80 cm in m    

theta_min = 0.0         # camera pitch angle 0 degree, camera pointed horizontal
theta_max = 0.5         # camera pitch angle in rad, around 30 degree downward tilt, upper bound 

Y_far = 60.0        # distant 60 m obstacle             
Y_near = 15.0       # nearby 15 m obstacle 
Z = 1.65            # nearby obstacle height in 165 cm in m


bundles = [           #f = focal length in mm  # t_u(pixel size) in mm
    {"name": "OV07962-E62A",    "f": 2.8,   "t_u": 0.006,   "price": 7191,     "unit": 1000},
    {"name": "OV07690-R202A",   "f": 2.8,   "t_u": 0.00175, "price": 4312,     "unit": 1000},
    {"name": "OVM9724-RYDA-ND", "f": 1.66,  "t_u": 0.0014,  "price": 12718,    "unit": 2500}
]


results = []  # results list 

for bundle in bundles:
    f = bundle["f"]
    t_u = bundle["t_u"]
    α = f/t_u   

    # utilizing projection function based on the equation in the paper "Multi Domain optimization with SysML modeling"
    def v_projection(Y, Z, h, theta): 
        numerator = α * (Y * math.sin(theta) + (Z - h) * math.cos(theta)) 
        denominator =    Y * math.cos(theta) - (Z - h) * math.sin(theta)
        return v0 + (numerator / denominator)
 
    # target function maximize v for near obstacle 
    def target(var):
        h, theta = var # decision variables are camera height and pitch 
        return -v_projection(Y_near, Z, h, theta)  # minimize v, return negative for v_near in order to maximize v   ("maximize v for near obstacle..")

    def constraint_far(var):
        h, theta = var 
        return v_projection(Y_far, Z, h, theta) - 350.0 # 𝑣(60m, Z) >= 350 pixels for distant (60m) obstacle detection, ensure top of 165 cm obstacle at 60 m  is at or below 350

    def constraint_near(var):
        h, theta = var
        return 460.0 - v_projection(Y_near, Z, h, theta) # 𝑣(15m, Z) <= 460 pixels for nearby (15m) obstacle detection, 165 cm at 15 m isn't below 460 


    # constraint for SLSQP method           # https://docs.scipy.org/doc/scipy/tutorial/optimize.html#id16
    constraint = [{'type': 'ineq', 'fun': constraint_far},      # v_far > = 350
                  {'type': 'ineq', 'fun': constraint_near}]     # v_near < = 460
    
    # intial guess for height in meters and tilt in rad [h, theta] within bounds   https://www2.hawaii.edu/~jonghyun/classes/S18/CEE696/files/04_scipy_optimize.pdf
    x0 = [0.75, 0.4]   #  *tweaked couple of times*

    # optimization solver using SLSQP method
    result = minimize(target, x0, bounds=[(h_min, h_max), (theta_min, theta_max)],
                       constraints=constraint, method='SLSQP')

    
    # extract the results # https://www2.hawaii.edu/~jonghyun/classes/S18/CEE696/files/04_scipy_optimize.pdf , https://docs.scipy.org/doc/scipy/tutorial/optimize.html#id16
    h_optimal, theta_optimal = result.x   
    v_near_optimal = v_projection(Y_near, Z, h_optimal, theta_optimal)
    v_far_optimal = v_projection(Y_far, Z, h_optimal, theta_optimal)
    

    unit_price = bundle["price"] / bundle["unit"]
    cost_per_car = 2 * unit_price


    results.append({
        "name": bundle["name"],
        "alpha_px": α, 
        "h_optimal": h_optimal, 
        "theta_optimal": theta_optimal,
        "v_near": v_near_optimal, 
        "v_far": v_far_optimal,
        "cost_per_car": cost_per_car,
        #"t_u": t_u
        "price": bundle["price"],
        "unit": bundle["unit"]
    })


## For Question 1  

print("Question 1 (OV07962-E62A module) ")
print(f"optimal v: {results[0]['v_near']:.3f} pixels")
print(f"camera height: {results[0]['h_optimal']:.4f} m")
print(f"camera pitch: {results[0]['theta_optimal']:.4f} radians ({results[0]['theta_optimal'] * 180/math.pi:.2f} degrees)")
print(f"distant obstacle check: {results[0]['v_far']:.3f} pixels >= 350")
print(f"optimization success? : {result.success}")
print(f"message: {result.message}")


print(f"\n")
print(f"\n")

## For Question 2 bundles

# results for each bundle
print("Question 2 (OV07962-E62A module & OV07690-R202A & OVM9724-RYDA-ND modules)")
for r in results:
    print(f"camera: {r['name']}")
    print(f"α = {r['alpha_px']:.1f} pixels")
    print(f"optimal h = {r['h_optimal']:.4f} m, theta = {r['theta_optimal']:.4f} rad ({r['theta_optimal'] * 180/math.pi:.2f} degree)")
    print(f"v_near = {r['v_near']:.3f} pixels, v_far = {r['v_far']:.3f} pixels")
    print(f" cost per car = ${r['cost_per_car']:.2f}")
    print(f"\n")

print("Question 2 (cost analysis for the modules)")
for r in results:
    print(f"camera: {r['name']}")
    print(f"unit price: ${r['price'] / r['unit']:.3f} per module")
    print(f"cost per car (2 modules): ${r['cost_per_car']:.2f}")
    print(f"v_near = {r['v_near']:.3f} pixels")
    print(f"v_far = {r['v_far']:.3f} pixels")
    print(f"\n")
