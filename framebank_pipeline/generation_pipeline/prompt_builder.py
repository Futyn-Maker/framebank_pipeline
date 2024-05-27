from generation_pipeline.process_train import process_train_file
from generation_pipeline.process_test import process_test_input
from generation_pipeline.instructions import instructions

def build_prompt(train_file, test_input, stage, output):
    instruction = instructions[f"stage_{stage}"]
    train_examples = process_train_file(train_file, stage)
    test_input = process_test_input(test_input, stage)
    if output:
        test_input += f"\n{output}"
    prompt = f"{instruction}\n\n\n{train_examples}\n\n\n{test_input}\n\nOutput:"
    return prompt