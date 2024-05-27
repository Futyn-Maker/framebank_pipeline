import pandas as pd
import re
import nltk
from nltk.corpus import framenet as fn


def clean_text(text):
    """Remove text within brackets and parentheses."""
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\{.*?\}', '', text)
    return text.strip()

def get_core_fe_definitions(frame):
    """Get core Frame Elements definitions."""
    core_fes = {fe.name: fe.definition for fe in frame.FE.values() if fe.coreType == 'Core'}
    return core_fes

def generate_output(grouped_data):
    """Generate formatted output string."""
    results = []
    for fn_name, data in grouped_data.items():
        lus = " > ".join(sorted(set(data['lexemes'])))
        example = data['example']
        fn_definition = data['fn_definition']
        fn_core_fes = " > ".join(data['core_fes'].keys())
        fn_core_fes_definitions = " > ".join(data['core_fes'].values())
        
        output = f"Input:\nLUs: {lus}\nExample: {example}\nFN Name: {fn_name}\nFN Core FEs: {fn_core_fes}\nFN Definition: {fn_definition}\nFN Core FEs definitions: {fn_core_fes_definitions}"
        results.append(output)
    return results

def main():
    framebank_df = pd.read_csv('data/LinkedToFrameNet.csv')
    framebank_dict_cx_df = pd.read_csv('data/framebank_dict_cx.txt', sep='\t')

    grouped_data = {}

    for _, row in framebank_df.iterrows():
        if pd.isna(row['FrameNetFrame']) or "?" in row['FrameNetFrame']:
            continue

        frame_number = row['FrameNo']
        sub_frame_number = row['SubFrameNo']
        frame = fn.frame_by_name(row['FrameNetFrame'])
        token = row['Verb']
        frame_number_prefix = f"{frame_number}."
        
        matching_constructions = framebank_dict_cx_df[
            (framebank_dict_cx_df['Constr'].str.startswith(f"{token} ")) & 
            (framebank_dict_cx_df['ConstrName'].str.startswith(frame_number_prefix))
        ]

        if not matching_constructions.empty:
            if len(matching_constructions) == 1:
                example = matching_constructions.iloc[0]['Example']
            else:
                example = matching_constructions.iloc[1]['Example']

            try:
                example = clean_text(example.split('.')[0] + '.')
            except AttributeError:
                print("Skipped")
                continue

            core_fes = get_core_fe_definitions(frame)
            fn_definition = frame.definition.strip()

            if row['FrameNetFrame'] not in grouped_data:
                grouped_data[row['FrameNetFrame']] = {
                    'lexemes': [],
                    'example': example,
                    'fn_definition': fn_definition,
                    'core_fes': core_fes
                }

            lexemes = re.sub(r'\d', '', row['Constr']).replace(".", "").strip().split(',')
            grouped_data[row['FrameNetFrame']]['lexemes'].extend(lexemes)

    results = generate_output(grouped_data)
    
    with open('data/data_for_generation.txt', 'w', encoding='utf-8') as f:
        for result in results:
            f.write(result)
            f.write("\n\n\n")

if __name__ == "__main__":
    main()
    