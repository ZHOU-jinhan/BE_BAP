import BAP_solver
import BAP_GUI
import numpy as np
from tkinter import *

class BAP(BAP_GUI.FenPrincipale):
    def __init__(self):
        BAP_GUI.FenPrincipale.__init__(self)
        self.__bouton4 = Button(self, text='Calcul', command=self.resolve).pack(side=LEFT, padx=5, pady=5)
        self.bus = None

    def dist_matrix(self):
        n = len(self.liste_node)
        X = np.repeat(self.x_nodes,n).reshape([n,n]); Y = np.repeat(self.y_nodes,n).reshape(n,n)
        X = X-X.T; Y = Y-Y.T
        return (X**2+Y**2)**0.5

    def cal_matrix(self):
        self.temps_matrix = self.dist_matrix()

    def ajouter_noeud(self,x,y):
        BAP_GUI.FenPrincipale.ajouter_noeud(self,x,y)
        self.bus = None

    def supprimer_noeud(self,x,y):
        BAP_GUI.FenPrincipale.supprimer_noeud(self,x,y)
        self.bus = None
    
    def resolve(self):
        self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)
        if len(self.liste_node)<2:
            return 0
        if self.bus == None:
            self.cal_matrix()
            self.bus = BAP_solver.BusPath(len(self.liste_node),self.temps_matrix)
        for _ in range(50):
            self.bus.path()
        self.title("BAP Solver - IterTours = %s"%self.bus.iter)
        print(self.bus.best_passage.path)
        for k in range(1,len(self.bus.best_passage.path)):
            start, end = self.bus.best_passage.path[k-1], self.bus.best_passage.path[k]
            if end == -1:
                if k != 1:
                    continue
                else:
                    end = self.bus.arrete_m
            if start == -1:
                start = self.bus.arrete_m
            self.zoneAffichage.line(self.x_nodes[start],self.y_nodes[start],self.x_nodes[end],self.y_nodes[end])
        self.zoneAffichage.placer_noeud(self.x_nodes[self.bus.arrete_m],self.y_nodes[self.bus.arrete_m],3, "red")

if __name__ == "__main__":
    bap = BAP()
    bap.mainloop()
