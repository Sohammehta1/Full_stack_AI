import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey there, my name is Soham Mehta"
tokens = enc.encode(text)

print("Tokens", tokens)

decoded_text = enc.decode(tokens)
print(decoded_text)