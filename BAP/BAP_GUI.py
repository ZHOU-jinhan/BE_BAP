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

    def placer_noeud(self, x_centre, y_centre, rayon=5, couleur="black"):
        node=self.creer_noeud(x_centre, y_centre, rayon, couleur)
        self.update()
        return node

    def rien(self, event):
        pass

    def line(self, x1, y1, x2, y2):
        self.create_line(x1, y1, x2, y2, fill="red")

class InfoNoeud(Tk):
    def __init__(self, parent, id_):
        Tk.__init__(self)
        self.parent = parent
        self.id_ = id_
        f1 = Frame(self)
        f1.pack()
        Label(f1, text="Nb_up :\t").pack(side = LEFT)
        self.E1 = Entry(f1, bd=5)
        self.E1.pack(side = RIGHT)
        f2 = Frame(self)
        f2.pack()
        Label(f2, text="Nb_down :\t").pack(side = LEFT)
        self.E2 = Entry(f2, bd=5)
        self.E2.pack(side = RIGHT)
        Button(self, text='OK', command=self.quit).pack(side=BOTTOM)
        self.E1.bind('<KeyRelease-Return>', self.E1_finir)
        self.E2.bind('<KeyRelease-Return>', self.E2_finir)
        self.E1.focus()
        
    def E1_finir(self,event):
        try:
            dis = int(self.E1.get())
            if dis >= 0:
                self.parent.noeud_info[self.id_][0]= dis
        except:
            pass
        self.E2.focus()
	
    def E2_finir(self,event):
        try:
            dis = float(self.E2.get())
            if dis >= 0:
                self.parent.noeud_info[self.id_][1] = dis
        except:
            pass
        if self.parent.liste_node_info[self.id_]!=None:
            self.parent.zoneAffichage.delete(self.parent.liste_node_info[self.id_])
        x,y = self.parent.x_nodes[self.id_],self.parent.y_nodes[self.id_]
        m,n = self.parent.noeud_info[self.id_]
        self.parent.liste_node_info[self.id_] = self.parent.zoneAffichage.\
                                                create_text(x+50,y,fill="blue",\
                                                            text="Nb_up=%s\nNb_down=%s"%(m,n))
        self.update()
        self.destroy()

    def quit(self):
        try:
            dis = int(self.E1.get())
            if dis >= 0:
                self.parent.noeud_info[self.id_][0] = dis
        except:
            pass
        try:
            dis = float(self.E2.get())
            if dis >= 0:
                self.parent.noeud_info[self.id_][1] = dis
        except:
            pass
        if self.parent.liste_node_info[self.id_]!=None:
            self.parent.zoneAffichage.delete(self.parent.liste_node_info[self.id_])
        m,n = self.parent.noeud_info[self.id_]
        x,y = self.parent.x_nodes[self.id_],self.parent.y_nodes[self.id_]
        self.parent.liste_node_info[self.id_] = self.parent.zoneAffichage.\
                                                create_text(x+50,y,fill="blue",\
                                                            text="Nb_up=%s\nNb_down=%s"%(m,n))
        self.update()
        self.destroy()

class InfoRoute(Tk):
    def __init__(self, parent, ids):
        Tk.__init__(self)
        self.parent = parent
        self.id_ = ids
        f1 = Frame(self)
        f1.pack()
        Label(f1, text="Distance :\t").pack(side = LEFT)
        self.E1 = Entry(f1, bd=5)
        self.E1.pack(side = RIGHT)
        f2 = Frame(self)
        f2.pack()
        Label(f2, text="Vitesse :\t").pack(side = LEFT)
        self.E2 = Entry(f2, bd=5)
        self.E2.pack(side = RIGHT)
        f3 = Frame(self)
        f3.pack()
        Label(f3, text="Frequence :\t").pack(side = LEFT)
        self.E3 = Entry(f3, bd=5)
        self.E3.pack(side = RIGHT)
        f4 = Frame(self)
        f4.pack()
        Label(f4, text="Nb_libre :\t").pack(side = LEFT)
        self.E4 = Entry(f4, bd=5)
        self.E4.pack(side = RIGHT)
        Button(self, text='OK', command=self.quit).pack(side=BOTTOM)
        self.E1.bind('<KeyRelease-Return>', self.E1_finir)
        self.E2.bind('<KeyRelease-Return>', self.E2_finir)
        self.E3.bind('<KeyRelease-Return>', self.E3_finir)
        self.E4.bind('<KeyRelease-Return>', self.E4_finir)
        self.E1.focus()
        
    def E1_finir(self,event):
        try:
            dis = float(self.E1.get())
            if dis >= 0:
                self.parent.route_info[self.id_][0]= dis
        except:
            pass
        self.E2.focus()

    def E2_finir(self,event):
        try:
            dis = float(self.E2.get())
            if dis >= 0:
                self.parent.route_info[self.id_][1]= dis
        except:
            pass
        self.E3.focus()

    def E3_finir(self,event):
        try:
            dis = float(self.E3.get())
            if dis >= 0:
                self.parent.route_info[self.id_][2]= dis
        except:
            pass
        self.E4.focus()
	
    def E4_finir(self,event):
        try:
            dis = int(self.E4.get())
            if dis >= 0:
                self.parent.route_info[self.id_][3] = dis
        except:
            pass
        if self.id_ in self.parent.liste_route_info.keys():
            self.parent.zoneAffichage.delete(self.parent.liste_route_info[self.id_])
        x1,y1 = self.parent.x_nodes[self.id_[0]],self.parent.y_nodes[self.id_[0]]
        x2,y2 = self.parent.x_nodes[self.id_[1]],self.parent.y_nodes[self.id_[1]]
        m,n,f,k = self.parent.route_info[self.id_]
        if x2>x1:
            self.parent.liste_route_info[self.id_] = self.parent.zoneAffichage.\
                                                     create_text((x1+x2)/2+50,(y1+y2)/2,fill="blue",\
                                                                 text="Distance=%s\nVitesse=%s\nFreq=%s\nNb_libre=%s"%(m,n,f,k))
            self.parent.liste_route.append([(x1+x2)/2+50,(y1+y2)/2])
            self.parent.liste_route_node.append(self.id_)
        else:
            self.parent.liste_route_info[self.id_] = self.parent.zoneAffichage.\
                                                     create_text((x1+x2)/2-50,(y1+y2)/2,fill="blue",\
                                                                 text="Distance=%s\nVitesse=%s\nFreq=%s\nNb_libre=%s"%(m,n,f,k))
            self.parent.liste_route.append([(x1+x2)/2+50,(y1+y2)/2])
            self.parent.liste_route_node.append(self.id_)
        self.update()
        self.destroy()

    def quit(self):
        try:
            dis = int(self.E1.get())
            if dis >= 0:
                self.parent.route_info[self.id_][0] = dis
        except:
            pass
        try:
            dis = float(self.E2.get())
            if dis >= 0:
                self.parent.route_info[self.id_][1] = dis
        except:
            pass
        try:
            dis = float(self.E3.get())
            if dis >= 0:
                self.parent.route_info[self.id_][2] = dis
        except:
            pass
        try:
            dis = int(self.E4.get())
            if dis >= 0:
                self.parent.route_info[self.id_][3] = dis
        except:
            pass
        if self.id_ in self.parent.liste_route_info.keys():
            self.parent.zoneAffichage.delete(self.parent.liste_node_info[self.id_])
        x1,y1 = self.parent.x_nodes[self.id_[0]],self.parent.y_nodes[self.id_[0]]
        x2,y2 = self.parent.x_nodes[self.id_[1]],self.parent.y_nodes[self.id_[1]]
        m,n,f,k = self.parent.route_info[self.id_]
        if x2>x1:
            self.parent.liste_route_info[self.id_] = self.parent.zoneAffichage.\
                                                     create_text((x1+x2)/2+50,(y1+y2)/2,fill="blue",\
                                                                 text="Distance=%s\nVitesse=%s\nFreq=%s\nNb_libre=%s"%(m,n,f,k))
            self.parent.liste_route.append([(x1+x2)/2+50,(y1+y2)/2])
            self.parent.liste_route_node.append(self.id_)
        else:
            self.parent.liste_route_info[self.id_] = self.parent.zoneAffichage.\
                                                     create_text((x1+x2)/2-50,(y1+y2)/2,fill="blue",\
                                                                 text="Distance=%s\nVitesse=%s\nFreq=%s\nNb_libre=%s"%(m,n,f,k))
            self.parent.liste_route.append([(x1+x2)/2+50,(y1+y2)/2])
            self.parent.liste_route_node.append(self.id_)
        self.update()
        self.destroy()
    
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('BAP Solver')
        self.zoneAffichage = ZoneAffichage(self)
        self.zoneAffichage.pack()
        self.__bouton1 = Button(self, text='Ajouter des noeuds', command=self.ajouter).pack(side=LEFT, padx=5, pady=5)
        self.__bouton2 = Button(self, text='Supprimer des noeuds', command=self.supprimer).pack(side=LEFT, padx=5, pady=5)
        self.__bouton3 = Button(self, text='Definir des noeuds', command=self.node_def).pack(side=LEFT, padx=5, pady=5)
        self.__bouton4 = Button(self, text='Definir des routes', command=self.route_def).pack(side=LEFT, padx=5, pady=5)
        self.__bouton5 = Button(self, text='Supprimer des définitions', command=self.def_remove).pack(side=LEFT, padx=5, pady=5)
        self.__bouton6 = Button(self, text='Effacer', command=self.effacer).pack(side=LEFT, padx=5, pady=5)
        self.liste_node=[];self.liste_node_info=[];self.liste_route_info={}
        self.liste_route=[];self.liste_route_node=[]
        self.x_nodes=[];self.y_nodes=[]
        self.noeud_info=[];self.route_info=None
        self.route_fin=-1

    def ajouter(self):
        self.zoneAffichage.bind('<Button-1>', self.ajouter_noeud)

    def supprimer(self):
        if len(self.liste_node)>=1:
            self.zoneAffichage.bind('<Button-1>', self.supprimer_noeud)
        else:
            self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)

    def node_def(self):
        if len(self.liste_node_info)>=1:
            self.zoneAffichage.bind('<Button-1>', self.definir_noeud)
        else:
            self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)

    def route_def(self):
        self.route_fin = -1
        if len(self.liste_node)>=2:
            self.zoneAffichage.bind('<Button-1>', self.definir_route)
        else:
            self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)

    def def_remove(self):
        self.zoneAffichage.bind('<Button-1>', self.undefinir)

    def definir_noeud(self,event):
        x,y = event.x, event.y
        nodes = np.append(self.x_nodes,self.y_nodes).reshape(2,-1)
        distances = np.linalg.norm(nodes.T-np.array([x,y]),axis=1)
        if distances.size!=0:
            id_ = np.argmin(distances)
            if distances[id_]<6:
                InfoNoeud(self,id_)

    def definir_route(self,event):
        x,y = event.x, event.y
        nodes = np.append(self.x_nodes,self.y_nodes).reshape(2,-1)
        distances = np.linalg.norm(nodes.T-np.array([x,y]),axis=1)
        if distances.size!=0:
            id_ = np.argmin(distances)
            if distances[id_]<6:
                if self.route_fin>=0:
                    InfoRoute(self,(self.route_fin,id_))
                    self.route_fin = -1
                else:
                    self.route_fin = id_

    def undefinir(self,event):
        x,y = event.x, event.y
        nodes = np.append(self.x_nodes,self.y_nodes).reshape(2,-1)
        distances = np.linalg.norm(nodes.T-np.array([x,y]),axis=1)
        if distances.size!=0:
            id_ = np.argmin(distances)
            if distances[id_]<6:
                label = self.liste_node_info[id_]
                if label != None:
                    self.liste_node_info[id_] = None
                    self.zoneAffichage.delete(label)
                self.noeud_info[id_] = [0,1]
                self.zoneAffichage.update()
        routes = np.array(self.liste_route)
        if routes.size !=0:
            distances = np.abs(routes-np.array([x,y]))
            distances[:,0] = distances[:,0]/50;distances[:,1] = distances[:,1]/20
            distances = np.max(distances,axis=1)
            if distances.size!=0:
                id_ = np.argmin(distances)
                if distances[id_]<1.2:
                    self.liste_route.pop(id_)
                    route_id = self.liste_route_node.pop(id_)
                    route = self.liste_route_info[route_id]
                    del self.liste_route_info[route_id]
                    self.zoneAffichage.delete(route)
                    self.route_info[route_id]=[-1,-1,-1,-1]
                    self.zoneAffichage.update()
            if len(self.liste_route)<1 and all(np.array(self.liste_node_info)==None):
                self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)

    def ajouter_noeud(self, event):
        x,y = event.x, event.y
        node = self.zoneAffichage.placer_noeud(x,y)
        self.liste_node.append(node)
        self.x_nodes.append(x)
        self.y_nodes.append(y)
        self.liste_node_info.append(None)
        self.noeud_info.append([1,1])
        if type(self.route_info)==type(None):
            self.route_info = np.array([[[-1,-1,-1,-1]]])
        else:
            self.route_info = np.append(np.append(self.route_info,\
                                                  -1*np.ones([1,self.route_info.shape[0],4]),axis=0),\
                                        -1*np.ones([self.route_info.shape[0]+1,1,4]),axis=1)

    def supprimer_noeud(self, event):
        x,y = event.x, event.y
        nodes = np.append(self.x_nodes,self.y_nodes).reshape(2,-1)
        distances = np.linalg.norm(nodes.T-np.array([x,y]),axis=1)
        if distances.size!=0:
            id_ = np.argmin(distances)
            if distances[id_]<6:
                node=self.liste_node.pop(id_)
                self.x_nodes.pop(id_)
                self.y_nodes.pop(id_)
                label = self.liste_node_info.pop(id_)
                if label != None:
                    self.zoneAffichage.delete(label)
                self.noeud_info.pop(id_)
                self.zoneAffichage.delete(node);k=0
                while k < len(self.liste_route_node):
                    if id_ in self.liste_route_node[k]:
                        self.liste_route.pop(k)
                        route_id = self.liste_route_node.pop(k)
                        route = self.liste_route_info[route_id]
                        del self.liste_route_info[route_id]
                        self.zoneAffichage.delete(route)
                    else:
                        k+=1
                self.route_info = np.delete(np.delete(self.route_info,id_,axis=0),id_,axis=1)
        if len(self.liste_node)<1:
            self.zoneAffichage.bind('<Button-1>', self.zoneAffichage.rien)
        self.zoneAffichage.update()

    def effacer(self):
        """ Efface la zone graphique """
        self.zoneAffichage.delete(ALL)
        self.liste_node.clear()
        self.x_nodes.clear();self.y_nodes.clear()
        self.liste_node_info.clear()

if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()
