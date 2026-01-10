import csv

#rapide script pour avoir un csv plus petit sur lequel on va travailler (5 entrées)
input_file = "rcsb_pdb_custom_report_20260109152453.csv"
output_file = "smaller5.csv"

def filter_csv_top_5(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as f_in, \
         open(out_path, 'w', encoding='utf-8') as f_out:
        
        lines = f_in.readlines()
        
        # 1. Copier les deux lignes d'en-tête
        if len(lines) >= 1:
            f_out.write(lines[0])
        if len(lines) >= 2:
            f_out.write(lines[1])
        
        # 2. Parcourir les données et compter les identifiants uniques
        entry_count = 0
        for line in lines[2:]:
            # Dans ce CSV, une nouvelle entrée commence par un guillemet (ex: "2KUP")
            # Les lignes de continuation commencent par une virgule
            if line.startswith('"'):
                entry_count += 1
            
            # Si on dépasse 5 entrées, on s'arrête
            if entry_count > 5:
                break
                
            f_out.write(line)

if __name__ == "__main__":
    filter_csv_top_5(input_file, output_file)
    print(f"Fichier filtré créé : {output_file}")