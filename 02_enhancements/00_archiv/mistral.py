# from transformers import AutoModelForCausalLM, AutoTokenizer
# model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16, attn_implementation="flash_attention_2", device_map="auto")
# tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
# Load model directly
#
# messages = [
#     {"role": "user", "content": "Bitte in leichte Sprache übersetzen: 'Deutsche Staatsbürger*innen sind verpflichtet, einen gültigen Personalausweis (oder Reisepass) zu besitzen, sobald sie 16 Jahre alt sind.'"},
# ]

# model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")

# generated_ids = model.generate(model_inputs, max_new_tokens=100, do_sample=True)
#tokenizer.batch_decode(generated_ids)[0]


from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("abacusai/Smaug-72B-v0.1")
model = AutoModelForCausalLM.from_pretrained("abacusai/Smaug-72B-v0.1")

prompt = "Bitte in leichte Sprache übersetzen: 'Deutsche Staatsbürger*innen sind verpflichtet, einen gültigen Personalausweis (oder Reisepass) zu besitzen, sobald sie 16 Jahre alt sind.'"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=30)
tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]