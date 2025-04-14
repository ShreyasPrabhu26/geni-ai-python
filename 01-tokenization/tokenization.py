import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocalbulary size:", encoder.n_vocab) 

text = "Shreyas Here!"

tokens = encoder.encode(text)
print("Tokens:", tokens)
print("Decoded:", encoder.decode(tokens))
print("Token count:", len(tokens))