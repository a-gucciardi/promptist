# Local LLM 
A minimal setup for quick testing and evaluation of open-source Large Language Models (LLMs). This project uses the [KoboldCpp](https://github.com/LostRuins/koboldcpp?tab=readme-ov-file#linux-usage-precompiled-binary-recommended) framework for its simplicity and compatibility with quantized models.

> **Note:** This setup was originally created for internal use with a Discord bot, currently powered by a local Ollama instance.

---
## Status
### Current Features

* Lightweight framework for testing LLMs locally.
* API experimentation and benchmarking tools.
* Compatible with GGUF-format models.

### Coming Soon

* Multimodal capabilities speed and bench tests.
* Ollama benchmarks.

---

## Structure
```bash
kobold_llm/
├── aibot.py      # Discord bot / interaction logic
├── perf.py       # Performance measurement
├── toker.py      # Tokenization tests
└── bench.ipynb   # Benchmarking notebook
```


## Usage Steps :
1. **Install KoboldCpp**
   Follow the instructions in the [KoboldCpp GitHub](https://github.com/LostRuins/koboldcpp?tab=readme-ov-file#linux-usage-precompiled-binary-recommended).

2. **Download Models**

   * Filtered from Hugging Face in GGUF format (most links are provided in [model_links](/models/links.txt)).
   ```bash
   cd models
   wget https://huggingface.co/unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF/resolve/main/DeepSeek-R1-0528-Qwen3-8B-Q4_K_S.gguf
   ```
   * Manually converted from other formats (requires [kb tools](https://kcpptools.concedo.workers.dev/)). 

3. **Play Around with APIs**
   Check out these Python scripts for interaction and testing:

   * [`aibot.py`](/kobold_llm/aibot.py): Basic chatbot logic
   * [`perf.py`](/kobold_llm/perf.py): Performance tester
   * [`toker.py`](/kobold_llm/toker.py): Token-level analysis

4. **Run Benchmarks**

   * Use the provided [`bench.ipynb`](/kobold_llm/bench.ipynb) Jupyter Notebook for:

     * Speed testing
     * Simple result visualizations

---
