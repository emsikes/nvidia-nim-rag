# Performance Benchmark Results

**Date:** 2025-11-02  
**Hardware:** RTX 4070 (12GB VRAM), WSL2  
**Model:** Llama 3.1 8B (via Ollama on Windows)

## Results Summary

### Query Performance
- **Average response time:** 9.40s
- **Median response time:** 9.15s
- **Fastest response:** 8.14s
- **Slowest response:** 11.09s
- **Standard deviation:** 1.08s (very consistent!)

### Guardrails Performance
- **Average blocked query time:** 0.93s
- **Guardrails detect bad queries ~10x faster**
- Prevents wasted computation on harmful requests

### Comparison
- **Cloud API baseline:** 80.00s
- **Current system:** 9.40s
- **Speed improvement:** **8.5x faster!** 🚀

## Analysis

The 9-10 second response time includes:
1. Vector search (~0.5s)
2. Context retrieval (~0.5s)  
3. LLM generation via Ollama (~7-8s)
4. NeMo Guardrails validation (~1s)

Guardrails add minimal overhead and actually save time by catching bad queries early.