import os
#focus on scraped_characters folder to get all the stuff.
def refine(folder):
    normals = 'Normal Moves '
    specials = 'Special Moves '
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        #check for .txt extension
        if filename.endswith('.txt'):
            with open(filepath, 'r') as f:
                text = f.read()
                #thinking to just scrape all the moves - like look for all the normal moves.
                start_norm = text.find(normals)
                end_specials = text.find(specials, start_norm)
                if start_norm != -1 and end_specials != -1:
                    norm_section = text[start_norm:end_specials]
                    #write to new subfolder
                    subfolder_path = os.path.join(folder, 'refined')
                    os.makedirs(subfolder_path, exist_ok=True)
                    output_file_path = os.path.join(subfolder_path, filename)
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(norm_section)
                

def main():
    folder = 'scraped_characters'
    refine(folder)

if __name__ == "__main__":
    main()