from generation_pipeline.prompt_builder import build_prompt
from generation_pipeline.generator import query_model


def make_frame(train_file, test_input):
    output = ""

    for stage in range(1, 5):
        if stage == 4:
            test_output = "\n".join(output.split("\n")[:-1])
        else:
            test_output = output
        prompt = build_prompt(train_file, test_input, stage, test_output.strip())
        output += "\n" + query_model(prompt)
    return output.strip()
