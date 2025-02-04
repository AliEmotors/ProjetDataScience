# stats.py

# Variables pour stocker les données des thèmes
# Remplacez ces valeurs par vos données réelles

themes_data = {
    "Energy Market": 23.94,
    "Contracts": 16.11,
    "Meeting Planning": 15.28,
    "Personal": 6.77,
    "Human Resources": 4.59,
    "IT" : 4.37,
    "Legal" : 3.80,
    "Finance": 2.79
}

# Emails Topics Repartition
topic_stats = [(theme, value) for theme, value in themes_data.items()]  # Liste des thèmes et pourcentages

# Legal-Spam-Noise

legal_spam_noise_stats = {
    "Legal": 38,
    "Spam": 30,
    "Noise": 13}
legal_spam_noise = [(theme, value) for theme, value in legal_spam_noise_stats.items()]  # Liste des thèmes et pourcentages