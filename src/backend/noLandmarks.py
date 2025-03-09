import json
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extraire l'intervalle de frames consécutives avec des landmarks valides à partir d'un fichier JSON."
    )
    parser.add_argument('json_file', help="Chemin vers le fichier JSON contenant les frames")
    parser.add_argument('-o', '--output', help="Fichier JSON de sortie", default="output.json")
    return parser.parse_args()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def filter_consecutive_frames(frames_data):
    """
    Parcourt le dictionnaire des frames (ex. "frame_105", "frame_112", etc.),
    considère qu'une frame est valide si sa donnée est une liste (landmarks détectés)
    et retourne le sous-ensemble (en conservant les clés originales) correspondant 
    à l'intervalle consécutif le plus long (basé sur la partie numérique du nom de frame).
    """
    valid_frames = []
    
    # Construire une liste de tuples : (numéro, clé, donnée)
    for frame_key, data in frames_data.items():
        if isinstance(data, list):
            try:
                num = int(frame_key.split('_')[1])
                valid_frames.append((num, frame_key, data))
            except (IndexError, ValueError):
                # Si le format de la clé n'est pas "frame_<number>", on ignore
                continue
    
    # Trier les frames par numéro
    valid_frames.sort(key=lambda x: x[0])
    
    best_interval = []
    current_interval = []
    prev_num = None

    # Parcourir les frames triées pour trouver la plus longue séquence consécutive
    for num, key, data in valid_frames:
        if prev_num is None or num == prev_num + 1:
            current_interval.append((num, key, data))
        else:
            if len(current_interval) > len(best_interval):
                best_interval = current_interval
            current_interval = [(num, key, data)]
        prev_num = num

    # Dernière vérification pour le cas où la séquence la plus longue serait à la fin
    if len(current_interval) > len(best_interval):
        best_interval = current_interval

    # Recréer un dictionnaire à partir de la meilleure séquence trouvée
    filtered_data = {}
    for _, key, data in best_interval:
        filtered_data[key] = data

    return filtered_data

def main():
    args = parse_arguments()
    frames_data = load_json(args.json_file)
    
    # Filtrer pour obtenir l'intervalle consécutif le plus long de frames valides
    filtered_data = filter_consecutive_frames(frames_data)
    
    # Écrire le résultat dans le fichier JSON de sortie
    with open(args.output, 'w') as outfile:
        json.dump(filtered_data, outfile, indent=4)
    
    print(f"Filtered data has been written to {args.output}")

if __name__ == "__main__":
    main()
