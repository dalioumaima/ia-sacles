from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
from fuzzywuzzy import fuzz
import os
import unicodedata, re, math 
from web_booster import web_answer

app = Flask(__name__, static_folder="build", static_url_path="/")
CORS(app)
THEMES = {
    "intelligence artificielle": ["intelligence artificielle", "ia", "ai", "artificielle", "machine learning", "inteligence artif","IA","AI"],
    "soft skills": ["soft skill", "softskills", "soft-skills", "compétence douce", "soft", "softs", "compétences","adaptabilité", "communication", "esprit d'équipe", "organisation", "autonomie"],
    "communication": ["communication", "communiquer", "comm","rapport","rapport académique","bibliographie","article"],
    "langues": ["langues", "langage", "anglais", "français", "espagnol", "allemand"],
    "cv": ["cv", "curriculum", "curriculum vitae", "c.v.", "rédaction", "rubrique", "section", "formation","expérience", "expériences", "compétence", "compétences", "photo", "structure", "résumé", "profil","trou dans le cv", "erreur cv", "modèle cv"],
    "entretien": ["entretien", "recrutement", "oral", "interview","questions entretien", "présentation", "préparer entretien", "parlez-moi de vous", "difficile","simulateur", "recrutement", "recruteur","questions difficiles", "présentez-vous", "simulation entretien","entretien technique"],
    "lettre de motivation": ["lettre motivation", "motivation", "Lettre de motivation","normes de lettre de motivation", "titre de lettre", "bullet", "signature", "conclure", "outils lettre","cover letter"],
    "traduction": ["traduction", "translate", "traduire", "traduit", "comment dit-on", "comment dire"],
    "synonyme": ["synonyme", "syno", "donne un synonyme", "autre mot pour"],
    "antonyme": ["antonyme", "anton", "contraires", "contraire", "opposé", "donne un antonyme"],
    "conjugaison": ["conjugaison", "conjuguer", "verbe", "temps", "présent", "imparfait", "passé", "futur"],
    "python": ["python", "py", "pyhton", "piton"],
    "r": ["r", "langage r"],
    "data mining": ["data mining", "datamining", "mining", "extraction données"],
    "scales": ["scales","SCALES","Bootcamps","Study Skills","module Writing and Oratory Skills","plagiat"],
    "mill": ["MILL","mill"],
    "worc": ["Worc","WORC","worc"],
    "STADAC": ["STADAC","stadac","Stadac","outil de programmation"],
    "CS": ["cs","CS","Community Service","citoyenneté","civic engagement"],
    "cap": ["CAP","cap","IELTS","IP", "IP3"],
    "LAPEX": ["lapex","LAPEX","Study Skills","LCSS","Skills Portfolio","Portfolio","LRS","langues","LCSS","exigences linguistiques","progrès en langues","langues étrangères","OTS"],
    "data science": ["data science", "datascience", "data scientist", "science des données"],
    "techniques de recherche d'emploi et stage": ["offres", "plateforme","candidature spontanée", "postuler","recherche", "stage", "emploi", "postuler", "candidature", "offre d'emploi","plateforme emploi", "jobteaser", "indeed", "welcome to the jungle","étranger", "trouver un emploi","travail","job","recherche d'emploi"],
    "linkedin": ["linkedin", "profil linkedin", "compte linkedin", "ajouter sur linkedin", "réseau linkedin","importance linkedin", "recommandation linkedin", "message linkedin", "partager linkedin"],
    "réseautage professionnel": ["réseau","contacts", "piston", "groupe", "meetup", "relations", "réseautage", "contacts pro"],
    "orientation professionnelle": ["projet professionnel", "orientation", "carrière", "m2", "positionnement", "grand groupe", "startup", "PME"],
    "événements professionnels": ["meet & greet", "événement", "intervenant", "agenda", "calendrier", "timide", "observer", "plateforme événement","Meet & Greet", "événements","Meet & Greet","Meet&Greet","Meet and Greet"],
    "valorisation des expériences": ["valoriser", "expériences internationales", "doctorat", "projet académique", "engagement associatif", "compétence transférable"],
    "préparation personnelle": ["préparer", "se sentir prêt", "présentation personnelle", "se présenter", "mentalement"],
    "personnel scales": ["personnel","staff","responsable","manager","academic advisor","program officer","operation officer","qui est","responsable de","en charge de","dirige","encadre","programme Study Skills","programme Lapex","lapex","worc","study skills","stadac","langues","programme des langues","LAPEX","qui t'as crée","programmé"],
    "généralités et questions fréquentes": ["fin d'études", "taille entreprise", "questions fréquentes", "généralités"]
}


base = [

    {
        "question": "C'est quoi l'intelligence artificielle ?",
        "reponse": "C'est la discipline qui vise à faire réaliser à des machines des tâches normalement humaines.",
        "theme": "intelligence artificielle",
        "type": "definition",
        "propositions": [
            "Un langage de programmation",
            "Un ordinateur portable",
            "Un navigateur web"
        ]
    },
    {
        "question": "Définis l'intelligence artificielle.",
        "reponse": "L'intelligence artificielle est un ensemble de méthodes permettant aux machines de simuler des comportements humains.",
        "theme": "intelligence artificielle",
        "type": "definition",
        "propositions": [
            "Une feuille de calcul Excel",
            "Un matériel informatique",
            "Une base de données"
        ]
    },
{
  "question": "Quel domaine fait partie de l'intelligence artificielle ?",
  "reponse": "Traitement du langage naturel",
  "theme": "intelligence artificielle",
  "type": "quiz",
  "propositions": [
    "Traitement du langage naturel",
    "Jardinage",
    "Cuisine"
  ]
},
{
  "question": "L’intelligence artificielle permet…",
  "reponse": "De simuler le raisonnement humain par des machines",
  "theme": "intelligence artificielle",
  "type": "quiz",
  "propositions": [
    "D’augmenter la vitesse d’Internet",
    "De simuler le raisonnement humain par des machines",
    "De créer des fruits"
  ]
},
{
  "question": "À quoi sert le data mining ?",
  "reponse": "À extraire des connaissances cachées dans des données",
  "theme": "data mining",
  "type": "quiz",
  "propositions": [
    "À cuisiner plus vite",
    "À extraire des connaissances cachées dans des données",
    "À traduire des textes"
  ]
},
{
  "question": "Quel outil est utilisé en data mining ?",
  "reponse": "Weka",
  "theme": "data mining",
  "type": "quiz",
  "propositions": [
    "Weka",
    "Word",
    "Excel"
  ]
},
{
  "question": "Quel langage est utilisé en data science ?",
  "reponse": "Python",
  "theme": "data science",
  "type": "quiz",
  "propositions": [
    "Python",
    "HTML",
    "Photoshop"
  ]
},
{
  "question": "La data science sert à…",
  "reponse": "Analyser et valoriser des données",
  "theme": "data science",
  "type": "quiz",
  "propositions": [
    "Dessiner des tableaux",
    "Analyser et valoriser des données",
    "Nettoyer des ordinateurs"
  ]
},
{
  "question": "Quelle bibliothèque Python permet de faire des graphiques ?",
  "reponse": "Matplotlib",
  "theme": "python",
  "type": "quiz",
  "propositions": [
    "Matplotlib",
    "Requests",
    "Numpy"
  ]
},
{
  "question": "Quel package Python est spécialisé dans l’analyse de données ?",
  "reponse": "Pandas",
  "theme": "python",
  "type": "quiz",
  "propositions": [
    "Pandas",
    "Scipy",
    "Flask"
  ]
},
{
  "question": "Quelle bibliothèque sert à la manipulation de données en R ?",
  "reponse": "dplyr",
  "theme": "r",
  "type": "quiz",
  "propositions": [
    "dplyr",
    "pandas",
    "matplotlib"
  ]
},
    {
  "question": "C'est quoi SCALES ?",
  "reponse": "SCALES est le Skills Cluster for Agile Learning in Economics & Social Sciences, une structure de l’UM6P dédiée à l’accompagnement, la formation et l’innovation pédagogique dans les domaines des sciences économiques, sociales et de gestion.",
  "theme": "SCALES",
  "type": "definition"
},
    {
    "question": "Quels sont les programmes proposés par SCALES ?",
    "reponse": "SCALES propose plusieurs programmes innovants : Community Service, Internship Program (IP), Immersion Program in Public Policy (IP3), Career Advisory Program (CAP), et des bootcamps en statistiques, data analysis et intelligence artificielle.",
    "theme": "SCALES",
    "type": "liste"
  },
  {
    "question": "Quelles sont les missions principales de SCALES ?",
    "reponse": "Les missions de SCALES sont de favoriser l’employabilité des étudiants, développer leurs compétences transversales et accompagner l’innovation pédagogique dans les sciences sociales et économiques.",
    "theme": "SCALES",
    "type": "definition"
  },
  {
    "question": "À qui s’adressent les programmes de SCALES ?",
    "reponse": "Les programmes SCALES s’adressent aux étudiants de la FGSES, en licence, master, ou formation professionnelle, souhaitant renforcer leurs compétences et s’ouvrir sur le monde professionnel.",
    "theme": "SCALES",
    "type": "definition"
  },
  {
    "question": "Comment puis-je participer aux activités SCALES ?",
    "reponse": "Pour participer, il suffit de suivre les communications SCALES via les canaux officiels (email, affichage, Canvas) et de s’inscrire aux programmes ou ateliers proposés.",
    "theme": "SCALES",
    "type": "definition"
  },
    {
    "question": "C'est quoi le programme IP proposé par SCALES ?",
    "reponse": "IP accompagne les étudiants pour trouver et réussir leur stage en entreprise.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "En quoi consiste le programme IP3 de SCALES ?",
    "reponse": "IP3 immerge les étudiants dans les politiques publiques à travers visites et ateliers.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Que propose le programme SATDAC de SCALES ?",
    "reponse": "SATDAC initie les étudiants à la data, la statistique et au codage via des ateliers pratiques.",
    "theme": "SATDAC",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que le LAPEX chez SCALES ?",
    "reponse": "LAPEX propose des projets et ateliers pratiques pour apprendre en expérimentant.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "En quoi consiste le programme Community Service (CS) proposé par SCALES ?",
    "reponse": "CS engage les étudiants dans des projets solidaires au service de la communauté.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "C’est quoi les Bootcamps SCALES ?",
    "reponse": "Bootcamps : sessions courtes pour apprendre rapidement des compétences clés.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Que propose WORC dans les programmes SCALES ?",
    "reponse": "WORC offre des ateliers pour améliorer la recherche et la communication.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "À quoi sert le programme MILL de SCALES ?",
    "reponse": "MILL forme à l’analyse critique des médias et à la veille digitale.",
    "theme": "mill",
    "type": "definition"
 },
    {
    "question": "Qu’est-ce que le programme LAPEX ?",
    "reponse": "LAPEX est le programme de langues pour l’économie et les sciences sociales à la FGSES, pour développer les compétences linguistiques, l’ouverture culturelle et l’employabilité.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quels sont les objectifs des programmes de langues à la FGSES ?",
    "reponse": "Développer la compétence multilingue, la communication interculturelle et l’ouverture internationale des étudiants.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quelles langues sont proposées à la FGSES ?",
    "reponse": "Français, anglais, arabe, espagnol, allemand, mandarin, arabe standard et darija pour les internationaux.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Quels sont les programmes de langues à la FGSES ?",
    "reponse": "Langues d’instruction (français, anglais, arabe), langues étrangères (espagnol, allemand, mandarin), langues pour internationaux (arabe standard, darija, FLE).",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Quels sont les niveaux A1, A2, B1, B2, C1, C2 à la FGSES ?",
    "reponse": "A1 = débutant, A2 = élémentaire, B1 = intermédiaire, B2 = indépendant, C1 = avancé, C2 = maîtrise.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "À quoi correspond le niveau B1 ?",
    "reponse": "B1 : niveau intermédiaire permettant de se débrouiller dans la plupart des situations et de produire un discours simple sur des sujets familiers.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "À quoi correspond le niveau C1 ?",
    "reponse": "C1 : niveau avancé, expression fluide, compréhension de textes complexes, autonomie dans l’usage académique et professionnel.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "À quoi correspond le niveau B2 ?",
    "reponse": "B2 : niveau indépendant, comprendre des textes complexes, interagir avec spontanéité et produire un discours clair sur une variété de sujets.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’une langue d’instruction à la FGSES ?",
    "reponse": "Langue utilisée pour l’enseignement des cours : anglais, français, arabe.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Quelles sont les conditions pour s’inscrire à un cours de langue à la FGSES ?",
    "reponse": "Passer un test de placement pour définir le niveau d’entrée, inscription selon les exigences du programme.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Quelles sont les exigences linguistiques pour valider mon diplôme à la FGSES ?",
    "reponse": "C1 dans deux langues d’instruction, B1 dans une troisième ou une langue étrangère (espagnol, allemand, mandarin).",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quels sont les niveaux requis pour chaque langue à la fin du cursus ?",
    "reponse": "Au moins C1 dans deux langues (anglais, français, arabe) et B1 dans une troisième langue ou une langue étrangère.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Quels tests de placement existent à la FGSES ?",
    "reponse": "Test écrit et oral pour toutes les langues proposées, à l’entrée en licence ou en master.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "En quoi consiste un test de placement en langues à la FGSES ?",
    "reponse": "Test composé d’une partie écrite (jusqu’à 60 minutes) et orale (jusqu’à 15 minutes) pour évaluer le niveau de l’étudiant.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Comment se fait le suivi des progrès en langues à la FGSES ?",
    "reponse": "Par micro-tâches, tests finaux, placement par niveau, et monitoring continu des progrès.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Comment sont évalués les progrès en langues à la FGSES ?",
    "reponse": "Évaluations continues (micro-tâches 30%), examens finaux (65%), et engagement (5%).",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Que veut dire LRS, OTS ou UPR sur le relevé de notes ?",
    "reponse": "LRS : exigences satisfaites ; OTS : en voie de satisfaction ; UPR : progrès insuffisants.",
    "theme": "LAPEX",
    "type": "definition"
  },
     {
    "question": "c'est quoi OTS?",
    "reponse": "OTS : en voie de satisfaction",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que le portfolio de langues ?",
    "reponse": "Document officiel attestant du niveau linguistique de l’étudiant à la sortie de la FGSES.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Est-ce que je peux prendre plusieurs cours de langues à la FGSES ?",
    "reponse": "Oui, il est possible de suivre plusieurs langues si l’emploi du temps le permet.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Y a-t-il des enseignants natifs pour les langues étrangères à la FGSES ?",
    "reponse": "Oui, des natifs enseignent certaines langues pour garantir l’immersion.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Que sont les séminaires LCSS ?",
    "reponse": "Série de séminaires sur les liens entre langue, culture et disciplines sociales, avec conférences et ateliers.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quels sont les bénéfices des séminaires LCSS ?",
    "reponse": "Mieux comprendre la culture, améliorer la communication, découvrir d’autres disciplines.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’un projet média dans le MILL ?",
    "reponse": "Projet créatif comme un podcast, un reportage ou une vidéo sur un sujet d’actualité.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Comment se passe un Film Debate ?",
    "reponse": "Projection d’un film suivie d’un débat structuré, puis rédaction d’un rapport.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Comment sont organisés les ateliers de data analysis à SCALES ?",
    "reponse": "Sessions pratiques d’initiation aux outils statistiques et à l’analyse de données, souvent en petits groupes.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quels sont les axes du module Study Skills ?",
    "reponse": "Écriture/oratoire, data/statistiques, engagement citoyen, culture de l’information, insertion professionnelle.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quelles compétences sont développées dans le module Writing and Oratory Skills ?",
    "reponse": "Rédaction académique, communication orale, argumentation, prise de parole en public.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quels sont les objectifs de la compétence Media & Information Literacy ?",
    "reponse": "Comprendre, analyser et produire des contenus médiatiques de façon critique.",
    "theme": "scales",
    "type": "definition"
  },
    {
    "question": "C'est quoi CAP ?",
    "reponse": "CAP est un module qui prépare les étudiants à l’insertion professionnelle par des ateliers, des simulations et des rencontres avec des professionnels.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que CAP ?",
    "reponse": "CAP signifie Preparation for Professional Integration. Il aide les étudiants à construire leur projet professionnel.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Que veut dire CAP ?",
    "reponse": "CAP est le module de préparation à l’insertion professionnelle au sein de SCALES.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "C'est quoi MILL ?",
    "reponse": "MILL signifie Media & Information Literacy Lab. C’est une unité qui développe l’esprit critique face à l’information et aux médias.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que MILL ?",
    "reponse": "MILL est un module qui apprend aux étudiants à analyser, produire et comprendre les médias.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Que veut dire MILL ?",
    "reponse": "MILL est le laboratoire de culture de l’information et des médias de SCALES.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "C'est quoi STADAC ?",
    "reponse": "STADAC signifie Statistics, Data Analysis and Coding. C’est le module qui initie les étudiants à l’analyse de données, à la statistique et à la programmation.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que STADAC ?",
    "reponse": "STADAC est le module de SCALES pour apprendre la statistique, la data et le codage.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Que veut dire STADAC ?",
    "reponse": "STADAC est le module Statistics, Data Analysis & Coding à la FGSES.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "C'est quoi WORC ?",
    "reponse": "WORC signifie Writing & Oratory Skills. C’est le module qui développe la rédaction et la prise de parole.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "C'est quoi CS ?",
    "reponse": "CS signifie Civic Engagement. C’est l’unité de service citoyen qui développe l’engagement et le travail en équipe.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "C'est quoi LAPEX ?",
    "reponse": "LAPEX est le programme de langues de la FGSES pour progresser en langues et s’ouvrir à l’international.",
    "theme": "LAPEX",
    "type": "definition"
  },
 
  {
    "question": "C'est quoi CAP ?",
    "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que CAP ?",
    "reponse": "CAP signifie Preparation for Professional Integration, pour accompagner les étudiants vers l'emploi.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Que veut dire CAP ?",
    "reponse": "CAP est l’acronyme de Preparation for Professional Integration à SCALES.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "À quoi sert le CAP ?",
    "reponse": "Le CAP aide à préparer son projet professionnel et à réussir les entretiens.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "En quoi consiste CAP ?",
    "reponse": "CAP propose ateliers, Meet&Greet et simulations pour préparer les étudiants à la vie active.",
    "theme": "événements professionnels",
    "type": "definition"
  },

  {
    "question": "C'est quoi MILL ?",
    "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l'analyse critique des médias.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que MILL ?",
    "reponse": "MILL aide les étudiants à comprendre et produire des contenus médias de façon responsable.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Que veut dire MILL ?",
    "reponse": "MILL signifie Media & Information Literacy Lab, le module médias et information de SCALES.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "Quel est l’objectif de MILL ?",
    "reponse": "Développer l’esprit critique face à l’information et aux médias.",
    "theme": "mill",
    "type": "definition"
  },
  {
    "question": "En quoi consiste MILL ?",
    "reponse": "C’est un module qui propose ciné-débats, projets médias, podcasts et ateliers de lutte contre la désinformation.",
    "theme": "mill",
    "type": "definition"
  },

  {
    "question": "C'est quoi STADAC ?",
    "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que STADAC ?",
    "reponse": "STADAC initie les étudiants à la statistique, l’analyse de données et le codage en R/Python.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Que veut dire STADAC ?",
    "reponse": "STADAC signifie Statistics, Data Analysis and Coding.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "À quoi sert STADAC ?",
    "reponse": "STADAC forme à la manipulation des données et aux outils numériques.",
    "theme": "STADAC",
    "type": "definition"
  },

  {
    "question": "C'est quoi WORC ?",
    "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que WORC ?",
    "reponse": "WORC améliore les compétences d’écriture académique et de communication orale.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Que veut dire WORC ?",
    "reponse": "worc signifie Writing & Oratory Skills.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Quel est l’objectif de WORC ?",
    "reponse": "Permettre de rédiger des rapports et de s’exprimer en public efficacement.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "C'est quoi CS ?",
    "reponse": "CS est l’unité Civic Engagement, pour le service citoyen et l’engagement sur le campus.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que CS ?",
    "reponse": "CS valorise l’engagement solidaire et le travail en équipe par des rôles associatifs.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "Que veut dire CS ?",
    "reponse": "CS signifie Civic Engagement à la FGSES.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "C'est quoi LAPEX ?",
    "reponse": "LAPEX est le programme de langues de la FGSES pour progresser et s’ouvrir à l’international.",
    "theme": "LAPEX ",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que LAPEX ?",
    "reponse": "LAPEX permet de renforcer ses compétences linguistiques et interculturelles.",
    "theme": "LAPEX ",
    "type": "definition"
  },
  {
    "question": "Que veut dire LAPEX ?",
    "reponse": "LAPEX signifie Languages for Economics & Social Sciences.",
    "theme": "LAPEX ",
    "type": "definition"
  },
  {
    "question": "C'est quoi SCALES ?",
    "reponse": "SCALES est le cluster UM6P qui accompagne les étudiants dans le développement de compétences transversales.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu'est-ce que SCALES ?",
    "reponse": "SCALES propose des modules innovants pour préparer à la vie professionnelle et citoyenne.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Que veut dire SCALES ?",
    "reponse": "SCALES signifie Skills Cluster for Agile Learning in Economics & Social Sciences.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "À quoi sert SCALES ?",
    "reponse": "SCALES prépare à l’employabilité et au développement personnel.",
    "theme": "scales",
    "type": "definition"
  },

  {
    "question": "C'est quoi un CV ?",
    "reponse": "Un CV est un document qui présente votre parcours, vos compétences et vos expériences pour candidater à un poste.",
    "theme": "cv",
    "type": "definition"
  },
  {
    "question": "Comment rédiger un CV ?",
    "reponse": "Un bon CV doit être clair, structuré et adapté à chaque candidature.",
    "theme": "cv",
    "type": "definition"
  },
  {
    "question": "Quelles sont les rubriques d’un CV ?",
    "reponse": "État civil, formation, expériences, compétences, langues, centres d’intérêt.",
    "theme": "cv",
    "type": "definition"
  },
  {
    "question": "Pourquoi faire un CV ?",
    "reponse": "Le CV sert à valoriser son parcours pour postuler à un stage ou un emploi.",
    "theme": "cv",
    "type": "definition"
  },
  {
    "question": "C'est quoi un rapport ?",
    "reponse": "Un rapport est un document écrit qui présente l’analyse d’un projet, d’un stage ou d’une recherche.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment rédiger un rapport ?",
    "reponse": "Structure ton rapport : introduction, développement, conclusion et bibliographie.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelles sont les étapes de la rédaction d’un rapport ?",
    "reponse": "Planification, recherche, rédaction, relecture, mise en page.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "C'est quoi une lettre de motivation ?",
    "reponse": "C’est un document qui explique pourquoi vous postulez à une formation, un stage ou un emploi.",
    "theme": "lettre de motivation",
    "type": "definition"
  },
  {
    "question": "Comment rédiger une lettre de motivation ?",
    "reponse": "Présente ton profil, explique ta motivation et ce que tu peux apporter à l’organisation.",
    "theme": "lettre de motivation",
    "type": "definition"
  },
  {
    "question": "Pourquoi faire une lettre de motivation ?",
    "reponse": "Pour convaincre un recruteur de la cohérence de ton projet et de ton intérêt.",
    "theme": "lettre de motivation",
    "type": "definition"
  },
  {
    "question": "C'est quoi un entretien ?",
    "reponse": "C’est une rencontre orale entre un candidat et un recruteur pour évaluer la compatibilité au poste.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment préparer un entretien ?",
    "reponse": "Renseigne-toi sur l’entreprise, anticipe les questions, prépare tes arguments et entraîne-toi.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelles sont les erreurs à éviter en entretien ?",
    "reponse": "Ne pas se renseigner sur l’entreprise, manquer d’arguments, être en retard ou négliger la présentation.",
    "theme": "entretien",
    "type": "definition"
  },
{"question": "Comment commencer ma recherche de stage ou d'emploi ?", "reponse": "Commence par définir ton projet professionnel : quel secteur t'intéresse, quels types de postes ? Ensuite, prépare ton CV et ton profil LinkedIn. Tu peux utiliser les plateformes comme LinkedIn, Welcome to the Jungle, Indeed, ou celles de ton école/université.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Où puis-je trouver des offres de stage ?", "reponse": "Tu peux consulter : Les plateformes de ton établissement (ex: Career Center), LinkedIn, Indeed, Jobteaser, Les sites des entreprises qui t’intéressent directement, Les salons de l’emploi et forums étudiants.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Quels sites utiliser ?", "reponse": "LinkedIn, Indeed, Welcome to the Jungle, Jobteaser, site de l’APEC, Monster, Glassdoor, ou encore les sites propres aux entreprises ou à ton établissement.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Mieux vaut postuler partout ou cibler ?", "reponse": "Il vaut mieux cibler : 10 candidatures bien préparées et personnalisées valent mieux que 50 candidatures génériques. Prends le temps d’analyser chaque offre, d’adapter ton CV et ta lettre.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Comment contacter une entreprise sans offre ?", "reponse": "Envoie une candidature spontanée : Trouve le bon interlocuteur, rédige un mail court et personnalisé, joins ton CV et relance poliment une fois/semaine maximum.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Lettre spontanée : comment faire ?", "reponse": "Adresse-toi au bon contact (RH, manager, etc.), explique ta démarche en quelques lignes, valorise tes compétences et montre que tu as compris les enjeux de l’entreprise.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Comment structurer une candidature spontanée efficace ?", "reponse": "1. Accroche personnalisée. 2. Mise en avant de tes compétences & motivation pour l’entreprise. 3. Conclusion claire avec proposition d’échange.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Puis-je utiliser la même lettre pour plusieurs candidatures ?", "reponse": "Non : chaque lettre doit être adaptée à l’entreprise et au poste. Le recruteur repère vite les lettres génériques.", "theme": "techniques de recherche d'emploi et stage", "type": "definition"},
{"question": "Quelles sont les erreurs à éviter sur un CV ?", "reponse": "Un CV trop long (1 page suffit pour un étudiant de licence), des fautes d’orthographe, un design trop chargé, une absence de résultats chiffrés ou d’exemples concrets.", "theme": "cv", "type": "definition"},
{"question": "Pourquoi mon CV ne marche pas ?", "reponse": "Manque de clarté, trop d’informations non pertinentes, présentation peu soignée, ou absence d’éléments mesurables sur tes réalisations.", "theme": "cv", "type": "definition"},
{"question": "Et si on me parle d’un trou dans le CV ?", "reponse": "Prépare une explication honnête : reprise d’études, projet personnel, bénévolat, etc. Mets l’accent sur ce que tu as appris pendant cette période.", "theme": "cv", "type": "definition"},
{"question": "Quelles erreurs éviter dans un CV ?", "reponse": "Évite les fautes, les designs trop chargés, et reste synthétique (une page).", "theme": "cv", "type": "definition"},
{"question": "Dois-je répéter mon CV dans la lettre de motivation ?", "reponse": "Non, la lettre complète le CV en apportant des éléments plus personnels.", "theme": "cv", "type": "definition"},
{"question": "Comment rédiger une bonne lettre de motivation ?", "reponse": "Structure ta lettre en 3 parties : Introduction : pourquoi tu écris ? Toi + l’entreprise : ce que tu peux apporter, pourquoi tu es motivé. Adapte toujours ta lettre à l’offre et à l’entreprise. Conclusion : proposition d’un entretien, formule de politesse.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Quelle est la longueur idéale d’une lettre de motivation ?", "reponse": "Une demi-page à une page maximum.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Faut-il mettre un titre dans une lettre de motivation ?", "reponse": "Non obligatoire, mais ça peut aider à préciser l’objet de ta candidature.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Comment commencer une lettre de motivation ?", "reponse": "Évite le classique “Je vous adresse ma candidature...”. Privilégie une accroche personnalisée ou un élément en lien direct avec l’offre ou l’entreprise.", "theme": "lettre de motivation", "type": "definition"},
{"question": "À qui dois-je adresser ma lettre ?", "reponse": "Si possible à une personne identifiée (manager, RH). Sinon, 'Madame, Monsieur'.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Faut-il signer une lettre de motivation ?", "reponse": "Oui si tu l’envoies par courrier, optionnel par mail (mais termine toujours par une formule de politesse).", "theme": "lettre de motivation", "type": "definition"},
{"question": "Peut-on utiliser des bullet points dans une lettre ?", "reponse": "Oui si c’est pertinent, mais reste sobre et lisible.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Comment conclure efficacement ?", "reponse": "Exprime ton souhait de rencontre/échange et termine par une formule polie.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Existe-t-il des outils pour m’aider à rédiger ma lettre ?", "reponse": "Oui : Canva, DoYouBuzz, Kickresume, Jobteaser… Mais relis toujours et adapte toi-même le contenu !", "theme": "lettre de motivation", "type": "definition"},
{"question": "Comment me préparer pour un entretien d'embauche ?", "reponse": "Renseigne-toi sur l'institution (valeurs, projets, chiffres clés). Prépare des réponses aux questions classiques (forces/faiblesses, présentation, etc.). Entraîne-toi à parler de ton parcours en 2-3 minutes. Prépare des questions à poser au recruteur.", "theme": "entretien", "type": "definition"},
{"question": "Que répondre à la question “Parlez-moi de vous” ?", "reponse": "Structure ta réponse en 3 temps : Ton parcours académique, Tes expériences professionnelles ou associatives, Ce que tu recherches et pourquoi tu es ici aujourd’hui.", "theme": "entretien", "type": "definition"},
{"question": "Que faire face aux questions difficiles en entretien ?", "reponse": "Sois honnête, transforme les faiblesses en apprentissage, et prépare des exemples précis pour illustrer tes réponses.", "theme": "entretien", "type": "definition"},
{"question": "Comment se préparer à un entretien technique ou d’expertise ?", "reponse": "Revois les fondamentaux de ton domaine, prépare des cas concrets, et entraîne-toi à expliquer clairement ta démarche.", "theme": "entretien", "type": "definition"},
{"question": "Pourquoi est-il important d’avoir un profil LinkedIn ?", "reponse": "LinkedIn te permet : De te rendre visible auprès des recruteurs, De te constituer un réseau professionnel, D’accéder à des offres cachées ou exclusives, De suivre l’actualité des entreprises.", "theme": "réseautage professionnel", "type": "definition"},
{"question": "Comment développer mon réseau professionnel ?", "reponse": "Ajoute tes camarades, profs, anciens de ton école. Participe à des événements (conférences, forums, webinars). Envoie des messages personnalisés pour entrer en contact. Partage ou commente des contenus pertinents sur LinkedIn.", "theme": "réseautage professionnel", "type": "definition"},
{"question": "Réseau vs piston : quelle différence ?", "reponse": "Le réseau est basé sur la confiance, les échanges et le professionnalisme. Le piston, c’est une recommandation sans forcément de fond. Le réseau t’informe, t’oriente, te recommande si tu as montré tes qualités.", "theme": "réseautage professionnel", "type": "definition"},
{"question": "Comment construire un réseau utile pour mon avenir pro ?", "reponse": "Entretiens tes relations avec tes anciens stages, alternances, enseignants. Participe à des meetups, conférences, salons spécialisés. Rejoins des groupes LinkedIn dans ton domaine.", "theme": "réseautage professionnel", "type": "definition"},
{"question": "Quelles sont les soft skills les plus recherchées par les employeurs ?", "reponse": "Communication, Esprit d’équipe, Sens de l’organisation, Capacité d’adaptation, Esprit critique / résolution de problèmes.", "theme": "soft skills", "type": "definition"},
{"question": "Quelles compétences mettre en avant ?", "reponse": "Celles attendues dans le poste visé : soft skills (adaptabilité, autonomie, communication), langues, outils techniques, connaissance du secteur.", "theme": "soft skills", "type": "definition"},
{"question": "Comment valoriser mes expériences internationales ?", "reponse": "Souligne ton autonomie, ton adaptabilité, ta capacité à évoluer dans un autre contexte. Donne des exemples concrets de projets réalisés.", "theme": "soft skills", "type": "definition"},
{"question": "Comment construire mon projet professionnel ?", "reponse": "Pose-toi les bonnes questions : Qu’est-ce que j’aime faire ? Quelles sont mes compétences ? Quels secteurs m’attirent ? Quel mode de travail me convient (startup, grand groupe, etc.) ? Discute avec des professionnels ou un conseiller d’orientation pour affiner ton projet.", "theme": "orientation professionnelle", "type": "definition"},
{"question": "Comment affiner mon positionnement professionnel avant la fin de mon M2 ?", "reponse": "Identifie les métiers cibles en fonction de tes compétences et aspirations. Renseigne-toi sur les débouchés concrets de ta spécialisation. Consulte les fiches métiers (APEC, ONISEP, Pôle Emploi) et parle à des anciens élèves pour mieux cerner les réalités du marché.", "theme": "orientation professionnelle", "type": "definition"},
{"question": "Est-ce que je dois choisir entre grand groupe, PME ou startup ?", "reponse": "Tout dépend de ton profil et de tes attentes : Grand groupe : structuration, formations internes, image. PME/Startup : polyvalence, responsabilité rapide, agilité. Expérimente si possible via des stages ou alternances.", "theme": "orientation professionnelle", "type": "definition"},
{"question": "Qu’est-ce qu’un Meet & Greet ?", "reponse": "Une rencontre informelle entre étudiants, alumni et professionnels pour échanger, poser des questions et développer ton réseau.", "theme": "événements professionnels", "type": "definition"},
{"question": "Puis-je échanger mes coordonnées avec les intervenants ?", "reponse": "Oui, il est conseillé d’ajouter les intervenants sur LinkedIn, avec un message personnalisé.", "theme": "événements professionnels", "type": "definition"},
{"question": "Est-ce que je peux participer même si je suis timide ou indécis ?", "reponse": "Oui, ces événements sont conçus pour permettre à tous de découvrir différents parcours et d’élargir leur réseau, même en tant qu’observateur.", "theme": "événements professionnels", "type": "definition"},
{"question": "Où trouver le calendrier des Meet & Greet ?", "reponse": "L’agenda est disponible sur la plateforme de ton établissement, dans les emails d’annonce ou auprès du service carrière.", "theme": "événements professionnels", "type": "definition"},
{"question": "Comment valoriser mes expériences internationales ?", "reponse": "Mets en avant ton autonomie, ta capacité à évoluer dans des environnements différents, et les compétences acquises sur le terrain.", "theme": "valorisation des expériences", "type": "definition"},
{"question": "Est-ce qu’un doctorat est bien vu en entreprise ?", "reponse": "Oui, surtout dans les secteurs de la R&D, du conseil ou de la data. Mets en avant l’esprit d’analyse et la rigueur scientifique développés durant le doctorat.", "theme": "valorisation des expériences", "type": "definition"},
{"question": "Que faire si je n’ai pas d’expérience à valoriser ?", "reponse": "Mets l’accent sur tes projets académiques, ton engagement associatif, ou toute autre expérience où tu as démontré des compétences transférables.", "theme": "valorisation des expériences", "type": "definition"},
{"question": "Comment bien me préparer à un entretien ?", "reponse": "Prépare-toi mentalement, anticipe les questions classiques et travaille ta présentation personnelle en 2 minutes.", "theme": "préparation personnelle", "type": "definition"},
{"question": "Comment me sentir prêt(e) ?", "reponse": "Entraîne-toi à l’oral avec des proches ou en enregistrant ta présentation. Visualise un échange constructif et bienveillant.", "theme": "préparation personnelle", "type": "definition"},
{"question": "Comment bien me présenter ?", "reponse": "Structure ta présentation : parcours académique, expériences-clés, compétences fortes et projet actuel.", "theme": "préparation personnelle", "type": "definition"},
{"question": "Je suis en fin d'études, que faire ?", "reponse": "Clarifie ton projet professionnel, mobilise ton réseau, reste ouvert aux opportunités de stage ou de premier emploi, et prends rendez-vous avec le service carrière.", "theme": "généralités et questions fréquentes", "type": "definition"},
{"question": "Quelle taille d’entreprise est faite pour moi ?", "reponse": "Réfléchis à tes priorités : autonomie, cadre, diversité de missions, perspectives d’évolution… Discute avec des professionnels de différents environnements.", "theme": "généralités et questions fréquentes", "type": "definition"},
{"question": "Puis-je utiliser la même lettre pour plusieurs candidatures ?", "reponse": "Non, il est important de personnaliser chaque lettre pour montrer ton intérêt réel pour le poste et l'entreprise.", "theme": "généralités et questions fréquentes", "type": "definition"},
{"question": "C'est quoi CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Qu'est-ce que CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Que veut dire CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Que signifie CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "CAP c’est quoi ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "CAP, c’est quoi ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Peux-tu expliquer CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "À quoi sert le CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Quel est le but de CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Pourquoi CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Pourquoi faire CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Qu’apprend-on dans CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Donne-moi une définition de CAP.", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Définition CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Cest quoi cap ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Qu’est ce que cap ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Cap c koi ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Cap c’est pour quoi ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Cap, definition ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "En quoi consiste CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "But du module CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Utilité du CAP ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "CAP à la FGSES ?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "What is CAP?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Explain CAP", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "CAP meaning?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "What does CAP stand for?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "Purpose of CAP?", "reponse": "CAP est le module qui prépare les étudiants à l’insertion professionnelle par des ateliers et simulations.", "theme": "cap", "type": "definition"},
{"question": "C'est quoi MILL ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Qu'est-ce que MILL ?", "reponse": "MILL est le module qui apprend à comprendre et produire des contenus médias de façon responsable.", "theme": "mill", "type": "definition"},
{"question": "Que veut dire MILL ?", "reponse": "MILL signifie Media & Information Literacy Lab, le module médias et information de SCALES.", "theme": "mill", "type": "definition"},
{"question": "Que signifie MILL ?", "reponse": "MILL signifie Media & Information Literacy Lab, le module médias et information de SCALES.", "theme": "mill", "type": "definition"},
{"question": "MILL c’est quoi ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "MILL, c’est quoi ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Peux-tu expliquer MILL ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "À quoi sert MILL ?", "reponse": "MILL sert à développer l’esprit critique face à l’information et aux médias.", "theme": "mill", "type": "definition"},
{"question": "Quel est le but de MILL ?", "reponse": "Développer l’esprit critique face à l’information et aux médias.", "theme": "mill", "type": "definition"},
{"question": "Pourquoi MILL ?", "reponse": "Pour apprendre à décrypter l’information et à éviter la désinformation.", "theme": "mill", "type": "definition"},
{"question": "Pourquoi faire MILL ?", "reponse": "Pour devenir un citoyen critique à l’ère numérique.", "theme": "mill", "type": "definition"},
{"question": "Qu’apprend-on dans MILL ?", "reponse": "À analyser, produire et comprendre les médias et l’information.", "theme": "mill", "type": "definition"},
{"question": "Donne-moi une définition de MILL.", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Définition MILL ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Cest quoi mill ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Qu’est ce que mill ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Mill c koi ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Mill c’est pour quoi ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Mill, definition ?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "En quoi consiste MILL ?", "reponse": "MILL propose ciné-débats, projets médias, podcasts et ateliers de lutte contre la désinformation.", "theme": "mill", "type": "definition"},
{"question": "But du module MILL ?", "reponse": "Développer l’esprit critique face à l’information et aux médias.", "theme": "mill", "type": "definition"},
{"question": "Utilité du MILL ?", "reponse": "Comprendre les médias et l’information à l’ère numérique.", "theme": "mill", "type": "definition"},
{"question": "MILL à la FGSES ?", "reponse": "MILL est le module Media & Information Literacy Lab de SCALES à la FGSES.", "theme": "mill", "type": "definition"},
{"question": "What is MILL?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Explain MILL", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "MILL meaning?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "What does MILL stand for?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "Purpose of MILL?", "reponse": "MILL est le module Media & Information Literacy Lab qui forme à l’analyse critique des médias.", "theme": "mill", "type": "definition"},
{"question": "C'est quoi STADAC ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Qu'est-ce que STADAC ?", "reponse": "STADAC initie les étudiants à la statistique, l’analyse de données et le codage en R/Python.", "theme": "stadac", "type": "definition"},
{"question": "Que veut dire STADAC ?", "reponse": "STADAC signifie Statistics, Data Analysis and Coding.", "theme": "stadac", "type": "definition"},
{"question": "Que signifie STADAC ?", "reponse": "STADAC signifie Statistics, Data Analysis and Coding.", "theme": "stadac", "type": "definition"},
{"question": "STADAC c’est quoi ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "STADAC, c’est quoi ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Peux-tu expliquer STADAC ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "À quoi sert STADAC ?", "reponse": "STADAC forme à la manipulation des données et aux outils numériques.", "theme": "stadac", "type": "definition"},
{"question": "Quel est le but de STADAC ?", "reponse": "Former à l’analyse statistique et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Pourquoi STADAC ?", "reponse": "Pour maîtriser l’analyse de données et le codage utiles en sciences sociales.", "theme": "stadac", "type": "definition"},
{"question": "Pourquoi faire STADAC ?", "reponse": "Pour acquérir des bases en data science et programmation.", "theme": "stadac", "type": "definition"},
{"question": "Qu’apprend-on dans STADAC ?", "reponse": "À utiliser R, Python et analyser des données.", "theme": "stadac", "type": "definition"},
{"question": "Donne-moi une définition de STADAC.", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Définition STADAC ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Cest quoi stadac ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Qu’est ce que stadac ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Stadac c koi ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Stadac c’est pour quoi ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Stadac, definition ?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "En quoi consiste STADAC ?", "reponse": "STADAC initie à la programmation, la data et l’analyse statistique.", "theme": "stadac", "type": "definition"},
{"question": "But du module STADAC ?", "reponse": "Maîtriser la manipulation et la visualisation de données.", "theme": "stadac", "type": "definition"},
{"question": "Utilité du STADAC ?", "reponse": "Acquérir les bases de l’analyse statistique moderne.", "theme": "stadac", "type": "definition"},
{"question": "STADAC à la FGSES ?", "reponse": "STADAC est le module de data science de SCALES à la FGSES.", "theme": "stadac", "type": "definition"},
{"question": "What is STADAC?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Explain STADAC", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "STADAC meaning?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "What does STADAC stand for?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "Purpose of STADAC?", "reponse": "STADAC est le module Statistics, Data Analysis and Coding dédié à l’analyse de données et à la programmation.", "theme": "stadac", "type": "definition"},
{"question": "C'est quoi WORC ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "Qu'est-ce que WORC ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "Que veut dire WORC ?", "reponse": "WORC signifie Writing & Oratory Skills, le module d’expression écrite et orale.", "theme": "worc", "type": "definition"},
{"question": "WORC c’est quoi ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "WORC, c’est quoi ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "Peux-tu expliquer WORC ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "À quoi sert WORC ?", "reponse": "WORC sert à améliorer l’écriture académique et la communication orale.", "theme": "worc", "type": "definition"},
{"question": "Pourquoi WORC ?", "reponse": "Pour mieux s’exprimer à l’écrit et à l’oral dans le contexte académique.", "theme": "worc", "type": "definition"},
{"question": "Qu’apprend-on dans WORC ?", "reponse": "À rédiger des textes académiques et à présenter ses idées à l’oral.", "theme": "worc", "type": "definition"},
{"question": "Donne-moi une définition de WORC.", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "Définition WORC ?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "What is WORC?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "WORC meaning?", "reponse": "WORC est le module Writing & Oratory Skills qui développe la rédaction et la prise de parole en public.", "theme": "worc", "type": "definition"},
{"question": "C'est quoi CS ?", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "Qu'est-ce que CS ?", "reponse": "CS est l’unité d’engagement citoyen où les étudiants participent à la vie du campus.", "theme": "CS", "type": "definition"},
{"question": "Que veut dire CS ?", "reponse": "CS signifie Civic Engagement à la FGSES.", "theme": "CS", "type": "definition"},
{"question": "CS c’est quoi ?", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "Peux-tu expliquer CS ?", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "À quoi sert CS ?", "reponse": "CS permet aux étudiants de s’impliquer et de développer leur sens du service et du travail en équipe.", "theme": "CS", "type": "definition"},
{"question": "Pourquoi CS ?", "reponse": "Pour développer l’engagement citoyen et la solidarité sur le campus.", "theme": "CS", "type": "definition"},
{"question": "Qu’apprend-on dans CS ?", "reponse": "À s’engager, aider la communauté et travailler en équipe.", "theme": "CS", "type": "definition"},
{"question": "Donne-moi une définition de CS.", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "Définition CS ?", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "What is CS?", "reponse": "CS signifie Civic Engagement, l’unité de service citoyen et engagement sur le campus.", "theme": "CS", "type": "definition"},
{"question": "C'est quoi LAPEX ?", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "Qu'est-ce que LAPEX ?", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "Que veut dire LAPEX ?", "reponse": "LAPEX signifie Languages for Economics & Social Sciences.", "theme": "lapex", "type": "definition"},
{"question": "LAPEX c’est quoi ?", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "Peux-tu expliquer LAPEX ?", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "Pourquoi LAPEX ?", "reponse": "Pour améliorer ses compétences linguistiques et découvrir d’autres cultures.", "theme": "lapex", "type": "definition"},
{"question": "À quoi sert LAPEX ?", "reponse": "LAPEX sert à progresser dans plusieurs langues et à obtenir des certifications.", "theme": "lapex", "type": "definition"},
{"question": "Qu’apprend-on dans LAPEX ?", "reponse": "À communiquer dans différentes langues et à se préparer à l’international.", "theme": "lapex", "type": "definition"},
{"question": "Donne-moi une définition de LAPEX.", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "What is LAPEX?", "reponse": "LAPEX est le programme de langues pour progresser et s’ouvrir à l’international.", "theme": "lapex", "type": "definition"},
{"question": "C'est quoi SCALES ?", "reponse": "SCALES est le cluster qui accompagne les étudiants dans le développement de compétences transversales.", "theme": "scales", "type": "definition"},
{"question": "Qu'est-ce que SCALES ?", "reponse": "SCALES propose des modules innovants pour préparer à la vie professionnelle et citoyenne.", "theme": "scales", "type": "definition"},
{"question": "Que veut dire SCALES ?", "reponse": "SCALES signifie Skills Cluster for Agile Learning in Economics & Social Sciences.", "theme": "scales", "type": "definition"},
{"question": "À quoi sert SCALES ?", "reponse": "SCALES prépare à l’employabilité et au développement personnel.", "theme": "scales", "type": "definition"},
{"question": "Pourquoi SCALES ?", "reponse": "Pour accompagner les étudiants dans l’acquisition de compétences clés pour le XXIe siècle.", "theme": "scales", "type": "definition"},
{"question": "But de SCALES ?", "reponse": "Développer les soft skills et préparer à la réussite professionnelle.", "theme": "scales", "type": "definition"},
{"question": "SCALES c’est quoi ?", "reponse": "SCALES est le cluster qui accompagne les étudiants dans le développement de compétences transversales.", "theme": "scales", "type": "definition"},
{"question": "What is SCALES?", "reponse": "SCALES est le cluster qui accompagne les étudiants dans le développement de compétences transversales.", "theme": "scales", "type": "definition"},
{"question": "C'est quoi un CV ?", "reponse": "Un CV est un document qui présente votre parcours, vos compétences et vos expériences.", "theme": "cv", "type": "definition"},
{"question": "Comment rédiger un CV ?", "reponse": "Un bon CV doit être clair, structuré et adapté à chaque candidature.", "theme": "cv", "type": "definition"},
{"question": "Quelles sont les rubriques d’un CV ?", "reponse": "État civil, formation, expériences, compétences, langues, centres d’intérêt.", "theme": "cv", "type": "definition"},
{"question": "Pourquoi faire un CV ?", "reponse": "Le CV sert à valoriser son parcours pour postuler à un stage ou un emploi.", "theme": "cv", "type": "definition"},
{"question": "Qu’est-ce qu’un bon CV ?", "reponse": "Un bon CV est concis, sans faute, personnalisé et facile à lire.", "theme": "cv", "type": "definition"},
{"question": "Définition CV ?", "reponse": "Un CV est un résumé professionnel de votre parcours et compétences.", "theme": "cv", "type": "definition"},
{"question": "What is a CV?", "reponse": "A CV is a document summarizing your education, skills, and experience.", "theme": "cv", "type": "definition"},
{"question": "How to write a CV?", "reponse": "A good CV should be clear, structured, and tailored to each application.", "theme": "cv", "type": "definition"},

{"question": "C'est quoi un rapport ?", "reponse": "Un rapport est un document écrit qui présente l’analyse d’un projet, d’un stage ou d’une recherche.", "theme": "communication", "type": "definition"},
{"question": "Comment rédiger un rapport ?", "reponse": "Structure ton rapport : introduction, développement, conclusion et bibliographie.", "theme": "communication", "type": "definition"},
{"question": "Quelles sont les étapes de la rédaction d’un rapport ?", "reponse": "Planification, recherche, rédaction, relecture, mise en page.", "theme": "communication", "type": "definition"},
{"question": "Pourquoi faire un rapport ?", "reponse": "Pour analyser, synthétiser et communiquer des résultats ou une expérience.", "theme": "communication", "type": "definition"},
{"question": "Définition rapport ?", "reponse": "Un rapport est un document de synthèse sur une expérience, un stage ou un projet.", "theme": "communication", "type": "definition"},
{"question": "What is a report?", "reponse": "A report is a written document presenting the analysis of a project, internship, or research.", "theme": "communication", "type": "definition"},
{"question": "How to write a report?", "reponse": "Structure your report: introduction, main body, conclusion, and references.", "theme": "communication", "type": "definition"},
{"question": "C'est quoi une lettre de motivation ?", "reponse": "C’est un document qui explique pourquoi vous postulez à une formation, un stage ou un emploi.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Comment rédiger une lettre de motivation ?", "reponse": "Présente ton profil, explique ta motivation et ce que tu peux apporter à l’organisation.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Pourquoi faire une lettre de motivation ?", "reponse": "Pour convaincre un recruteur de la cohérence de ton projet et de ton intérêt.", "theme": "lettre de motivation", "type": "definition"},
{"question": "Définition lettre de motivation ?", "reponse": "Une lettre de motivation présente vos arguments pour obtenir une place ou un emploi.", "theme": "lettre de motivation", "type": "definition"},
{"question": "What is a cover letter?", "reponse": "A cover letter explains why you are applying and what you can bring to the organization.", "theme": "lettre de motivation", "type": "definition"},
{"question": "How to write a cover letter?", "reponse": "Introduce yourself, explain your motivation, and show your added value.", "theme": "lettre de motivation", "type": "definition"},
{"question": "C'est quoi un entretien ?", "reponse": "C’est une rencontre orale entre un candidat et un recruteur pour évaluer la compatibilité au poste.", "theme": "entretien", "type": "definition"},
{"question": "Comment préparer un entretien ?", "reponse": "Renseigne-toi sur l’entreprise, anticipe les questions, prépare tes arguments et entraîne-toi.", "theme": "entretien", "type": "definition"},
{"question": "Quelles sont les erreurs à éviter en entretien ?", "reponse": "Ne pas se renseigner sur l’entreprise, manquer d’arguments, être en retard ou négliger la présentation.", "theme": "entretien", "type": "definition"},
{"question": "Définition entretien ?", "reponse": "Un entretien est un échange formel pour évaluer la candidature à un poste ou une formation.", "theme": "entretien", "type": "definition"},
{"question": "What is an interview?", "reponse": "An interview is a meeting between a candidate and a recruiter to assess suitability for a position.", "theme": "entretien", "type": "definition"},
{"question": "How to succeed in an interview?", "reponse": "Prepare well, be confident, and communicate your strengths clearly.", "theme": "entretien", "type": "definition"},
{"question": "Quelles sont les modalités de validation de l’unité Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Comment valider Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Validation Study Skills, comment faire ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "C'est quoi la validation de Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Peux-tu expliquer la validation de Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Study Skills, comment réussir ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Comment obtenir la validation de Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Qu'est-ce qu'il faut pour valider Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Comment ça marche Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Modalités de validation de Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "What are the requirements to pass Study Skills?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "How to validate Study Skills unit?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Study Skills validation process?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Validation Study Skills ?", "reponse": "Pour valider l’unité Study Skills, il faut participer activement, réaliser les tâches demandées et obtenir la note minimale à l’évaluation.", "theme": "scales", "type": "definition"},
{"question": "Quels sont les objectifs du module LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Objectifs de LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Pourquoi suivre LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "À quoi sert LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Peux-tu expliquer LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "C'est quoi LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "LAPEX c’est quoi ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Définition LAPEX ?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "What is LAPEX?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Why LAPEX?", "reponse": "LAPEX permet de progresser dans plusieurs langues et d’obtenir des certifications reconnues.", "theme": "LAPEX", "type": "definition"},
{"question": "Qu’est-ce que le Skills Portfolio ?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "Skills Portfolio, c’est quoi ?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "Définition Skills Portfolio ?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "A quoi sert le Skills Portfolio ?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "Pourquoi faire un Skills Portfolio ?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "How does Skills Portfolio work?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},
{"question": "What is the Skills Portfolio?", "reponse": "Le Skills Portfolio est un dossier récapitulant toutes les compétences validées pendant votre parcours.", "theme": "LAPEX", "type": "definition"},

    {
    "question": "En quoi consiste le module CAP ?",
    "reponse": "Prépare les étudiants à l’insertion professionnelle via ateliers CV, lettre, entretiens, réseautage.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quelles sont les étapes du module CAP ?",
    "reponse": "Self-Reflection, Exploration, Preparation, Launch : réflexion, exploration, préparation, lancement dans la vie pro.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quels outils prépare-t-on pour la recherche d’emploi ?",
    "reponse": "CV, lettre de motivation, LinkedIn, préparation aux entretiens et à la négociation.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que Meet & Greet dans le CAP ?",
    "reponse": "Rencontres entre étudiants et professionnels pour découvrir des métiers et développer son réseau.",
    "theme": "événements professionnels",
    "type": "definition"
  },
  {
    "question": "Quelles compétences sont évaluées lors des entretiens simulés chez SCALES ?",
    "reponse": "Communication, attitude pro, gestion du stress, capacité à argumenter et convaincre.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quels sont les projets possibles dans le Community Service (CS) ?",
    "reponse": "Projets solidaires, bénévolat, actions associatives au service de la communauté.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "En quoi consiste un bootcamp SCALES ?",
    "reponse": "Session intensive et courte pour acquérir rapidement une compétence pratique.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quels sont les avantages du module LAPEX ?",
    "reponse": "Améliorer son niveau en langues, élargir ses perspectives et faciliter la mobilité internationale.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quelles sont les certifications internationales reconnues à la FGSES ?",
    "reponse": "IELTS, TOEFL, DELF/DALF, Selectividad, certificats d’allemand ou mandarin.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment se déroule l’IELTS à la FGSES ?",
    "reponse": "L’IELTS est organisé sur place en partenariat avec le British Council, composé d’une partie écrite et orale.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quelle est la validité de l’IELTS ?",
    "reponse": "Le certificat IELTS est valable deux ans à compter de la date du test.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quelle différence entre IELTS Academic et General ?",
    "reponse": "IELTS Academic pour les études, IELTS General pour l’immigration ; seuls les scores Academic sont acceptés pour l’échange universitaire.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quels clubs ou activités existent pour progresser en langues à la FGSES ?",
    "reponse": "Book Club, Debating Society, Drama Club, Film Club, conférences et projets associatifs multilingues.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’un placement test à la FGSES ?",
    "reponse": "Test initial obligatoire pour déterminer le niveau et orienter vers le groupe adéquat.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’un Walk-in dans les modules de langues ?",
    "reponse": "Séance de tutorat individuel ou en petit groupe pour répondre aux questions spécifiques.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’une micro-tâche en langues ?",
    "reponse": "Exercice court, noté, permettant de valider une compétence précise (compréhension, expression…).",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’un mode de livraison hybride ?",
    "reponse": "Cours combinant présentiel, auto-apprentissage en ligne et sessions guidées à distance.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quelle est la politique d’évaluation des modules de langues ?",
    "reponse": "Évaluation continue (micro-tâches), examen final et prise en compte de la participation active.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quel est le barème de passage pour réussir un module ?",
    "reponse": "La note minimale pour valider un module est 10/20.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’une attestation de niveau de langue à la FGSES ?",
    "reponse": "Document délivré à la fin des études indiquant le niveau atteint pour chaque langue suivie.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quels sont les avantages de participer à des activités extrascolaires en langue ?",
    "reponse": "Renforcer l’aisance orale, développer son réseau, pratiquer la langue en situation réelle.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que SCALES ?",
    "reponse": "SCALES est un cluster pédagogique à l’UM6P, dédié à l’innovation, l’accompagnement et le développement des compétences transversales des étudiants.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’un entretien d’embauche ?",
    "reponse": "Un entretien d’embauche est une rencontre entre un candidat et un employeur pour évaluer l’adéquation entre le profil du candidat et le poste à pourvoir.",
    "theme": "entretien",
    "type": "definition"
  },
    {
    "question": "Qu’est-ce que le module Study Skills ?",
    "reponse": "Le module Study Skills est un bloc obligatoire pour tous les étudiants de la FGSES, axé sur les compétences transversales et techniques clés pour la réussite académique et l’insertion professionnelle.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quels sont les objectifs du module Study Skills ?",
    "reponse": "Développer l’efficacité d’apprentissage, la pensée critique, la communication, l’autonomie et l’engagement professionnel.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quels sont les cinq unités du module Study Skills ?",
    "reponse": "1. Writing & Oratory Skills (WORC), 2. Statistics, Data Analysis & Coding (STADAC), 3. Civic Engagement (CS), 4. Media & Information Literacy (MILL), 5. Preparation for Professional Integration (CAP).",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment est structuré le module Study Skills ?",
    "reponse": "Le module comprend cinq unités réparties sur plusieurs semestres, à valider selon le parcours de licence ou master.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment se valide chaque unité Study Skills ?",
    "reponse": "Chaque unité vaut 0,5 ECTS ; validation par participation aux activités, réalisation des tâches et réussite à l’évaluation.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu’arrive-t-il si je ne valide pas une unité Study Skills ?",
    "reponse": "L’unité doit être repassée l’année suivante ; l’échec répété retarde la diplomation.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que l’unité Writing & Oratory Skills (WORC) ?",
    "reponse": "Unité dédiée à la maîtrise de l’écriture et de l’expression orale dans le contexte académique et professionnel.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Que fait-on dans l’unité Writing & Oratory Skills (WORC) ?",
    "reponse": "Ateliers sur la rédaction académique, la synthèse, la communication écrite, la prise de parole, le débat, la présentation et la modération.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Comment valider l’unité Writing & Oratory Skills (WORC) ?",
    "reponse": "Il faut réussir un atelier de rédaction (5h) et un atelier d’expression orale (5h), avec évaluation à la fin de chaque atelier.",
    "theme": "worc",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que l’unité Statistics, Data Analysis & Coding (STADAC) ?",
    "reponse": "Unité consacrée à l’initiation à la statistique, à la manipulation et à la visualisation de données avec R et Python.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Quelles compétences développe-t-on dans STADAC ?",
    "reponse": "Statistiques de base, structures de données, programmation en R et Python, manipulation et visualisation de données.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Comment valider l’unité STADAC ?",
    "reponse": "Réussir deux trainings : un en R (12h), un en Python (12h), avec évaluation à la fin de chaque formation.",
    "theme": "STADAC",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que Civic Engagement (CS) ?",
    "reponse": "C’est une unité d’engagement citoyen où l’étudiant participe à des rôles solidaires sur le campus, développant travail d’équipe et responsabilité.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "Quels rôles peut-on avoir dans Civic Engagement ?",
    "reponse": "Library Assistant, Student Life Assistant, Administrative Task Operator, Writing & Language Tutor.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "Comment valider l’unité Civic Engagement ?",
    "reponse": "Effectuer au moins 3h de service citoyen et rédiger un feedback écrit sur l’expérience.",
    "theme": "CS",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que Media & Information Literacy (MILL) ?",
    "reponse": "Unité pour apprendre à évaluer, utiliser et produire de l’information de façon critique et responsable à l’ère numérique.",
    "theme": "MILL",
    "type": "definition"
  },
  {
    "question": "Quelles activités trouve-t-on dans MILL ?",
    "reponse": "Conférence InfoLab 360°, simulation de crise de désinformation, ciné-débat, production de podcast, film ou interview.",
    "theme": "MILL",
    "type": "definition"
  },
  {
    "question": "Comment valider l’unité MILL ?",
    "reponse": "Choisir et réussir une activité de 7h : InfoLab, ciné-débat ou projet média, avec évaluation à la fin.",
    "theme": "MILL",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que CAP (Preparation for Professional Integration) ?",
    "reponse": "Unité dédiée à la préparation à l’insertion professionnelle : exploration de carrière, ateliers, rencontres pros et simulations d’entretien.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quelles sont les étapes du CAP ?",
    "reponse": "Self-Reflection (auto-évaluation), Exploration (Meet&Greet), Preparation (ateliers), Launch (entretiens ou Career Day).",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Comment valider le CAP ?",
    "reponse": "Compléter le test d’auto-évaluation, assister à 2 Meet&Greet, participer à 2 ateliers et réussir la simulation d’entretien.",
    "theme": "cap",
    "type": "definition"
  },
  {
    "question": "Quels formats d’apprentissage existent pour Study Skills ?",
    "reponse": "Présentiel, e-learning (asynchrone), ou hybride (blended learning) via la plateforme Canvas.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment sont gérées les absences dans Study Skills ?",
    "reponse": "Toute absence doit être justifiée officiellement ; sinon, l’unité est invalidée.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quelle est la politique anti-plagiat de SCALES ?",
    "reponse": "Tout plagiat ou tricherie conduit à une sanction disciplinaire.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment s’inscrire aux ateliers SCALES ?",
    "reponse": "Inscription obligatoire via le portail SCALES ; places attribuées selon le principe du premier arrivé, premier servi.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Puis-je modifier mon inscription à un atelier ?",
    "reponse": "Non, sauf cas de force majeure justifié (médical ou académique).",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Que faire en cas de problème technique ?",
    "reponse": "Signaler le problème à l’équipe SCALES avant la date limite ; les réclamations tardives ne sont pas acceptées.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Quelles sont les règles d’utilisation des contenus SCALES ?",
    "reponse": "Les contenus multimédias sont réservés à un usage pédagogique, toute réutilisation non autorisée est interdite.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment suivre sa progression dans Study Skills ?",
    "reponse": "Un rapport de progression est envoyé chaque semestre, listant les unités validées et celles à compléter.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce que le Skills Portfolio ?",
    "reponse": "Dossier remis en fin d’études, récapitulant la progression et les compétences validées dans Study Skills.",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quelles sont les mentions du Skills Portfolio ?",
    "reponse": "SRS (requirements satisfied), OTSS (on track), UPSS (unsatisfactory progress).",
    "theme": "LAPEX",
    "type": "definition"
  },
  {
    "question": "Quelles sont les conséquences d’une progression insatisfaisante dans Study Skills ?",
    "reponse": "Tout retard ou échec non corrigé dans Study Skills retarde la diplomation.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Qui contacter en cas de question ou de difficulté dans Study Skills ?",
    "reponse": "Contacter l’équipe SCALES pour tout problème lié aux unités transversales, inscriptions ou questions techniques.",
    "theme": "scales",
    "type": "definition"
  },
  {
    "question": "Comment bien se présenter lors d’un entretien ?",
    "reponse": "Commencez par une présentation claire et structurée : indiquez votre nom, formation, expériences majeures, puis expliquez en quoi votre profil correspond au poste visé.",
    "theme": "entretien",
    "type": "definition"
  },
    {
    "question": "Comment rédiger un CV efficace ?",
    "reponse": "Un CV efficace doit être clair, concis, structuré : commence par l’état civil, la formation, l’expérience, les compétences et les centres d’intérêt, en adaptant à chaque poste visé.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelles sont les erreurs à éviter dans un CV ?",
    "reponse": "Éviter les fautes d’orthographe, les informations inutiles, les expériences trop anciennes, et ne jamais mentir sur ses compétences ou son parcours.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment valoriser ses expériences dans un CV ?",
    "reponse": "Décris chaque expérience avec des verbes d’action, mets en avant les réalisations concrètes, chiffres et résultats obtenus.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Que mettre dans la rubrique compétences d’un CV ?",
    "reponse": "Liste les compétences techniques (logiciels, langues, outils) et les soft skills (travail en équipe, communication, organisation…).",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment rédiger une lettre de motivation ?",
    "reponse": "Présente-toi brièvement, explique pourquoi tu postules, en quoi ton profil correspond, et termine par une formule de politesse et une demande d’entretien.",
    "theme": "lettre de motivation",
    "type": "definition"
  },
  {
    "question": "Comment rédiger un rapport académique ?",
    "reponse": "Respecte une structure claire : introduction, méthodologie, résultats, analyse/discussion, conclusion. Utilise un style formel, des titres et des références.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment choisir le plan d’un rapport ?",
    "reponse": "Analyse l’objectif du rapport et organise tes idées en grandes parties logiques : contexte, problématique, analyse, solutions, conclusion.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Qu’est-ce qu’une bibliographie dans un rapport ?",
    "reponse": "C’est la liste des sources utilisées : livres, articles, sites web. Elle doit respecter les normes académiques (APA, Chicago…).",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment éviter le plagiat dans un rapport ?",
    "reponse": "Il faut toujours citer ses sources, paraphraser correctement, et utiliser un logiciel anti-plagiat si possible.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment rédiger un article scientifique ?",
    "reponse": "Structure l’article en : résumé, introduction, méthodes, résultats, discussion, conclusion, références. Sois précis, objectif et cite toutes les sources.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelle est la différence entre un rapport et un article ?",
    "reponse": "Le rapport présente une analyse approfondie sur un sujet ou projet, l’article vise à partager des résultats scientifiques avec la communauté.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelles sont les qualités d’un bon rapport écrit ?",
    "reponse": "Clarté, logique, concision, pertinence, respect des consignes et bonne présentation visuelle.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment faire un sommaire dans un rapport ?",
    "reponse": "Insère après la page de garde une liste des parties et sous-parties avec numéros de page pour faciliter la lecture.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment structurer l’introduction d’un rapport ?",
    "reponse": "Présente le contexte, l’objectif, la problématique et annonce la structure du document.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Faut-il mettre une conclusion dans un rapport ou un article ?",
    "reponse": "Oui, elle récapitule les résultats, apporte une réponse à la problématique et ouvre sur des perspectives.",
    "theme": "communication",
    "type": "definition"
  },
  {
    "question": "Quels sont les types de questions posées en entretien ?",
    "reponse": "Questions sur le parcours, les compétences techniques, les qualités humaines (soft skills), la motivation, la gestion de situations difficiles et la connaissance de l’entreprise.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelles sont les erreurs à éviter en entretien ?",
    "reponse": "Évitez de manquer de ponctualité, de parler négativement de vos anciens employeurs, de ne pas préparer vos réponses ou de manquer de confiance en vous.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment répondre à la question 'Quelles sont vos qualités et vos défauts' ?",
    "reponse": "Soyez honnête : choisissez des qualités utiles au poste et des défauts non bloquants, en montrant que vous cherchez à vous améliorer.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Pourquoi est-il important de se renseigner sur l’entreprise avant un entretien ?",
    "reponse": "Cela montre votre motivation et vous permet d’adapter vos réponses. Vous démontrez que vous comprenez les valeurs et les besoins de l’employeur.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment gérer le stress lors d’un entretien ?",
    "reponse": "Préparez-vous à l’avance, entraînez-vous à répondre à des questions, respirez profondément avant d’entrer et gardez une attitude positive.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Que faire après un entretien d’embauche ?",
    "reponse": "Envoyez un message de remerciement pour montrer votre intérêt et demandez un retour sur votre entretien si possible.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quels documents préparer pour un entretien ?",
    "reponse": "CV actualisé, lettre de motivation, copies de diplômes, certificats, portfolio, et tout document demandé par l’employeur.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Citez des soft skills importants pour réussir un entretien.",
    "reponse": "Communication, esprit d’équipe, gestion du temps, adaptabilité, esprit d’initiative, et capacité à résoudre les problèmes.",
    "theme": "soft skills",
    "type": "definition"
  },
  {
    "question": "Comment expliquer un trou dans son CV en entretien ?",
    "reponse": "Soyez transparent et expliquez ce que vous avez fait pendant cette période (formations, bénévolat, projets personnels…). Mettez l’accent sur les compétences acquises.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment conclure un entretien d’embauche ?",
    "reponse": "Remerciez l’interlocuteur pour son temps, réaffirmez votre motivation et demandez les prochaines étapes du processus.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Quelle tenue vestimentaire adopter pour un entretien ?",
    "reponse": "Adoptez une tenue professionnelle et sobre, adaptée au secteur d’activité. Soignez votre apparence et évitez les tenues trop décontractées.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Que répondre à 'Pourquoi voulez-vous travailler ici ?'",
    "reponse": "Montrez que vous avez étudié l’entreprise et que ses valeurs, missions ou projets correspondent à vos aspirations et compétences.",
    "theme": "entretien",
    "type": "definition"
  },
  {
    "question": "Comment décrire SCALES en une phrase ?",
    "reponse": "SCALES est un cluster pédagogique dédié à l’acquisition de compétences transversales pour l’employabilité des étudiants en sciences économiques et sociales.",
    "theme": "SCALES",
    "type": "definition"
  },
  {
    "question": "Donne-moi un exemple de question à poser à la fin d’un entretien.",
    "reponse": "Pouvez-vous me décrire une journée type pour ce poste ? Quels sont les principaux défis à relever ? Comment évaluez-vous la réussite dans ce rôle ?",
    "theme": "entretien",
    "type": "conseil"
    },
{
  "question": "Quel outil en R permet de faire des applications web ?",
  "reponse": "Shiny",
  "theme": "r",
  "type": "quiz",
  "propositions": [
    "Shiny",
    "NumPy",
    "Excel"
  ]
},
{
  "question": "Qu’est-ce qu’une base de données ?",
  "reponse": "Un système de stockage et gestion d’informations",
  "theme": "informatique",
  "type": "quiz",
  "propositions": [
    "Un plat marocain",
    "Un système de stockage et gestion d’informations",
    "Un animal"
  ]
},
{
  "question": "Quel outil permet de versionner du code ?",
  "reponse": "Git",
  "theme": "informatique",
  "type": "quiz",
  "propositions": [
    "Git",
    "Word",
    "PowerPoint"
  ]
},
{
  "question": "Quelle compétence est un soft skill ?",
  "reponse": "La gestion du temps",
  "theme": "soft skills",
  "type": "quiz",
  "propositions": [
    "La gestion du temps",
    "La multiplication",
    "La conjugaison"
  ]
},
{
  "question": "Quel soft skill favorise le travail d’équipe ?",
  "reponse": "L’écoute active",
  "theme": "soft skills",
  "type": "quiz",
  "propositions": [
    "L’écoute active",
    "L’endormissement",
    "La course à pied"
  ]
},
     {
    "question": "À quoi sert SCALES à l’UM6P ?",
    "reponse": "Développer les compétences transversales des étudiants",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Développer les compétences transversales des étudiants",
      "Donner des notes de sport",
      "Organiser des sorties scolaires uniquement"
    ]
  },
  {
    "question": "Quel module n’est pas inclus dans Study Skills ?",
    "reponse": "Biologie moléculaire",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Biologie moléculaire",
      "Writing & Oratory Skills",
      "Media & Information Literacy"
    ]
  },
  {
    "question": "Comment valider une unité Study Skills ?",
    "reponse": "Participer, réaliser les tâches et réussir l’évaluation",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Participer, réaliser les tâches et réussir l’évaluation",
      "Ne pas assister et rendre une feuille blanche",
      "Faire un exposé sur le sport"
    ]
  },
  {
    "question": "Que développe-t-on dans l’unité WORC ?",
    "reponse": "Écriture et expression orale",
    "theme": "worc",
    "type": "quiz",
    "propositions": [
      "Écriture et expression orale",
      "Peinture sur soie",
      "Cuisine marocaine"
    ]
  },
  {
    "question": "Quelle activité est propre à l’unité MILL ?",
    "reponse": "Ciné-débat et production média",
    "theme": "mill",
    "type": "quiz",
    "propositions": [
      "Ciné-débat et production média",
      "Simulation d’attaque informatique",
      "Cours de natation"
    ]
  },
  {
    "question": "Quel est l’objectif principal de CAP ?",
    "reponse": "Préparer à l’insertion professionnelle",
    "theme": "cap",
    "type": "quiz",
    "propositions": [
      "Préparer à l’insertion professionnelle",
      "Créer une pièce de théâtre",
      "Apprendre à cuisiner"
    ]
  },
  {
    "question": "Que faut-il faire pour valider Civic Engagement (CS) ?",
    "reponse": "Réaliser un service citoyen et un feedback écrit",
    "theme": "CS",
    "type": "quiz",
    "propositions": [
      "Réaliser un service citoyen et un feedback écrit",
      "Participer à une compétition sportive",
      "Ne rien rendre"
    ]
  },
  {
    "question": "Quel outil est utilisé dans STADAC ?",
    "reponse": "Python",
    "theme": "STADAC",
    "type": "quiz",
    "propositions": [
      "Python",
      "Photoshop",
      "WordPress"
    ]
  },
  {
    "question": "Qu’est-ce qu’un projet média dans MILL ?",
    "reponse": "Créer un podcast, vidéo ou interview",
    "theme": "mill",
    "type": "quiz",
    "propositions": [
      "Créer un podcast, vidéo ou interview",
      "Faire un exposé sur le sport",
      "Écrire un roman"
    ]
  },
  {
    "question": "Combien d’ECTS vaut une unité Study Skills ?",
    "reponse": "0,5 ECTS",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "0,5 ECTS",
      "10 ECTS",
      "3 ECTS"
    ]
  },
  {
    "question": "Quelle absence n’est pas justifiée pour Study Skills ?",
    "reponse": "Oubli de réveil",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Oubli de réveil",
      "Raison médicale documentée",
      "Convocation officielle"
    ]
  },
  {
    "question": "Qu’est-ce que le Skills Portfolio ?",
    "reponse": "Un dossier récapitulant les compétences acquises",
    "theme": "LAPEX",
    "type": "quiz",
    "propositions": [
      "Un dossier récapitulant les compétences acquises",
      "Un album photo",
      "Un rapport de stage"
    ]
  },
  {
    "question": "Quel niveau de langue valide la diplomation à la FGSES ?",
    "reponse": "C1 dans deux langues",
    "theme": "LAPEX",
    "type": "quiz",
    "propositions": [
      "C1 dans deux langues",
      "A1 dans toutes les langues",
      "B2 uniquement en anglais"
    ]
  },
  {
    "question": "Que veut dire la mention LRS sur le relevé de notes ?",
    "reponse": "Exigences linguistiques satisfaites",
    "theme": "LAPEX",
    "type": "quiz",
    "propositions": [
      "Exigences linguistiques satisfaites",
      "Langue réformée spéciale",
      "Liste des résultats scolaires"
    ]
  },
  {
    "question": "Quelle compétence est un soft skill ?",
    "reponse": "La gestion du temps",
    "theme": "soft skills",
    "type": "quiz",
    "propositions": [
      "La gestion du temps",
      "La multiplication",
      "La conjugaison"
    ]
  },
  {
    "question": "Quel format d’apprentissage existe pour Study Skills ?",
    "reponse": "Présentiel, e-learning ou hybride",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Présentiel, e-learning ou hybride",
      "Uniquement à distance",
      "Sans inscription"
    ]
  },
  {
    "question": "Comment s’appelle l’unité d’analyse de données dans Study Skills ?",
    "reponse": "STADAC",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "STADAC",
      "MILL",
      "CAP"
    ]
  },
  {
    "question": "Quel module développe la citoyenneté à la FGSES ?",
    "reponse": "Civic Engagement (CS)",
    "theme": "CS",
    "type": "quiz",
    "propositions": [
      "Civic Engagement (CS)",
      "Statistics",
      "Media Literacy"
    ]
  },
  {
    "question": "Qu’est-ce que LAPEX ?",
    "reponse": "Programme pour progresser en langues et s’ouvrir à l’international",
    "theme": "LAPEX",
    "type": "quiz",
    "propositions": [
      "Programme pour progresser en langues et s’ouvrir à l’international",
      "Une méthode de calcul",
      "Un festival musical"
    ]
  },
  {
    "question": "Quelles langues peut-on apprendre à la FGSES ?",
    "reponse": "Anglais, français, arabe, espagnol, allemand, mandarin",
    "theme": "LAPEX",
    "type": "quiz",
    "propositions": [
      "Anglais, français, arabe, espagnol, allemand, mandarin",
      "Latin et grec ancien",
      "Uniquement l’arabe"
    ]
  },
  {
    "question": "Comment valider l’unité MILL ?",
    "reponse": "Réaliser une activité média ou participer à un ciné-débat",
    "theme": "mill",
    "type": "quiz",
    "propositions": [
      "Réaliser une activité média ou participer à un ciné-débat",
      "Faire un exposé sur la chimie",
      "Organiser une fête"
    ]
  },
  {
    "question": "Quel format d’activité n’est pas accepté pour valider Civic Engagement ?",
    "reponse": "Créer un groupe WhatsApp",
    "theme": "CS",
    "type": "quiz",
    "propositions": [
      "Créer un groupe WhatsApp",
      "Library Assistant",
      "Writing & Language Tutor"
    ]
  },
  {
    "question": "Quelle note minimale pour valider un module Study Skills ?",
    "reponse": "10/20",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "10/20",
      "15/20",
      "5/20"
    ]
  },
  {
    "question": "Quel outil de programmation apprend-on dans STADAC ?",
    "reponse": "Python",
    "theme": "STADAC",
    "type": "quiz",
    "propositions": [
      "Python",
      "Java",
      "Dreamweaver"
    ]
  },
  {
    "question": "Quelle est la conséquence d’un plagiat chez SCALES ?",
    "reponse": "Sanction disciplinaire",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Sanction disciplinaire",
      "Un bonus de points",
      "Un passage automatique"
    ]
  },
  {
    "question": "Quel service contacter en cas de problème avec Study Skills ?",
    "reponse": "L’équipe SCALES",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "L’équipe SCALES",
      "Le club de sport",
      "Le service restauration"
    ]
  },
  {
    "question": "Comment valider un atelier WORC ?",
    "reponse": "Participer à 5h de rédaction et 5h d’oral",
    "theme": "worc",
    "type": "quiz",
    "propositions": [
      "Participer à 5h de rédaction et 5h d’oral",
      "Rédiger un poème",
      "Suivre une série TV"
    ]
  },
  {
    "question": "Quelle activité n’est pas proposée dans MILL ?",
    "reponse": "Atelier pâtisserie",
    "theme": "mill",
    "type": "quiz",
    "propositions": [
      "Atelier pâtisserie",
      "Ciné-débat",
      "Podcast"
    ]
  },
  {
    "question": "Quel est le rôle d’un Library Assistant en Civic Engagement ?",
    "reponse": "Aider à la gestion de la bibliothèque",
    "theme": "CS",
    "type": "quiz",
    "propositions": [
      "Aider à la gestion de la bibliothèque",
      "Organiser des matchs de foot",
      "Tenir une buvette"
    ]
  },
  {
    "question": "Quelle activité ne valide pas l’unité CAP ?",
    "reponse": "Aller à un concert",
    "theme": "cap",
    "type": "quiz",
    "propositions": [
      "Aller à un concert",
      "Faire un entretien simulé",
      "Assister à un atelier CV"
    ]
  },
  {
    "question": "Quel est l’objectif des ateliers Meet&Greet dans CAP ?",
    "reponse": "Découvrir des métiers et professionnels",
    "theme": "événements professionnels",
    "type": "quiz",
    "propositions": [
      "Découvrir des métiers et professionnels",
      "Organiser une compétition de danse",
      "Préparer un buffet"
    ]
  },
  {
    "question": "Quel format de cours existe pour Study Skills ?",
    "reponse": "Présentiel, e-learning, hybride",
    "theme": "scales",
    "type": "quiz",
    "propositions": [
      "Présentiel, e-learning, hybride",
      "Téléphone seulement",
      "Cours uniquement en vidéo TikTok"
    ]
  },
  {
    "question": "Quel est l’ordre logique d’un rapport académique ?",
    "reponse": "Introduction, méthodologie, résultats, conclusion",
    "theme": "communication",
    "type": "quiz",
    "propositions": [
      "Introduction, méthodologie, résultats, conclusion",
      "Sommaire, blague, dessin",
      "Liste de courses"
    ]
  },
  {
    "question": "Pourquoi faire une bibliographie dans un rapport ?",
    "reponse": "Pour citer les sources utilisées",
    "theme": "communication",
    "type": "quiz",
    "propositions": [
      "Pour citer les sources utilisées",
      "Pour décorer la fin",
      "Pour raconter sa vie"
    ]
  },
  {
    "question": "Que faut-il éviter dans un CV ?",
    "reponse": "Les fautes d’orthographe",
    "theme": "cv",
    "type": "quiz",
    "propositions": [
      "Les fautes d’orthographe",
      "Les compétences",
      "La photo d’identité"
    ]
  },
  {
    "question": "Quel est le but d’une lettre de motivation ?",
    "reponse": "Expliquer sa motivation et sa valeur ajoutée",
    "theme": "lettre de motivation",
    "type": "quiz",
    "propositions": [
      "Expliquer sa motivation et sa valeur ajoutée",
      "Présenter sa famille",
      "Faire des blagues"
    ]
 },
{
  "question": "La communication non verbale comprend…",
  "reponse": "Les gestes et mimiques",
  "theme": "communication",
  "type": "quiz",
  "propositions": [
    "Les gestes et mimiques",
    "Le code Python",
    "La lecture rapide"
  ]
},
{
  "question": "Une bonne communication en équipe nécessite…",
  "reponse": "L’empathie et l’écoute",
  "theme": "communication",
  "type": "quiz",
  "propositions": [
    "L’empathie et l’écoute",
    "Beaucoup de bruit",
    "Ignorer les autres"
  ]
},
{
  "question": "Quel élément ne doit PAS apparaître dans un CV ?",
  "reponse": "Des fautes d’orthographe",
  "theme": "cv",
  "type": "quiz",
  "propositions": [
    "Des fautes d’orthographe",
    "Ses coordonnées",
    "Ses compétences"
  ]
},
{
  "question": "Quel est le but du CV ?",
  "reponse": "Décrocher un entretien",
  "theme": "cv",
  "type": "quiz",
  "propositions": [
    "Décrocher un entretien",
    "Faire plaisir à ses amis",
    "Décorer son mur"
  ]
},
{
  "question": "Pour réussir un entretien, il faut…",
  "reponse": "Bien se préparer",
  "theme": "entretien",
  "type": "quiz",
  "propositions": [
    "Bien se préparer",
    "Arriver en retard",
    "Mentir sur son CV"
  ]
},
{
  "question": "Que faut-il faire en entretien ?",
  "reponse": "Écouter attentivement le recruteur",
  "theme": "entretien",
  "type": "quiz",
  "propositions": [
    "Écouter attentivement le recruteur",
    "Parler sans écouter",
    "Regarder son téléphone"
  ]
},
{
  "question": "Que doit-on trouver dans un rapport académique ?",
  "reponse": "Une introduction, un développement et une conclusion",
  "theme": "communication",
  "type": "quiz",
  "propositions": [
    "Une introduction, un développement et une conclusion",
    "Juste la conclusion",
    "Uniquement la page de garde"
  ]
},
{
  "question": "Qu’est-il important de faire en rédigeant un rapport ?",
  "reponse": "Soigner la présentation et citer ses sources",
  "theme": "communication",
  "type": "quiz",
  "propositions": [
    "Soigner la présentation et citer ses sources",
    "Oublier les citations",
    "Écrire sans structure"
  ]
},
{
  "question": "Comment dit-on 'stylo' en anglais ?",
  "reponse": "pen",
  "theme": "traduction",
  "type": "quiz",
  "propositions": [
    "pencil",
    "pen",
    "book"
  ]
},
{
  "question": "Traduction de 'maison' en espagnol ?",
  "reponse": "casa",
  "theme": "traduction",
  "type": "quiz",
  "propositions": [
    "libro",
    "casa",
    "perro"
  ]
},
{
  "question": "Complétez : je ____ (être, présent)",
  "reponse": "suis",
  "theme": "conjugaison",
  "type": "quiz",
  "propositions": [
    "suis",
    "étais",
    "serai"
  ]
},
{
  "question": "Complétez : nous ____ (avoir, présent)",
  "reponse": "avons",
  "theme": "conjugaison",
  "type": "quiz",
  "propositions": [
    "avons",
    "aurez",
    "aurions"
  ]
},
{
  "question": "Quel est un synonyme de 'heureux' ?",
  "reponse": "joyeux",
  "theme": "synonyme",
  "type": "quiz",
  "propositions": [
    "joyeux",
    "triste",
    "lourd"
  ]
},
{
  "question": "Quel est un synonyme de 'difficile' ?",
  "reponse": "compliqué",
  "theme": "synonyme",
  "type": "quiz",
  "propositions": [
    "simple",
    "compliqué",
    "court"
  ]
},
{
  "question": "Quel est l’antonyme de 'petit' ?",
  "reponse": "grand",
  "theme": "antonyme",
  "type": "quiz",
  "propositions": [
    "grand",
    "court",
    "mince"
  ]
},
{
  "question": "Quel est l’antonyme de 'rapide' ?",
  "reponse": "lent",
  "theme": "antonyme",
  "type": "quiz",
  "propositions": [
    "lent",
    "vite",
    "jeune"
  ]
},
{
  "question": "Quel mot anglais signifie 'table' ?",
  "reponse": "table",
  "theme": "langues",
  "type": "quiz",
  "propositions": [
    "pen",
    "table",
    "house"
  ]
},
{
  "question": "En français, 'dog' veut dire…",
  "reponse": "chien",
  "theme": "langues",
  "type": "quiz",
  "propositions": [
    "chien",
    "chat",
    "oiseau"
  ]
},

  # --- INTELLIGENCE ARTIFICIELLE ---
  {
    "question": "C'est quoi l'intelligence artificielle ?",
    "reponse": "L’intelligence artificielle est la discipline qui vise à faire réaliser à des machines des tâches normalement humaines, comme apprendre, raisonner ou comprendre le langage.",
    "theme": "intelligence artificielle",
    "type": "definition"
  },
  {
    "question": "Définis l'intelligence artificielle.",
    "reponse": "L'intelligence artificielle regroupe des méthodes permettant à un ordinateur d’imiter l’intelligence humaine.",
    "theme": "intelligence artificielle",
    "type": "definition"
  },
    {
    "question": "c'est quoi IA ?",
    "reponse": "L'intelligence artificielle regroupe des méthodes permettant à un ordinateur d’imiter l’intelligence humaine.",
    "theme": "intelligence artificielle",
    "type": "definition"
  },
  {
    "question": "Quels sont les domaines de l'intelligence artificielle ?",
    "reponse": "L’intelligence artificielle couvre de nombreux domaines : vision par ordinateur, traitement du langage naturel, robotique, jeux, recommandation, optimisation, etc.",
    "theme": "intelligence artificielle",
    "type": "definition"
  },
  {
    "question": "Donne un exemple d'application de l'IA.",
    "reponse": "La reconnaissance faciale sur les smartphones est une application courante de l'IA.",
    "theme": "intelligence artificielle",
    "type": "exemple"
  },
  {
    "question": "Quels sont les avantages de l'IA ?",
    "reponse": "L’IA permet d’automatiser des tâches, d’analyser de grandes données et de créer de nouveaux services innovants.",
    "theme": "intelligence artificielle",
    "type": "avantage"
  },
  {
    "question": "L'IA permet quoi ?",
    "reponse": "De faire réaliser à un ordinateur des tâches habituellement réservées à l'humain.",
    "theme": "intelligence artificielle",
    "type": "quiz",
    "propositions": [
      "De faire réaliser à un ordinateur des tâches habituellement réservées à l'humain.",
      "D'envoyer des emails.",
      "De dessiner sans électricité.",
      "De réparer une voiture."
    ]
  },

  # --- DATA MINING ---
  {
    "question": "C'est quoi le data mining ?",
    "reponse": "Le data mining, ou fouille de données, regroupe des techniques pour explorer de grands ensembles de données afin d’en extraire des connaissances utiles.",
    "theme": "data mining",
    "type": "definition"
  },
  {
    "question": "Donne un exemple d'outil de data mining.",
    "reponse": "Weka, Orange et RapidMiner sont des outils de data mining.",
    "theme": "data mining",
    "type": "exemple"
  },
  {
    "question": "À quoi sert le data mining ?",
    "reponse": "À détecter des tendances ou corrélations dans des données volumineuses.",
    "theme": "data mining",
    "type": "quiz",
    "propositions": [
      "À détecter des tendances ou corrélations dans des données volumineuses.",
      "À gérer des emails.",
      "À écrire des romans.",
      "À laver des voitures."
    ]
  },
  {
    "question": "Quel est l'objectif du data mining ?",
    "reponse": "Extraire des informations cachées à partir des bases de données.",
    "theme": "data mining",
    "type": "quiz",
    "propositions": [
      "Extraire des informations cachées à partir des bases de données.",
      "Créer des tableaux Excel.",
      "Imprimer des documents.",
      "Dessiner des graphiques à la main."
    ]
  },

  # --- DATA SCIENCE ---
  {
    "question": "Quels sont les outils de data science ?",
    "reponse": "Python, R, Tableau et SQL sont parmi les outils principaux de la data science.",
    "theme": "data science",
    "type": "outil"
  },
  {
    "question": "Cite une bibliothèque Python pour la data science.",
    "reponse": "Pandas, Numpy et Scikit-learn sont des bibliothèques incontournables pour la data science.",
    "theme": "data science",
    "type": "outil"
  },
  {
    "question": "Donne un exemple de projet en data science.",
    "reponse": "Une prédiction de ventes, un moteur de recommandation, ou une détection de fraudes sont des projets classiques en data science.",
    "theme": "data science",
    "type": "exemple"
  },
  # --- PYTHON ---
  {
    "question": "Qu'est-ce que Pandas en Python ?",
    "reponse": "Pandas est une bibliothèque Python pour manipuler et analyser des tableaux de données (DataFrames).",
    "theme": "python",
    "type": "definition"
  },
  {
    "question": "Cite une bibliothèque Python pour l'IA.",
    "reponse": "TensorFlow et PyTorch sont deux bibliothèques majeures utilisées pour l'IA en Python.",
    "theme": "python",
    "type": "outil"
  },
  {
    "question": "À quoi sert Matplotlib ?",
    "reponse": "Matplotlib sert à créer des graphiques et des visualisations de données en Python.",
    "theme": "python",
    "type": "quiz",
    "propositions": [
      "Matplotlib sert à créer des graphiques et des visualisations de données en Python.",
      "À faire des calculs d'intérêts.",
      "À envoyer des emails.",
      "À gérer des fichiers PDF."
    ]
  },
  {
    "question": "Cite une bibliothèque pour le traitement du langage naturel.",
    "reponse": "NLTK et spaCy sont deux bibliothèques majeures de NLP en Python.",
    "theme": "python",
    "type": "outil"
  },
  {
    "question": "Donne un exemple d'utilisation de scikit-learn.",
    "reponse": "Scikit-learn permet de faire de la classification, de la régression, du clustering, de la réduction de dimension, etc.",
    "theme": "python",
    "type": "exemple"
  },

  # --- R ---
  {
    "question": "Qu'est-ce que ggplot2 en R ?",
    "reponse": "ggplot2 est la bibliothèque la plus utilisée en R pour la visualisation de données.",
    "theme": "r",
    "type": "definition"
  },
  {
    "question": "Donne une bibliothèque de manipulation de données en R.",
    "reponse": "dplyr et tidyr sont des bibliothèques très utilisées pour manipuler les données en R.",
    "theme": "r",
    "type": "outil"
  },
  {
    "question": "À quoi sert Shiny en R ?",
    "reponse": "Shiny permet de créer des applications web interactives directement à partir du langage R.",
    "theme": "r",
    "type": "exemple"
  },

  # --- SOFT SKILLS ---
  {
    "question": "Donne un exemple de soft skill.",
    "reponse": "La gestion du temps, l'esprit d'équipe et la créativité sont des exemples de soft skills.",
    "theme": "soft skills",
    "type": "definition"
  },
  {
    "question": "Cite une compétence clé en soft skills.",
    "reponse": "La capacité à travailler en équipe est une compétence essentielle.",
    "theme": "soft skills",
    "type": "quiz",
    "propositions": [
      "La capacité à travailler en équipe est une compétence essentielle.",
      "La capacité à dormir debout.",
      "La capacité à ignorer les autres.",
      "La capacité à lire très vite."
    ]
  },
  {
    "question": "Qu'est-ce qu'un soft skill ?",
    "reponse": "Un soft skill est une compétence comportementale, comme l'écoute active, la gestion du temps ou le leadership.",
    "theme": "soft skills",
    "type": "definition"
  },
  {
    "question": "Donne un exemple de soft skill utile pour réussir un entretien.",
    "reponse": "La gestion du stress et l'aisance à l'oral sont des soft skills essentiels en entretien.",
    "theme": "soft skills",
    "type": "exemple"
  },

  # --- COMMUNICATION ---
  {
    "question": "Communication écrite",
    "reponse": "Compétence essentielle dans les études et le travail. Elle implique la capacité à exprimer ses idées de façon claire, structurée et adaptée à l’audience.",
    "theme": "communication",
    "type": "definition"
  },
  {
    "question": "La communication non verbale",
    "reponse": "C’est l’ensemble des gestes, postures, mimiques qui complètent ou remplacent le langage parlé.",
    "theme": "communication",
    "type": "quiz",
    "propositions": [
      "C’est l’ensemble des gestes, postures, mimiques qui complètent ou remplacent le langage parlé.",
      "C’est la communication avec des animaux.",
      "C’est la communication par email uniquement.",
      "C’est un logiciel de discussion."
    ]
  },
  {
    "question": "Cite une compétence clé en communication.",
    "reponse": "L'écoute active est une compétence clé en communication.",
    "theme": "communication",
    "type": "soft skill"
  },
  {
    "question": "Quels sont les avantages de bien communiquer ?",
    "reponse": "Une bonne communication améliore la cohésion d’équipe, réduit les conflits et favorise l’efficacité.",
    "theme": "communication",
    "type": "avantage"
  },
  {
    "question": "Qui t'a crée?",
    "reponse": "DALI Oumaima.",
    "theme": "personnel scales",
    "type": "avantage"
  },
    {
    "question": "Qui t'a programmé ?",
    "reponse": "DALI Oumaima.",
    "theme": "personnel scales",
    "type": "avantage"
  },
  {
    "question": "Qui la directrice de Scales?",
    "reponse": "the wonderful Amal",
    "theme": "personnel scales",
    "type": "avantage"
  },
  # --- TRADUCTION ---
  {
    "question": "Comment dit-on 'merci' en anglais ?",
    "reponse": "Thank you.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Comment dit-on 'ordinateur' en espagnol ?",
    "reponse": "Ordenador.",
    "theme": "traduction",
    "type": "quiz",
    "propositions": [
      "Ordenador.",
      "Libro.",
      "Mesa.",
      "Perro."
    ]
  },
  {
    "question": "Comment dit-on 'livre' en anglais ?",
    "reponse": "Book.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Comment dit-on 'famille' en espagnol ?",
    "reponse": "Familia.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Donne-moi la traduction de 'ordinateur' en anglais.",
    "reponse": "Computer.",
    "theme": "traduction",
    "type": "definition"
  },

  # --- CONJUGAISON ---
  {
    "question": "Conjugaison de être au présent",
    "reponse": "Présent du verbe ÊTRE : je suis, tu es, il/elle/on est, nous sommes, vous êtes, ils/elles sont.",
    "theme": "conjugaison",
    "type": "definition"
  },
  {
    "question": "Conjugue 'avoir' au présent.",
    "reponse": "J'ai, tu as, il a, nous avons, vous avez, ils ont.",
    "theme": "conjugaison",
    "type": "quiz",
    "propositions": [
      "J'ai, tu as, il a, nous avons, vous avez, ils ont.",
      "J'avais, tu avais...",
      "J'aurai, tu auras...",
      "J'eus, tu eus..."
    ]
  },
  {
    "question": "Conjugue 'venir' au futur.",
    "reponse": "Je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront.",
    "theme": "conjugaison",
    "type": "definition"
  },

  # --- SYNONYME ---
  {
    "question": "Donne un synonyme de 'important'.",
    "reponse": "Essentiel.",
    "theme": "synonyme",
    "type": "definition"
  },
  {
    "question": "Donne un synonyme de 'difficile'.",
    "reponse": "Complexe.",
    "theme": "synonyme",
    "type": "definition"
  },
  {
    "question": "Donne un synonyme de 'rapide'.",
    "reponse": "Prompt.",
    "theme": "synonyme",
    "type": "definition"
  },

  # --- ANTONYME ---
  {
    "question": "Quel est le contraire de 'difficile' ?",
    "reponse": "Le contraire de 'difficile' est 'facile'.",
    "theme": "antonyme",
    "type": "antonyme"
  },
  {
    "question": "Quel est le contraire de 'heureux' ?",
    "reponse": "Le contraire de 'heureux' est 'malheureux'.",
    "theme": "antonyme",
    "type": "antonyme"
  },
  {
    "question": "Quel est le contraire de 'rapide' ?",
    "reponse": "Le contraire de 'rapide' est 'lent'.",
    "theme": "antonyme",
    "type": "antonyme"
  },

  # --- LANGUES ---
  {
    "question": "Quel est l'avantage de parler plusieurs langues ?",
    "reponse": "Cela facilite la communication internationale.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Pourquoi apprendre les langues étrangères ?",
    "reponse": "Pour pouvoir communiquer avec des personnes du monde entier.",
    "theme": "langues",
    "type": "quiz",
    "propositions": [
      "Pour pouvoir communiquer avec des personnes du monde entier.",
      "Pour oublier sa langue maternelle.",
      "Pour travailler uniquement dans son pays.",
      "Pour avoir moins d'amis."
    ]
  },
    # --- TRADUCTION ---
  {
    "question": "Comment dit-on 'merci' en anglais ?",
    "reponse": "Thank you.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Comment dit-on 'ordinateur' en espagnol ?",
    "reponse": "Ordenador.",
    "theme": "traduction",
    "type": "quiz",
    "propositions": [
      "Ordenador.",
      "Libro.",
      "Mesa.",
      "Perro."
    ]
  },
  {
    "question": "Comment dit-on 'livre' en anglais ?",
    "reponse": "Book.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Comment dit-on 'famille' en espagnol ?",
    "reponse": "Familia.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Donne-moi la traduction de 'ordinateur' en anglais.",
    "reponse": "Computer.",
    "theme": "traduction",
    "type": "definition"
  },

  # --- CONJUGAISON ---
  {
    "question": "Conjugaison de être au présent",
    "reponse": "Présent du verbe ÊTRE : je suis, tu es, il/elle/on est, nous sommes, vous êtes, ils/elles sont.",
    "theme": "conjugaison",
    "type": "definition"
  },
  {
    "question": "Conjugue 'avoir' au présent.",
    "reponse": "J'ai, tu as, il a, nous avons, vous avez, ils ont.",
    "theme": "conjugaison",
    "type": "quiz",
    "propositions": [
      "J'ai, tu as, il a, nous avons, vous avez, ils ont.",
      "J'avais, tu avais...",
      "J'aurai, tu auras...",
      "J'eus, tu eus..."
    ]
  },
  {
    "question": "Conjugue 'venir' au futur.",
    "reponse": "Je viendrai, tu viendras, il viendra, nous viendrons, vous viendrez, ils viendront.",
    "theme": "conjugaison",
    "type": "definition"
  },

  # --- SYNONYME ---
  {
    "question": "Donne un synonyme de 'important'.",
    "reponse": "Essentiel.",
    "theme": "synonyme",
    "type": "definition"
  },
  {
    "question": "Donne un synonyme de 'difficile'.",
    "reponse": "Complexe.",
    "theme": "synonyme",
    "type": "definition"
  },
  {
    "question": "Donne un synonyme de 'rapide'.",
    "reponse": "Prompt.",
    "theme": "synonyme",
    "type": "definition"
  },

  # --- ANTONYME ---
  {
    "question": "Quel est le contraire de 'difficile' ?",
    "reponse": "Le contraire de 'difficile' est 'facile'.",
    "theme": "antonyme",
    "type": "antonyme"
  },
  {
    "question": "Quel est le contraire de 'heureux' ?",
    "reponse": "Le contraire de 'heureux' est 'malheureux'.",
    "theme": "antonyme",
    "type": "antonyme"
  },
  {
    "question": "Quel est le contraire de 'rapide' ?",
    "reponse": "Le contraire de 'rapide' est 'lent'.",
    "theme": "antonyme",
    "type": "antonyme"
  },

  # --- LANGUES ---
  {
    "question": "Quel est l'avantage de parler plusieurs langues ?",
    "reponse": "Cela facilite la communication internationale.",
    "theme": "langues",
    "type": "definition"
  },
  {
    "question": "Pourquoi apprendre les langues étrangères ?",
    "reponse": "Pour pouvoir communiquer avec des personnes du monde entier.",
    "theme": "langues",
    "type": "quiz",
    "propositions": [
      "Pour pouvoir communiquer avec des personnes du monde entier.",
      "Pour oublier sa langue maternelle.",
      "Pour travailler uniquement dans son pays.",
      "Pour avoir moins d'amis."
    ]
  },
  # --- INFORMATIQUE / PROGRAMMATION ---
  {
    "question": "Qu'est-ce qu'une base de données ?",
    "reponse": "Une base de données est un système organisé permettant de stocker, gérer et rechercher efficacement des informations.",
    "theme": "informatique",
    "type": "definition"
  },
  {
    "question": "Cite une bibliothèque de visualisation Python.",
    "reponse": "Matplotlib, Seaborn et Plotly sont utilisées pour la visualisation en Python.",
    "theme": "python",
    "type": "outil"
  },
  {
    "question": "À quoi sert NumPy en Python ?",
    "reponse": "NumPy permet de manipuler des tableaux de nombres et de faire des calculs scientifiques rapides.",
    "theme": "python",
    "type": "definition"
  },
  {
    "question": "À quoi sert dplyr en R ?",
    "reponse": "dplyr permet de filtrer, trier, transformer et résumer des données efficacement en R.",
    "theme": "r",
    "type": "definition"
  },
  {
    "question": "Donne un exemple d’application de la data science.",
    "reponse": "La prédiction de ventes, la détection de fraudes ou la recommandation de produits sont des applications classiques.",
    "theme": "data science",
    "type": "exemple"
  },

  # --- SOFT SKILLS / SYNONYMES (complément) ---
  {
    "question": "Donne un synonyme de 'motivation'.",
    "reponse": "Enthousiasme, détermination.",
    "theme": "synonyme",
    "type": "definition"
  },
  {
    "question": "Donne un synonyme de 'compétence'.",
    "reponse": "Aptitude, savoir-faire.",
    "theme": "synonyme",
    "type": "definition"
  },

  # --- CONJUGAISON (complément) ---
  {
    "question": "Conjugue 'aller' au présent.",
    "reponse": "Je vais, tu vas, il/elle va, nous allons, vous allez, ils/elles vont.",
    "theme": "conjugaison",
    "type": "definition"
  },
  {
    "question": "Conjugue 'être' à l’imparfait.",
    "reponse": "J’étais, tu étais, il/elle était, nous étions, vous étiez, ils/elles étaient.",
    "theme": "conjugaison",
    "type": "definition"
  },
  {
    "question": "Conjugue 'prendre' au passé composé.",
    "reponse": "J’ai pris, tu as pris, il/elle a pris, nous avons pris, vous avez pris, ils/elles ont pris.",
    "theme": "conjugaison",
    "type": "definition"
  },

  # --- TRADUCTION (complément) ---
  {
    "question": "Traduction de 'maison' en anglais.",
    "reponse": "House.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Traduction de 'livre' en espagnol.",
    "reponse": "Libro.",
    "theme": "traduction",
    "type": "definition"
  },
  {
    "question": "Traduction de 'ordinateur' en allemand.",
    "reponse": "Computer.",
    "theme": "traduction",
    "type": "definition"
  },
    {
    "question": "Où peut-on trouver un job rapidement ?",
    "reponse": "Sur les sites d’emploi en ligne (LinkedIn, Indeed, Rekrute, Anapec), via ton réseau professionnel, ou en envoyant des candidatures spontanées directement aux entreprises.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment trouver un stage en entreprise ?",
    "reponse": "Prépare un CV ciblé, cherche sur les plateformes spécialisées (LinkedIn, Welcome to the Jungle, sites d’universités), et contacte aussi directement les recruteurs ou responsables RH.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Quels sites utiliser pour chercher un emploi ?",
    "reponse": "LinkedIn, Indeed, Glassdoor, Monster, ainsi que les plateformes locales comme Rekrute ou Anapec.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "liste"
  },
  {
    "question": "Comment décrocher un job sans expérience ?",
    "reponse": "Mets en avant tes stages, projets scolaires, activités associatives, et compétences transférables. Fais aussi des candidatures spontanées pour montrer ta motivation.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment utiliser LinkedIn pour trouver un emploi ?",
    "reponse": "Optimise ton profil (photo pro, résumé clair, compétences), suis des entreprises, active les alertes d’offres, et contacte directement les recruteurs.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "méthode"
  },
  {
    "question": "Comment se démarquer dans une candidature ?",
    "reponse": "Personnalise ton CV et ta lettre de motivation, mets en avant tes résultats chiffrés, et joins un portfolio ou des exemples concrets de ton travail.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Faut-il envoyer des candidatures spontanées ?",
    "reponse": "Oui, car beaucoup de postes ne sont pas publiés. Cible les entreprises qui t’intéressent et envoie un mail court avec ton CV en expliquant ta valeur ajoutée.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment augmenter mes chances de décrocher un entretien ?",
    "reponse": "Adapte ton CV à chaque offre, prépare un pitch de présentation, active ton réseau, et relance poliment après ta candidature.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "méthode"
  },
  {
    "question": "Quels sont les canaux efficaces pour trouver un job ?",
    "reponse": "Sites d’emploi, réseaux sociaux professionnels, cooptation (amis/collègues), événements de networking, forums emploi et salons de recrutement.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "liste"
  },
  {
    "question": "Comment préparer une recherche d’emploi efficace ?",
    "reponse": "Définis clairement le type de poste que tu veux, organise ton temps (ex: 2h par jour de candidatures), et tiens un tableau de suivi des offres et contacts.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "méthode"
  },
  {
    "question": "Quels conseils pour décrocher un stage rapidement ?",
    "reponse": "Commence tôt, contacte tes professeurs et anciens camarades, prépare un mail de motivation clair, et montre ta motivation même pour des missions courtes.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment relancer après une candidature ?",
    "reponse": "Envoie un mail court et poli 7 jours après ta candidature, en rappelant ton intérêt et en proposant d’échanger davantage.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "script"
  },
    {
    "question": "Comment rédiger un CV attractif ?",
    "reponse": "Mets en avant tes expériences avec des résultats chiffrés, garde une mise en page claire, et adapte ton contenu à chaque offre d’emploi.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Quelles sont les erreurs à éviter dans un CV ?",
    "reponse": "Éviter les fautes d’orthographe, les informations inutiles (âge, état civil si non requis), les CV trop longs et les formulations vagues.",
    "theme": "cv",
    "type": "liste"
  },
  {
    "question": "Combien de pages doit faire un CV ?",
    "reponse": "En général une seule page suffit pour un jeune diplômé ou un profil junior, deux pages maximum pour un profil confirmé.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Faut-il mettre une photo sur son CV ?",
    "reponse": "Cela dépend du pays et du secteur. En France, la photo est encore courante, mais elle doit être professionnelle. Dans certains pays comme le Royaume-Uni ou les États-Unis, elle est déconseillée.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Comment décrire mes expériences dans le CV ?",
    "reponse": "Utilise des verbes d’action, précise les missions principales et surtout les résultats obtenus (exemple : 'Augmentation de 15% des ventes grâce à une nouvelle campagne marketing').",
    "theme": "cv",
    "type": "méthode"
  },
  {
    "question": "Quels éléments inclure absolument dans un CV ?",
    "reponse": "Les coordonnées, le titre du poste ciblé, un résumé ou profil professionnel, les expériences clés, les formations et les compétences techniques et linguistiques.",
    "theme": "cv",
    "type": "checklist"
  },
  {
    "question": "Dois-je adapter mon CV pour chaque candidature ?",
    "reponse": "Oui, il est recommandé d’adapter le titre, les compétences mises en avant et l’ordre des expériences selon l’offre visée.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Comment expliquer un trou dans le CV ?",
    "reponse": "Reste factuel, indique la raison brièvement (formation, projet personnel, période familiale) et montre ce que tu as appris durant ce temps.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Qu’est-ce qu’un CV orienté résultats ?",
    "reponse": "Un CV qui met l’accent sur les réalisations chiffrées plutôt que sur les tâches (exemple : 'Réduction du temps de traitement de 20% en optimisant un processus').",
    "theme": "cv",
    "type": "definition"
  },
  {
    "question": "Dois-je mettre mes soft skills dans le CV ?",
    "reponse": "Oui, mais plutôt de façon subtile : montre-les à travers tes expériences et réalisations plutôt qu’en liste brute.",
    "theme": "cv",
    "type": "conseil"
  },
  {
    "question": "Quels outils utiliser pour créer un CV ?",
    "reponse": "Canva, Word, ou des générateurs en ligne spécialisés. Attention à rester simple et lisible pour passer les systèmes ATS.",
    "theme": "cv",
    "type": "liste"
  },
  {
    "question": "Comment rendre mon CV compatible ATS ?",
    "reponse": "Utilise un format simple (texte, pas d’images ni tableaux complexes), insère des mots-clés de l’offre, et exporte en PDF.",
    "theme": "cv",
    "type": "méthode"
  },
    {
    "question": "Je cherche du travail, que faire ?",
    "reponse": "Commence par cibler le type de poste que tu veux, prépare un CV clair, inscris-toi sur des plateformes d’emploi, et active ton réseau personnel et professionnel.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment postuler à l’étranger ?",
    "reponse": "Prépare un CV adapté aux standards du pays (ex : 1 page en anglais sans photo pour le Royaume-Uni ou les États-Unis), améliore ton niveau de langue, et utilise LinkedIn ou les sites internationaux pour postuler.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "méthode"
  },
  {
    "question": "Je ne trouve pas d’emploi, que dois-je faire ?",
    "reponse": "Diversifie tes recherches : utilise plusieurs sites, envoie aussi des candidatures spontanées, améliore ton CV et demande des retours pour l’optimiser.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment décrocher un travail sans expérience ?",
    "reponse": "Mets en avant tes projets scolaires, stages, bénévolat ou activités associatives. Les recruteurs valorisent aussi la motivation et les compétences transférables.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Quelles sont les meilleures techniques pour trouver un emploi ?",
    "reponse": "1) Personnaliser chaque candidature, 2) activer ton réseau et demander des recommandations, 3) publier du contenu pertinent sur LinkedIn, 4) relancer après avoir postulé.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "liste"
  },
  {
    "question": "Je veux trouver un stage, comment faire ?",
    "reponse": "Cherche sur les plateformes étudiantes et LinkedIn, contacte les entreprises directement, et demande à tes professeurs ou anciens camarades de te recommander.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "conseil"
  },
  {
    "question": "Comment élargir mes chances de trouver du travail ?",
    "reponse": "Ne te limite pas à un seul canal : combine sites d’emploi, candidatures spontanées, salons de recrutement, et échanges directs avec des professionnels.",
    "theme": "techniques de recherche d'emploi et stage",
    "type": "méthode"
  },
    {
    "question": "Quel mot-clé permet de définir une fonction en Python ?",
    "reponse": "def",
    "theme": "python",
    "type": "quiz",
    "propositions": ["def", "function", "fun"]
  },
  {
    "question": "Quelle bibliothèque Python est utilisée pour manipuler des tableaux multidimensionnels ?",
    "reponse": "NumPy",
    "theme": "python",
    "type": "quiz",
    "propositions": ["NumPy", "Matplotlib", "Requests"]
  },
  {
    "question": "Quelle méthode permet de lire un fichier CSV avec pandas ?",
    "reponse": "read_csv",
    "theme": "python",
    "type": "quiz",
    "propositions": ["read_csv", "load_csv", "open_csv"]
  },
  {
    "question": "Quel est le symbole utilisé pour les commentaires en Python ?",
    "reponse": "#",
    "theme": "python",
    "type": "quiz",
    "propositions": ["#", "//", "/* */"]
  },
  {
    "question": "Quelle librairie Python est la plus utilisée pour le machine learning ?",
    "reponse": "scikit-learn",
    "theme": "python",
    "type": "quiz",
    "propositions": ["scikit-learn", "Flask", "OpenCV"]
  },
  {
    "question": "Quelle fonction Python affiche un texte à l’écran ?",
    "reponse": "print",
    "theme": "python",
    "type": "quiz",
    "propositions": ["print", "echo", "display"]
  },
  {
    "question": "Quel type de boucle parcourt une séquence en Python ?",
    "reponse": "for",
    "theme": "python",
    "type": "quiz",
    "propositions": ["for", "foreach", "loop"]
  },
  {
    "question": "Quel est le type de données renvoyé par la fonction input() en Python ?",
    "reponse": "str",
    "theme": "python",
    "type": "quiz",
    "propositions": ["str", "int", "float"]
  },
  {
    "question": "Quelle fonction retourne la longueur d’une liste en Python ?",
    "reponse": "len",
    "theme": "python",
    "type": "quiz",
    "propositions": ["len", "length", "size"]
  },
  {
    "question": "Quelle structure de données Python garantit des clés uniques ?",
    "reponse": "dictionnaire",
    "theme": "python",
    "type": "quiz",
    "propositions": ["dictionnaire", "liste", "tuple"]
  },
  {
    "question": "Quelle fonction sert à gérer les exceptions en Python ?",
    "reponse": "try/except",
    "theme": "python",
    "type": "quiz",
    "propositions": ["try/except", "catch", "error handling"]
  },
  {
    "question": "Quelle bibliothèque Python est utilisée pour la visualisation de données ?",
    "reponse": "Matplotlib",
    "theme": "python",
    "type": "quiz",
    "propositions": ["Matplotlib", "NumPy", "Seaborn"]
  },
  {
    "question": "Quel framework Python est utilisé pour créer des APIs rapides ?",
    "reponse": "FastAPI",
    "theme": "python",
    "type": "quiz",
    "propositions": ["FastAPI", "Django", "Flask"]
  },
  {
    "question": "Quelle est la valeur de 2**3 en Python ?",
    "reponse": "8",
    "theme": "python",
    "type": "quiz",
    "propositions": ["8", "6", "9"]
  },
  {
    "question": "Quelle méthode permet de supprimer un élément d’une liste Python ?",
    "reponse": "remove",
    "theme": "python",
    "type": "quiz",
    "propositions": ["remove", "delete", "pop"]
  },
  {
    "question": "Quelle bibliothèque Python est utilisée pour le deep learning ?",
    "reponse": "TensorFlow",
    "theme": "python",
    "type": "quiz",
    "propositions": ["TensorFlow", "Pandas", "BeautifulSoup"]
  },
  {
    "question": "Quelle commande permet d’installer une librairie Python ?",
    "reponse": "pip install",
    "theme": "python",
    "type": "quiz",
    "propositions": ["pip install", "python add", "lib install"]
  },
  {
    "question": "Quel mot-clé est utilisé pour créer une classe en Python ?",
    "reponse": "class",
    "theme": "python",
    "type": "quiz",
    "propositions": ["class", "object", "define"]
  },
  {
    "question": "Quelle fonction retourne le type d’une variable en Python ?",
    "reponse": "type",
    "theme": "python",
    "type": "quiz",
    "propositions": ["type", "typeof", "class"]
  },
  {
    "question": "Quel package Python est utilisé pour le scraping web ?",
    "reponse": "BeautifulSoup",
    "theme": "python",
    "type": "quiz",
    "propositions": ["BeautifulSoup", "Seaborn", "scikit-learn"]
  },
    {
    "question": "Quel symbole est utilisé pour assigner une valeur en R ?",
    "reponse": "<-",
    "theme": "r",
    "type": "quiz",
    "propositions": ["<-", "=", ":"]
  },
  {
    "question": "Quelle fonction affiche les six premières lignes d’un DataFrame en R ?",
    "reponse": "head",
    "theme": "r",
    "type": "quiz",
    "propositions": ["head", "top", "first"]
  },
  {
    "question": "Quel package R est spécialisé dans la visualisation ?",
    "reponse": "ggplot2",
    "theme": "r",
    "type": "quiz",
    "propositions": ["ggplot2", "dplyr", "tidyr"]
  },
  {
    "question": "Quelle fonction calcule la moyenne en R ?",
    "reponse": "mean",
    "theme": "r",
    "type": "quiz",
    "propositions": ["mean", "avg", "moyenne"]
  },
  {
    "question": "Quel package R est utilisé pour manipuler les données ?",
    "reponse": "dplyr",
    "theme": "r",
    "type": "quiz",
    "propositions": ["dplyr", "shiny", "caret"]
  },
  {
    "question": "Quelle fonction R lit un fichier CSV ?",
    "reponse": "read.csv",
    "theme": "r",
    "type": "quiz",
    "propositions": ["read.csv", "load.csv", "import.csv"]
  },
  {
    "question": "Quelle fonction calcule la médiane en R ?",
    "reponse": "median",
    "theme": "r",
    "type": "quiz",
    "propositions": ["median", "mean", "mode"]
  },
  {
    "question": "Quel package R est utilisé pour le machine learning ?",
    "reponse": "caret",
    "theme": "r",
    "type": "quiz",
    "propositions": ["caret", "shiny", "ggplot2"]
  },
  {
    "question": "Quelle fonction affiche la structure d’un objet en R ?",
    "reponse": "str",
    "theme": "r",
    "type": "quiz",
    "propositions": ["str", "structure", "summary"]
  },
  {
    "question": "Quel opérateur logique teste l’égalité en R ?",
    "reponse": "==",
    "theme": "r",
    "type": "quiz",
    "propositions": ["==", "=", "==="]
  },
  {
    "question": "Quel package R est utilisé pour les applications web interactives ?",
    "reponse": "shiny",
    "theme": "r",
    "type": "quiz",
    "propositions": ["shiny", "dplyr", "tidyr"]
  },
  {
    "question": "Quelle fonction renvoie la variance en R ?",
    "reponse": "var",
    "theme": "r",
    "type": "quiz",
    "propositions": ["var", "variance", "sd"]
  },
  {
    "question": "Quelle fonction calcule l’écart-type en R ?",
    "reponse": "sd",
    "theme": "r",
    "type": "quiz",
    "propositions": ["sd", "stdev", "sqrt"]
  },
  {
    "question": "Quelle fonction combine des vecteurs en R ?",
    "reponse": "c",
    "theme": "r",
    "type": "quiz",
    "propositions": ["c", "combine", "concat"]
  },
  {
    "question": "Quelle fonction renvoie les dimensions d’un DataFrame en R ?",
    "reponse": "dim",
    "theme": "r",
    "type": "quiz",
    "propositions": ["dim", "size", "shape"]
  },
  {
    "question": "Quel package R est utilisé pour l’imputation de données manquantes ?",
    "reponse": "mice",
    "theme": "r",
    "type": "quiz",
    "propositions": ["mice", "tidyr", "caret"]
  },
  {
    "question": "Quel opérateur sert à la concaténation de chaînes en R ?",
    "reponse": "paste",
    "theme": "r",
    "type": "quiz",
    "propositions": ["paste", "concat", "join"]
  },
  {
    "question": "Quelle fonction R affiche un résumé statistique des données ?",
    "reponse": "summary",
    "theme": "r",
    "type": "quiz",
    "propositions": ["summary", "describe", "info"]
  },
  {
    "question": "Quelle fonction génère des nombres aléatoires suivant une loi normale en R ?",
    "reponse": "rnorm",
    "theme": "r",
    "type": "quiz",
    "propositions": ["rnorm", "norm", "randn"]
  },
  {
    "question": "Quel package R est utilisé pour manipuler les données sous forme de tableaux rapides ?",
    "reponse": "data.table",
    "theme": "r",
    "type": "quiz",
    "propositions": ["data.table", "dplyr", "tidyr"]
  },
    {
    "question": "Quelle bibliothèque Python est principalement utilisée avec les GPU pour le deep learning ?",
    "reponse": "PyTorch",
    "theme": "python",
    "type": "quiz",
    "propositions": ["PyTorch", "scikit-learn", "Seaborn"]
  },
  {
    "question": "Quel est le module de haut niveau de TensorFlow pour créer des réseaux de neurones ?",
    "reponse": "Keras",
    "theme": "python",
    "type": "quiz",
    "propositions": ["Keras", "NumPy", "Matplotlib"]
  },
  {
    "question": "Quelle fonction PyTorch est utilisée pour calculer la rétropropagation ?",
    "reponse": "backward()",
    "theme": "python",
    "type": "quiz",
    "propositions": ["backward()", "fit()", "train()"]
  },
  {
    "question": "Quel framework Python est utilisé pour traiter de très grands volumes de données distribuées ?",
    "reponse": "PySpark",
    "theme": "python",
    "type": "quiz",
    "propositions": ["PySpark", "FastAPI", "TensorFlow"]
  },
  {
    "question": "Quelle bibliothèque Python est spécialisée dans le calcul parallèle sur de grands DataFrames ?",
    "reponse": "Dask",
    "theme": "python",
    "type": "quiz",
    "propositions": ["Dask", "Polars", "pandas"]
  },
  {
    "question": "Quel est l’optimiseur par défaut utilisé dans Keras ?",
    "reponse": "Adam",
    "theme": "python",
    "type": "quiz",
    "propositions": ["Adam", "SGD", "RMSprop"]
  },
  {
    "question": "Quelle est la fonction d’activation la plus utilisée dans les réseaux de neurones profonds ?",
    "reponse": "ReLU",
    "theme": "python",
    "type": "quiz",
    "propositions": ["ReLU", "Sigmoid", "Tanh"]
  },
  {
    "question": "Quel package Python est utilisé pour la visualisation interactive de gros jeux de données ?",
    "reponse": "Plotly",
    "theme": "python",
    "type": "quiz",
    "propositions": ["Plotly", "Matplotlib", "Seaborn"]
  },
  {
    "question": "Quel type de réseau neuronal est utilisé pour l’analyse d’images ?",
    "reponse": "CNN (Convolutional Neural Network)",
    "theme": "python",
    "type": "quiz",
    "propositions": ["CNN (Convolutional Neural Network)", "RNN (Recurrent Neural Network)", "GAN (Generative Adversarial Network)"]
  },
  {
    "question": "Quel type de réseau est utilisé pour le traitement du langage naturel en deep learning ?",
    "reponse": "RNN (Recurrent Neural Network)",
    "theme": "python",
    "type": "quiz",
    "propositions": ["RNN (Recurrent Neural Network)", "CNN", "DBN"]
  },
     {
    "question": "Quelle fonction R est utilisée pour effectuer une analyse de variance (ANOVA) ?",
    "reponse": "aov",
    "theme": "r",
    "type": "quiz",
    "propositions": ["aov", "anova", "lm"]
  },
  {
    "question": "Quel package R est utilisé pour les modèles de forêts aléatoires ?",
    "reponse": "randomForest",
    "theme": "r",
    "type": "quiz",
    "propositions": ["randomForest", "glmnet", "xgboost"]
  },
  {
    "question": "Quel package R est utilisé pour le boosting en apprentissage automatique ?",
    "reponse": "xgboost",
    "theme": "r",
    "type": "quiz",
    "propositions": ["xgboost", "caret", "shiny"]
  },
  {
    "question": "Quelle fonction R est utilisée pour ajuster un modèle de régression logistique ?",
    "reponse": "glm(..., family=binomial)",
    "theme": "r",
    "type": "quiz",
    "propositions": ["glm(..., family=binomial)", "lm", "logit"]
  },
  {
    "question": "Quel package R est utilisé pour l’analyse de survie ?",
    "reponse": "survival",
    "theme": "r",
    "type": "quiz",
    "propositions": ["survival", "lifelines", "timeSeries"]
  },
  {
    "question": "Quelle fonction R est utilisée pour obtenir les valeurs propres d’une matrice ?",
    "reponse": "eigen",
    "theme": "r",
    "type": "quiz",
    "propositions": ["eigen", "svd", "values"]
  },
  {
    "question": "Quel package R permet de travailler avec des modèles de séries temporelles avancés ?",
    "reponse": "forecast",
    "theme": "r",
    "type": "quiz",
    "propositions": ["forecast", "tsibble", "caret"]
  },
  {
    "question": "Quelle fonction R est utilisée pour effectuer une analyse en composantes principales (ACP) ?",
    "reponse": "prcomp",
    "theme": "r",
    "type": "quiz",
    "propositions": ["prcomp", "pca", "princomp"]
  },
  {
    "question": "Quel package R est utilisé pour l’apprentissage profond ?",
    "reponse": "keras",
    "theme": "r",
    "type": "quiz",
    "propositions": ["keras", "tensorflow", "torch"]
  },
  {
    "question": "Quelle fonction R permet d’effectuer une régression Ridge ou Lasso ?",
    "reponse": "glmnet",
    "theme": "r",
    "type": "quiz",
    "propositions": ["glmnet", "lm", "ridge"]
  },
    {
    "question": "Qui est le Manager de SCALES ?",
    "reponse": "Amal Ouyizeme est la Manager de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui dirige SCALES ?",
    "reponse": "Amal Ouyizeme est la Manager de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui est la responsable de SCALES ?",
    "reponse": "Amal Ouyizeme est la Manager de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },

  {
    "question": "Qui est l’Academic Advisor de SCALES ?",
    "reponse": "Najib Bounahai est l’Academic Advisor de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui occupe le poste d’Academic Advisor ?",
    "reponse": "Najib Bounahai est l’Academic Advisor de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui conseille académiquement SCALES ?",
    "reponse": "Najib Bounahai est l’Academic Advisor de SCALES.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui est responsable du programme LAPEX ?",
    "reponse": "Badreddine Sandid est en charge de LAPEX et WORC.",
    "theme": "personnel scales",
    "type": "definition"
  },
    {
    "question": "Qui est en charge du programme LAPEX et WORC ?",
    "reponse": "Badreddine Sandid est en charge de LAPEX et WORC.",
    "theme": "personnel scales",
    "type": "definition"
  },
{
    "question": "Qui est en charge du programme des langues ?",
    "reponse": "Badreddine Sandid est en charge de LAPEX et WORC.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui gère le programme LAPEX ?",
    "reponse": "Badreddine Sandid est en charge de LAPEX et WORC.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui s’occupe de WORC ?",
    "reponse": "Badreddine Sandid est sont en charge de LAPEX et WORC.",
    "theme": "personnel scales",
    "type": "definition"
  },

  {
    "question": "Qui est responsable du programme de stages ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },
     {
    "question": "Qui est responsable des stages ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },
    {
    "question": "Qui est responsable des programme d'IP, IP3, CAP, MILL, Bootcamps ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },
    {
    "question": "Qui s’occupe d'IP, IP3, CAP, MILL, Bootcamps ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui encadre les stages IP et IP3 ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui gère les Bootcamps à SCALES ?",
    "reponse": "Khadija Alaoui est Senior Operation Officer et responsable des stages (IP, IP3, CAP, MILL, Bootcamps).",
    "theme": "personnel scales",
    "type": "definition"
  },

  {
    "question": "Qui est responsable du programme STADAC ?",
    "reponse": "Meryem Bouaalal et Oumaima Dali sont Junior Operation Officers en charge du programme STADAC.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui s’occupe de STADAC ?",
    "reponse": "Meryem Bouaalal et Oumaima Dali sont Junior Operation Officers en charge du programme STADAC.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui gère le programme STADAC à SCALES ?",
    "reponse": "Meryem Bouaalal et Oumaima Dali sont Junior Operation Officers en charge du programme STADAC.",
    "theme": "personnel scales",
    "type": "definition"
  },

  {
    "question": "Qui est responsable du programme Study Skills ?",
    "reponse": "Ikrame Ennabil est Junior Operation Officer en charge de Study Skills.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui gère Study Skills à SCALES ?",
    "reponse": "Ikrame Ennabil est Junior Operation Officer en charge de Study Skills.",
    "theme": "personnel scales",
    "type": "definition"
  },
  {
    "question": "Qui s’occupe du programme Study Skills ?",
    "reponse": "Ikrame Ennabil est Junior Operation Officer en charge de Study Skills.",
    "theme": "personnel scales",
    "type": "definition"
  }
]

def extraire_theme(question_user):
    question_user = question_user.lower()
    best_theme = None
    best_score = 0
    for theme, mots in THEMES.items():
        for mot in mots:
            if mot in question_user or fuzz.ratio(mot, question_user) > 80:
                return theme
            score = fuzz.partial_ratio(mot, question_user)
            if score > best_score:
                best_score = score
                best_theme = theme
    # Reconnaissance manuelle en cas d'ambiguïté
    keywords = {
    "intelligence artificielle": ["intelligence artificielle", "ia", "ai", "artificielle", "machine learning", "inteligence artif","IA","AI"],
    "soft skills": ["soft skill", "softskills", "soft-skills", "compétence douce", "soft", "softs", "compétences","adaptabilité", "communication", "esprit d'équipe", "organisation", "autonomie"],
    "communication": ["communication", "communiquer", "comm","rapport","rapport académique","bibliographie","article"],
    "langues": ["langues", "langage", "anglais", "français", "espagnol", "allemand"],
    "cv": ["cv", "curriculum", "curriculum vitae", "c.v.", "rédaction", "rubrique", "section", "formation","expérience", "expériences", "compétence", "compétences", "photo", "structure", "résumé", "profil","trou dans le cv", "erreur cv", "modèle cv"],
    "entretien": ["entretien", "recrutement", "oral", "interview","questions entretien", "présentation", "préparer entretien", "parlez-moi de vous", "difficile","simulateur", "recrutement", "recruteur","questions difficiles", "présentez-vous", "simulation entretien","entretien technique"],
    "lettre de motivation": ["lettre motivation", "motivation", "Lettre de motivation","normes de lettre de motivation", "titre de lettre", "bullet", "signature", "conclure", "outils lettre","cover letter"],
    "traduction": ["traduction", "translate", "traduire", "traduit", "comment dit-on", "comment dire"],
    "synonyme": ["synonyme", "syno", "donne un synonyme", "autre mot pour"],
    "antonyme": ["antonyme", "anton", "contraires", "contraire", "opposé", "donne un antonyme"],
    "conjugaison": ["conjugaison", "conjuguer", "verbe", "temps", "présent", "imparfait", "passé", "futur"],
    "python": ["python", "py", "pyhton", "piton"],
    "r": ["r", "langage r"],
    "data mining": ["data mining", "datamining", "mining", "extraction données"],
    "scales": ["scales","SCALES","Bootcamps","Study Skills","module Writing and Oratory Skills","plagiat"],
    "mill": ["MILL","mill"],
    "worc": ["Worc","WORC","worc"],
    "STADAC": ["STADAC","stadac","Stadac","outil de programmation"],
    "CS": ["cs","CS","Community Service","citoyenneté","civic engagement"],
    "cap": ["CAP","cap","IELTS","IP", "IP3"],
    "LAPEX": ["lapex","LAPEX","Study Skills","LCSS","Skills Portfolio","Portfolio","LRS","langues","LCSS","exigences linguistiques","progrès en langues","langues étrangères","OTS"],
    "data science": ["data science", "datascience", "data scientist", "science des données"],
    "techniques de recherche d'emploi et stage": ["offres", "plateforme","candidature spontanée", "postuler","recherche", "stage", "emploi", "postuler", "candidature", "offre d'emploi","plateforme emploi", "jobteaser", "indeed", "welcome to the jungle","étranger", "trouver un emploi","travail","job","recherche d'emploi"],
    "linkedin": ["linkedin", "profil linkedin", "compte linkedin", "ajouter sur linkedin", "réseau linkedin","importance linkedin", "recommandation linkedin", "message linkedin", "partager linkedin"],
    "réseautage professionnel": ["réseau","contacts", "piston", "groupe", "meetup", "relations", "réseautage", "contacts pro"],
    "orientation professionnelle": ["projet professionnel", "orientation", "carrière", "m2", "positionnement", "grand groupe", "startup", "PME"],
    "événements professionnels": ["meet & greet", "événement", "intervenant", "agenda", "calendrier", "timide", "observer", "plateforme événement","Meet & Greet", "événements","Meet & Greet","Meet&Greet","Meet and Greet"],
    "valorisation des expériences": ["valoriser", "expériences internationales", "doctorat", "projet académique", "engagement associatif", "compétence transférable"],
    "préparation personnelle": ["préparer", "se sentir prêt", "présentation personnelle", "se présenter", "mentalement"],
    "personnel scales": ["personnel","staff","responsable","manager","academic advisor","program officer","operation officer","qui est","responsable de","en charge de","dirige","encadre","programme Study Skills","programme Lapex","lapex","worc","study skills","stadac","langues","programme des langues","LAPEX","qui t'as crée","programmé"],
    "généralités et questions fréquentes": ["fin d'études", "taille entreprise", "questions fréquentes", "généralités"]
        
    }
# ===================== INTELLIGENCE OFFLINE =====================
def _norm(s: str) -> str:
    s = s or ""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("\u00A0", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

_BASE_NORM = []
for i, item in enumerate(base):
    _BASE_NORM.append({
        "i": i,
        "q_norm": _norm(item.get("question", "")),
        "r": item.get("reponse", ""),
        "theme": item.get("theme", ""),
        "theme_norm": _norm(item.get("theme", "")),
        "type": (item.get("type", "") or "").lower(),
        "orig": item
    })

_THEMES_NORM = { _norm(tk): list({ _norm(w) for w in kws }) for tk, kws in THEMES.items() }

def _detect_theme_norm(q: str) -> str:
    qn = _norm(q)
    best_theme, best_hit = "general", 0
    for t_norm, kws in _THEMES_NORM.items():
        hit = 1 if any(kw and kw in qn for kw in kws) else 0
        if hit > best_hit:
            best_theme, best_hit = t_norm, hit
    return best_theme

def _candidates_by_theme(q: str):
    t = _detect_theme_norm(q)
    if t == "general":
        return _BASE_NORM
    kws = set(_THEMES_NORM.get(t, []))
    if not kws:
        return _BASE_NORM
    res = []
    qn = _norm(q)
    for it in _BASE_NORM:
        if it["theme_norm"] == t or any(kw and kw in it["q_norm"] for kw in kws):
            res.append(it)
    return res if len(res) >= 5 else _BASE_NORM

def _score(q_norm: str, cand_q_norm: str) -> int:
    a = fuzz.token_set_ratio(q_norm, cand_q_norm)
    b = fuzz.partial_ratio(q_norm, cand_q_norm)
    c = fuzz.token_sort_ratio(q_norm, cand_q_norm)
    return int(0.5*a + 0.3*b + 0.2*c)

# ===================== THEMATIC KB =====================
_THEMATIC_KB = {
    "cv": {
        "principes": ["1 page claire", "Résultats chiffrés", "Mots-clés de l’offre", "Mise en page simple"],
        "actions": ["Adapter le titre", "Mettre projets pertinents", "Nettoyer fautes", "Exporter en PDF"]
    },
    "techniques de recherche d'emploi et stage": {
        "principes": ["Cibler offres alignées", "Activer réseau", "Candidatures personnalisées"],
        "actions": ["Suivre candidatures", "Contacter 2 personnes", "Relancer en J+7"]
    },
    "python": {
        "principes": ["pandas, NumPy", "scikit-learn", "PEP8 + virtualenv"],
        "actions": ["pd.read_csv()", "pd.merge()", "model.fit()"]
    },
    "r": {
        "principes": ["tidyverse, ggplot2", "lm/glm", "caret"],
        "actions": ["filter+mutate", "ggplot", "lm() + summary()"]
    },
    "intelligence artificielle": {
        "principes": ["Classification, régression, clustering", "Toujours valider par métriques"],
        "actions": ["Clarifier la tâche", "Commencer baseline simple"]
    }
}

def _generate_thematic_answer(question: str) -> str:
    t_norm = _detect_theme_norm(question)
    # map clé
    def _key_real(norm_key):
        for k in _THEMATIC_KB.keys():
            if _norm(k) == norm_key:
                return k
        return None
    real_key = _key_real(t_norm)
    if not real_key:
        return "Je n’ai pas cette info exacte. Donne plus de contexte (CV, emploi, Python, R, IA)."
    kb = _THEMATIC_KB[real_key]
    lines = [f"Réponse rapide — thème {real_key} :"]
    if kb.get("principes"):
        lines.append("Principes clés :")
        for p in kb["principes"]:
            lines.append(f"• {p}")
    if kb.get("actions"):
        lines.append("Actions concrètes :")
        for a in kb["actions"]:
            lines.append(f"• {a}")
    return "\n".join(lines)

# ===================== SMART ANSWER + QUIZ =====================
def smart_answer(question: str) -> str:
    q = (question or "").strip()
    if not q:
        return "Pose ta question et je t’aide 😊"
    qn = _norm(q)
    for it in _BASE_NORM:
        if qn == it["q_norm"]:
            return it["r"]
    cands = _candidates_by_theme(q)
    best, best_s = None, -1
    for it in cands:
        s = _score(qn, it["q_norm"])
        if s > best_s:
            best, best_s = it, s
    if best and best_s >= 90: return best["r"]
    if best and best_s >= 75: return best["r"]
    return _generate_thematic_answer(q)

# ===================== QUIZ INTELLIGENT (utilisé en interne) =====================
def smart_quiz(question: str):
    q = (question or "").strip()
    if not q:
        return {"reponse": "Pose une question de quiz.", "propositions": []}
    qn = _norm(q)

    # exact parmi les items de type quiz
    for it in _BASE_NORM:
        if it["type"] == "quiz" and qn == it["q_norm"]:
            return {
                "reponse": it["orig"].get("reponse", ""),
                "propositions": it["orig"].get("propositions", []) or []
            }

    # fuzzy parmi les quiz
    quiz_cands = [it for it in _BASE_NORM if it["type"] == "quiz"]
    if not quiz_cands:
        return {"reponse": "Aucun quiz défini.", "propositions": []}

    best, best_s = None, -1
    for it in quiz_cands:
        s = _score(qn, it["q_norm"])
        if s > best_s:
            best, best_s = it, s

    if best and best_s >= 80:
        return {
            "reponse": best["orig"].get("reponse", ""),
            "propositions": best["orig"].get("propositions", []) or []
        }
    return {"reponse": "Quiz introuvable, reformule.", "propositions": []}


# ===================== ROUTE /repondre (POST uniquement) =====================
@app.route('/repondre', methods=['POST'])
def repondre():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    return jsonify({"reponse": smart_answer(question)})


# ===================== OUTILS THEME (compatibilité) =====================
# mapping "thème normalisé" -> "thème EXACT tel que présent dans la base"
_THEME_KEYS_ORIG = sorted({(e.get("theme") or "").strip() for e in base if e.get("theme")})
_NORM2ORIG = {_norm(t): t for t in _THEME_KEYS_ORIG if t}

def _resolve_theme_for_quiz(question_text: str, explicit_theme: str = "") -> str:
    """
    Renvoie un nom de thème EXACT (présent dans la base) ou ''.
    Ordre:
      1) thème explicite (payload)
      2) extraire_theme() (ton ancienne fonction)
      3) _detect_theme_norm() -> mappée via _NORM2ORIG
    """
    # 1) thème explicite
    if explicit_theme:
        t = explicit_theme.strip()
        if t in _THEME_KEYS_ORIG:
            return t
        tnorm = _norm(t)
        if tnorm in _NORM2ORIG:
            return _NORM2ORIG[tnorm]

    # 2) ancienne détection
    try:
        t = extraire_theme(question_text or "")
        if t and t in _THEME_KEYS_ORIG:
            return t
        if t:
            tnorm = _norm(t)
            if tnorm in _NORM2ORIG:
                return _NORM2ORIG[tnorm]
    except Exception:
        pass

    # 3) nouvelle détection
    tnorm = _detect_theme_norm(question_text or "")
    return _NORM2ORIG.get(tnorm, "")


# ===================== ROUTE /quiz (POST uniquement, même format qu'avant) =====================
@app.route('/quiz', methods=['POST'])
def quiz():
    data = request.get_json(silent=True) or {}

    # Comme avant : la "question" sert à déduire le thème
    question_raw = (data.get('question') or '').strip()
    theme_hint   = (data.get('theme') or '').strip()   # optionnel pour forcer un thème
    # -> utilise le resolve pour être robuste mais garde le même résultat final
    theme = _resolve_theme_for_quiz(question_raw.lower(), theme_hint)

    quiz = []
    if theme:
        # mêmes filtres que ton ancien code : EXACTEMENT 3 propositions
        candidats = [
            e for e in base
            if e.get("theme") == theme
               and isinstance(e.get("propositions"), list)
               and len(e["propositions"]) == 3
        ]
        random.shuffle(candidats)
        for entry in candidats[:5]:
            # même construction de réponses que l'ancien code
            reponses = [entry.get("reponse", "")] + [
                p for p in entry.get("propositions", []) if p != entry.get("reponse", "")
            ]
            reponses = [r for r in reponses if isinstance(r, str) and r.strip()]
            random.shuffle(reponses)
            if not reponses:
                continue
            try:
                correct_index = reponses.index(entry.get("reponse", ""))
            except ValueError:
                reponses.insert(0, entry.get("reponse", ""))
                correct_index = 0
            quiz.append({
                "q": entry.get("question", ""),
                "a": reponses,
                "correct": correct_index
            })

    # même sortie qu'avant (au moins 2 éléments si possible)
    return jsonify({"quiz": quiz[:max(2, len(quiz))]})

@app.route("/web_answer", methods=["POST"])
def web_answer_route():
    data = request.get_json(silent=True) or {}
    q = (data.get("question") or data.get("message") or "").strip()
    if not q:
        return jsonify({"answer": "Pose ta question et je t’aide 😊", "sources": []})
    res = web_answer(q)
    return jsonify(res)

# ====== Route spéciale pour servir le React build (doit être tout à la fin) ======
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)










































