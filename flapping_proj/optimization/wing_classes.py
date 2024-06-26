from optimization.inertial_properties import *
import numpy as np
#wing with a trailing edge shaped like a bezier curve.
#there is the leading edge, a hinge bar, and trailing edge connected by a film 

class BezierWing():
    y0 = None
    z0 = None
    y1 = None
    z1 = None
    y2 = None
    z2 = None
    y3 = None
    z3 = None

    D_LE = 0.001 #m
    D_TE = 0.001 #m
    D_H  = 0.00025 #m

    #1d array of [Ixx, Iyy, Izz, Ixy, Ixz, Iyz]
    I = None

    #Wing mass
    m = None
    
    def y(self, t):
        return (1 - t)**3 * self.y0 + 3*(1 - t)**2 * t * self.y1 + 3*(1 - t) * t**2 * self.y2 + t**3  * self.y3
    
    def z(self, t):
        return (1 - t)**3 * self.z0 + 3*(1 - t)**2 * t * self.z1 + 3*(1 - t) * t**2 * self.z2 + t**3  * self.z3
    
    def dy(self, t):
        return 3 * (1 - t)**2 * (self.y1 - self.y0) + 6 * (1 - t) * t * (self.y2 - self.y1) + 3 * t**2 * (self.y3 - self.y2)
    
    def dz(self, t):
        return 3 * (1 - t)**2 * (self.z1 - self.z0) + 6 * (1 - t) * t * (self.z2 - self.z1) + 3 * t**2 * (self.z3 - self.z2)
    
    def __init__(self, y_0, z_0, y_1, z_1, y_2, z_2, y_3, z_3):
        self.y0 = y_0
        self.z0 = z_0
        self.y1 = y_1
        self.z1 = z_1
        self.y2 = y_2
        self.z2 = z_2
        self.y3 = y_3
        self.z3 = z_3

        self.m = bez_wing_mass(self, d_le = self.D_LE, d_h = self.D_H, d_te = self.D_TE)

        self.I = bez_wing_I(self, self.m, d_le = self.D_LE, d_h = self.D_H, d_te = self.D_TE)
        

#Inertial Return: 1d array of [Ixx, Iyy, Izz, Ixy, Ixz, Iyz]
class TriWing():
    #diagram in ./assets/triangular_wing_diagram.png
    def __init__(self, y0, z0, y1, z1, y2, z2):
        self.y0 = y0 #coords
        self.z0 = z0
        self.y1 = y1
        self.z1 = z1
        self.y2 = y2
        self.z2 = z2
        self.leading_edge_rod_diameter = 0.001 #m leading edge carbon fiber rod diameter
        self.spar_rod_diameter = 0.0005 #m Spar carbon fiber rod diameter
        self.trailing_edge_rod_diameter = 0.0005 #m trailing edge carbon fiber rod diameter
        
        #Mass of leading edge, trailing edge, spar, and mass of plastic film
        self.mass = line_m(y0, 0, y2, 0, self.leading_edge_rod_diameter) + line_m(y0, z0, y1, z1, diameter=self.trailing_edge_rod_diameter) + line_m(y1, z0, y1, z1, self.spar_rod_diameter) + film_m(self)
        
        #center of mass each component * mass of component / overall mass = COM coordinates
        self.com = (line_com(y0, 0, y2, 0, self.leading_edge_rod_diameter) + line_com(y0, z0, y1, z1, self.trailing_edge_rod_diameter) + line_com(y1, z0, y1, z1, self.spar_rod_diameter) + film_com(self)) / self.mass
        com_magnitude_sqr = self.com[0]**2 + self.com[1]**2

        self.I_origin = line_I(y0, 0, y2, 0, self.leading_edge_rod_diameter) + line_I(y0, z0, y1, z1, self.trailing_edge_rod_diameter) + line_I(y1, z0, y1, z1, self.spar_rod_diameter) + film_I(self)
        #1d array of [Ixx, Iyy, Izz, Ixy, Ixz, Iyz]
        self.I = self.I_origin - self.mass * np.array([com_magnitude_sqr, com_magnitude_sqr - self.com[0]**2, com_magnitude_sqr - self.com[1]**2, 0, 0, -self.com[0] * self.com[1]])


    #Coordinates along wing given parametric value t
    def y(self, t):
        t_adj = np.heaviside(t - .5, .5)
        return ((self.y1 - self.y0) * 2*t + self.y0) * (1 - t_adj) + t_adj * ((self.y2 - self.y1) * (2*t - 1) + self.y1)
    
    def z(self, t):
        t_adj = np.heaviside(t - .5, .5)
        return ((self.z1 - self.z0) * 2*t + self.z0) * (1 - t_adj) + t_adj * ((self.z2 - self.z1) * (2*t - 1) + self.z1)
        
    def dy(self, t):
        t_adj = np.heaviside(t - .5, .5)
        return (self.y1 - self.y0) * (1 - t_adj) + t_adj * (self.y2 - self.y1)
    
    def dz(self, t):
        t_adj = np.heaviside(t - .5, .5)
        return (self.z1 - self.z0) * (1 - t_adj) + t_adj * (self.z2 - self.z1)
        

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    tri_wing = TriWing(0.001, -0.001, .05, -.025, .1, -.00025)
    # mass1 = film_m(tri_wing)
    # print(film_com(tri_wing) / mass1)

    # t = np.linspace(0, 1)
    # plt.plot(tri_wing.dy(t), tri_wing.dz(t), marker = "o")
    
    print(tri_wing.I)
    print(tri_wing.I[0] + tri_wing.I[1] - tri_wing.I[2])
    print(tri_wing.I[0] + tri_wing.I[2] - tri_wing.I[1])
    print(tri_wing.I[2] + tri_wing.I[1] - tri_wing.I[0])
