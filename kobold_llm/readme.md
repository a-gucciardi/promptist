## bench notebook
Speedtest notebook on selected quantized models from HF.  
Model range from 7b to 70b sizes.  
  - manual speeds tests
  - automated speeds tests

Due to the default parameters used (most probably), the models are outputing some speed differences.  

## LLMBOT

AIBot - Simple AI API Client
A lightweight Python client for streaming text generation from AI APIs (Kobold, HF models in GGUF).
TODO : add context support.  


 - Streams responses in real-time
 - Supports vision models with image input
 - Automatic server connection and status checking
 - Simple command-line interface
 - Handles both positional arguments and stdin input



Usage
```bash
python aibot.py [prompt] [options]
```
Options

-s, --server: Server address (default: localhost)
-p, --port: Server port (default: 5001)
-l, --loops: Number of generation turns (default: 1)
-i, --images: Image files for vision models (newline-separated paths)
-n, --new: Create new context flag (important default)

Examples
```bash
# Basic usage
python aibot.py "Tell me a story"

# With custom host
python aibot.py -s 192.168.1.100 -p 8080 "Hello world"

# Multiple prompt turns
python aibot.py -l 3 "Continue this conversation"

# With images - depends on the model
python aibot.py -i "image1.jpg" "Describe this image"

# From stdin
echo "What are you?" | python aibot.py
```

### perf.py
 - measure the performance of the AI API on the last llm request.  
 - processing speed
 - generation speed
 - total t/s

### toker.py
 - returns the number of tokens calculated for the string(s) provided as positional arguments.  
 - argument -l gives full list of tokens instead.  