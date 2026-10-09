# Architecture boundaries

Separate request/config and context/state objects, geometry builders, individual generation layers, render payload builders, UI/server adapters, persistence adapters, and tests for each layer plus the pipeline contract.

A generation pipeline should receive or create a context, call ordered layers, pass the result from one layer to the next, and collect timing or metadata. For example:

```python
ctx = GeometryLayer().apply(ctx)
ctx = LandscapeLayer().apply(ctx)
ctx = OceanLayer().apply(ctx)
ctx = ClimateLayer().apply(ctx)
ctx = RiversLayer().apply(ctx)
ctx = BiomeLayer().apply(ctx)
return ctx
```

The pipeline itself must not calculate geometry, landscape, oceans, climate, rivers or biomes. Do not hide them inside one “manager”, “handler”, “pipeline”, or “world” object.

Studio/UI code may parse controls, invoke the application use case, and render the returned payload. It must not decide domain semantics such as ocean, lake, river, biome, drainage, or terrain classification. When reviewing a change, ask whether its responsibility belongs to domain logic, application orchestration or an adapter, and whether the new boundary has coverage.
