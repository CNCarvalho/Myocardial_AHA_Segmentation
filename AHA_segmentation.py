"""
By Catarina Carvalho
catarina.neves.carvalho@tecnico.ulisboa.pt

"""

#%% Imports
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

#%% Main class

class AHA_segmentation(object):
    def __init__(self, image_matrix, myocardial_mask, mode, vmax=None):
        # Initialize variables
        self.mode = mode
        if mode == 'basal' or mode == 'mid':
            self.n_segments = 6
        elif mode == 'apical':
            self.n_segments = 4
        else:
            sys.exit('Only "basal", "mid" and "apical" modes supported.')
            
        self.image = image_matrix
        self.mask = myocardial_mask
            
        self.max_dim = max(np.shape(self.image))
        self.center_point = [np.shape(self.image)[0]/2, np.shape(self.image)[1]/2]
        self.center_point_i = [np.shape(self.image)[0]/2, np.shape(self.image)[1]/2]
        self.angle_increment = 0
        
        # Start plotting figure
        self.fig, self.ax = plt.subplots(figsize=[15,10])
        self.fig.subplots_adjust(bottom=0.2)
        if vmax is None:
            self.ax.imshow(self.image, cmap='gray')
        else:
            self.ax.imshow(self.image, cmap='gray', vmax=vmax)
        
        ax_slider_rot = self.fig.add_axes([0.25, 0.05, 0.5, 0.03], facecolor='lightgoldenrodyellow')
        ax_slider_x = self.fig.add_axes([0.25, 0.10, 0.5, 0.03], facecolor='lightcyan')
        ax_slider_y = self.fig.add_axes([0.25, 0.15, 0.5, 0.03], facecolor='lavenderblush')

        xa1, xa2, xb1, xb2, xc1, xc2, ya1, ya2, yb1, yb2, yc1, yc2 = self.get_line_coordinates()
        self.a = self.ax.plot([xa1, xa2], [ya1, ya2], 'red')[0]
        self.b = self.ax.plot([xb1, xb2], [yb1, yb2], 'blue')[0]
        self.c = self.ax.plot([xc1, xc2], [yc1, yc2], 'green')[0]
        self.circle = self.ax.scatter(xa1, ya1, color='red', s=100)
        self.square = self.ax.scatter(xb2, yb2, color='blue', marker="s", s=100)
        

        self.slider_rot = Slider(ax_slider_rot, label='Rotation', valmin=-180, valmax=180, valinit=0, valstep=0.1, track_color='lavender', initcolor='black', color='mediumslateblue')
        self.slider_x = Slider(ax_slider_x, label='Translate y', valmin=-self.max_dim/2, valmax=self.max_dim/2, valinit=0, valstep=1, track_color='lightcyan', initcolor='black', color='lightseagreen')
        self.slider_y = Slider(ax_slider_y, label='Translate x', valmin=-self.max_dim/2, valmax=self.max_dim/2, valinit=0, valstep=1, track_color='lightgoldenrodyellow', initcolor='black', color='yellowgreen')

        
    def get_line_coordinates(self):
        
        angle = self.angle_increment
        if self.n_segments == 6:
            alphas = [0, 60, 120]
        elif self.n_segments == 4:
            alphas = [45, 135, 45]
            
        max_dim = self.max_dim/4
        center = self.center_point
        
        slopea = np.tan((alphas[0]+angle)*np.pi/180)
        slopeb = np.tan((alphas[1]+angle)*np.pi/180)
        slopec = np.tan((alphas[2]+angle)*np.pi/180)
        
        ya = max_dim/np.sqrt((1+slopea**2))
        xa = ya*slopea
        ya1 = center[1] - ya
        ya2 = center[1] + ya
        xa1 = center[0] - xa
        xa2 = center[0] + xa
        
        yb = max_dim/np.sqrt((1+slopeb**2))
        xb = yb*slopeb
        yb1 = center[1] - yb
        yb2 = center[1] + yb
        xb1 = center[0] - xb
        xb2 = center[0] + xb
        
        yc = max_dim/np.sqrt((1+slopec**2))
        xc = yc*slopec
        yc1 = center[1] - yc
        yc2 = center[1] + yc
        xc1 = center[0] - xc
        xc2 = center[0] + xc
        
        return ya1, ya2, yb1, yb2, yc1, yc2, xa1, xa2, xb1, xb2, xc1, xc2
    
    def get_line_y(self, x):
        angle = self.angle_increment
        if self.n_segments == 6:
            alphas = [0, 60, 120]
        center = [0,0]
        center[1] = np.shape(self.image)[0] - self.center_point[1]
        center[0] = self.center_point[0]
        
        slopea = np.tan((alphas[0]+angle)*np.pi/180)
        slopeb = np.tan((alphas[1]+angle)*np.pi/180)
        slopec = np.tan((alphas[2]+angle)*np.pi/180)
        
        ba = center[1]-slopea*center[0]
        bb = center[1]-slopeb*center[0]
        bc = center[1]-slopec*center[0]
        
        ya = slopea*x+ba
        yb = slopeb*x+bb
        yc = slopec*x+bc

        return ya, yb, yc
    
    def update_rot(self, val):
        # Pick angle increment from slider
        ind = self.slider_rot.val
        self.angle_increment = ind
        # Update line coordinates
        xa1, xa2, xb1, xb2, xc1, xc2, ya1, ya2, yb1, yb2, yc1, yc2 = self.get_line_coordinates()
        self.a.set_ydata([ya1, ya2])
        self.b.set_ydata([yb1, yb2])
        self.c.set_ydata([yc1, yc2])
        self.a.set_xdata([xa1, xa2])
        self.b.set_xdata([xb1, xb2])
        self.c.set_xdata([xc1, xc2])
        self.circle.set_offsets([xa1,ya1])
        self.square.set_offsets([xb2,yb2])
        
        
    def update_x(self, val):
        ind = self.slider_x.val
        self.center_point[0] = self.center_point_i[0] + ind
        xa1, xa2, xb1, xb2, xc1, xc2, ya1, ya2, yb1, yb2, yc1, yc2 = self.get_line_coordinates()
        self.a.set_ydata([ya1, ya2])
        self.b.set_ydata([yb1, yb2])
        self.c.set_ydata([yc1, yc2])
        self.a.set_xdata([xa1, xa2])
        self.b.set_xdata([xb1, xb2])
        self.c.set_xdata([xc1, xc2])
        self.circle.set_offsets([xa1,ya1])
        self.square.set_offsets([xb2,yb2])
        

    def update_y(self, val):
        ind = self.slider_y.val
        self.center_point[1] = self.center_point_i[1] + ind
        xa1, xa2, xb1, xb2, xc1, xc2, ya1, ya2, yb1, yb2, yc1, yc2 = self.get_line_coordinates()
        self.a.set_ydata([ya1, ya2])
        self.b.set_ydata([yb1, yb2])
        self.c.set_ydata([yc1, yc2])
        self.a.set_xdata([xa1, xa2])
        self.b.set_xdata([xb1, xb2])
        self.c.set_xdata([xc1, xc2])
        self.circle.set_offsets([xa1,ya1])
        self.square.set_offsets([xb2,yb2])
        
    # Main method
    def segment(self):
        self.slider_rot.on_changed(self.update_rot)
        self.slider_x.on_changed(self.update_x)
        self.slider_y.on_changed(self.update_y)
        plt.show()
        
    def save_segments(self):
        mask_ = np.zeros_like(self.image)

        for yy in range(np.shape(self.mask)[1]):
            for xx in range(np.shape(self.mask)[0]):
                
                if self.mask[xx,yy] !=0:
                
                    xa1, xa2, xb1, xb2, xc1, xc2, ya1, ya2, yb1, yb2, yc1, yc2 = self.get_line_coordinates()
                    
                    veca = (xa2-xa1, ya2-ya1)
                    vecb = (xb2-xb1, yb2-yb1)
                    dota = (xa2-yy, ya2-xx)
                    dotb = (xb2-yy, yb2-xx)
                    Pa = veca[0]*dota[1]-veca[1]*dota[0]
                    Pb = vecb[0]*dotb[1]-vecb[1]*dotb[0]
                    
                    if self.n_segments == 6:
                        if self.mode == 'basal':
                            mask_vals = [1, 2, 3, 4, 5, 6]
                        elif self.mode == 'mid':
                            mask_vals = [7, 8, 9, 10, 11, 12]
                        
                        vecc = (xc2-xc1, yc2-yc1)
                        dotc = (xc2-yy, yc2-xx)
                        Pc = vecc[0]*dotc[1]-vecc[1]*dotc[0]
                        
                        if Pb >= 0 and Pc >= 0:
                            mask_[xx,yy] = mask_vals[0]
                        elif Pa >= 0 and Pb <= 0:
                            mask_[xx,yy] = mask_vals[1]
                        elif Pc >= 0 and Pa <= 0:
                            mask_[xx,yy] = mask_vals[2]
                        elif Pc <= 0 and Pb <= 0:
                            mask_[xx,yy] = mask_vals[3]
                        elif Pb >= 0 and Pa <= 0:
                            mask_[xx,yy] = mask_vals[4]
                        elif Pa >= 0 and Pc <= 0:
                            mask_[xx,yy] = mask_vals[5]
                            
                            
                    elif self.n_segments == 4:
                        if Pb >= 0 and Pa >= 0:
                            mask_[xx,yy] = 13
                        elif Pa <= 0 and Pb >= 0:
                            mask_[xx,yy] = 14
                        elif Pb <= 0 and Pa <= 0:
                            mask_[xx,yy] = 15
                        elif Pa >= 0 and Pb <= 0:
                            mask_[xx,yy] = 16
        
        return mask_


