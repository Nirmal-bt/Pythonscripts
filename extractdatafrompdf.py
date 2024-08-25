import fitz  # PyMuPDF
import re
import os
import pandas as pd
# Function to find text and get the row's text
def find_text_and_get_row(pdf_file, search_term):
    document = fitz.open(pdf_file)
    myval=0 
    
    for page_number in range(len(document)):
        page = document.load_page(page_number)
        blocks = page.get_text("blocks")  # Get text blocks
        
        for i,block in  enumerate(blocks):
            
            x0, y0, x1, y1, text = block[:4] + (block[4],)
            if search_term in text.strip():
                # print(text.strip())
                
                # results.append((page_number, block))
                # print(f"Found '{search_term}' on page {page_number + 1} at coordinates ({x0}, {y0}), ({x1}, {y1})")
                # print(f"Row text: {text}")
                if i+1 < len(blocks):

                    nexblock = blocks[i+1]
                    a, b, c, d, e = nexblock[:4] + (nexblock[4],)
                    # print(f"value is on page {page_number + 1} at coordinates ({a}, {b}), ({c}, {d})")
                    # print(f"Row text: {e}")

                    match = re.search(r'\d+\.\d+|\d+',e)
                    if match:
                         myval= float(match.group())
                     
                    break
                    

            
                
               
    document.close()
   
    
    return myval

# Example usage


def outerfunc(pdf_file,filename):
    final_values=[]
    search_array=["Haemoglobin (Hb)",
                "WBC count ",
                "Platelet count",
                "Blood Glucose",
                "HPLC",
                "CHOD-POD",
                "LDL Cholesterol",
                "HDL Cholesterol",
                "Triglycerides",
                "Creatinine",
                "Aspartate Transaminase(AST",
                "Alanine Transaminase(ALT/",
                "Alkaline Phosphatase",
                "Total Protein",
                "Albumin",
                "Globulin",
                "Gamma-Glutamyl Transferase"
                ]
    # search_term="Aspartate Transaminase(AST"
    # final_values.append(find_text_and_get_row(pdf_file, search_term))

    for search_term in search_array:
        final_values.append(find_text_and_get_row(pdf_file, search_term))


    columns=["HB","WBC","Platelets","RBS","HbA1C","Cholestrol","LDL","HDL","TG","Creatinine","SGOT","SGPT","ALP","Protein","Albumin","Globulin","GGT"]
    df = pd.DataFrame(data=[final_values],columns=columns) 
    username = os.path.splitext(filename)[0]
    df.insert(0,"Name",username)
    print(df)
    return df


#main
source_folder = "enter ur source"

all_dfs=[]

for filename in os.listdir(source_folder):
    if filename.endswith('.pdf'):
        pdf_file = os.path.join(source_folder,filename)
        df = outerfunc(pdf_file,filename)
        if df is not None:
            all_dfs.append(df)
                
myfinal_df=pd.concat(all_dfs,ignore_index=True)
output_file='enter path for output'
myfinal_df.to_excel(output_file, index=False)
