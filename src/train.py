# Adapted From: https://github.com/tatsu-lab/stanford_alpaca/blob/main/train.py

#    Copyright 2023 Rohan Taori, Ishaan Gulrajani, Tianyi Zhang, Yann Dubois, Xuechen Li
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from dataclasses import dataclass, field
from typing import Dict, Optional

import torch
import transformers
from datasets import load_from_disk
from transformers import Trainer


@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(default="facebook/opt-125m")


@dataclass
class DataArguments:
    data_path: str = field(
        default=None, metadata={"help": "Path to the training data."}
    )


@dataclass
class TrainingArguments(transformers.TrainingArguments):
    cache_dir: Optional[str] = field(default=None)
    optim: str = field(default="adamw_torch")
    model_max_length: int = field(
        default=2048,
        metadata={
            "help": "Maximum sequence length. Sequences will be right padded (and possibly truncated)."
        },
    )


def safe_save_model_for_hf_trainer(trainer: transformers.Trainer, output_dir: str):
    """Collects the state dict and dump to disk."""
    state_dict = trainer.model.state_dict()
    if trainer.args.should_save:
        cpu_state_dict = {key: value.cpu() for key, value in state_dict.items()}
        del state_dict
        trainer._save(output_dir, state_dict=cpu_state_dict)  # noqa


@dataclass
class Collator(object):
    def __call__(self, instances):
        input_ids = torch.stack([torch.LongTensor(i["input_ids"]) for i in instances])
        labels = input_ids.clone()
        # For Anonymize Token
        labels[labels == 32000] = -100
        return {"input_ids": input_ids, "labels": input_ids}


def make_data_module(data_args) -> Dict:
    train_dataset = load_from_disk(data_args.data_path)
    data_collator = Collator()
    return dict(
        train_dataset=train_dataset,
        eval_dataset=None,
        data_collator=data_collator,
    )


def train():
    parser = transformers.HfArgumentParser(
        (ModelArguments, DataArguments, TrainingArguments)
    )
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    revision = (
        "pr/7" if "decapoda-research/llama" in model_args.model_name_or_path else "main"
    )
    model = transformers.AutoModelForCausalLM.from_pretrained(
        model_args.model_name_or_path,
        cache_dir=training_args.cache_dir,
        revision=revision,
    )
    # For Anonymize Token
    model.resize_token_embeddings(model.config.vocab_size + 1)
    data_module = make_data_module(data_args=data_args)
    trainer = Trainer(model=model, args=training_args, **data_module)
    trainer.train()
    trainer.save_state()
    model.resize_token_embeddings(model.config.vocab_size)
    safe_save_model_for_hf_trainer(trainer=trainer, output_dir=training_args.output_dir)


if __name__ == "__main__":
    train()
