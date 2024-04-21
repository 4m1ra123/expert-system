from flask import Flask, render_template, redirect, request, session
from inference import ForwardChaining


app = Flask(__name__)
app.secret_key = "votre_clé_secrète"  # Clé secrète nécessaire pour utiliser la session


#Ne pas oublier l'utilisation des sessions pour sauvegarder les donnees recuperees d'une page a une autre.


@app.route('/',methods = ['GET'])
def MainPage():
    
    session['reconomic']=[]
    session['rfinancial']=[]
    session['rtechnical']=[]
    session['rcommercial']=[]
    return render_template("firstPage.html")


@app.route('/secondPage.html',methods = ['GET'])
def index():
    return render_template("secondPage.html")


@app.route('/thirdPage.html',methods = ['GET'])
def index2():

    return render_template("thirdPage.html")


@app.route('/thirdPage.html',methods = ['POST'])
def sector():
    secteur = request.form.get('options')
    session['secteur'] = secteur  # Stockage de la variable secteur dans la session
    print(secteur)
    return redirect("commercialAspect.html")
    



@app.route('/commercialAspect.html',methods = ['GET'])
def commercial_aspect():

    secteur=session.get('secteur')
    print(secteur)
    return render_template("commercialAspect.html")




@app.route('/commercialAspect.html',methods = ['POST'])
def resultcommercial_aspect(): 


    secteur=session.get('secteur')
    print(secteur)

    commercial = [request.form.get('q1')
    , request.form.get('q2')
    , request.form.get('q3')
    , request.form.get('q4')
    , request.form.get('q5')
    ]
    print(commercial)

    session['commercial']= commercial
    return redirect("technicalAspect.html")






@app.route('/technicalAspect.html',methods = ['GET'])
def technicalaspect():
    return render_template("technicalAspect.html")



@app.route('/technicalAspect.html',methods = ['POST'])
def resulttechnical_aspect():
    
    technical = [request.form.get('q1')
    , request.form.get('q2')
    , request.form.get('q3')
    , request.form.get('q4')
    ]
    print(technical)
  

    session['technical']= technical
    return redirect("economicAspect.html")






@app.route('/economicAspect.html',methods = ['GET'])
def economic_aspect():

    secteur=session.get('secteur')
    print(secteur)
    return render_template("economicAspect.html")




@app.route('/economicAspect.html',methods = ['POST'])
def resulteconomic_aspect(): 



    economic = [request.form.get('q1')
    , request.form.get('q2')
    , request.form.get('q3')
    , request.form.get('q4')
   
    ]
    print(economic)

    session['economic']= economic
    return redirect("financialAspect.html")



@app.route('/financialAspect.html',methods = ['GET'])
def financial_aspect():

    secteur=session.get('secteur')
    print(secteur)
    return render_template("financialAspect.html")






@app.route('/financialAspect.html',methods = ['POST'])
def resultpage(): 
    financial = [request.form.get('q1')
    , request.form.get('q2')
    , request.form.get('q3')
    , request.form.get('q4')
   , request.form.get('q5')
    ]
    print(financial)

    commercial=session.get('commercial')
    economic=session.get('economic')
    technical=session.get('technical')

    # Création d'une liste pour toutes les réponses
    working_mem = []

    # Ajout des réponses financières à la liste
    working_mem.extend(filter(lambda x: x is not None and x != '', financial))

    # Ajout des réponses commerciales, économiques et techniques à la liste
    working_mem.extend(filter(lambda x: x is not None and x != '', commercial))
    working_mem.extend(filter(lambda x: x is not None and x != '', economic))
    working_mem.extend(filter(lambda x: x is not None and x != '', technical))

    print(working_mem)


    # Nouvelle liste pour stocker les réponses avec la substitution
    secteur=session.get('secteur')
    params = []

    # Boucle à travers toutes les réponses
    for response in working_mem:
        if response and 'externalites' not in response:
            # Substituer toutes les occurrences de 'x' par 'secteur' sauf dans 'externalites'
            response = response.replace('x', secteur)
        # Ajouter la réponse modifiée à la nouvelle liste
        params.append(response)

    print(params)

    results = ForwardChaining(params)
    print(results)

    if results==[]:
        result='Votre projet n\'est realisable sur aucun aspect'

        reconomic = 'non-feasible'

        rfinancial = 'non-feasible'

        rtechnical = 'non-feasible'

        rcommercial = 'non-feasible'


        session['reconomic']=reconomic
        session['rfinancial']=rfinancial
        session['rtechnical']=rtechnical
        session['rcommercial']=rcommercial

        session['result']=result
        session['secteur']=secteur
        return redirect("result.html")
    
    else:
    

        rcommercial="Feasible"
        rtechnical="Feasible"
        rfinancial="Feasible"
        reconomic="Feasible"

        required_aspects = {
        'TIC': ['Commercial', 'Technique', 'Financier', 'Economique'],
        'Educ': ['Commercial', 'Technique', 'Financier', 'Economique'],
        'Commerce': ['Commercial', 'Technique', 'Financier', 'Economique']
        }

        # Initialize a set to keep track of missing aspects for the current sector
        missing_aspects = set(required_aspects[secteur])

        # Iterate through results to identify missing aspects for the current sector
        for result in results:
            # Parse the aspect and sector from the result
            aspect, result_sector = str(result).split("(")[1].split(")")[0].split(",")
            
            # Check if the result is for the current sector
            if result_sector.strip() == secteur:
                # Remove the aspect from missing aspects if it's found in the result
                if aspect.strip() in missing_aspects:
                    missing_aspects.remove(aspect.strip())

        # Check if there are any missing aspects for the current sector
        if not missing_aspects:
            print(f"The project is feasible in all aspects for {secteur}.")
            result = f"The project is feasible in all aspects for {secteur}."
        else:
            print(f"The project is not feasible in all aspects for {secteur}. ")
            result = f"The project is not feasible in all aspects for {secteur}."

        if 'Commercial' in missing_aspects:
            rcommercial = 'non-feasible'
        if 'Technique' in missing_aspects:
            rtechnical = 'non-feasible'
        if 'Financier' in missing_aspects:
            rfinancial = 'non-feasible'
        if 'Economique' in missing_aspects:
            reconomic = 'non-feasible'


        session['reconomic']=reconomic
        session['rfinancial']=rfinancial
        session['rtechnical']=rtechnical
        session['rcommercial']=rcommercial

        session['result']=result
        session['secteur']=secteur

        return redirect("result.html")





@app.route('/result.html',methods = ['get'])
def explanation():
    reconomic=session.get('reconomic')
    rcommercial=session.get('rcommercial')
    rfinancial=session.get('rfinancial')
    rtechnical=session.get('rtechnical')


    result=session.get('result')
    secteur=session.get('secteur')
    session['technical']=[]
    session['secteur']=[]
    session['commercial']=[]
    session['economic']=[]
    # Initialisation des variables pour les directives et les conseils
    directive = ""
    advice = ""

    # Directives et advices pour le secteur TIC
    if secteur == 'TIC':
        if reconomic == 'Feasible':
            directive += "- The TIC project is deemed economically feasible. Reasons:\n"
            directive += "  - It is managed by a responsible entity and has a low negative impact.\n"
            advice += "- For the TIC project, identify ways to reduce the negative impact while capitalizing on the project's positive aspects to support economic growth and foster innovation.\n"
        else:
            directive += "- The TIC project is deemed non-economically feasible. Reasons:\n"
            directive += "  - Despite being managed by a responsible entity, its negative impact is significant.\n"
            advice += "- For the TIC project, explore initiatives that promote employment and contribute to the creation of a sustainable economic environment, such as vocational training programs or partnerships with local businesses.\n"

        if rcommercial == 'Feasible':
            directive += "- The TIC project is deemed commercially feasible. Reasons:\n"
            directive += "  - It presents a high potential clientele, with significant strengths and moderate weaknesses.\n"
            advice += "- For the TIC project, ensure to capitalize on its high potential clientele by developing targeted marketing strategies and reinforcing your strengths.\n"
        else:
            directive += "- The TIC project is deemed non-commercially feasible. Reasons:\n"
            directive += "  - It presents a moderate clientele with a weak concept.\n"
            advice += "- For the TIC project, consider revisiting your marketing and sales plan to better target your audience and review your concept to make it more marketable.\n"

        if rfinancial == 'Feasible':
            directive += "- The TIC project is deemed financially feasible. Reasons:\n"
            directive += "  - It ensures a sufficient return despite a high cost.\n"
            advice += "- For the TIC project, manage costs wisely despite satisfactory returns by identifying ways to optimize expenses and exploring additional sources of funding if necessary.\n"
        else:
            directive += "- The TIC project is deemed non-financially feasible. Reasons:\n"
            directive += "  - Despite ensuring a sufficient return, its cost is high.\n"
            advice += "- For the TIC project, reconsider your financial strategy and seek ways to reduce costs while maintaining the economic viability of the project.\n"

        if rtechnical == 'Feasible':
            directive += "- The TIC project is deemed technically feasible. Reasons:\n"
            directive += "  - It is technologically advanced and stable.\n"
            advice += "- For the TIC project, continue to maintain cutting-edge technology and stability by staying updated with the latest trends and investing in research and development.\n"
        else:
            directive += "- The TIC project is deemed non-technically feasible. Reasons:\n"
            directive += "  - Despite being technologically advanced, it is not stable.\n"
            advice += "- For the TIC project, identify technical gaps and invest in solutions to strengthen stability and performance.\n"





    if secteur == 'Educ':
        if reconomic == 'Feasible':
            directive += "- The Education project is deemed economically feasible. Reasons:\n"
            directive += "  - It has an impact on employment and presents no conflicts.\n"
            advice += "- For the Education project, explore initiatives that promote employment and contribute to the creation of a sustainable economic environment, such as vocational training programs or partnerships with local businesses.\n"
        else:
            directive += "- The Education project is deemed non-economically feasible. Reasons:\n"
            directive += "  - Despite having an impact on employment, it presents conflicts.\n"
            advice += "- For the Education project, explore alternative economic models and strategies to enhance its contribution to the economy while addressing feasibility issues.\n"

        if rcommercial == 'Feasible':
            directive += "- The Education project is deemed commercially feasible. Reasons:\n"
            directive += "  - It has high strengths and moderate weaknesses.\n"
            advice += "- For the Education project, highlight your strengths and focus on aspects of the project that are appealing to your target audience, such as innovative educational programs or strategic partnerships.\n"
        else:
            directive += "- The Education project is deemed non-commercially feasible. Reasons:\n"
            directive += "  - Despite having high strengths, it does not meet commercial criteria.\n"
            advice += "- For the Education project, analyze identified weaknesses in your commercial strategy and seek innovative solutions to attract interest from stakeholders and potential investors.\n"

        if rfinancial == 'Feasible':
            directive += "- The Education project is deemed financially feasible. Reasons:\n"
            directive += "  - It has a low cost and a moderate expected profit.\n"
            advice += "- For the Education project, continue to optimize costs to maximize expected benefits and consider investment strategies to strengthen the project's financial viability.\n"
        else:
            directive += "- The Education project is deemed non-financially feasible. Reasons:\n"
            directive += "  - Despite having a low cost, its expected profit is insufficient.\n"
            advice += "- For the Education project, evaluate alternative financing options and explore strategic partnerships to ensure long-term financial viability of the project.\n"

        if rtechnical == 'Feasible':
            directive += "- The Education project is deemed technically feasible. Reasons:\n"
            directive += "  - It is technologically current, stable, and well-organized.\n"
            advice += "- For the Education project, continue to enhance your technical infrastructure to offer a modern and interactive learning experience to users.\n"
        else:
            directive += "- The Education project is deemed non-technically feasible. Reasons:\n"
            directive += "  - Despite being technologically current, it is not stable.\n"
            advice += "- For the Education project, continue to enhance your technical infrastructure to offer a modern and interactive learning experience to users.\n"

    if secteur == 'Commerce':
        if reconomic == 'Feasible':
            directive += "- The Commerce project is deemed economically feasible. Reasons:\n"
            directive += "  - It has a low negative impact and is managed by a responsible entity.\n"
            advice += "- For the Commerce project, adopt responsible business practices to mitigate the negative impact and proactively contribute to local or regional economic development.\n"
        else:
            directive += "- The Commerce project is deemed non-economically feasible. Reasons:\n"
            directive += "  - Despite having a low negative impact, it is not managed by a responsible entity.\n"
            advice += "- For the Commerce project, consider corporate social responsibility initiatives to mitigate negative impact and promote sustainable economic development.\n"

        if rcommercial == 'Feasible':
            directive += "- The Commerce project is deemed commercially feasible. Reasons:\n"
            directive += "  - It has a moderate clientele, a weak concept but high strengths.\n"
            advice += "- For the Commerce project, leverage your high strengths to consolidate your market position and explore ways to enhance your concept to attract a broader clientele.\n"
        else:
            directive += "- The Commerce project is deemed non-commercially feasible. Reasons:\n"
            directive += "  - Despite having a moderate clientele, its concept is weak.\n"
            advice += "- For the Commerce project, identify specific areas that contributed to its commercial infeasibility and explore readjustment strategies to better meet market needs.\n"

        if rfinancial == 'Feasible':
            directive += "- The Commerce project is deemed financially feasible. Reasons:\n"
            directive += "  - It has an average price and cost, with a satisfactory return and financial security.\n"
            advice += "- For the Commerce project, maintain a balance between price and cost to ensure ongoing profitability while exploring financial security solutions to ensure long-term stability.\n"
        else:
            directive += "- The Commerce project is deemed non-financially feasible. Reasons:\n"
            directive += "  - Despite having an average price and cost, its return is not satisfactory.\n"
            advice += "- For the Commerce project, analyze financial aspects that contributed to its infeasibility and develop action plans to optimize financial resources and ensure sustainable growth.\n"

        if rtechnical == 'Feasible':
            directive += "- The Commerce project is deemed technically feasible. Reasons:\n"
            directive += "  - It is well-organized, technologically current with a moderate probable cost.\n"
            advice += "- For the Commerce project, ensure to maintain your organization and stay updated with the latest industry technologies to remain competitive in the constantly evolving market.\n"
        else:
            directive += "- The Commerce project is deemed non-technically feasible. Reasons:\n"
            directive += "  - Despite being well-organized, it is not technologically current.\n"
            advice += "- For the Commerce project, address identified technical challenges by investing in cutting-edge solutions and implementing efficient processes to ensure product or service quality and reliability.\n"




    return render_template("result.html", result=result, secteur=secteur, reconomic=reconomic,
                           rcommercial=rcommercial, rfinancial=rfinancial, rtechnical=rtechnical,
                           directive=directive, advice=advice)



if __name__ == "__main__":
    app.run()