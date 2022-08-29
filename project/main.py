#1. necessary importations:
from flask import Flask, render_template, request, redirect, url_for
import os
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy 
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required
from datetime import datetime, timedelta


#2. Create variables and configure MySQL connection details:
app = Flask(__name__)
db=SQLAlchemy(app)

DATABASE_URL ='postgres://oobcbidulaqvrb:76f6fdf6b9c5e47aac3d297b850566f2a0038683c466b1c2bdf85e9bc70b995a@ec2-44-210-36-247.compute-1.amazonaws.com:5432/d6vtmvq648cu3o'
#DATABASE_URL=
#app.config['SQLALCHEMY_DATABASE_URI']='postgres://kxknemtmelhnoe:5114c7c4a16b5edb4ef1b7d660f9ffba70295a5466465604612222d286f2f384@ec2-3-217-113-25.compute-1.amazonaws.com:5432/d6svlihbs0m18v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# it's for extra protection)
SECRET_KEY = ')6VQ)s*z26B#D*>'

admin = Admin(app,name='Interface Administrateur')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'


#Database Model class
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    email= db.Column(db.String(100))
    visited= db.Column(db.DateTime(timezone=True))


db.session.commit()
admin.add_view(ModelView(User,db.session))    

#Configuration for uploaded files:
UPLOAD_FOLDER_1 = r'C:\Users\lenovo\FlaskProject\project\ConsolidationFiles'
UPLOAD_FOLDER_2 = r'C:\Users\lenovo\FlaskProject\project\BoFiles'
UPLOAD_FOLDER_3 = r'C:\Users\lenovo\FlaskProject\project\Result_ConsolFiles'
UPLOAD_FOLDER_4 = r'C:\Users\lenovo\FlaskProject\project\ControleFiles'
UPLOAD_FOLDER_5 = r'C:\Users\lenovo\FlaskProject\project\Result_ControleBancaire_Files'

ALLOWED_EXTENSIONS = {'xslx'}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/accueil/ChoixControle')
def ChoixControle():
    return render_template("ChoixControle.html")

@app.route('/accueil/historique',methods = ['GET', 'POST'])
def historique():
    return render_template("historique.html")

def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            return os.listdir(path)  

#Affichage des fichiers uploadés dans l'historique; 5 directories
@app.route('/accueil/historique/FichiersDeConsolidations',methods = ['GET', 'POST'])
def consol_file():
    try:
        target="C:/Users/lenovo/FlaskProject/project/ConsolidationFiles"
        files=[]
        for file in get_files(target):
            files.append(file) 
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")   
    return render_template("consol_file.html",files=get_files(target))


@app.route('/accueil/historique/FichiersDeControle',methods = ['GET', 'POST'])
def controle_file():
    try:
        target="C:/Users/lenovo/FlaskProject/project/ControleFiles"
        files=[]
        for file in get_files(target):
            files.append(file)  
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")    
    return render_template("controle_file.html",files=get_files(target))


@app.route('/accueil/historique/FichiersResultatConsolidation',methods = ['GET', 'POST'])
def result_Consolfile():
    try:
        target="C:/Users/lenovo/FlaskProject/project/Result_ConsolFiles"
        files=[]
        for file in get_files(target):
            files.append(file)  
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")    
    return render_template("result_Consolfile.html",files=get_files(target))


@app.route('/accueil/historique/FichiersResultatControleBancaire',methods = ['GET', 'POST'])
def result_Controlefile():
    try:
        target="C:/Users/lenovo/FlaskProject/project/Result_ControleBancaire_Files"
        filee=[]
        for file in get_files(target):
            filee.append(file)   
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")   
    return render_template("result_Controlefile.html",filee=get_files(target))


@app.route('/accueil/historique/FichiersBO',methods = ['GET', 'POST'])
def bo_file():
    try:
        target="C:/Users/lenovo/FlaskProject/project/BoFiles"
        files=[]
        for file in get_files(target):
            files.append(file)   
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")   
    return render_template("bo_file.html",files=get_files(target))

@app.route('/accueil/historique/FichiersBOs',methods = ['GET', 'POST'])
def bo_files():
    try:
        target="C:/Users/lenovo/FlaskProject/project/Result_Comparaison_BO"
        files=[]
        for file in get_files(target):
            files.append(file)   
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")   
    return render_template("bo_files.html",files=get_files(target))



@app.route('/login/', methods = ['POST', 'GET'])
def login():
     
    if request.method == 'POST':
        try:
            username=request.form['username']
            password=request.form['password']
            user = User.query.filter_by(username=username).first()
            if (username=='admin'):
                if(password=='admin'):
                    return redirect('/admin/')
            if user:
                if user.password==password:
                    login_user(user)
                    return redirect(url_for('accueil'))
            else:
                # Account doesnt exist or username/password incorrect
                print('Nom d utilisateur ou mot de passe incorrect') 
                return redirect(url_for('login'))
        except:
            return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
    return render_template('index.html')
 

@app.route('/accueil/')
@login_required
def accueil():
    try:
        return render_template('accueil.html')
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  

@app.route('/accueil/logout/')
def logout():
    try:
        logout_user()
        return redirect(url_for('login'))
    except:
        return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  




@app.route('/accueil/consolidation/',methods = ['POST', 'GET'])
def consolidation():
    #Declarations:
    #pour pouvoir utiliser ces variables par la suite dans toutes les parties du traitement
    global startDate,endDate  
    if request.method == 'POST':
        if request.form['action']=='Valider':
            try:
        #1ère partie concerne la saisie de la date de début et celle de fin:
                startDate=datetime.strptime(request.form['start_date'],'%Y-%m-%d') #Modification de la forme de str à date:
                endDate=datetime.strptime(request.form['end_date'],'%Y-%m-%d') 
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  

        #La 2ème partie concerne le traitement des fichiers de consolidation: 
        if request.form['action']=='Télécharger les fichiers de consolidation':
            try:
                global file,data,files,data0,results
                results = []
                data = []
                file=[] 
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_1
                files = request.files.getlist("uploadExcel")
                for fic in files:
                    fic.save(os.path.join(app.config['UPLOAD_FOLDER'], fic.filename))
                    file.append(fic)
                for i in (range(len(file))) :
                    try:
                    #list of files making
                        data.append(pd.read_excel(file[i], header=11, dtype={'Date' : str}))
                        data[i]=data[i][:-1]
                        if list(data[i].columns)[0]=="Unnamed: 0" :
                            data[i] = data[i].drop(columns = ["Unnamed: 0"])
                        data[i].columns = ['date','v_dtt_support','v_dtt_charge','v_dtt_ab_hebdo','v_dtt_ab_mens',\
                                            'v_dtt_ab_mens_etud','v_agence_support_b','v_agence_support_c','v_agence_voyage',\
                                            'v_agence_ab_hebdo','v_agence_ab_mens',\
                                            'v_agence_ab_mens_etud','v_depo_support_b','v_depo_support_c','v_depo_voyage',\
                                            'v_depo_ab_hebdo','v_depo_ab_mens','v_depo_ab_mens_etud',\
                                            'v_pv_support_b','v_pv_voyage',\
                                            'ca_dtt_support','ca_dtt_charge','ca_dtt_ab_hebdo','ca_dtt_ab_mens',\
                                            'ca_dtt_ab_mens_etud','ca_dtt_banque',\
                                            'ca_agence_support_b','ca_agence_support_c','ca_agence_voyage',\
                                            'ca_agence_ab_hebdo','ca_agence_ab_mens',\
                                            'ca_agence_ab_mens_etud','ca_agence_banque',\
                                            'ca_depo_support_b','ca_depo_support_c','ca_depo_voyage',\
                                            'ca_depo_ab_hebdo','ca_depo_ab_mens','ca_depo_ab_mens_etud',\
                                            'ca_pv_support_b','ca_pv_voyage','rembours_banque','total']
                        #drop nan values in end of file
                        #print(len(data))
                        data[i] = data[i].drop(data[i][data[i]['date'].isnull()].index)
                        data[i] = data[i].fillna(0)

                        #lists initialization
                        e_dtt_support = []
                        e_dtt_charge = []
                        e_dtt_ab_hebdo = []
                        e_dtt_ab_mens = []
                        e_dtt_ab_mens_etud = []
                        e_agence_support_b = []
                        e_agence_support_c = []
                        e_agence_voyage = []
                        e_agence_ab_hebdo = []
                        e_agence_ab_mens = []
                        e_agence_ab_mens_etud = []
                        e_depo_support_b = []
                        e_depo_support_c = []
                        e_depo_voyage = []
                        e_depo_ab_hebdo = []
                        e_depo_ab_mens = []
                        e_depo_ab_mens_etud = []
                        e_pv_support_b = []
                        e_pv_voyage = []

                        #gabs calculation in same file càd différence entre nbr de cartes vendus et prix de leur vente présenté par le prestataire lui-même:
                        e_dtt_support = data[i]['ca_dtt_support'] - (data[i]['v_dtt_support']*2)
                        e_dtt_charge = data[i]['ca_dtt_charge'] - (data[i]['v_dtt_charge']*6)
                        e_dtt_ab_hebdo = data[i]['ca_dtt_ab_hebdo'] - (data[i]['v_dtt_ab_hebdo']*60)
                        e_dtt_ab_mens = data[i]['ca_dtt_ab_mens'] - (data[i]['v_dtt_ab_mens']*230)
                        e_dtt_ab_mens_etud = data[i]['ca_dtt_ab_mens_etud'] - (data[i]['v_dtt_ab_mens_etud']*150)
                        e_agence_support_b = data[i]['ca_agence_support_b'] - (data[i]['v_agence_support_b']*2)
                        e_agence_support_c = data[i]['ca_agence_support_c'] - (data[i]['v_agence_support_c']*15)
                        e_agence_voyage = data[i]['ca_agence_voyage'] - (data[i]['v_agence_voyage']*6)
                        e_agence_ab_hebdo = data[i]['ca_agence_ab_hebdo'] - (data[i]['v_agence_ab_hebdo']*60)
                        e_agence_ab_mens = data[i]['ca_agence_ab_mens'] - (data[i]['v_agence_ab_mens']*230)
                        e_agence_ab_mens_etud = data[i]['ca_agence_ab_mens_etud'] - (data[i]['v_agence_ab_mens_etud']*150)
                        e_depo_support_b = data[i]['ca_depo_support_b'] - (data[i]['v_depo_support_b']*2)
                        e_depo_support_c = data[i]['ca_depo_support_c'] - (data[i]['v_depo_support_c']*15)
                        e_depo_voyage = data[i]['ca_depo_voyage'] - (data[i]['v_depo_voyage']*6)
                        e_depo_ab_hebdo = data[i]['ca_depo_ab_hebdo'] - (data[i]['v_depo_ab_hebdo']*60)
                        e_depo_ab_mens = data[i]['ca_depo_ab_mens'] - (data[i]['v_depo_ab_mens']*230)
                        e_depo_ab_mens_etud = data[i]['ca_depo_ab_mens_etud'] - (data[i]['v_depo_ab_mens_etud']*150)
                        e_pv_support_b = data[i]['ca_pv_support_b'] - (data[i]['v_pv_support_b']*2)
                        e_pv_voyage = data[i]['ca_pv_voyage'] - (data[i]['v_pv_voyage']*6)

                        #dataframe making
                        d = {
                        'Date' : data[i]['date'],
                        'Dtt Ecart support' : e_dtt_support,
                        'Dtt chargement' : e_dtt_charge,
                        'Dtt Ecart Ab Hebdo' : e_dtt_ab_hebdo,
                        'Dtt Ecart Ab Mens' : e_dtt_ab_mens,
                        'Dtt Ecart Ab Mens Etud' : e_dtt_ab_mens_etud,
                        'Agence Ecart support BSC' : e_agence_support_b,
                        'Agence Ecart support CSC' : e_agence_support_c,
                        'Agence Ecart voyage' : e_agence_voyage,
                        'Agence Ecart Ab Hebdo' : e_agence_ab_hebdo,
                        'Agence Ecart Ab Mens' : e_agence_ab_mens,
                        'Agence Ecart Ab Mens Etud' : e_agence_ab_mens_etud,
                        'Depo Ecart support BSC' : e_depo_support_b,
                        'Depo Ecart support CSC' : e_depo_support_c,
                        'Depo Ecart voyage' : e_depo_voyage,
                        'Depo Ecart Ab Hebdo' : e_depo_ab_hebdo,
                        'Depo Ecart Ab Mens' : e_depo_ab_mens,
                        'Depo Ecart Ab Mens Etud' : e_depo_ab_mens_etud,
                        'PV Ecart support BSC' : e_pv_support_b,
                        'PV Ecart voyage' : e_pv_voyage
                        }
                        #gabs dataframe
                        results.append(pd.DataFrame(data = d))

                        #affichage colonne de l'erreur si ecart != 0
                        for j in range(len(results[i])) :
                            if results[i]['Dtt Ecart support'][j] != 0 :
                                phrase="Probleme DTT Support"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if results[i]['Dtt chargement'][j] != 0  :
                                phrase="Probleme DTT Chargement"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if results[i]['Dtt Ecart Ab Hebdo'][j] != 0  :
                                phrase="Probleme DTT Ab Hebdo"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if results[i]['Dtt Ecart Ab Mens'][j] != 0 :
                                phrase="Probleme DTT Ab Mens" 
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if (results[i]['Dtt Ecart Ab Mens Etud'][j] != 0) :
                                print(results[i]['Date'][j]+" : Probleme DTT Ab Mens Etud\n")
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if (results[i]['Agence Ecart support BSC'][j] != 0) :
                                phrase="Probleme Agence support BSC"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if (results[i]['Agence Ecart support CSC'][j] != 0) :
                                phrase="Probleme Agence support CSC"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if (results[i]['Agence Ecart voyage'][j] != 0) :
                                phrase="Probleme Agence Voyage"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)  
                            if (results[i]['Agence Ecart Ab Hebdo'][j] != 0) :
                                phrase="Probleme Agence Ab Hebdo"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                
                            if (results[i]['Agence Ecart Ab Mens'][j] != 0) :
                                phrase="Probleme Agence Ab Mens"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)               
                            if (results[i]['Agence Ecart Ab Mens Etud'][j] != 0) :
                                phrase="Probleme Agence Ab Mens Etud"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                
                            if (results[i]['Depo Ecart support BSC'][j] != 0) :
                                phrase="Probleme Depo support BSC"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)               
                            if (results[i]['Depo Ecart support CSC'][j] != 0) :
                                phrase="Probleme Depo support CSC"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                                     
                            if (results[i]['Depo Ecart voyage'][j] != 0) :
                                phrase="Probleme Depo Voyage"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            if (results[i]['Depo Ecart Ab Hebdo'][j] != 0) :
                                phrase="Probleme Depo Ab Hebdo"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                      
                            if (results[i]['Depo Ecart Ab Mens'][j] != 0) :
                                phrase="Probleme Depo Ab Mens"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                     
                            if (results[i]['Depo Ecart Ab Mens Etud'][j] != 0) :
                                phrase="Probleme Depo Ab Mens Etud" 
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                    
                            if (results[i]['PV Ecart support BSC'][j] != 0) :
                                phrase="Probleme PV Support BSC"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)                     
                            if results[i]['PV Ecart voyage'][j] != 0 :
                                phrase="Probleme PV Voyage"
                                var=results[i]['Date'][j]
                                return render_template('Probleme.html',phrase=phrase,var=var)
                            
                    except Exception as e :
                        print(e)
                    #continue
                data0 = data[0]
                #match the dates in 2 files
                for i in range(1,len(file)):
                    data1 = data[i]
                    for d0,date_0 in data0['date'].items():
                        for d1,date_1 in data1['date'].items():
                            if (str(date_0) == str(date_1)) and str(date_0) != 'Total':
                                #put sums in file #iloc[row,column]
                                #vente : update old values 
                                data0.iloc[d0, data0.columns.get_loc('v_dtt_support')] = (float(data0['v_dtt_support'][d0]) + float(data1['v_dtt_support'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_dtt_charge')] = (float(data0['v_dtt_charge'][d0]) + float(data1['v_dtt_charge'][d1]))                               
                                data0.iloc[d0, data0.columns.get_loc('v_dtt_ab_hebdo')] = (float(data0['v_dtt_ab_hebdo'][d0]) + float(data1['v_dtt_ab_hebdo'][d1]))        
                                data0.iloc[d0, data0.columns.get_loc('v_dtt_ab_mens')] = (float(data0['v_dtt_ab_mens'][d0]) + float(data1['v_dtt_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_dtt_ab_mens_etud')] = (float(data0['v_dtt_ab_mens_etud'][d0]) + float(data1['v_dtt_ab_mens_etud'][d1]))     
                                data0.iloc[d0, data0.columns.get_loc('v_agence_support_b')] = (float(data0['v_agence_support_b'][d0]) + float(data1['v_agence_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_agence_support_c')] = (float(data0['v_agence_support_c'][d0]) + float(data1['v_agence_support_c'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_agence_voyage')] = (float(data0['v_agence_voyage'][d0]) + float(data1['v_agence_voyage'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_agence_ab_hebdo')] = (float(data0['v_agence_ab_hebdo'][d0]) + float(data1['v_agence_ab_hebdo'][d1]))   
                                data0.iloc[d0, data0.columns.get_loc('v_agence_ab_mens')] = (float(data0['v_agence_ab_mens'][d0]) + float(data1['v_agence_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_agence_ab_mens_etud')] = (float(data0['v_agence_ab_mens_etud'][d0]) + float(data1['v_agence_ab_mens_etud'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_support_b')] = (float(data0['v_depo_support_b'][d0]) + float(data1['v_depo_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_support_c')] = (float(data0['v_depo_support_c'][d0]) + float(data1['v_depo_support_c'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_voyage')] = (float(data0['v_depo_voyage'][d0]) + float(data1['v_depo_voyage'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_ab_hebdo')] = (float(data0['v_depo_ab_hebdo'][d0]) + float(data1['v_depo_ab_hebdo'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_ab_mens')] = (float(data0['v_depo_ab_mens'][d0]) + float(data1['v_depo_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_depo_ab_mens_etud')] = (float(data0['v_depo_ab_mens_etud'][d0]) + float(data1['v_depo_ab_mens_etud'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_pv_support_b')] = (float(data0['v_pv_support_b'][d0]) + float(data1['v_pv_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('v_pv_voyage')] = (float(data0['v_pv_voyage'][d0]) + float(data1['v_pv_voyage'][d1]))

                                #ca : update old values 
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_support')] = (float(data0['ca_dtt_support'][d0]) + float(data1['ca_dtt_support'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_charge')] = (float(data0['ca_dtt_charge'][d0]) + float(data1['ca_dtt_charge'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_ab_hebdo')] = (float(data0['ca_dtt_ab_hebdo'][d0]) + float(data1['ca_dtt_ab_hebdo'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_ab_mens')] = (float(data0['ca_dtt_ab_mens'][d0]) + float(data1['ca_dtt_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_ab_mens_etud')] = (float(data0['ca_dtt_ab_mens_etud'][d0]) + float(data1['ca_dtt_ab_mens_etud'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_dtt_banque')] = (float(data0['ca_dtt_banque'][d0]) + float(data1['ca_dtt_banque'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_support_b')] = (float(data0['ca_agence_support_b'][d0]) + float(data1['ca_agence_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_support_c')] = (float(data0['ca_agence_support_c'][d0]) + float(data1['ca_agence_support_c'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_voyage')] = (float(data0['ca_agence_voyage'][d0]) + float(data1['ca_agence_voyage'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_ab_hebdo')] = (float(data0['ca_agence_ab_hebdo'][d0]) + float(data1['ca_agence_ab_hebdo'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_ab_mens')] = (float(data0['ca_agence_ab_mens'][d0]) + float(data1['ca_agence_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_ab_mens_etud')] = (float(data0['ca_agence_ab_mens_etud'][d0]) + float(data1['ca_agence_ab_mens_etud'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_agence_banque')] = (float(data0['ca_agence_banque'][d0]) + float(data1['ca_agence_banque'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_support_b')] = (float(data0['ca_depo_support_b'][d0]) + float(data1['ca_depo_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_support_c')] = (float(data0['ca_depo_support_c'][d0]) + float(data1['ca_depo_support_c'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_voyage')] = (float(data0['ca_depo_voyage'][d0]) + float(data1['ca_depo_voyage'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_ab_hebdo')] = (float(data0['ca_depo_ab_hebdo'][d0]) + float(data1['ca_depo_ab_hebdo'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_ab_mens')] = (float(data0['ca_depo_ab_mens'][d0]) + float(data1['ca_depo_ab_mens'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_depo_ab_mens_etud')] = (float(data0['ca_depo_ab_mens_etud'][d0]) + float(data1['ca_depo_ab_mens_etud'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_pv_support_b')] = (float(data0['ca_pv_support_b'][d0]) + float(data1['ca_pv_support_b'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('ca_pv_voyage')] = (float(data0['ca_pv_voyage'][d0]) + float(data1['ca_pv_voyage'][d1]))
                                data0.iloc[d0, data0.columns.get_loc('total')] = (float(data0['total'][d0]) + float(data1['total'][d1]))
                                #drop matched dates from file 1
                                data1= data1.drop([d1])           
                    data0 = pd.concat([data0,data1])
                    data0 = data0.reset_index(drop=True)
    
                #data0 = data0 = data0[:-1]  
                start = datetime.strptime(str(startDate),'%Y-%m-%d %H:%M:%S')
                end = datetime.strptime(str(endDate),'%Y-%m-%d %H:%M:%S')          
                for k in range(len(data0)):
                    if(datetime.strptime(data0['date'][k],'%Y-%m-%d %H:%M:%S')<start or datetime.strptime(data0['date'][k],'%Y-%m-%d %H:%M:%S')>end):
                        data0 = data0.drop([k])

                data0 = data0.reset_index(drop=True)
                data0 = data0.sort_values(by=['date'])
                depart=startDate.strftime("%Y-%m-%d")
                fin=endDate.strftime("%Y-%m-%d")
                data0.to_excel(r'C:\Users\lenovo\FlaskProject\project\GeneratedConsolFiles\Fichier_De_Consolidation_Générée_Du_'+str(depart)+'_Au_'+str(fin)+'.xlsx',index=False)
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
            
        #UPload file BO + Son Traitement:
        if request.form['action']=='Télécharger le fichier BO':
            try:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_2
                f = request.files['uploadBo']
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
                data_BO = pd.read_excel(f) 
                data_BO = data_BO[:-1]  #delete total row

                #Calcul totaux dtt agence depo 
                dtt_total = data0["ca_dtt_support"] + data0["ca_dtt_charge"] + data0["ca_dtt_ab_hebdo"] + data0["ca_dtt_ab_mens"] + data0["ca_dtt_ab_mens_etud"] 
                data0.insert(25, 'dtt_total', dtt_total)
                
                agence_total = data0["ca_agence_support_b"] + data0["ca_agence_support_c"] + data0["ca_agence_voyage"] + data0["ca_agence_ab_hebdo"] + data0["ca_agence_ab_mens"] + data0["ca_agence_ab_mens_etud"] 
                data0.insert(33, 'agence_total', agence_total)
                
                depo_total = data0["ca_depo_support_b"] + data0["ca_depo_support_c"] + data0["ca_depo_voyage"] + data0["ca_depo_ab_hebdo"] + data0["ca_depo_ab_mens"] + data0["ca_depo_ab_mens_etud"]
                data0.insert(41, 'depo_total', depo_total)

                data0 = data0.sort_values(by=['date'])

                data0.insert(26, 'dtt_BO', data_BO['DTT'])
                data0.insert(35, 'agence_BO', data_BO['TPV'])
                data0.insert(44, 'depo_BO', data_BO['TV'])
                #drop usless columns
                data0 = data0.drop(data0.iloc[:, 1:21],axis = 1)
                #total columns coloration
                def highlight_cols(s):
                    color = 'yellow'
                    return 'background-color: %s' % color

                data0 = data0.style.applymap(highlight_cols, subset=pd.IndexSlice[:, ['dtt_total','agence_total', 'depo_total']])

                depart=startDate.strftime("%Y-%m-%d")
                fin=endDate.strftime("%Y-%m-%d")
                
                data0.to_excel(r'C:\Users\lenovo\FlaskProject\project\Result_ConsolFiles\Fichier_Resultat_Du_'+str(depart)+'_Au_'+str(fin)+'.xlsx',index=False)
                
                file_result =r'C:\Users\lenovo\FlaskProject\project\Result_ConsolFiles\Fichier_Resultat_Du_'+str(depart)+'_Au_'+str(fin)+'.xlsx'
                file_conso = file_result
                data_conso = pd.read_excel(file_conso)

                dtt_total=data_conso["dtt_total"].sum()
                agence_total=data_conso["agence_total"].sum()
                depo_total=data_conso["depo_total"].sum()

                dtt_total_bo=data_BO["DTT"].sum()
                agence_total_bo=data_BO["TPV"].sum()
                depo_total_bo=data_BO["TV"].sum()
                
                global ecart_dtt,ecart_agence,ecart_depositaire

                if float(dtt_total_bo) != float(dtt_total) :
                    ecart_dtt=float(dtt_total_bo) - float(dtt_total)
                else : 
                    ecart_dtt=0

                if float(agence_total_bo) != float(agence_total) :
                    ecart_agence=float(agence_total_bo) - float(agence_total)
                else : 
                    ecart_agence=0

                if float(depo_total_bo) != float(depo_total) :
                    ecart_depositaire=float(depo_total_bo) - float(depo_total)
                else : 
                    ecart_depositaire=0

                return render_template("resultat_consol.html",startDate=startDate,endDate=endDate,ecart_dtt=ecart_dtt,ecart_agence=ecart_agence,ecart_depositaire=ecart_depositaire,depart=depart,fin=fin)
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  

    return render_template('consolidation.html')


#Controle Bancaire par date de transaction:
@app.route('/accueil/ChoixControle/controleTransaction/',methods = ['POST', 'GET'])
def controleTransaction():
    #Declarations:
    global startDate,endDate  #pour pouvoir utiliser ces variables par la suite dans le traitement
    global result,fil
    if request.method == 'POST':
        #1ère partie concerne la saisie de la date de début et celle de fin:
        if request.form['action']=='Confirmer':
            try:
                startDate=datetime.strptime(request.form['startdate'],'%Y-%m-%d') #Modification de la forme de str à date:
                endDate=datetime.strptime(request.form['enddate'],'%Y-%m-%d')
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")             

        #La 2ème partie concerne le traitement des transactions:
        if request.form['action']=='Télécharger le fichier du contrôle bancaire':
            try:
                fil = []
                result = []
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_4
                fil= request.files['uploadExcels']
                fil.save(os.path.join(app.config['UPLOAD_FOLDER'], fil.filename))
                #concat all transactions
                result = pd.concat(pd.read_excel(fil, sheet_name=None) , ignore_index=True)
                #Rename columns, drop ...
                result = result.drop(columns=['Nom Commerçant', 'N° Commerçant', 'PTID', 'N° Carte', 'Type carte'])
                result = result.rename(columns={'Date Transaction':'Date et Heure Transaction','Montant ':'Montant Naps'}, inplace = False) 
                result['Date et Heure Transaction']= pd.to_datetime(result['Date et Heure Transaction'])
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
              
           
        #UPload file BO + Traitements:
        if request.form['action']=='Télécharger le fichier BO':
            try:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_2
                file_BO = request.files['uploadBoe']
                file_BO.save(os.path.join(app.config['UPLOAD_FOLDER'], file_BO.filename))
                data_BO = pd.read_excel(file_BO)

                data_BO['Date et Heure Transaction']= pd.to_datetime(data_BO['Date et Heure Transaction'])
                data_BO = data_BO.rename(columns={'Montant':'Montant BO'}, inplace = False) 
                
                #set seconds to 0:
                data_BO['Date et Heure Transaction'] = data_BO['Date et Heure Transaction'].apply(lambda t: t.replace(second=0))
                result['Date et Heure Transaction'] = result['Date et Heure Transaction'].apply(lambda t: t.replace(second=0))

                result = result.groupby(by=["Date et Heure Transaction"]).sum()
                result = result.reset_index()

                #Calcul de l'écart:
                result1 = result.merge(data_BO, on = ["Date et Heure Transaction"], how="outer")
                result1 = result1.fillna(0)
                result1['Ecart Naps/BO'] = result1['Montant Naps'] - result1['Montant BO'] 
            
                #Préparation du fichier résultat:
                depart=startDate.strftime("%Y-%m-%d")
                fin=endDate.strftime("%Y-%m-%d")
                result1.to_excel(r'C:\Users\lenovo\FlaskProject\project\Result_ControleBancaire_Files\Ecart_Bancaire_Transaction_Du_'+str(depart)+'_Au_'+str(fin)+'.xlsx',index=False)
                return render_template("result_controleBancaireTransaction.html",depart=depart,fin=fin)
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
            
    return render_template('controleParTransaction.html')




#Controle Bancaire par date de traitement:
@app.route('/accueil/ChoixControle/controleTraitement/',methods = ['POST', 'GET'])
def controleTraitement():
    #Declarations:
    global startDate,endDate  #pour pouvoir utiliser ces variables par la suite dans le traitement
    global result,fil
    if request.method == 'POST':
        #1ère partie concerne la saisie de la date de début et celle de fin:
        if request.form['action']=='Confirmer':
            try:
                startDate=datetime.strptime(request.form['startdate'],'%Y-%m-%d') #Modification de la forme de str à date:
                endDate=datetime.strptime(request.form['enddate'],'%Y-%m-%d')    
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")         

        #La 2ème partie concerne le traitement des transactions:
        if request.form['action']=='Télécharger le fichier du contrôle bancaire':
            try:
                fil = []
                result = []
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_4
                fil= request.files['uploadExcels']
                fil.save(os.path.join(app.config['UPLOAD_FOLDER'], fil.filename))
                #concat all transactions
                result = pd.concat(pd.read_excel(fil, sheet_name=None) , ignore_index=True)
                result = result.rename(columns={'Date Transaction':'Date et Heure Transaction','Montant ':'Montant'}, inplace = False) 
                result['Date Traitement']= pd.to_datetime(result['Date Traitement'])
                result = result.rename(columns={'Montant':'Montant Naps'}, inplace = False)
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
              
           
        #UPload file BO + Traitements:
        if request.form['action']=='Télécharger le fichier BO':
            try:
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_2
                file_BO = request.files['uploadBoe']
                file_BO.save(os.path.join(app.config['UPLOAD_FOLDER'], file_BO.filename))
                data_BO = pd.read_excel(file_BO)

                data_BO['Date et Heure Transaction']= pd.to_datetime(data_BO['Date et Heure Transaction'])
                data_BO = data_BO.rename({'Montant':'Montant BO'}, inplace = False) 
                data_BO = data_BO.rename(columns={'Montant':'Montant BO'}, inplace = False) 

                #Date traitement
                data_BO['Date Traitement'] = data_BO['Date et Heure Transaction'].apply(lambda t: t.replace(second=0))
                        
                #group by date
                result = result.groupby(by=["Date Traitement"]).sum()
                result = result.reset_index()

                #Calcul de l'écart:
                result1 = result.merge(data_BO, on = ["Date Traitement"], how="outer")
                result1 = result1.fillna(0)
                result1['Ecart Naps/BO'] = result1['Montant Naps'] - result1['Montant BO'] 
        
                #Préparation du fichier résultat:
                depart=startDate.strftime("%Y-%m-%d")
                fin=endDate.strftime("%Y-%m-%d")
                result1.to_excel(r'C:\Users\lenovo\FlaskProject\project\Result_ControleBancaire_Files\Ecart_Bancaire_Transaction_Traitement_Du_'+str(depart)+'_Au_'+str(fin)+'.xlsx',index=False)
                return render_template("result_controleBancaireTraitement.html",depart=depart,fin=fin)
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
            
    return render_template('controleParTraitement.html')




#Comparaison entre 2 fichiers BO:
@app.route('/accueil/ComparaisonBO/',methods = ['POST', 'GET'])
def comparaison():
    #Declarations:
    global result,fil
    if request.method == 'POST':    
        global startDate  
        global result,fil

        #1ère partie concerne la date; la date n'intervient pas dans le traitement mais permet la nomenclature du fichier résultat généré
        if request.form['action']=='Confirmer':
            try:
                startDate=datetime.strptime(request.form['startdate'],'%Y-%m-%d') 
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  


        #1er fichier BO:
        if request.form['action']=='Télécharger le 1er fichier BO':
            try:
                fil = []
                result = []
                app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_2
                fil= request.files['uploadExcels']
                fil.save(os.path.join(app.config['UPLOAD_FOLDER'], fil.filename))
                result = pd.read_excel(fil)
                result =result[:-1]

                result['Date']= pd.to_datetime(result['Date'])
                result = result.rename(columns={'DTT':'DTT_BO1'}, inplace = False)
                result = result.rename(columns={'TPV':'TPV_BO1'}, inplace = False)
                result = result.rename(columns={'TV':'TV_BO1'}, inplace = False)
                #Drop "Somme" column; on n'a pas utilisé un simple drop prq le nom de la colonne contient un espace et qui est traité comme caractère spécial
                result = result.loc[:, ~result.columns.str.contains('\s')]
            except:
                return("Errreur d'application : Veuillez demander de l'aide à votre administrateur")  
                
        #2ème fichier BO:
        if request.form['action']=='Télécharger le 2ème fichier BO':
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_2
            file_BO = request.files['uploadBoe']
            file_BO.save(os.path.join(app.config['UPLOAD_FOLDER'], file_BO.filename))
            data_BO = pd.read_excel(file_BO)
            data_BO= data_BO[:-1]

            data_BO['Date']= pd.to_datetime(data_BO['Date'])
            data_BO = data_BO.rename(columns={'DTT':'DTT_BO2'}, inplace = False)
            data_BO = data_BO.rename(columns={'TPV':'TPV_BO2'}, inplace = False)
            data_BO = data_BO.rename(columns={'TV':'TV_BO2'}, inplace = False)
            data_BO = data_BO.loc[:, ~data_BO.columns.str.contains('\s')]

            #Calcul de l'écart:
            result1 = result.merge(data_BO, on = ["Date"], how="left")
            result1 = result1.fillna(0)

            result1['ecart_dtt'] = result1['DTT_BO1'] - result1['DTT_BO2']
            result1['ecart_tpv']= result1['TPV_BO1'] - result1['TPV_BO2'] 
            result1['ecart_tv'] = result1['TV_BO1'] - result1['TV_BO2'] 

            date=startDate.strftime("%Y-%m-%d")
            result1.to_excel(r'C:\Users\lenovo\FlaskProject\project\Result_Comparaison_BO\Comparaison_BO_Du_'+str(date)+'.xlsx',index=False)
            #affichage colonne de l'erreur si ecart != 0
            for j in range(len(result1)) :
                if result1['ecart_dtt'][j] != 0 :
                    phrase="Probleme ecart DTT"
                    var=result1['Date'][j]
                    val=result1['ecart_dtt'][j]
                    return render_template('Probleme_Comparaison.html',phrase=phrase,var=var,val=val,date=date)
                if result1['ecart_tpv'][j] != 0 :
                    phrase="Probleme ecart TPV"
                    var=result1['Date'][j]
                    val=result1['ecart_tpv'][j]
                    return render_template('Probleme_Comparaison.html',phrase=phrase,var=var,val=val,date=date)
                if result1['ecart_tv'][j] != 0 :
                    phrase="Probleme ecart TV"
                    var=result1['Date'][j]
                    val=result1['ecart_tv'][j]
                    return render_template('Probleme_Comparaison.html',date=date,phrase=phrase,var=var,val=val)

            return render_template("result_compare_BO.html",date=date)
    return render_template('comparaisonBO.html')





#if __name__ == '__main__':
 #   app.run(debug=True)



