#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

@author: ThomasCoMo
@license: MIT

"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
#import os
#import gc
#import sys
import time
import pandas as pd
from ast import literal_eval
import math

class Ecriture:
    def __init__(self):
        self.nomSeance=""
        self.exo=""
        self.temps_repo =""
        self.NbSeries =""
        self.poids = []
        self.rep = []
        self.secondes = ""
        self.Dico={}

    def recupere_nomSeance(self):
        self.nomSeance=app.entreeNOM.get()
        print("nom de séance validé : %s"%self.nomSeance)
        
    def recupere_exo(self):
        self.exo = app.entree.get()
        print("nom Exercice : %s"%self.exo)

    def recupere_tempsRepo(self):
        self.temps_repo=app.entree1.get()
        print("temps de repos entre les séries : %s min"%self.temps_repo)

    def recupere_NbSeries(self):
        self.NbSeries=app.entree2.get()
        print("nombre de séries : %s"%self.NbSeries)
       
    def recupere_poids1(self):
        str1=app.entree3Z.get()
        str2=app.entree3Zrep.get()
        str1=str1.replace(" ","")
        str2=str2.replace(" ","")
        self.poids= list(str1.split(","))
        self.rep=list(str2.replace(" ","").split(","))
        print("poids série 1 : %s Kg %s Rep"%(self.poids,self.rep))
     


    def set_secondes(self,sec):
        self.secondes=sec



    def valider_exo(self):
        self.Dico[self.exo]=[self.exo,self.temps_repo,self.NbSeries,self.poids,self.rep]
        self.exo=""
        self.temps_repo =""
        self.NbSeries =""
        self.poids = []
        self.rep = []

    def save_exo(self):
        df = pd.DataFrame.from_dict(self.Dico, orient='index')
        df.columns = ['nom exo','repos','Nb series','poids','rep']
        df.to_csv('%s.csv'%self.nomSeance, index=False)
        self.nomSeance=""
        self.exo=""
        self.temps_repo =""
        self.NbSeries =""
        self.poids = []
        self.rep = []
        self.secondes = ""
        self.Dico={}

        


Ecriture_classe=Ecriture()

class Lecture:
    def __init__(self):
        self.nomSeance=""
        self.liste_nom=[]
        self.liste_nbSerie=[]
        self.liste_tpsRepos=[]
        self.liste_poids1=[]
        self.liste_rep1 = []
        self.index = 0
        

    def lecture(self,nomSeance):
        self.nomSeance=nomSeance
        self.liste_nom=[]
        self.liste_nbSerie=[]
        self.liste_tpsRepos=[]
        self.liste_poids1=[]
        self.liste_rep1 = []
        self.index = 0
        f = open('%s.csv'%self.nomSeance)
        df=pd.read_csv(f,index_col=None)
        df['poids']=df['poids'].apply(literal_eval)
        df['rep']=df['rep'].apply(literal_eval)
        for i in range(df.shape[0]):
            self.liste_nom.append(df['nom exo'].loc[i])
            frac, whole = math.modf(float(df['repos'].loc[i]))
            self.liste_tpsRepos.append(int(whole*60+round(frac,2)*100))
            self.liste_nbSerie.append(df['Nb series'].loc[i])
            self.liste_poids1.append(df['poids'].loc[i])
            self.liste_rep1.append(df['rep'].loc[i])
        print(self.liste_poids1,self.liste_rep1)
        f.close()
        
    def add_index(self):
        if self.index<len(self.liste_nom)-1:
            self.index=self.index+1

    def sous_index(self):
        if self.index>0:
            self.index=self.index-1


    def modif_nomExo(self):
        self.liste_nom[self.index]=app.entreeA.get()
        print("nom modifié : %s" %self.liste_nom[self.index])
        
    def modif_nbSeries(self):
        self.liste_nbSerie[self.index]=app.entreeB.get()
        print("nb Series modifié : %s" %self.liste_nbSerie[self.index])
        
    def modif_tpsRepo(self):
        print(self.liste_tpsRepos)
        temps = float(app.entreeC.get())
        frac, whole = math.modf(temps)
        temps=whole*60+round(frac,2)*100
        self.liste_tpsRepos[self.index]=str(temps)
        print(self.liste_tpsRepos)
        print("temps modifié : %s" %self.liste_tpsRepos[self.index])
        
    def modif_poids1(self):
        str1=app.entreeD.get()
        str1=str1.replace(" ","")
        self.liste_poids1[self.index]= list(str1.split(","))
        print("poids1 modifié : %s" %self.liste_poids1[self.index])
        

    def modif_rep1(self):
        str2=app.entreeH.get()
        str2=str2.replace(" ","")
        self.liste_rep1[self.index]=list(str2.replace(" ","").split(","))
        print("rep1 poids1 modifié : %s" %self.liste_rep1[self.index])


    def savefile(self):
        for i in range(len(self.liste_tpsRepos)):
            temps=(float(self.liste_tpsRepos[i]))
            temps=(temps-temps%60)/60+(temps%60)/100
            self.liste_tpsRepos[i]=temps
            
        dict = {'nom exo':self.liste_nom, 'repos':self.liste_tpsRepos,'Nb series':self.liste_nbSerie,'poids':self.liste_poids1,'rep':self.liste_rep1}
        df = pd.DataFrame(dict)
        df.to_csv('%s.csv'%self.nomSeance,index=False)
        app.ouvrirSeance(self.nomSeance)


    def countdown(self,t):
        t = int(t)
        while t:
            mins,secs = divmod(t,60)
            timer= '{:02d}:{:02d}'.format(mins,secs)
            print(timer, end="\n")
            time.sleep(1)
            t-=1
        print("FIN DU TEMPS GO PUUUUSH")
        
    def decompte(self, count):
        mins,secs = divmod(int(count),60)
        timer= '{:02d}:{:02d}'.format(mins,secs)
        lab.config(text=str(timer))
        if int(count) > 0 :
            self.o2.after(1000,decompte, int(count)-1)
        if int(count) == 0 :
            popup_showinfo()

lecture = Lecture()

            
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.n = ttk.Notebook()  # Création du système d'onglets
        self.n.pack()
        self.o1 = ttk.Frame(self.n)       # Ajout de l'onglet 1
        self.o1.pack()
        self.o2 = ttk.Frame(self.n)       # Ajout de l'onglet 2
        self.o2.pack()
        self.o3 = ttk.Frame(self.n)       # Ajout de l'onglet 2
        self.o3.pack()
        self.n.add(self.o1, text='Créer')      # Nom de l'onglet 1
        self.n.add(self.o2, text='Lire')      # Nom de l'onglet 2
        self.n.add(self.o3, text='Modifier')      # Nom de l'onglet 2
        self.nombreSerie = 0
        self.oldNombreSerie=0
        self.nom="Push_Exemple"
        # premier volet
        self.Cre_nom_seance()
        self.Cre_nom_exo()
        self.Cre_nomb_serie()
        self.Cre_tps_repos()
        self.Existe=1
        self.liste=[11,13,15,17,19,21,23,25,27,29,31]
        self.Cre_poids_rep()
        self.Cre_but_val()
        self.Cre_but_se()
        # second volet
        self.Li_nom_seance()
        # troisieme volet
        self.mod_nom_exo()
        self.mod_nb_serie()
        self.mod_tpsRepos()
        self.mod_poids_rep()
        self.mod_valider_exo()
        
        
    def Cre_nom_seance(self):
        self.label = Label(self.o1, text="nom séance")
        self.label.grid(row=1, column=1)
        self.value = StringVar() 
        self.value.set("Push_Exemple")
        self.entreeNOM = Entry(self.o1, textvariable=self.value, width=30)
        self.entreeNOM.grid(row=2, column=1)
        self.bouton = Button(self.o1, text="Valider nom Séance", command=Ecriture_classe.recupere_nomSeance)
        self.bouton.grid(row=2, column=2)

    def Cre_nom_exo(self):
        self.label = Label(self.o1, text="nom Exercice :")
        self.label.grid(row=3, column=1)
        self.value = StringVar() 
        self.value.set("exemple : DC")
        self.entree = Entry(self.o1, textvariable=self.value, width=30)
        self.entree.grid(row=4, column=1)
        self.bouton = Button(self.o1, text="Valider nom Ecriture", command=Ecriture_classe.recupere_exo)
        self.bouton.grid(row=4, column=2)
        
    def Cre_nomb_serie(self):
        self.label = Label(self.o1, text="nombre de séries")
        self.label.grid(row=5, column=1)
        self.value1 = StringVar() 
        self.value1.set("3")
        self.entree2 = Entry(self.o1, textvariable=self.value1, width=10)
        self.entree2.grid(row=6, column=1)
        self.bouton = Button(self.o1, text="Valider Nb Séries", command=Ecriture_classe.recupere_NbSeries)
        self.bouton.grid(row=6, column=2)


    def set_nombreSerie(self):
        self.OldNombreSerie=self.nombreSerie
        self.nombreSerie=self.entree2.get()
        self.bouton_val.destroy()
        if self.Existe == 0:
            for i in range(int(self.OldNombreSerie)):
                liste=self.o1.grid_slaves(row=[self.liste[i]])
                liste2=self.o1.grid_slaves(row=[self.liste[i]-1])
                for l in liste:
                    l.destroy()
                for l in liste2:
                    l.destroy()
        self.Cre_poids_rep()
        self.Existe=0
        
    def Cre_tps_repos(self):
        self.label = Label(self.o1, text="temps de repos (min) (2\'30\'\' => 2.30)")
        self.label.grid(row=7, column=1)
        self.value11 = StringVar() 
        self.value11.set("2.00")
        self.entree1 = Entry(self.o1, textvariable=self.value11, width=30)
        self.entree1.grid(row=8, column=1)
        self.bouton = Button(self.o1, text="Valider tps repos", command=Ecriture_classe.recupere_tempsRepo)
        self.bouton.grid(row=8, column=2)
            


    def Cre_poids_rep(self):
        self.label = Label(self.o1, text="poids format : 10, 10, 10, 10 [...]")
        self.label.grid(row=10, column=1)
        self.value2 = StringVar() 
        self.value2.set("20, 30, 40")
        self.entree3Z = Entry(self.o1, textvariable=self.value2, width=30)
        self.entree3Z.grid(row=11, column=1)
        self.label = Label(self.o1, text="nombre de Rep")
        self.label.grid(row=12, column=1)
        self.value3Zrep = StringVar() 
        self.value3Zrep.set("12, 10, 8 ")
        self.entree3Zrep = Entry(self.o1, textvariable=self.value3Zrep, width=30)
        self.entree3Zrep.grid(row=13, column=1)
        self.bouton = Button(self.o1, text="Valider poids, reps", command=Ecriture_classe.recupere_poids1)
        self.bouton.grid(row=13, column=2)


    def Cre_but_val(self):
        self.bouton_val = Button(self.o1, text="Valider Exo", command=Ecriture_classe.valider_exo)
        self.bouton_val.grid(row=14, column=1)
        
    def Cre_but_se(self):
        self.bouton_val = Button(self.o1, text="Valider SEANCE", command=Ecriture_classe.save_exo)
        self.bouton_val.grid(row=15, column=1)

    def Li_nom_seance(self):
        self.labelNomSeance = Label(self.o2, text="Nom seance, sans extension")
        self.labelNomSeance.grid(row=1,column=1)
        self.valueNom = StringVar() 
        self.valueNom.set(self.nom)
        self.entreeNomSeance = Entry(self.o2, textvariable=self.valueNom, width=20)
        self.entreeNomSeance.grid(row=2, column=1)
        self.bouton = Button(self.o2, text="ouvrir fichier séance", command=self.define_nom_seance)
        self.bouton.grid(row=2, column=2)

    def Li_nom_exo(self):
        self.labelNomExo = Label(self.o2, text="Nom ")
        self.labelNomExo.grid(row=3,column=1)
        self.valueNomExo = StringVar()
        self.valueNomExo.set(lecture.liste_nom[lecture.index])
        self.labelNe = Label(self.o2, textvariable=self.valueNomExo)
        self.labelNe.grid(row=3,column=2)

    def Li_nb_serie(self):
        self.labelNbSerie = Label(self.o2, text="Nombre de séries")
        self.labelNbSerie.grid(row=4,column=1)
        self.valueNbSerie = StringVar()
        self.valueNbSerie.set(lecture.liste_nbSerie[lecture.index])
        self.labelNmS = Label(self.o2, textvariable=self.valueNbSerie)
        self.labelNmS.grid(row=4,column=2)

    def Li_temps_repos(self):
        self.labeltpsRepos = Label(self.o2, text="temps de repos")
        self.labeltpsRepos.grid(row=5,column=1)
        self.labeltps = Label(self.o2, text="minutes")
        self.labeltps.grid(row=5,column=3)
        self.valuetpsRepos = StringVar()
#        frac, whole = math.modf(lecture.liste_tpsRepos[lecture.index])
#        self.valuetpsRepos.set(whole/60+frac/100)
        temps=lecture.liste_tpsRepos[lecture.index]
        self.valuetpsRepos.set((temps-temps%60)/60+(temps%60)/100)
        self.labelTs = Label(self.o2, textvariable=self.valuetpsRepos)
        self.labelTs.grid(row=5,column=2)



    def Li_poids_rep(self):
        for i in range(int(lecture.liste_nbSerie[lecture.index])):
            self.labelPoids1 = Label(self.o2, text="poids série %s : "%str(i+1))
            self.labelPoids1.grid(row=self.liste[i]-1,column=1)
            self.labelPoids11 = Label(self.o2, text="Kg")
            self.labelPoids11.grid(row=self.liste[i]-1,column=3)
            self.valuePoids1 = StringVar()
            self.valuePoids1.set('%s'%lecture.liste_poids1[lecture.index][i])
            self.labelP1 = Label(self.o2, textvariable=self.valuePoids1)
            self.labelP1.grid(row=self.liste[i]-1,column=2)
            self.valuerep1 = StringVar()
            self.valuerep1.set('%s'%lecture.liste_rep1[lecture.index][i])
            self.labelrep1 = Label(self.o2, textvariable=self.valuerep1)
            self.labelrep1.grid(row=self.liste[i]-1, column=4)
            self.labelPoids11 = Label(self.o2, text="rep")
            self.labelPoids11.grid(row=self.liste[i]-1,column=5)

    def clear(self):
        for widget in self.o2.winfo_children():
            widget.destroy()

    def Li_timer(self):
        self.bouton = Button(self.o2, text="timer", command=lambda: self.decompte(lecture.liste_tpsRepos[lecture.index]))
        self.bouton.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]+1,column=2)
        self.bouton = Button(self.o2, text="previous", command=self.previous_ind)
        self.bouton.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]+2,column=1)
        self.bouton = Button(self.o2, text="next", command=self.next_ind)
        self.bouton.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]+2,column=3)

    def changeText(self):
        lecture.add_index()
        self.values.set(lecture.index)
    
    def define_nom_seance(self):
        self.nomSeance=app.entreeNomSeance.get()
        self.nom=app.entreeNomSeance.get()
        self.ouvrirSeance(self.nomSeance)
    
    def ouvrirSeance(self,nom):
        lecture.lecture(nom)

        self.clear()
        self.Li_nom_seance()
        self.Li_nom_exo()
        self.Li_temps_repos()
        self.Li_nb_serie()
        self.Li_poids_rep()
        self.Li_timer()
        self.Li_timer_but()
        self.Li_poids_rep()


        
    def next_ind(self):
        lecture.add_index()

        self.clear()
        self.Li_nom_seance()
        self.Li_nom_exo()
        self.Li_temps_repos()
        self.Li_nb_serie()
        self.Li_poids_rep()
        self.Li_timer()
        self.Li_timer_but()
        self.Li_poids_rep()

        
    def previous_ind(self):
        lecture.sous_index()

        self.clear()
        self.Li_nom_seance()
        self.Li_nom_exo()
        self.Li_temps_repos()
        self.Li_nb_serie()
        self.Li_poids_rep()
        self.Li_timer()
        self.Li_timer_but()
        self.Li_poids_rep()


    def countdown2(self,t):
        t = int(t)
        while t:
            mins,secs = divmod(t,60)
            timer= '{:02d}:{:02d}'.format(mins,secs)
            print(timer, end="\n")
            time.sleep(1)
            t-=1
        print("FIN DE PAUSE")
        self.popup_showinfo()

    def decompte(self,count=10):
        mins,secs = divmod(int(count),60)
        timer= '{:02d}:{:02d}'.format(mins,secs)
        self.lab.config(text=str(timer))
        if int(count) > 0 :
            self.o2.after(1000,self.decompte, int(count)-1)
        if int(count) == 0 :
            self.popup_showinfo()
            
    def popup_showinfo(self):
        showinfo("Timer", "FIIIIIIIIIN")

    def Li_timer_but(self):
        self.labelsec = Label(self.o2, text="timer entre éxos :")
        self.labelsec.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]-1,column=1)
        self.valuesec = StringVar() 
        self.valuesec.set("4.00")
        self.entreesec = Entry(self.o2, textvariable=self.valuesec, width=4)
        self.entreesec.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]-1, column=2)
#        frac, whole = math.modf(float(self.entreesec.get()))
#        self.bouton = Button(self.o2, text="timer entre éxos", command=lambda: self.decompte(int(whole*60+round(frac,2)*100)))
        self.bouton = Button(self.o2, text="timer entre éxos", command=self.timer_entre_exos)
        self.bouton.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]+2, column=2)
        self.lab=Label(self.o2, text="")
        self.lab.config(font=('Helvatical bold',20))
        self.lab.grid(row=self.liste[int(lecture.liste_nbSerie[lecture.index])]+3, column=2)
        
    def timer_entre_exos(self):
        frac, whole = math.modf(float(self.entreesec.get()))
        self.decompte(int(whole*60+round(frac,2)*100))
        
    def mod_nom_exo(self):
        self.label = Label(self.o3, text="nom exercice :")
        self.label.grid(row=1, column=1)
        self.value = StringVar() 
        self.value.set("")
        self.entreeA = Entry(self.o3, textvariable=self.value, width=20)
        self.entreeA.grid(row=2, column=1)
        self.bouton = Button(self.o3, text="Valider nom exercice", command=lecture.modif_nomExo)
        self.bouton.grid(row=2, column=2)
        
    def mod_nb_serie(self):   
        self.label = Label(self.o3, text="nbr séries")
        self.label.grid(row=3, column=1)
        self.value1 = StringVar() 
        self.value1.set("")
        self.entreeB = Entry(self.o3, textvariable=self.value1, width=20)
        self.entreeB.grid(row=4, column=1)
        self.bouton = Button(self.o3, text="modifier Nb Séries", command=lecture.modif_nbSeries)
        self.bouton.grid(row=4, column=2)
     
    def mod_tpsRepos(self):
        self.label = Label(self.o3, text="tmps (min) (2\'30 => 2.30)")
        self.label.grid(row=5, column=1)
        self.value11 = StringVar() 
        self.value11.set("")
        self.entreeC = Entry(self.o3, textvariable=self.value11, width=20)
        self.entreeC.grid(row=6, column=1)
        self.bouton = Button(self.o3, text="modif tps repos", command=lecture.modif_tpsRepo)
        self.bouton.grid(row=6, column=2)
        
    def mod_poids_rep(self):
        self.label = Label(self.o3, text="poids")
        self.label.grid(row=7, column=1)
        self.value2 = StringVar() 
        self.value2.set("")
        self.entreeD = Entry(self.o3, textvariable=self.value2, width=20)
        self.entreeD.grid(row=8, column=1)
        self.bouton = Button(self.o3, text="modif poids 1", command=lecture.modif_poids1)
        self.bouton.grid(row=8, column=2)
        self.value2H = StringVar() 
        self.value2H.set("")
        self.label = Label(self.o3, text="rep")
        self.label.grid(row=9, column=1)
        self.entreeH = Entry(self.o3, textvariable=self.value2H, width=20)
        self.entreeH.grid(row=10, column=1)
        self.bouton = Button(self.o3, text="modif rep 1", command=lecture.modif_rep1)
        self.bouton.grid(row=10, column=2)
        
    def mod_valider_exo(self):
        self.bouton = Button(self.o3, text="Valider modif", command=lecture.savefile)
        self.bouton.grid(row=11, column=1)


root=tk.Tk()
root.title('WorkOut Soft')
app=Application(master=root)
app.mainloop()

