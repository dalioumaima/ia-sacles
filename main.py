from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
from fuzzywuzzy import fuzz
import os

app = Flask(__name__, static_folder="build", static_url_path="/")
CORS(app)

THEMES = {
    "intelligence artificielle": ["intelligence artificielle", "ia", "ai", "artificielle", "machine learning", "inteligence artif"],
    "soft skills": ["soft skill", "softskills", "soft-skills", "compétence douce", "soft", "softs"],
    "communication": ["communication", "communiquer", "comm"],
    "langues": ["langues", "langage", "anglais", "français", "espagnol", "allemand"],
    "cv": ["cv", "curriculum", "curriculum vitae", "c.v.", "bon cv", "rédaction cv"],
    "entretien": ["entretien", "recrutement", "oral", "interview"],
    "traduction": ["traduction", "translate", "traduire", "traduit", "comment dit-on", "comment dire"],
    "synonyme": ["synonyme", "syno", "donne un synonyme", "autre mot pour"],
    "antonyme": ["antonyme", "anton", "contraires", "contraire", "opposé", "donne un antonyme"],
    "conjugaison": ["conjugaison", "conjuguer", "verbe", "temps", "présent", "imparfait", "passé", "futur"],
    "python": ["python", "py", "pyhton", "piton"],
    "r": ["r", "langage r"],
    "data mining": ["data mining", "datamining", "mining", "extraction données"],
    "data science": ["data science", "datascience", "data scientist", "science des données"]
}

base = [
     # Exemples pour plusieurs thèmes, à enrichir
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
  "theme": "rédaction",
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
  "theme": "rédaction",
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
    "theme": "IA",
    "type": "avantage"
  },
  {
    "question": "Qui la directrice de Scales?",
    "reponse": "the wonderful Amal",
    "theme": "IA",
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
        "conjugaison": ["conjugue", "conjugaison", "conjuguer", "verbe", "temps", "présent", "imparfait", "passé", "futur"],
        "traduction": ["traduit", "traduction", "translate", "traduire", "comment dit-on", "comment dire"],
        "synonyme": ["synonyme", "syno", "donne un synonyme", "autre mot pour"],
        "antonyme": ["antonyme", "contraire", "opposé", "donne un antonyme"],
        "langues": ["anglais", "espagnol", "français", "allemand", "langue"]
    }
    for th, mots in keywords.items():
        if any(m in question_user for m in mots):
            return th
    if best_score > 45:
        return best_theme
    return None

def simple_reformulation(texte, theme):
    if texte:
        alternatives = [
            lambda s: f"En d'autres termes ({theme}) : {s}",
            lambda s: f"Autrement dit ({theme}) : " + s.lower(),
            lambda s: f"On peut résumer ainsi ({theme}) : {s}",
            lambda s: s.replace("c'est", "cela désigne").replace("C'est", "Cela désigne"),
            lambda s: f"On pourrait dire que ({theme}) : " + s.lower()
        ]
        reformulation = random.choice(alternatives)(texte)
        if reformulation == texte:
            reformulation = f"Pour faire simple ({theme}) : " + texte
        return reformulation
    else:
        # Si pas de définition dans la base, essaye de paraphraser la question en réponse
        return f"Je comprends que tu veux une définition sur le thème '{theme}'. En résumé, c'est un concept clé à approfondir dans ce domaine."

@app.route('/repondre', methods=['POST'])
def repondre():
    data = request.get_json()
    question = data.get('question', '').strip().lower()
    previous = data.get('previous', None)
    theme = extraire_theme(question)

    # 1. D'abord, cherche une correspondance quasi exacte de la question !
    for elem in base:
        if elem.get("question") and fuzz.token_set_ratio(elem["question"].lower(), question) > 87:
            return jsonify({"reponse": elem["reponse"]})

    # 2. Si demande de reformulation ou de définition, fait une reformulation intelligente (jamais hors sujet)
    if any(mot in question for mot in ["reformule", "explique autrement", "définition", "c'est quoi", "definir", "expliquer"]):
        defs = [elem["reponse"] for elem in base if elem.get("theme") == theme and elem.get("type") == "definition"]
        if defs:
            reformu = [d for d in defs if d != previous]
            if reformu:
                return jsonify({"reponse": simple_reformulation(random.choice(reformu), theme)})
            else:
                return jsonify({"reponse": simple_reformulation(defs[0], theme)})
        else:
            return jsonify({"reponse": simple_reformulation(None, theme if theme else "cette thématique")})

    # 3. Sinon, réponse normale (définition prioritaire par thème si rien d'autre trouvé)
    for elem in base:
        if elem.get("theme") == theme and elem.get("type") == "definition":
            return jsonify({"reponse": elem["reponse"]})
    for elem in base:
        if elem.get("theme") == theme:
            return jsonify({"reponse": elem["reponse"]})
    return jsonify({"reponse": f"Je n'ai pas encore de réponse détaillée pour ce sujet, mais tu peux préciser ta question ou changer la formulation."})

@app.route('/quiz', methods=['POST'])
def quiz():
    data = request.get_json()
    question = data.get('question', '').lower()
    theme = extraire_theme(question)
    quiz = []
    if theme:
        candidats = [e for e in base if e.get("theme") == theme and "propositions" in e and len(e["propositions"]) == 3]
        random.shuffle(candidats)
        for entry in candidats[:5]:
            reponses = [entry["reponse"]] + [p for p in entry["propositions"] if p != entry["reponse"]]
            random.shuffle(reponses)
            correct_index = reponses.index(entry["reponse"])
            quiz.append({
                "q": entry["question"],
                "a": reponses,
                "correct": correct_index
            })
    return jsonify({"quiz": quiz[:max(2, len(quiz))]})


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
