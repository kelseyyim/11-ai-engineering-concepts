# 8. Model artifacts and quantization

## Why it matters

A model name is a convenient label, not a complete reproducibility record. Deployable behavior depends on weights, tokenizer, prompt template, runtime, and settings. Keep track of the exact artifacts that produced a result so you can investigate regressions instead of guessing which component changed.

Safetensors stores tensors in a format designed to avoid executing arbitrary code during tensor loading. GGUF packages tensors with standardized metadata for compatible inference engines. These formats are not interchangeable promises that every runtime can execute every architecture.

Quantization represents weights with fewer bits, often reducing storage and memory requirements. That can make a larger model practical on limited hardware, but quality and speed need measurement. A quantization label describes a representation, not a universal accuracy score.

## Build it

Choose two already-available variants of the same model family with different quantization levels. Before running them, record their source, license, artifact digest or pinned revision, tokenizer/template, runtime version, and file sizes. Use the same prompt set, generation limits, hardware, and evaluation rubric for both.

Measure task accuracy, cold-start time, steady-state generation latency, and peak memory separately. Include a failure-sensitive task such as extracting numbers exactly, rather than scoring only fluent prose. Select the smallest variant that meets your task's acceptance threshold; do not assume the smallest file is always fastest.

For Ollama imports, inspect the current import guide before preparing a Modelfile. Its documented GGUF import flow expects quantization to be performed beforehand. The accompanying lab intentionally avoids conversion and downloads so you can learn request handling independently.

## Watch out

A “4-bit” description is not a complete memory estimate: metadata, mixed-precision tensors, caches, and runtime buffers add overhead. Changing the context budget also changes the experiment.

Safer serialization does not guarantee trustworthy model behavior, a legitimate license, or a harmless surrounding repository. Review provenance and avoid executing unfamiliar setup scripts just because the weights look plausible.

## Learn more

- [Safetensors documentation](https://huggingface.co/docs/safetensors/index): tensor-format purpose and loading model.
- [Hugging Face GGUF guide](https://huggingface.co/docs/hub/gguf): metadata and quantized tensor representations.
- [Ollama model imports](https://docs.ollama.com/import): supported artifact import workflows.

Resource review: 2026-10-07.

[Back to the guide](../README.md#table-of-contents)
