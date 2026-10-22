# Diagrams

Editable sources live in `src/` (PlantUML). Rendered images in `export/` are generated from them and committed so reviewers can see them on GitHub without tools.

| File | Diagram | Used in |
|---|---|---|
| `01-system-context.puml` | C4 System Context | DOC-07 §7.3 |
| `02-use-case.puml` | UML Use Case | DOC-07 §7.4 |
| `03-container.puml` | C4 Container | DOC-07 §7.5 |
| `04-component.puml` | C4 Component (draft) | DOC-07 §7.6 |
| `05-er.puml` | Logical data model | DOC-07 §7.8 |
| `06-seq-single.puml` | Sequence: single-text analysis | DOC-07 §7.9.1 |
| `07-seq-batch.puml` | Sequence: batch analysis | DOC-07 §7.9.2 |
| `08-batch-states.puml` | State machine: batch lifecycle | DOC-07 §7.7 |
| `09-deployment.puml` | C4 Deployment | DOC-07 §7.10 |
| `10-ml-pipeline.puml` | Activity: offline ML pipeline | DOC-07 §7.11 |

## Rendering

Requirements: Java 11+ and Graphviz (`dot`). C4 diagrams use the C4-PlantUML standard library bundled with PlantUML (`!include <C4/...>`), so no internet access is needed.

```bash
# from repository root
curl -L -o tools/plantuml.jar \
  https://github.com/plantuml/plantuml/releases/download/v1.2024.7/plantuml-1.2024.7.jar
java -jar tools/plantuml.jar -tsvg -o ../export docs/diagrams/src/*.puml
java -jar tools/plantuml.jar -tpng -o ../export docs/diagrams/src/*.puml
```

Alternatively, use the PlantUML extension for VS Code / IntelliJ, or paste a source into the online editor at plantuml.com.

## Rules

1. Edit only `src/*.puml`; never edit exported images by hand.
2. Re-export images in the **same commit** as the source change, e.g.
   `DIP-11: add retry branch to batch sequence diagram`.
3. Component and entity names must match DOC-06 §6.7 and DOC-07 §7.13; rename in all three places at once.
