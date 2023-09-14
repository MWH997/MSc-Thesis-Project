import jsonify
import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer

def model(description):

    # Load the model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained(model_path).to(device)
    tokenizer = T5Tokenizer.from_pretrained(model_path, legacy=False)
    if not description:
        return jsonify({'error': 'Description is required.'}), 400
    
    inputs = tokenizer.encode(description, return_tensors='pt').to(device)
    outputs = model.generate(inputs, max_length=1700, do_sample=True, temperature=0.7)
    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Here you can add your fix_aiml_structure function and other utilities
    fixed_output = fix_aiml_structure(decoded_output)
    
    return jsonify({'aiml': fixed_output})