#%%
import time                         # Package for runtime estimation.
import numpy as np                  # Package for mathematical operations.
from matplotlib import pyplot, cm   # Package for plotting simulation results.

time1 = time.perf_counter()         # Start the timer for the program execution.

#######################
# Geometry Definition #
#######################

L = 1                               # Length of element, in meters.

##################
# Discretization #
##################

dx = 0.01                           # Size of discretization step, in meters.
nx = int(L/dx) + 1                  # Total number of points in the x-direction, unitless. Add one point as there are
                                    # (n+1) points for n elements. Use int to avoid Python breaking.
x = np.linspace(0,L,nx)             # Creation of the x vector for plotting purposes. It is composed of linearly spaced points.

t_sim = 150                         # Total physical time to simulate, in seconds.
dt = 0.5                            # Time discretization, in seconds.
nt = int(t_sim/dt)                  # Total number of timesteps, unitless. Use int to avoid Python breaking.

#######################
# Material Properties #
#######################

rho = 8050                          # Material density, in kilograms per meter cubed.
cp = 500                            # Material specific heat capacity, in joules per kilogram kelvin.
k = 14.4                              # Material thermal conductivity, in watts per meter kelvin.

##############################################
# Initial Conditions and Array Initalization #
##############################################

T_A = 303.15                        # Set the initial condition temperature to 303.15 Kelvin.
T = np.ones(nx) * T_A               # Initalize the temperature array, and apply the initial condition.

###########################
# Simulation and Plotting #
###########################

for counter in range(1,nt):         # Use a counter variable to iterate through each time step.
    Tn = T.copy()                   # Copy the temperature array from the previous time step to the current time step.
    T[1:-1] = Tn[1:-1] + ((k * dt)/(rho * cp))*((Tn[2:] - 2 * Tn[1:- 1] + Tn[0:-2])/(dx ** 2)) 

    T[0] = 293.15                   # Enforce constant temperature boundary condition at x = 0.
    T[-1] = T[-2]                   # Enforce zero gradient boundary condition at x = L.

    ####################
    # Plotting Figures #
    ####################

    fig = pyplot.figure(figsize=(11, 7), dpi=100)                               # Create a new figure.
    ax = pyplot.gca                                                             # Get figure axes.
    pyplot.plot(x,T)                                                            # Plot the temperature array at the current time step.
    fig.suptitle('Temperature distribution at t = '+ str(counter) + ' s.')      # Apply titles, labels, then save the figure.
    pyplot.xlabel('Distance [m]')                                               
    pyplot.ylabel('Temperature [K]')
    pyplot.savefig('figures/figure'+str(counter)+'.png', dpi=150, transparent=False, facecolor='#ffffff', bbox_inches='tight', pad_inches=0.25)

    ####################
    # Progress Counter #
    ####################

    if (round((counter/nt)*100,2)%5 == 0) :                             # If the step number represents a percentage that is a multiple of 5%, enter the if statement.
            print('Progress: ' + str(round((counter/nt)*100,2)) + '%')  # Print the current percentage of time step progress (represented by the counter).

time2 = time.perf_counter()                                                                         # Stop the timer for the program execution.
print('Total execution time for '+str(nt)+' time steps: '+str(round((time2-time1),3))+' seconds.')  # Print the runtime for the program execution.
# %%