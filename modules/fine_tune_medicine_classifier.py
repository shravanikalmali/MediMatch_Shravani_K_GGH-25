# fine_tune_medicine_classifier.py
import os
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
from datasets import load_dataset
import evaluate

# 1. Load your dataset from CSV.
# The CSV file should have headers: "text" and "label" (where label 1 = valid medicine, 0 = not valid).
dataset = load_dataset("csv", data_files={"train": "medicine_dataset.csv", "test": "medicine_dataset.csv"}, delimiter=",")

print("Raw dataset:")
print(dataset)

# 2. Filter out examples with missing labels.
dataset = dataset.filter(lambda x: x["label"] is not None)

# 3. Cast labels to integers.
def cast_label(example):
    example["label"] = int(example["label"])
    return example

dataset = dataset.map(cast_label)

# 4. Choose a pre-trained model.
model_checkpoint = "emilyalsentzer/Bio_ClinicalBERT"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=2)

# 5. Tokenization function.
def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=32)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 6. Define training arguments.
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="steps",
    save_strategy="steps",
    save_steps=100,
    eval_steps=100,
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_steps=10,
    save_total_limit=3,
    load_best_model_at_end=True,
    metric_for_best_model="accuracy",
)

data_collator = DataCollatorWithPadding(tokenizer)

# 7. Load an accuracy metric.
accuracy_metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return accuracy_metric.compute(predictions=predictions, references=labels)

# 8. Create the Trainer.
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 9. Train the model.
trainer.train()

# 10. Save the fine-tuned model and tokenizer.
model.save_pretrained("./fine_tuned_medicine_classifier")
tokenizer.save_pretrained("./fine_tuned_medicine_classifier")
