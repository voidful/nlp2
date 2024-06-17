try:
    import numpy as np
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM

    torch.random.manual_seed(0)
except:
    print("Warning: transformers not installed. LLM will not work.")
    pass


class LMUtil:
    def __init__(self, model_name="gpt2",
                 tokenizer=None,
                 model=None,
                 device=None,
                 torch_dtype=torch.float16,
                 device_map="auto"):
        if not tokenizer:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        else:
            self.tokenizer = tokenizer
        if not device:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = device
        if not model:
            self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_dtype,
                                                              device_map=device_map)
        else:
            self.model = model
        self.model_name = model_name
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({"pad_token": "<pad>"})
        self.tokenizer.pad_token_id = 0
        self.tokenizer.padding_side = 'right'

    @staticmethod
    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def input_encode(self, input_sent):
        tensor_input = self.tokenizer.encode(input_sent, return_tensors='pt').to(self.device)
        return tensor_input

    def __call__(self, input_sent,
                 do_sample=False,
                 top_k=50,
                 top_p=0.95,
                 typical_p=1.0,
                 no_repeat_ngram_size=0,
                 temperature=1.0,
                 repetition_penalty=1.0,
                 guidance_scale=1,
                 max_new_tokens=512):

        tokenized = self.tokenizer(input_sent, padding=True, return_tensors='pt')
        input_ids = tokenized.input_ids.to(self.device)

        output_ids = self.model.generate(
            input_ids,
            do_sample=do_sample,
            top_k=top_k,
            top_p=top_p,
            typical_p=typical_p,
            no_repeat_ngram_size=no_repeat_ngram_size,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            guidance_scale=guidance_scale,
            max_new_tokens=max_new_tokens
            # stopping_criteria=self.stopping_criteria,
        )

        actual_seq_lengths = tokenized.attention_mask.sum(dim=1)
        output_ids = [output_id[seq_length:] for output_id, seq_length in zip(output_ids, actual_seq_lengths)]

        predictions = []
        for prediction in self.tokenizer.batch_decode(
                output_ids, skip_special_tokens=True, spaces_between_special_tokens=False
        ):
            prediction = prediction.strip()
            predictions.append(prediction)
        return predictions

    def score_choice(self, input_sent, labels, letter_choice=False, number_choice=False):
        score = []
        if letter_choice:
            labels = [f"{chr(65 + i)}" for i, option in enumerate(labels)]
        if number_choice:
            labels = [f"{i + 1}" for i, option in enumerate(labels)]
        for label in labels:
            with torch.inference_mode():
                input_sent_tokens = self.tokenizer.encode(input_sent, return_tensors='pt',
                                                          add_special_tokens=False).to(self.device)
                label_sent_tokens = self.tokenizer.encode(label, return_tensors='pt',
                                                          add_special_tokens=False).to(self.device)
                concatenated = torch.cat([
                    input_sent_tokens,
                    label_sent_tokens,
                    torch.tensor([[self.tokenizer.eos_token_id]]).to(self.device)], dim=-1)
                labels = torch.full_like(concatenated, -100).to(self.device)
                labels[:, -label_sent_tokens.shape[1] - 1:] = torch.cat(
                    [label_sent_tokens, torch.tensor([[self.tokenizer.eos_token_id]]).to(self.device)],
                    dim=-1)
                loss = self.model(concatenated[:, :-1], labels=labels[:, 1:]).loss
                normalized_loss = loss.item() / label_sent_tokens.shape[1]
                score.append(-normalized_loss)
        return self.softmax(score)
