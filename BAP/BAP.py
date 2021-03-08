import BAP_solver
import BAP_GUI
import numpy as np
from tkinter import *

class BAP(BAP_GUI.FenPrincipale):
    def __init__(self):
        BAP_GUI.FenPrincipale.__init__(self)
        self.__bouton6 = Button(self, text='Calcul', command=self.resolve).pack(side=LEFT, padx=5, pady=5)
        self.bus = None

    def dist_matrix(self):
        n = len(self.liste_node)
        X = np.repeat(self.x_nodes,n).reshape([n,n]); Y = np.repeat(self.y_nodes,n).reshape(n,n)
        X = X-X.T; Y = Y-Y.T
        return (X**2+Y**2)**0.5

    def cal_matrix(self):
        distance_matrix = self.dist_matrix()
        distance_change = self.route_info[:,:,0]
        change_id = np.where(distance_change!=-1)[0]
        distance_matrix[change_id] = distance_change[change_id]
        vitesse_matrix = self.route_info[:,:,1]
        vitesse_matrix = np.where(vitesse_matrix!=-1, vitesse_matrix, 1)
        vitesse_matrix = np.where(vitesse_matrix!=0, vitesse_matrix, 1e-15)
        freq_matrix = self.route_info[:,:,2]
        freq_matrix = np.where(freq_matrix!=-1, freq_matrix, 1)
        freq_matrix = np.where(freq_matrix!=0, freq_matrix, 1e-15)
        lib_matrix = self.route_info[:,:,3]
        lib_matrix = np.where(lib_matrix!=-1, lib_matrix, 1)
        n = len(self.liste_node)
        lib_matrix += np.repeat(np.array(self.noeud_info)[:,1],n).reshape([n,n])
        lib_matrix = np.where(lib_matrix!=0, lib_matrix, 1e-15)
        besoin_matrix = np.repeat(np.array(self.noeud_info)[:,0],n).reshape([n,n])
        prop_matrix_a = besoin_matrix//lib_matrix
        prop_matrix_b = besoin_matrix%lib_matrix
        prop_matrix = ((prop_matrix_a-1)*prop_matrix_a+prop_matrix_b*prop_matrix_a)/besoin_matrix
        self.temps_matrix = distance_matrix/vitesse_matrix+1/freq_matrix* prop_matrix

    def ajouter_noeud(self,event):
        BAP_GUI.FenPrincipale.ajouter_noeud(self,event)
        self.bus = None

    def supprimer_noeud(self,event):
        BAP_GUI.FenPrincipale.supprimer_noeud(self,event)
        self.bus = None
    
    def resolve(self):
        self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)
        if len(self.liste_node)<2:
            return 0
        if self.bus == None:
            self.cal_matrix()
            self.bus = BAP_solver.BusPath(len(self.liste_node),self.temps_matrix)
        for i in range(50):
            if i == 0:
                self.bus.path(mode="r")
            else:
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
