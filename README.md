# annihilation_gg

Le script d'analyse suivant sert à analyser les spectres gamma de différentes sources radioactives dans le cadre de l'expérience d'annihilation gamma du cours de Physique
expérimentale 5 à l'université Laval.

## Class Spectre

La classe Spectre sert à encapsuler les spectres acquis et possède les méthodes et les attributs suivants:

Attributs :
- self.filename   : Un string qui contient le path du fichier.
- self.ydata      : Les données en y (counts).
- self.xdata      : Les données en x (channel).
- self.rois_infos : Une liste de tuples ou chaque tuple encode des infos sur un ROI et son fit gaussien ((start, stop), popt, pcov, fit_data).
- self.nb_rois    : Le nombre de ROI présent dans le spectre.

Méthodes:
- read_file()     : Lis le fichier .spe et extrait les informations importantes. La méthode est appelé par le constructeur et ne devrait plus être appelée par la suite.
- plot_spectrum() : Affiche le spectre au complet avec possibilité d'afficher les fits gaussien des ROIs sur ceux-ci.
- compute_fit()   : Méthode qui calcule le fit gaussien d'un ROI et retourne les informations pertinenentes sur celui-ci. La méthode est appelé par le constructeur et ne devrait plus être appelée par la suite.
- plot_Peaks()    : Méthode qui affiche les ROIs séparemment avec option d'afficher les fits gaussien sur ceux-ci.
- get_xdata()     : Méthode qui retourne self.xdata[startl: stop].
- get_Peaks()     : Méthode qui retourne les informations sur les peaks.

## Étalonnage

Le fichier utilitaire.py contient une fonction qui calcule un étalonnage avec un spectre contenant les photopics de plusieurs sources radioactives.
