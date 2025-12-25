import tkinter as tk
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import threading

_MAX_CONTEXT_LENGTH = 256


from transformers import BertTokenizer, BertForMaskedLM
import torch

# Load pre-trained BERT and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForMaskedLM.from_pretrained("bert-base-uncased")
model.eval()

def get_next_word(text_with_mask, top_k=5):
    # Tokenize input
    inputs = tokenizer.encode_plus(text_with_mask, return_tensors="pt")
    input_ids = inputs["input_ids"]
    mask_token_index = torch.where(input_ids == tokenizer.mask_token_id)[1]

    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Extract logits for [MASK] token
    mask_logits = logits[0, mask_token_index, :]

    # Get top k predictions
    top_k_ids = torch.topk(mask_logits, top_k, dim=1).indices[0].tolist()
    predictions = [tokenizer.decode([token_id]).strip() for token_id in top_k_ids]
    print(predictions)
    return predictions[0]

def async_suggest(text):
    if len(text.strip().split()) < 2:
        suggestion_label.config(text="Suggested: (Type more...)")
        return
    if not text.strip().endswith('.'):
        text = text.strip() + '.'
    input_text = text + " [MASK]"
    word = get_next_word(input_text)
    suggestion_label.config(text=f"Suggested: {word}")
    
def update_suggestion(event=None):
    '''Will call the fetch the next possible word'''
    text = text_widget.get("1.0", tk.END).strip()
    # try:
    #     tokens = _TOKENIZER.encode(text)
    #     if tokens and len(tokens) > _MAX_CONTEXT_LENGTH:
    #         tokens = tokens[-_MAX_CONTEXT_LENGTH:]
    #     input_text = _TOKENIZER.decode(tokens)
    #     suggestion_label.config(text="Thinking...")
    #     async_suggest(input_text)
    # except Exception as e:
    #     print(f"Error while encoding or starting thread: {e}")
    if not text.endswith('.'):
        text += '.'
    input_text = text.strip() + " [MASK]"
    async_suggest(input_text)


root = tk.Tk()
root.title("Autocomplete Editor")

# Text editor widget
text_widget = tk.Text(root, height=15, width=60, font=("Helvetica", 14))
text_widget.pack(padx=10, pady=10)
text_widget.bind("<KeyRelease>", update_suggestion)

# Label for showing next-word suggestion
suggestion_label = tk.Label(root, text="Suggested: ", font=("Helvetica", 12), fg="blue")
suggestion_label.pack(pady=(0, 10))

root.mainloop()