from typing import Iterable, List, Dict, Tuple

import numpy as np
from numpy.typing import NDArray

from pyQuantumDevice.designer.line import *

class FingerGate:
    def __init__(self, name: str, location: NDArray[np.float_], width: float, length: float, direction: str="front"):
        self.name = name
        self.location = location
        self.width = width
        self.radius = width/2
        self.body_length = length - self.radius
        self.edges = []
        if direction == "front":
            self.edges.append(location + np.array([-self.radius, self.body_length]))
            self.edges.append(location + np.array([-self.radius, 0]))
            self.edges.append(location + np.array([self.radius, 0]))
            self.edges.append(location + np.array([self.radius, self.body_length]))
            self.gatewire = ClosedLine([
                VerticalLine(self.edges[0], self.edges[1]),
                HalfCircle(self.location, self.edges[1]),
                VerticalLine(self.edges[2], self.edges[3]),
                HorizontalLine(self.edges[3], self.edges[0])
            ])
                
        if direction == "back":
            self.edges.append(location + np.array([self.radius, -self.body_length]))
            self.edges.append(location + np.array([self.radius, 0]))
            self.edges.append(location + np.array([-self.radius, 0]))
            self.edges.append(location + np.array([-self.radius, -self.body_length]))
            self.gatewire = ClosedLine([
                VerticalLine(self.edges[0], self.edges[1]),
                HalfCircle(self.location, self.edges[1]),
                VerticalLine(self.edges[2], self.edges[3]),
                HorizontalLine(self.edges[3], self.edges[0])
            ])
            
    def show(self, ax=None, color="k"):
        if ax:
            self.gatewire.show(ax, color=color)
        else:
            self.gatewire.show(color=color)
        ax.set_aspect(1)
        ax.text(self.location[0], self.location[1] - 2 * self.radius, self.name, horizontalalignment='center', verticalalignment='center', fontsize=12)
        return ax
    
class BackBone:
    def __init__(self, location: NDArray[np.float_], width: float, length: float):
        self.name = "Back bone"
        self.location = location
        self.front_tips = []
        self.back_tips = []
        self.edges = []
        self.edges.append(location + np.array([-length/2, - width/2]))
        self.edges.append(location + np.array([length/2, - width/2]))
        self.edges.append(location + np.array([length/2, width/2]))
        self.edges.append(location + np.array([-length/2, width/2]))
        
        self.gatewire = ClosedLine([
            HorizontalLine(self.edges[0], self.edges[1]),
            VerticalLine(self.edges[1], self.edges[2]),
            HorizontalLine(self.edges[2], self.edges[3]),
            VerticalLine(self.edges[3], self.edges[0])
        ])
    
    def add_tip(self, center: float, radius: float, direction="back"):
        if direction == "front":
            arc_start = np.array([center - radius, self.edges[0][1]])
            arc_end = np.array([center + radius, self.edges[0][1]])
            count = np.sum(np.array(self.front_tips) < center)
            new_lines = self.gatewire.lines[:2 * count]
            new_lines.append(HorizontalLine(self.gatewire.lines[2 * count].p1, arc_start))
            new_lines.append(HalfCircle(np.array([center, self.edges[0][1]]), arc_start))
            new_lines.append(HorizontalLine(arc_end, self.gatewire.lines[2 * count].p2))
            new_lines.extend(self.gatewire.lines[2 * count + 1:])
            self.gatewire = ClosedLine(new_lines)
            self.front_tips.append(center)
            
        elif direction == "back":
            arc_start = np.array([center + radius, self.edges[3][1]])
            arc_end = np.array([center - radius, self.edges[3][1]])
            count = len(self.front_tips) + np.sum(np.array(self.back_tips) > center)
            new_lines = self.gatewire.lines[:2 * count + 2]
            new_lines.append(HorizontalLine(self.gatewire.lines[2 * count + 2].p1, arc_start))
            new_lines.append(HalfCircle(np.array([center, self.edges[3][1]]), arc_start))
            new_lines.append(HorizontalLine(arc_end, self.gatewire.lines[2 * count + 2].p2))
            new_lines.extend(self.gatewire.lines[2 * count + 3:])
            self.gatewire = ClosedLine(new_lines)
            self.back_tips.append(center)
            
    def show(self, ax=None, color="k"):
        if ax:
            self.gatewire.show(ax, color=color)
        else:
            self.gatewire.show(color=color)
        ax.set_aspect(1)
        ax.text(self.location[0], self.location[1], self.name, horizontalalignment='center', verticalalignment='center', fontsize=12)
        return ax
    
class PlanView:
    def __init__(self, width: float, depth: float):
        self.width = width
        self.depth = depth
        self.gates = []
        self.occupied = lambda x: False
        
    def add_finger_gate(self, name: str, location: NDArray[np.float_], width: float, length: float=None, direction: str="front"):
        if not length:
            if direction == "front":
                length = self.depth - location[1] + width/2
            elif direction == "back":
                length = location[1] + width / 2
            else:
                raise ValueError()
        self.gates.append(
            FingerGate(name, location, width, length)
        )
        
    def add_back_bone(self, location: float, width: float, tips: Dict[str, List[Tuple[float, float]]]=None):
        self.gates.append(
            BackBone(np.array([self.width/2, location]), width, self.width)
        )
        if "front" in tips:
            for center, radius in tips["front"]:
                self.gates[-1].add_tip(center, radius, "front")
            
        if "back" in tips:
            for center, radius in tips["back"]:
                self.gates[-1].add_tip(center, radius, "back")
             
    def show(self):
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        plt.scatter([0, self.width, self.width, 0], [0, 0, self.depth, self.depth])
        for gate in self.gates:
            ax = gate.show(ax)
        ax.set_aspect(1)
            