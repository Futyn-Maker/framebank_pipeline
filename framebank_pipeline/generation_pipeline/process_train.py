from generation_pipeline.span_extractor import SpanExtractor


extractor = SpanExtractor()

def process_train_example(source_example, stage):
    input_section, output_section = source_example.strip().split("\n\n")
    input_lines = input_section.split("\n")[1:]
    output_lines = output_section.split("\n")[1:]
    
    input_dict = {}
    for line in input_lines:
        key, value = line.split(": ", 1)
        input_dict[key] = value
    
    output_dict = {}
    for line in output_lines:
        key, value = line.split(": ", 1)
        output_dict[key] = value
    
    if stage == 1:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Name: {input_dict['FN Name']}"
        output_result = f"Frame: {output_dict['Frame']}"
    elif stage == 2:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Name: {input_dict['FN Name']}\nFN Core FEs: {input_dict['FN Core FEs']}\nFrame: {output_dict['Frame']}"
        output_result = f"Core FEs: {output_dict['Core FEs']}"
    elif stage == 3:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {input_dict['Example']}\nFN Definition: {input_dict['FN Definition']}\nFN Core FEs definitions: {input_dict['FN Core FEs definitions']}\nFrame: {output_dict['Frame']}\nCore FEs: {output_dict['Core FEs']}"
        output_result = f"Frame Definition: {output_dict['Frame Definition']}\nCore FEs definitions: {output_dict['Core FEs definitions']}"
    elif stage == 4:
        input_result = f"LUs: {input_dict['LUs']}\nExample: {extractor(input_dict['Example'])}\nFrame: {output_dict['Frame']}\nCore FEs: {output_dict['Core FEs']}\nFrame Definition: {output_dict['Frame Definition']}"
        output_result = f"Labeled example: {output_dict['Labeled example']}"
    
    return f"Input:\n{input_result}\n\nOutput:\n{output_result}"

def process_train_file(file_path, stage):
    with open(file_path, encoding="utf-8") as train_file:
        examples = train_file.read().strip().split("\n\n\n")
        processed_examples = [process_train_example(example, stage) for example in examples]
        return "\n\n\n".join(processed_examples)
