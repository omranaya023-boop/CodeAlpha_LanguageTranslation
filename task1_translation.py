import customtkinter as ctk
from tkinter import messagebox
import pyttsx3
from transformers import pipeline

# Configuration de l'apparence
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Initialisation du moteur vocal
engine = pyttsx3.init()

# --- CHARGEMENT DU MODÈLE DE TRADUCTION LOCAL ---
# On utilise un modèle léger spécialisé Français <-> Anglais pour commencer
print("Chargement du modèle de traduction local (veuillez patienter)...")
# Ce modèle est très léger et rapide une fois téléchargé
translator_fr_en = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")
translator_en_fr = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")
print("Modèle prêt !")

def translate_text():
    text = input_text.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showwarning("Attention", "Veuillez entrer du texte.")
        return
    
    src_lang = source_lang_combo.get()
    tgt_lang = target_lang_combo.get()
    
    try:
        # Traduction locale (Hors ligne)
        if src_lang == "Français" and tgt_lang == "Anglais":
            result = translator_fr_en(text)[0]['translation_text']
        elif src_lang == "Anglais" and tgt_lang == "Français":
            result = translator_en_fr(text)[0]['translation_text']
        else:
            result = "[Erreur] Pour cette démo, seules les paires FR-EN et EN-FR sont supportées localement."
            
        output_text.delete("1.0", "end")
        output_text.insert("1.0", result)
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la traduction : {e}")

def copy_text():
    text = output_text.get("1.0", "end-1c").strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Succès", "Texte copié !")

def speak_text():
    text = output_text.get("1.0", "end-1c").strip()
    if text and not text.startswith("["):
        engine.say(text)
        engine.runAndWait()

def swap_languages():
    src = source_lang_combo.get()
    tgt = target_lang_combo.get()
    source_lang_combo.set(tgt)
    target_lang_combo.set(src)

# --- Création de l'interface ---
root = ctk.CTk()
root.title("CodeAlpha - Pro Translator (Local AI)")
root.geometry("600x550")

title_label = ctk.CTkLabel(root, text="🌍 Traducteur IA Local", font=("Roboto", 24, "bold"))
title_label.pack(pady=20)

# Frame pour les langues (Limité à FR et EN pour le modèle local)
frame_lang = ctk.CTkFrame(root, fg_color="transparent")
frame_lang.pack(pady=10)

langues = ["Français", "Anglais"]

source_lang_combo = ctk.CTkComboBox(frame_lang, values=langues, width=150, state="readonly")
source_lang_combo.set("Français")
source_lang_combo.pack(side="left", padx=10)

swap_btn = ctk.CTkButton(frame_lang, text="⇄", width=40, command=swap_languages, font=("Arial", 16, "bold"))
swap_btn.pack(side="left", padx=5)

target_lang_combo = ctk.CTkComboBox(frame_lang, values=langues, width=150, state="readonly")
target_lang_combo.set("Anglais")
target_lang_combo.pack(side="left", padx=10)

ctk.CTkLabel(root, text="Texte à traduire :", font=("Roboto", 14)).pack(anchor="w", padx=40)
input_text = ctk.CTkTextbox(root, width=500, height=100, font=("Roboto", 14))
input_text.pack(pady=5)

translate_btn = ctk.CTkButton(root, text="Traduire", command=translate_text, width=200, height=40, font=("Roboto", 14, "bold"))
translate_btn.pack(pady=15)

ctk.CTkLabel(root, text="Résultat :", font=("Roboto", 14)).pack(anchor="w", padx=40)
output_text = ctk.CTkTextbox(root, width=500, height=100, font=("Roboto", 14), text_color="#2ecc71")
output_text.pack(pady=5)

frame_actions = ctk.CTkFrame(root, fg_color="transparent")
frame_actions.pack(pady=15)

copy_btn = ctk.CTkButton(frame_actions, text="📋 Copier", command=copy_text, width=120, fg_color="#34495e", hover_color="#2c3e50")
copy_btn.pack(side="left", padx=10)

speak_btn = ctk.CTkButton(frame_actions, text="🔊 Écouter", command=speak_text, width=120, fg_color="#34495e", hover_color="#2c3e50")
speak_btn.pack(side="left", padx=10)

root.mainloop()