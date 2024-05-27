from tqdm import tqdm

from generation_pipeline.pipeline import make_frame


with open("data/data_for_generation.txt", "r", encoding="utf-8") as generation_data:
    inputs = generation_data.read().strip().split("\n\n\n")

outputs = inputs.copy()

for i, frame in tqdm(enumerate(inputs)):
    annotation = make_frame("data/train.txt", frame)
    outputs[i] += "\n\nOutput:\n" + annotation
    with open("data/generated_frames.txt", "w", encoding="utf-8") as output_file:
        output_file.write("\n\n\n".join(outputs))
