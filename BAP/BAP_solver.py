import numpy as np
import copy
from typing import List

class Passage:
    def __init__(self, bus, nb_arrete: int, temps_graph: List, arrete_m: int,\
                 alpha: float=4.0, beta: float=1.0):
        self.bus = bus
        self.nb_arrete = nb_arrete
        self.temps_graph = temps_graph
        self.temps_graph_ext = np.append(np.append(self.temps_graph,\
                                                   np.zeros([1,self.nb_arrete]),axis=0),\
                                         np.zeros([self.nb_arrete+1,1]),axis=1)
        self.arrete_m = arrete_m
        self.alpha = alpha
        self.beta = beta
        self.__reinit()

    def __reinit(self):
        self.temps_tot = 0
        self.arrete_actuelle = np.random.randint(0,self.nb_arrete-1)
        self.arrete_inconnue = np.ones(self.nb_arrete)
        self.arrete_inconnue[self.arrete_actuelle] = 0
        self.path = [self.arrete_actuelle]

    def __genetic(self):
        self.temps_tot = 0
        self.arrete_inconnue = np.ones(self.nb_arrete)
        pere_id,mere_id = np.random.choice(range(100),2)
        passage_pere = self.bus.passages[pere_id]
        passage_mere = self.bus.passages[mere_id]
        self.path = [passage_pere.path[0]];self.arrete_inconnue[passage_pere.path[0]] = 1
        n = 0
        for _ in range(1,np.random.randint(0,int(self.nb_arrete/2)-1)):
            while passage_pere.path[n] == -1:
                self.path.append(-1);self.path.append(self.arrete_m);n+=2
                self.arrete_inconnue[self.arrete_m] = 0
            self.path.append(passage_pere.path[n]);self.arrete_inconnue[passage_pere.path[n]] = 0
            self.temps_tot += self.temps_graph[self.path[-2],self.path[-1]]
        n = passage_mere.path.index(self.path[-1])+1
        id_fin = len(passage_mere.path);conn=0
        while n<id_fin:
            while passage_mere.path[n] == -1 or self.arrete_inconnue[passage_mere.path[n]] == 0:
                if passage_mere.path[n] == -1:
                    self.path.append(-1);self.path.append(self.arrete_m);n+=1
                n+=1 
                if n>=id_fin:
                    conn=1;break
            if conn:
                break
            self.path.append(passage_mere.path[n]);self.arrete_inconnue[passage_mere.path[n]] = 0
            self.temps_tot += self.temps_graph[self.path[-2],self.path[-1]]
        self.arrete_actuelle = self.path[-1]
        

    def __prochain_arrete(self):
        prochain_arrete_proba = (self.bus.pheromone_graph[self.arrete_actuelle,:]**self.alpha)\
                                *((self.temps_graph[self.arrete_actuelle,:]+1e-15)**(-self.beta))
        arrete_acces = np.where(self.arrete_inconnue*prochain_arrete_proba)[0]
        try:
            proba_tot = np.sum(prochain_arrete_proba[arrete_acces])
            if proba_tot > 0:
                proba = np.random.uniform(0,proba_tot)
                for arrete in arrete_acces:
                    proba -= prochain_arrete_proba[arrete]
                    if proba < 0:
                        return arrete
            return np.random.choice(arrete_acces)
        except:
            return None

    def __temps_cal(self):
        self.temps_tot = np.sum(self.temps_graph_ext[self.path[:-1],self.path[1:]])+\
                         np.sum(self.temps_graph_ext[self.path[1:],self.path[:-1]])

    def __transition(self,prochain_arrete: int):
        if prochain_arrete != None:
            if prochain_arrete != self.arrete_m and\
               self.temps_graph[self.arrete_actuelle,prochain_arrete]>self.temps_graph[self.arrete_m,prochain_arrete]:
                if -1 not in self.path and self.arrete_m not in self.path:
                    self.path.append(self.arrete_m)
                self.path.append(-1);self.path.append(self.arrete_m)
                self.temps_tot += self.temps_graph[self.arrete_m,prochain_arrete]
                self.arrete_inconnue[self.arrete_m] = 0
            else:
                self.temps_tot += self.temps_graph[self.arrete_actuelle,prochain_arrete]
            self.arrete_inconnue[prochain_arrete] = 0
            self.path.append(prochain_arrete)
        self.arrete_actuelle = prochain_arrete

    def path_cal(self,mode="r"):
        if mode == "r":
            self.__reinit()
        else:
            self.__genetic()
        while self.arrete_actuelle!=None:
            self.__transition(self.__prochain_arrete())
        if 1 in self.arrete_inconnue:
            self.temps_tot = np.inf
        else:
            self.__temps_cal()

class BusPath:
    def __init__(self, nb_arrete: float, temps_graph: List, rho: float=0.15, Q: float=100):
        self.rho = rho
        self.Q = Q
        self.nb_arrete = nb_arrete
        self.temps_graph = temps_graph
        self.arrete_m = np.argmin(np.sum(self.temps_graph,axis=1)+np.sum(self.temps_graph,axis=0))
        self.temps_graph_ext = np.append(np.append(self.temps_graph,\
                                                   np.zeros([1,self.nb_arrete]),axis=0),\
                                         np.zeros([self.nb_arrete+1,1]),axis=1)
        self.__reinit()

    def __reinit(self):
        self.pheromone_graph = np.ones([self.nb_arrete,self.nb_arrete])
        self.passages = [Passage(self, self.nb_arrete, self.temps_graph, self.arrete_m) for _ in range(100)]
        self.best_passage = Passage(self, self.nb_arrete, self.temps_graph, self.arrete_m)
        self.best_passage.temps_tot = np.inf
        self.iter = 0

    def path(self,mode="g"):
        self.iter += 1
        for passage in self.passages[:50]:
            passage.path_cal(mode)
            if passage.temps_tot < self.best_passage.temps_tot:
                self.best_passage = copy.deepcopy(passage)
        for passage in self.passages[50:]:
            passage.path_cal()
            if passage.temps_tot < self.best_passage.temps_tot:
                self.best_passage = copy.deepcopy(passage)
        self.__update_pheromone()

    def __update_pheromone(self):
        temp_pheromone = np.zeros([self.nb_arrete+1,self.nb_arrete+1])
        for passage in self.passages:
            if np.isinf(passage.temps_tot):
                continue
            id_r = np.where(passage.path==-1)[0]-1
            temp_pheromone[passage.path[:-1],passage.path[1:]] += self.Q / (1e-15+self.temps_graph_ext[passage.path[:-1],passage.path[1:]])
            temp_pheromone[passage.path[1:],passage.path[:-1]] += 0.5 * self.Q / (1e-15+self.temps_graph_ext[passage.path[1:],passage.path[:-1]])
        self.pheromone_graph = self.pheromone_graph * (1-self.rho) + temp_pheromone[:-1,:-1] * self.rho
