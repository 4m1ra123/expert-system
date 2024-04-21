from aima3.logic import *



def ForwardChaining(params):
    # create kb

    KB = FolKB()

    results = []

    # Rules

    KB.tell(expr('Techpointe(x) ==> Techcourante(x)'))
    KB.tell(expr('Techcourante(x) ==> Techobs(x)'))
    KB.tell(expr('Prix(x,Bas) ==> Prix(x,Moyen)'))
    KB.tell(expr('Prix(x,Moyen) ==> Prix(x,Eleve)'))

    #Volet Commercial

    KB.tell(expr('Pclient(TIC,Eleve) & Faiblesses(TIC,Modere) & Forces(TIC,Eleve) ==> Faisable(Commercial,TIC)'))
    KB.tell(expr('Pclient(Commerce,Modere) & Concu(Commerce,Faible) & forces(Commerce,Eleve) ==> Faisable(Commercial,Commerce)'))
    KB.tell(expr('Forces(Educ,Eleve) & Faiblesses(Educ,Modere) ==> Faisable(Commercial,Educ)'))

    #Volet Technique

    KB.tell(expr('Techpointe(TIC)  & Stable(TIC)==> Faisable(Technique,TIC)'))
    KB.tell(expr('Organise(Commerce) & Techcourante(Commerce) & Coutprob(Commerce,Modere) ==> Faisable(Technique,Commerce)'))
    KB.tell(expr('Techcourante(Educ)  & Stable(Educ) & Organise(Educ)==> Faisable(Technique,Educ)'))

    #volet Financier

    KB.tell(expr('Retour(TIC,Suffisant) & Cout(TIC,Eleve) ==> Faisable(Financier,TIC)'))
    KB.tell(expr('Prix(Commerce,Moyen) & Cout(Commerce,Moyen) & Retour(Commerce,satisfaisant) & Securitefinance(Commerce) ==> Faisable(Financier,Commerce)'))
    KB.tell(expr('Cout(Educ,bas) & Beneficeatt(Educ,Moyen) ==> Faisable(Financier,Educ)'))

    #Volet Economique

    KB.tell(expr('Responsable(TIC) & Negative(TIC,Faible) ==> Faisable(Economique,TIC) '))
    KB.tell(expr('Negative(Commerce,Faible)  & Responsable(Commerce) ==> Faisable(Economique,Commerce)'))
    KB.tell(expr('Impactemploi(Educ) &  Nonconflits(Educ)  ==> Faisable(Economique,Educ)'))

    #initialisation de l'agenda
    agenda=[]

    #L'ajout des faits récuperés de l'interface a l'agenda et a la KB'

    for param in params:
        KB.tell(expr(param))
        agenda.append(expr(param))
    #Initialisation de la mémoire
    memory={}

    seen=set()

    while  agenda:
        #Utilisation de la methode pop pour l'agenda "LIFO"
        fact=agenda.pop()
        
        if not fact in seen:
            seen.add(fact)
        '''
        Utilisation du forward chaining pour verifier pour chaque fait
        quelles regles sont activees pour les stocker temporairement dans
        working memory 
        '''
        if (list(fol_fc_ask(KB,fact))):
            
            memory[fact]=True
        else:
            memory[fact]=False



    # retourne vrai si la cle est presente dans le dict
    if memory.get(expr('Techpointe(x)'), False):
        agenda.append(expr('Techcourante(x)'))
    if memory.get(expr('Techcourante(x)'), False):
        agenda.append(expr('Techobs(x)'))


    #VOlet Commercial
    if (memory.get(expr('Pclient(TIC,Eleve)'), False) and memory.get(expr('Faiblesses(TIC,Modere)'), False) and 
                              memory.get(expr('Forces(TIC,Eleve)'), False)):
        agenda.append(expr('Faisable(Commercial,TIC)'))

    if (memory.get(expr('Pclient(Commerce,Modere)'), False) and  memory.get(expr('Concu(Commerce,Faible)'), False) and 
                    memory.get(expr('forces(Commerce,Eleve)'), False)):
        agenda.append(expr('Faisable(Commercial,Commerce)'))

    if (memory.get(expr('Forces(Educ,Eleve)'), False) and  memory.get(expr('Faiblesses(Educ,Modere)'), False)):
        agenda.append(expr('Faisable(Commercial,Educ)'))

    #Volet Technique
    if (memory.get(expr('Techpointe(TIC)'), False) and memory.get(expr('Stable(TIC)'), False)):
        agenda.append(expr('Faisable(Technique,TIC)'))

    if (memory.get(expr('Organise(Commerce)'), False) and memory.get(expr('Techcourante(Commerce)'), False) and 
                  memory.get(expr('Coutprob(Commerce,Modere)'), False)):
        
        agenda.append(expr('Faisable(Technique,Commerce)'))

    if (memory.get(expr('Techcourante(Educ)'), False) and memory.get(expr('Stable(Educ)'), False) and 
                 memory.get(expr('Organise(Educ)'), False)):
       
        agenda.append(expr('Faisable(Technique,Educ)'))

    #Volet Financier
    if (memory.get(expr('Retour(TIC,Suffisant)'), False) and memory.get(expr('Cout(TIC,Eleve)'), False)):
        
        agenda.append(expr('Faisable(Financier,TIC)'))

    if (memory.get(expr('Prix(Commerce,Moyen)'), False) and memory.get(expr('Cout(Commerce,Moyen)'), False) and 
     memory.get(expr('Retour(Commerce,satisfaisant)'), False) and memory.get(expr('Securitefinance(Commerce)'), False)):
            
            agenda.append(expr('Faisable(Financier,Commerce)'))

    if (memory.get(expr('Cout(Educ,bas)'), False) and  memory.get(expr('Beneficeatt(Educ,Moyen)'), False)):
       
         agenda.append(expr('Faisable(Financier,Educ)'))

    #Volet Economique

    if (memory.get(expr('Responsable(TIC)'), False) and memory.get(expr('Negative(TIC,Faible)'), False)):
        
        agenda.append(expr('Faisable(Economique,TIC)'))

    if (memory.get(expr('Negative(Commerce,Faible)'), False) and memory.get(expr('Responsable(Commerce)'), False)):
        
        agenda.append(expr('Faisable(Economique,Commerce)'))

    if (memory.get(expr('Impactemploi(Educ)'), False) and memory.get(expr('Nonconflits(Educ)'), False)):
        
        agenda.append(expr('Faisable(Economique,Educ)'))


    print(f'Agenda: {agenda}')

    return agenda























    #temp = fol_fc_ask(KB, expr('Faisable(y,x)'))
    #l = list(temp)
    #print(l)
    print("Le retour\n")
    
    
    #return l