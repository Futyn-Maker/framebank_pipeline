from generation_pipeline.span_extractor import SpanExtractor


extractor = SpanExtractor()

def process_test_input(input_section, stage):
    input_lines = input_section.strip().split("\n")[1:]

    input_dict = {}
    for line in input_lines:
        key, value = line.split(": ", 1)
        input_dict[key] = value
    
    if stage == 1:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Name: {input_dict['FN Name']}"
    elif stage == 2:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Name: {input_dict['FN Name']}\nFN Core FEs: {input_dict['FN Core FEs']}"
    elif stage == 3:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Definition: {input_dict['FN Definition']}\nFN Core FEs definitions: {input_dict['FN Core FEs definitions']}"
    elif stage == 4:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {extractor(input_dict['Example'])}"

    return f"Input:\n{input_result}"
