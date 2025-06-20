# -*- coding: utf-8 -*-
"""
Created on Thu Jun 19 15:25:28 2025

@author: 129391
"""

import os
import pydicom
from tkinter import Tk, filedialog, messagebox

def lire_dicom_fichier_ou_dossier():
    root = Tk()
    root.withdraw()

    # Demande à l'utilisateur ce qu'il veut ouvrir
    choix = messagebox.askyesno("Choix", "Voulez-vous ouvrir un fichier DICOM unique ?\n\nOui = Fichier\nNon = Dossier")

    if choix:
        # Sélection d'un fichier
        fichier = filedialog.askopenfilename(
            title="Sélectionnez un fichier DICOM",
            filetypes=[("Fichier DICOM", "*.dcm"), ("Tous les fichiers", "*.*")]
        )
        if fichier:
            fichiers = [fichier]
    else:
        # Sélection d'un dossier
        dossier = filedialog.askdirectory(title="Sélectionnez un dossier contenant des fichiers DICOM")
        if dossier:
            fichiers = [
                os.path.join(dossier, f)
                for f in sorted(os.listdir(dossier))
                if f.lower().endswith(".dcm")
            ]

    if not fichiers:
        print("Aucun fichier sélectionné.")
        return

    ct_affiche = False

    for fichier in fichiers:
        try:
            ds = pydicom.dcmread(fichier)

            if getattr(ds, "Modality", None) == "CT":
                if ct_affiche:
                    continue
                ct_affiche = True
                print(f"--- ✅ Première image CT : {os.path.basename(fichier)} ---")
            else:
                print(f"--- 📄 Fichier DICOM : {os.path.basename(fichier)} ({getattr(ds, 'Modality', 'Inconnu')}) ---")

            print(ds)
            print("\n" + "=" * 60 + "\n")

        except Exception as e:
            print(f"❌ Erreur avec le fichier {fichier} : {e}")

# Lancer la fonction
lire_dicom_fichier_ou_dossier()

