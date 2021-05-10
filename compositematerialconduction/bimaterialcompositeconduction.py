#%%
import time                         # Package for runtime estimation.
import numpy as np                  # Package for mathematical operations.
from matplotlib import pyplot, cm   # Package for plotting simulation results.

time1 = time.perf_counter()         # Start the timer for the program execution.

#######################
# Geometry Definition #
#######################

L1 = 0.5                            # Length of element, in meters.
L2 = 0.5

##################
# Discretization #
##################

dx = 0.0005                           # Size of discretization step, in meters.
nx1 = int(L1 / dx) + 1              # Total number of points in the x-direction, unitless. Add one point as there are
nx2 = int(L2 / dx) + 1              # Total number of points in the x-direction, unitless. Add one point as there are
x1 = np.linspace(0,L1,nx1)          # Creation of the x vector for plotting purposes. It is composed of linearly spaced points.
x2 = np.linspace(0,L2,nx1) + L1          # Creation of the x vector for plotting purposes. It is composed of linearly spaced points.

t_sim = 301                        # Total physical time to simulate, in seconds.
dt = 0.001                          # Time discretization, in seconds.
nt = int(t_sim/dt)                  # Total number of timesteps, unitless. Use int to avoid Python breaking.

#######################
# Material Properties #
#######################

rho1 = 8050                         # Material density, in kilograms per meter cubed. Use 8050 for steel, 8940 for copper.
cp1 = 500                           # Material specific heat capacity, in joules per kilogram kelvin. Use 500 for steel, 385 for copper.
k1 = 14.4                            # Material thermal conductivity, in watts per meter kelvin. Use 14.4 for steel, 385 for copper.

rho2 = 8940                         # Material density, in kilograms per meter cubed. Use 8050 for steel, 8940 for copper.
cp2 = 385                           # Material specific heat capacity, in joules per kilogram kelvin. Use 500 for steel, 385 for copper.
k2 = 385                            # Material thermal conductivity, in watts per meter kelvin. Use 14.4 for steel, 385 for copper.

##############################################
# Initial Conditions and Array Initalization #
##############################################

T_A = 303.15                        # Set the initial condition temperature to 303.15 Kelvin.
T1 = np.ones(nx1) * T_A             # Initalize the temperature array, and apply the initial condition.
T2 = np.ones(nx2) * T_A

###########################
# Simulation and Plotting #
###########################

for counter in range(1,nt):         # Use a counter variable to iterate through each time step.
    Tn1 = T1.copy()                   # Copy the temperature array from the previous time step to the current time step.
    Tn2 = T2.copy()                   # Copy the temperature array from the previous time step to the current time step.

    T1[1:-1] = Tn1[1:-1] + ((k1 * dt)/(rho1 * cp1))*((Tn1[2:] - 2 * Tn1[1:- 1] + Tn1[0:-2])/(dx ** 2)) 
    T2[1:-1] = Tn2[1:-1] + ((k2 * dt)/(rho2 * cp2))*((Tn2[2:] - 2 * Tn2[1:- 1] + Tn2[0:-2])/(dx ** 2)) 

    T1[0] = 273                     # Enforce constant temperature boundary condition at x = 0.
    T2[-1] = 323                    # Enforce constant temperature boundary condition at x = L1 + L2.
    
    T1[-1] = ((k1 * L1 * T1[-2]) + (k2 * L2 * T2[1])) / ((k2 * L1) + (k1 * L2))
    T2[0] = ((k1 * L1 * T1[-2]) + (k2 * L2 * T2[1])) / ((k2 * L1) + (k1 * L2))                 # Enforce boundary condition at interface.    

    if (counter%100 == 0):
        ####################
        # Plotting Figures #
        ####################

        fig = pyplot.figure(figsize=(11, 7), dpi=100)                               # Create a new figure.
        ax = pyplot.gca                                                             # Get figure axes.
        pyplot.plot(x1,T1,x2,T2)                                                            # Plot the temperature array at the current time step.
        fig.suptitle('Temperature distribution at t = '+ str(int(counter/(1/dt))) + ' s.')      # Apply titles, labels, then save the figure.
        pyplot.xlabel('Distance [m]')
        pyplot.xlim([0, (L1 + L2)])                                          
        pyplot.ylabel('Temperature [K]')
        pyplot.ylim([270, 325])
        pyplot.grid(linestyle = '--', linewidth = 0.5)
        pyplot.savefig('figures/figure'+str(int(counter/(1/dt)))+'.png', dpi=100, transparent=False, facecolor='#ffffff', bbox_inches='tight', pad_inches=0.25)

    ####################
    # Progress Counter #
    ####################

    if (round((counter / nt) * 100,8) % 10 == 0) :                             # If the step number represents a percentage that is a multiple of 5%, enter the if statement.
            print('Progress: ' + str(round((counter/nt)*100,2)) + '%')  # Print the current percentage of time step progress (represented by the counter).

# fig = pyplot.figure(figsize=(11, 7), dpi=100)                               # Create a new figure.
# ax = pyplot.gca                                                             # Get figure axes.
# pyplot.plot(x1,T1,x2,T2)                                                            # Plot the temperature array at the current time step.
# fig.suptitle('Temperature distribution at t = '+ str(int(counter/(1/dt))) + ' s.')      # Apply titles, labels, then save the figure.
# pyplot.xlabel('Distance [m]')
# pyplot.xlim([0, (L1 + L2)])                                          
# pyplot.ylabel('Temperature [K]')
# pyplot.ylim([270, 325])
# pyplot.grid(linestyle = '--', linewidth = 0.5)
time2 = time.perf_counter()                                                                         # Stop the timer for the program execution.
print('Total execution time for '+str(nt)+' time steps: '+str(round((time2-time1),3))+' seconds.')  # Print the runtime for the program execution.
# %%