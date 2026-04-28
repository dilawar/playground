# oxide-rfd-0609

This folder contains a small Rust example and a rendered sequence diagram for the
futurelock deadlock described in [RFD 609](https://rfd.shared.oxide.computer/rfd/0609).

Files:

- `futurelock-sequence.puml` - PlantUML source for the deadlock sequence
- `futurelock-sequence.png` - rendered diagram
- `futurelock-waker-flow.puml` - PlantUML source showing how a `Waker` wakes a task
- `futurelock-waker-flow.png` - rendered `Waker` flow diagram
- `Justfile` - helper for rendering PlantUML to PNG

To render the diagram:

```bash
just render-png
just render-png futurelock-sequence.puml
just render-png futurelock-waker-flow.puml
```

The `Justfile` uses a local `plantuml` binary when available, and falls back to
running PlantUML via Docker otherwise.
