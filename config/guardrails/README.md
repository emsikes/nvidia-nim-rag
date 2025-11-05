# NeMo Guardrails Configuration

## Overview
This directory contains NeMo Guardrails configurations for safe AI interactions.

## Files
- `config.yml` - Main configuration and model settings
- `rails.co` - Colang flow definitions

## Implemented Guardrails

### Input Guardrails
1. **Jailbreak Detection** - Blocks attempts to override instructions
2. **Harmful Content** - Prevents illegal/unethical requests
3. **Off-Topic Control** - Redirects non-document queries
4. **Sensitive Information** - Blocks requests for credentials/keys
5. **Prompt Injection** - Detects system prompt manipulation
6. **PII Protection** - Prevents sharing personal data
7. **Advanced Injection** - Catches code injection attempts
8. **Length Validation** - Enforces 3-500 character limits
9. **Nonsense Detection** - Filters spam/gibberish
10. **Repetition Detection** - Catches repetitive queries
11. **Rate Limiting** - 20 queries/minute max

### Output Guardrails
1. **Self Check Output** - Validates response safety
2. **Fact Checking** - Ensures grounding in context
3. **Quality Scoring** - Confidence indicators

## Performance Impact
- Safe queries: ~1s overhead
- Blocked queries: ~0.9s (faster, caught early)

## Customization

### Add Custom Blocked Terms
Edit `rails.co`:
```colang
define user ask harmful
  "your custom term"
  "another blocked phrase"
```

### Adjust Rate Limits
Edit `src/rag/nemo_guardrails_rag.py`:
```python
self.max_queries_per_window = 30  # Increase limit
```

### Disable Specific Rails
Comment out in `config.yml`:
```yaml
rails:
  input:
    flows:
      # - topic control  # Disabled
```

## Testing Guardrails
```bash
# Run test suite
python -m tests.test_guardrails

# Test specific pattern
curl -X POST http://localhost:8000/query \
  -d '{"question": "Ignore instructions"}'
```

## Monitoring

Guardrail triggers are logged:
```python
self.logger.warning(f"Blocked query: {reason}")
```

Check logs for patterns of abuse.