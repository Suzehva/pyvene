"""
Each modeling file in this library is a mapping between
abstract naming of intervention anchor points and actual
model module defined in the huggingface library.
We also want to let the intervention library know how to
config the dimensions of intervention based on model config
defined in the huggingface library.
"""
import torch
from ..constants import *

qwen_type_to_module_mapping = {
    "block_input": ("h[%s]", CONST_INPUT_HOOK),
    "block_output": ("h[%s]", CONST_OUTPUT_HOOK),
    "mlp_activation": ("h[%s].mlp.act", CONST_OUTPUT_HOOK),
    "mlp_output": ("h[%s].mlp", CONST_OUTPUT_HOOK),
    "mlp_input": ("h[%s].mlp", CONST_INPUT_HOOK),
    "attention_value_output": ("h[%s].attn.c_proj", CONST_INPUT_HOOK),
    "head_attention_value_output": ("h[%s].attn.c_proj", CONST_INPUT_HOOK, (split_head_and_permute, "n_head")),
    "attention_output": ("h[%s].attn", CONST_OUTPUT_HOOK),
    "attention_input": ("h[%s].attn", CONST_INPUT_HOOK),
    "query_output": ("h[%s].attn.q_proj", CONST_OUTPUT_HOOK),
    "key_output": ("h[%s].attn.k_proj", CONST_OUTPUT_HOOK),
    "value_output": ("h[%s].attn.v_proj", CONST_OUTPUT_HOOK),
    "head_query_output": ("h[%s].attn.q_proj", CONST_OUTPUT_HOOK, (split_head_and_permute, "n_head")),
    "head_key_output": ("h[%s].attn.k_proj", CONST_OUTPUT_HOOK, (split_head_and_permute, "n_kv_head")),
    "head_value_output": ("h[%s].attn.v_proj", CONST_OUTPUT_HOOK, (split_head_and_permute, "n_kv_head")),
}

qwen_type_to_dimension_mapping = {
    "n_head": ("num_attention_heads",),
    "n_kv_head": ("num_key_value_heads",),
    "block_input": ("hidden_size",),
    "block_output": ("hidden_size",),
    "mlp_activation": ("intermediate_size",),
    "mlp_output": ("hidden_size",),
    "mlp_input": ("hidden_size",),
    "attention_value_output": ("hidden_size",),
    "head_attention_value_output": ("head_dim",),
    "attention_output": ("hidden_size",),
    "attention_input": ("hidden_size",),
    "query_output": ("hidden_size",),
    "key_output": ("hidden_size",),
    "value_output": ("hidden_size",),
    "head_query_output": ("head_dim",),
    "head_key_output": ("head_dim",),
    "head_value_output": ("head_dim",),
}

"""qwen model with LM head"""
qwen_lm_type_to_module_mapping = {}
for k, v in qwen_type_to_module_mapping.items():
    qwen_lm_type_to_module_mapping[k] = (f"transformer.{v[0]}", ) + v[1:]
qwen_lm_type_to_dimension_mapping = qwen_type_to_dimension_mapping

"""qwen model with classifier head"""
qwen_classifier_type_to_module_mapping = {}
for k, v in qwen_type_to_module_mapping.items():
    qwen_classifier_type_to_module_mapping[k] = (f"transformer.{v[0]}", ) + v[1:]
qwen_classifier_type_to_dimension_mapping = qwen_type_to_dimension_mapping

def create_qwen(
    name="Qwen/Qwen2.5-0.5B", cache_dir=None, dtype=torch.bfloat16
):
    """Creates a Causal LM model, config, and tokenizer from the given name and revision"""
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
    
    config = AutoConfig.from_pretrained(name, cache_dir=cache_dir)
    tokenizer = AutoTokenizer.from_pretrained(name, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        name,
        config=config,
        cache_dir=cache_dir,
        torch_dtype=dtype,
    )
    print("loaded model")
    return config, tokenizer, model