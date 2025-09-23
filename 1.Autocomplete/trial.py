from transformers import BertTokenizer, BertForMaskedLM
import torch

# Load pre-trained BERT and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForMaskedLM.from_pretrained("bert-base-uncased")
model.eval()

def predict_masked_word(text_with_mask, top_k=5):
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

    return predictions

# Example sentence (you can change this)
input_text = "The taste of an apple is [MASK]."
predicted_words = predict_masked_word(input_text)

# print(f"Predictions for: '{input_text}'")
# for i, word in enumerate(predicted_words, 1):
#     print(f"{i}. {word}")

print("The most probable word is : ")
print(predicted_words[0])