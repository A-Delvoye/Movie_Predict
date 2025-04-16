# import os
# from scrapy.cmdline import execute

# print('hhhhhhhhhhhhheeeeeeeeeeelllllllllllllllllllloooooooooooooo')
# spider = "moviespider"

# project_root = "/opt/airflow/Movie_Predict/moviescraper"  # Dossier contenant scrapy.cfg
# # project_root='/home/addeche/Documents/Projets Python/scraping_allocine/automation_folder/Movie_Predict/moviescraper/'
# os.chdir(project_root)

# # log_directory = f"logs/scraping/{spider}"

# # # Créer le répertoire de logs s'il n'existe pas
# # if not os.path.exists(log_directory):
# #     print(f"Directory not exist : {os.path.exists(log_directory)} created.")
# #     os.makedirs(log_directory)
# #     print(log_directory)
# # else:
# #     print(f"Directory already exist.")

# # log_file = os.path.join(log_directory, f"{spider}.log")
# # print(log_file)

# try:
#     # print(f"Clean the logs in file : {log_file}")
#     # with open(log_file, 'w') as f:
#     #     pass
    
#     print(f"\nExecute spider : {spider}\n")
#     print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    
#     execute([
#         'scrapy',
#         'crawl',
#         spider,
#         '-o',
#         f'{spider}.csv',
#         # '-s',
#         # f'LOG_FILE={log_file}'
#     ])
#     print('FFFFFFFFFFFFFFFFFFFFFFFFIIIIIIIIIIIIIIIIIIIIIIIINNNNNNNNNNNNNNNNNNNNNN')
# except SystemExit as e:
#     print(f"\nError, exit script : {e}\n")
#     pass

# print(f"\nExtraction {spider} finish.\n")

#########################################################################################################


import subprocess
import os
from datetime import datetime

# Nom du spider à lancer
spider = "moviespider"

# Chemin absolu vers le dossier contenant scrapy.cfg
# project_root = "/opt/airflow/Movie_Predict/moviescraper"
project_root='/home/addeche/Documents/Projets Python/scraping_allocine/automation_folder/Movie_Predict/moviescraper/'
# Dossier de logs (optionnel)
# log_dir = f"/opt/airflow/logs/scrapy/{spider}"
# os.makedirs(log_dir, exist_ok=True)

# # Nom de fichier log avec timestamp
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# log_file = os.path.join(log_dir, f"{spider}_{timestamp}.log")

# # CSV de sortie
# output_file = os.path.join(project_root, f"{spider}.csv")

# Commande Scrapy à exécuter
# cmd = [
#     "scrapy", "crawl", spider,
#     "-o", output_file,
#     "-s", f"LOG_FILE={log_file}"
# ]

cmd = [
    "scrapy", "crawl", spider,
    "-o", 'moviespider2000_2025_test.csv'
]

# print(f"🚀 Lancement du spider '{spider}' dans {project_root}...")
# print(f"📄 Fichier de sortie : {output_file}")
# print(f"📝 Fichier de log    : {log_file}")

# Lancer la commande dans un sous-processus
result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)

# Affichage résultat
if result.returncode == 0:
    print("✅ Scrapy terminé avec succès.")
else:
    print(f"❌ Scrapy a échoué avec le code {result.returncode}")
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

print("🏁 Fin du script runner.py")