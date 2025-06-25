#!/bin/bash
# auto benchmark all models in the directory using koboldcpp API.

BENCH_FILE="bench.csv"

for model in ./*.gguf;do
    echo "Running benchmark for $model"
    ../koboldcpp --model "$model" --launch --benchmark "$BENCH_FILE"
    echo "Finished benchmarking $model_file"
    echo "###"
done

echo "All benchmarks completed."