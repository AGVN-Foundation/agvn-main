from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
response = generator('This is a good', do_sample=True, min_length=50)

print(response)
