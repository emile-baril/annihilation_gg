from Spectre import Spectre
from utilitaire import *
import numpy as np

# TODO : Ajouter le traitement des incertitudes.

def main():
    # Spectre de calibration
    spec_calib_fixe = Spectre("spectres\detecteur_fixe\cs137co57co60_calibration.Spe", 12)
    # spec_calib_fixe.plot_spectrum(_mk='x', fits=False)
    # spec_calib_fixe.plot_peaks(["Photopic du Co57", "Photopic du Cs137", "Premier photopic du Co60", "Deuxième photopic du Co60"], multiple=False, fits=True)

    # Étalonnage
    theoValues_calibration = [122, 662, 1173.2, 1332.5]
    popt_fixe, pcov_fixe, fitdata_fixe = etalonnage(spec_calib_fixe, theoValues_calibration, show=True)
    print(f"La regression linéaire de l'étalonnage donne une pente de {popt_fixe[0]}\pm {pcov_fixe[0]}"
        f" et une ordonnée à l'origine de {popt_fixe[1]}\pm{pcov_fixe[1]}")
    
    # Pic du Na22 pour le detecteur fixe
    photopicNa22 = Spectre("spectres\detecteur_fixe\\na22_spectrum_take2.Spe", 12)
    photopicNa22.plot_spectrum()
    # On get le pix
    photopic = photopicNa22.rois_infos[0]
    pic2 = photopicNa22.rois_infos[1]
    
    # Conversion de channel vers énergie
    channels = np.array(photopicNa22.xdata)
    energy_photopic = f(popt_fixe, channels)[photopic[0][0]:photopic[0][1]]
    counts_photpic = photopicNa22.ydata[photopic[0][0]:photopic[0][1]]
    # Erreur sur l'énergie obtenue par propagation d'incertitude
    delta_energy = incertitude_channel(channels, pcov_fixe)

    # Affichage du pic
    fig, ax = plt.subplots(1, 1)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.6)
    ax.set_ylabel("Comptes (-)")
    ax.set_xlabel("Energie (keV)")
    ax.errorbar(energy_photopic, counts_photpic,
                xerr=delta_energy[photopic[0][0]:photopic[0][1]], yerr=[np.sqrt(i) for i in counts_photpic], color="red", marker="o", ecolor="k", fmt='o', ms="5", label="Données expérimentales", zorder=1)
    
    # Curve fit du pic:
    popt_photopic, pcov_photopic = sp.curve_fit(Spectre.gauss, energy_photopic, counts_photpic, p0=[100, (photopic[0][0]+photopic[0][1])/2, (photopic[0][1]-photopic[0][0])/2, 0])
    fitData_photopic = Spectre.gauss(energy_photopic, *popt_photopic)
    ax.text(0.75, 0.90, f"$\mu$ = {popt_photopic[1]:.2f}", transform=ax.transAxes)
    ax.text(0.75, 0.85, f"$\sigma$ = {np.abs(popt_photopic[2]):.2f}", transform=ax.transAxes)
    ax.plot(energy_photopic, fitData_photopic, label="Lissage gaussien", zorder=10, linewidth=2)
    ax.legend(loc="upper left")
    plt.show()

    # Affichage du 2ième pic
    energy_pic2 = f(popt_fixe, channels)[pic2[0][0]:pic2[0][1]]
    counts_pic2= photopicNa22.ydata[pic2[0][0]:pic2[0][1]]

    # Affichage du pic
    fig, ax = plt.subplots(1, 1)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(0.6)
    ax.set_ylabel("Comptes (-)")
    ax.set_xlabel("Energie (keV)")
    ax.errorbar(energy_pic2, counts_pic2,
                xerr=delta_energy[pic2[0][0]:pic2[0][1]], yerr=[np.sqrt(i) for i in counts_pic2], color="red", marker="o", ecolor="k", fmt='o', ms="5", label="Données expérimentales", zorder=1)

    # Curve fit du pic:
    popt_pic2, pcov_pic2 = sp.curve_fit(Spectre.gauss, energy_pic2, counts_pic2, p0=[100, (energy_pic2[0]+energy_pic2[-1])/2, (energy_pic2[0]-energy_pic2[-1])/2, 0])
    fitData_pic2 = Spectre.gauss(energy_pic2, *popt_pic2)
    ax.text(0.75, 0.90, f"$\mu$ = {popt_pic2[1]:.2f}", transform=ax.transAxes)
    ax.text(0.75, 0.85, f"$\sigma$ = {np.abs(popt_pic2[2]):.2f}", transform=ax.transAxes)
    ax.plot(energy_pic2, fitData_pic2, label="Lissage gaussien", zorder=10, linewidth=2)
    ax.legend(loc="upper left")

    plt.show()

def incertitude_channel(channel, params_delta):
    # Caclul la propagation d'une incertitude
    delta_m = channel*params_delta[0]
    delta = np.sqrt(delta_m**2 + params_delta[1]**2)
    return delta

main()