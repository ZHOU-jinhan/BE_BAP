from tkinter import *
from tkinter.messagebox import showinfo
import random
import numpy as np

class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):
        self.__w = w
        self.__h = h
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)

    def not_used_keep_dessiner_graphe(self):
        for b in self.__liste_noeuds:
            b.deplacement()
        self.after(50, self.dessiner_graphe)

    def creer_noeud(self, x_centre, y_centre, rayon=5 , couleur="black", fill_color="white"):
        noeud=self.create_oval(x_centre - rayon, y_centre - rayon, x_centre + rayon, y_centre + rayon, outline=couleur, fill=fill_color)
        self.pack()
        return noeud

    def add_clique(self, event):
        self.__fen_parent.ajouter_noeud(event.x, event.y)

    def rem_clique(self, event):
        self.__fen_parent.supprimer_noeud(event.x, event.y)

    def placer_noeud(self, x_centre, y_centre, rayon=5, couleur="black"):
        node=self.creer_noeud(x_centre, y_centre, rayon, couleur)
        self.update()
        return node

    def rien(self, event):
        pass

    def line(self, x1, y1, x2, y2):
        self.create_line(x1, y1, x2, y2, fill="red")
        

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('BAP Solver')
        self.zoneAffichage = ZoneAffichage(self)
        self.zoneAffichage.pack()
        self.__bouton1 = Button(self, text='Ajouter des noeuds', command=self.ajouter).pack(side=LEFT, padx=5, pady=5)
        self.__bouton2 = Button(self, text='Supprimer des noeuds', command=self.supprimer).pack(side=LEFT, padx=5, pady=5)
        self.__bouton3 = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        self.liste_node=[]
        self.x_nodes=[];self.y_nodes=[]

    def ajouter(self):
        self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.add_clique)

    def supprimer(self):
        self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rem_clique)
        
    def ajouter_noeud(self, x, y):
        node = self.zoneAffichage.placer_noeud(x,y)
        self.liste_node.append(node)
        self.x_nodes.append(x)
        self.y_nodes.append(y)

    def supprimer_noeud(self, x, y):
        nodes = np.append(self.x_nodes,self.y_nodes).reshape(2,-1)
        distances = np.linalg.norm(nodes.T-np.array([x,y]),axis=1)
        try:
            id_ = np.argmin(distances)
            if distances[id_]<6:
                node=self.liste_node.pop(id_)
                self.x_nodes.pop(id_)
                self.y_nodes.pop(id_)
                self.zoneAffichage.delete(node)
                self.zoneAffichage.update()
        except:
            pass

    def effacer(self):
        """ Efface la zone graphique """
        self.zoneAffichage.delete(ALL)
        self.liste_node.clear()
        self.x_nodes.clear();self.y_nodes.clear()

if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
