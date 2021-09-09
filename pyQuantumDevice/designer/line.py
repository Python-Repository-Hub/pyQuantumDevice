from typing import Iterable, List

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt
from copy import copy

class Line:
    def __init__(self, p1: NDArray[np.float_], p2: NDArray[np.float_]):
        self.p1 = p1
        self.p2 = p2
            
    def show(self, ax=None):
        raise NotImplementedError()

    def join(self, other):
        if type(self) != type(other):
            self.p2 = other.p2
        else:
            raise ValueError()
            
class HorizontalLine(Line):
    def __init__(self, p1: NDArray[np.float_], p2: NDArray[np.float_]):
        if p1[1] != p2[1]:
            raise ValueError("Given two point is now horizontally located.")
        super().__init__(p1, p2)
        
    def show(self, ax=None, figsize=None, color="k"):
        x_list = np.linspace(self.p1[0], self.p2[0], 2)
        y_list = np.linspace(self.p1[1], self.p2[1], 2)
        
        if not figsize:
            figsize = (10, 10)
        if ax:
            ax.plot(x_list, y_list, color)
        else:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplots(111)
            ax.plot(x_list, y_list, color)
            fig.show()
        return ax
    
    def __str__(self):
        return f"HorizontalLine[({self.p1[0]}, {self.p1[1]}) -> ({self.p2[0]}, {self.p2[1]})]"
    
class VerticalLine(Line):
    def __init__(self, p1: NDArray[np.float_], p2: NDArray[np.float_]):
        if p1[0] != p2[0]:
            raise ValueError("Given two point is now vertically located.")
        super().__init__(p1, p2)
        
    def show(self, ax=None, figsize=None, color="k"):
        x_list = np.linspace(self.p1[0], self.p2[0], 2)
        y_list = np.linspace(self.p1[1], self.p2[1], 2)
        
        if not figsize:
            figsize = (10, 10)
        if ax:
            ax.plot(x_list, y_list, color)
        else:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplots(111)
            ax.plot(x_list, y_list, color)
            fig.show()
        return ax
    def __str__(self):
        return f"VerticalLine[({self.p1[0]}, {self.p1[1]}) -> ({self.p2[0]}, {self.p2[1]})]"
    
    
class HalfCircle(Line):
    def __init__(self, p_center: NDArray[np.float_], p_start: NDArray[np.float_]):
        self.radius = abs(p_start[0] - p_center[0])
        self.center = p_center
        if p_start[0] < p_center[0]:
            self.theta_start = np.pi
            p_end = np.array([p_center[0] + self.radius, p_center[1]])
        else:
            self.theta_start = 0
            p_end = np.array([p_center[0] - self.radius, p_center[1]])
        
        super().__init__(p_start, p_end)
        
    def show(self, ax=None, figsize=None, color="k"):
        theta_list = np.linspace(self.theta_start, self.theta_start + np.pi, 100)
        x_list = self.center[0] + self.radius * np.cos(theta_list)
        y_list = self.center[1] + self.radius * np.sin(theta_list)
        
        if not figsize:
            figsize = (10, 10)
        if ax:
            ax.plot(x_list, y_list, color)
        else:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplots(111)
            ax.plot(x_list, y_list, color)
            fig.show()
        return ax
    
    def __str__(self):
        return f"ArcLine[center:({self.center[0]}, {self.center[1]}), ({self.p1[0]}, {self.p1[1]}) -> ({self.p2[0]}, {self.p2[1]})]"
    
class JoinedLine(Line):
    def __init__(self, line_list: List[Line]):
        super().__init__(line_list[0].p1, line_list[-1].p2)
        self.lines = []
        working_line = None
        for i, line in enumerate(line_list):
            if not working_line:
                working_line = line
                
            elif type(working_line) == type(line):
                if not np.all(np.isclose(working_line.p2, line.p1)):
                    raise ValueError("Discontinuous line list.")
                working_line.join(line)

            else:                
                if not np.all(np.isclose(working_line.p2, line.p1)):
                    raise ValueError("Discontinuous line list.")
                self.lines.append(working_line)
                working_line = line
                
        self.lines.append(working_line)
    
    def show(self, ax=None, figsize=None, color="k"):
        if not figsize:
            figsize = (15, 15)
            
        if ax:
            for line in self.lines:
                line.show(ax, figsize)
        else:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
            for line in self.lines:
                line.show(ax, figsize, color=color)
            fig.show()
            
        return ax
    
    def __str__(self):
        __str = "JoinedLine[\n"
        for line in self.lines:
            __str += line.__str__()
            __str += "\n"
        __str += "]"
        return __str
            
class ClosedLine(JoinedLine):
    def __init__(self, line_list: List[Line]):
        super().__init__(line_list)
        if not np.all(np.isclose(self.lines[0].p1, self.lines[-1].p2)):
            raise ValueError("Given line list is not closed.")
                
    def __str__(self):
        __str = "ClosedLine[\n"
        for line in self.lines:
            __str += line.__str__()
            __str += "\n"
        __str += "]"
        return __str