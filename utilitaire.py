import numpy as np
import scipy.optimize as sp
import scipy.odr as odr
import matplotlib.pyplot as plt
from Spectre import Spectre

def f(params, x):
    return params[0]*x + params[1]

def etalonnage(spec: Spectre, theo, show=False):
    """Fonction qui calcue, affiche et retourne l'étalonnage en énergie d'un spectre.

    Args:
        spec (Spectre): Spectre d'étalonnage
        theo (list): Liste contenant les valeurs théoriques des points, en ordre
        show (bool, optional): true si l'on souhaite visualiser l'étalonnage, false sinon. Defaults to False.

    Returns:
        tuple: Le premier élément correspond aux paramètres optimaux, le deuxième à l'incertitude sur ceux-ci et le troisième aux données
                du lissage.
    """
    xdata = []
    erreur_x_data = []

    # Itérations sur les photopics dont l'énergie théorique est dans theo
    for peak in spec.get_Peaks():
        # Le centroid du photopic
        xdata.append(peak[1][1])
        erreur_x_data.append(np.abs(peak[1][2]))
    
    # Numpy array pour faciliter le traitement
    xdata = np.array(xdata)
    fitXData = np.linspace(0, 5000, 5000)
    ydata = np.array(theo)

    # curve fit
    model = odr.Model(f)
    myData = odr.Data(xdata, ydata, wd=erreur_x_data)
    monOdr = odr.ODR(myData, model, beta0=[35, -20])
    output = monOdr.run()
    fitData = f(output.beta, fitXData)

    fitUpper = f(output.beta + output.sd_beta, fitXData)
    fitLower = f(output.beta - output.sd_beta, fitXData)
    # Calculer R^2
    residuals = ydata- f(output.beta, xdata)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((ydata-np.mean(ydata))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # Affichage
    if show:
        fig, ax = plt.subplots()
        # Titres et labels d'axes
        fig.patch.set_facecolor('white')
        fig.patch.set_alpha(0.6)
        # ax.set_title("Étalonnage du détecteur NaI(Tl)")
        ax.set_xlabel("Canaux (-)")
        ax.set_ylabel("Énergie (keV)")

        # Ticks
        ax.tick_params(direction='in', length=3, width=1, colors='k',
                        grid_color='k', grid_alpha=0.5)
        
        
        # Équation et R^2
        ax.text(500, 1100, f"E = {output.beta[0]:.2f}$\cdot$Ch - {np.abs(output.beta[1]):.2f}", size=15)
        ax.text(500, 900, f"$R^2 = ${r_squared:.4f}", size=15)

        # Data et fit
        ax.set_xlim(0, 4096)
        ax.errorbar(xdata, ydata, xerr=erreur_x_data, ms=10, c="g", marker="^", ecolor='k', capsize=2, fmt="o", label="Données expérimentales")
        ax.plot(fitXData, fitData, "r--", label="Régression linéaire")
        ax.fill_between(fitXData, fitUpper, fitLower, alpha=0.2, label="Intervalle de confiance")
        ax.legend(loc = "lower right")

        # print(popt)
        plt.show()
    return output.beta, output.sd_beta, fitData

