"""Structural checks for an OpenAPI 3.1 file without network access.

1. YAML parses; required top-level fields present.
2. Every $ref resolves.
3. operationIds unique; every operation has responses.
4. Every {path_param} in a path is declared as an in:path parameter.
5. Every example / examples value validates against its schema (JSON Schema 2020-12).
6. Probability examples sum to 1 ± 0.001; polarity matches emotion mapping.
"""
import sys, re, copy
import yaml
from jsonschema import Draft202012Validator
from jsonschema.validators import RefResolver  # deprecated but fine offline

spec = yaml.safe_load(open(sys.argv[1], encoding="utf-8"))
errors = []
for key in ("openapi", "info", "paths", "components"):
    if key not in spec:
        errors.append(f"missing top-level '{key}'")

def resolve(ref):
    assert ref.startswith("#/"), ref
    node = spec
    for part in ref[2:].split("/"):
        if part not in node:
            raise KeyError(ref)
        node = node[part]
    return node

def walk(node, path="$"):
    if isinstance(node, dict):
        if "$ref" in node:
            try:
                resolve(node["$ref"])
            except KeyError:
                errors.append(f"unresolved $ref {node['$ref']} at {path}")
        for k, v in node.items():
            walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]")
walk(spec)

def deref(node):
    while isinstance(node, dict) and "$ref" in node:
        node = resolve(node["$ref"])
    return node

# OpenAPI-only keywords that are not JSON Schema; strip 'example' inside schemas.
root_schema = copy.deepcopy(spec)
resolver = RefResolver.from_schema(root_schema)

def validate(instance, schema, where):
    v = Draft202012Validator(schema, resolver=resolver)
    for e in v.iter_errors(instance):
        errors.append(f"example invalid at {where}: {e.message} (path {list(e.absolute_path)})")

POL = {"joy": "positive", "sadness": "negative", "anger": "negative", "fear": "negative",
       "surprise": "neutral", "neutral": "neutral"}

def semantic(instance, where):
    if isinstance(instance, dict):
        p = instance.get("probabilities")
        if isinstance(p, dict) and len(p) == 6:
            s = sum(p.values())
            if abs(s - 1) > 0.001:
                errors.append(f"probabilities sum {s:.3f} != 1 at {where}")
            top = max(p, key=p.get)
            if "emotion" in instance and instance["emotion"] != top:
                errors.append(f"emotion {instance['emotion']} != argmax {top} at {where}")
            if "confidence" in instance and abs(instance["confidence"] - p[top]) > 1e-9:
                errors.append(f"confidence != max prob at {where}")
        if "emotion" in instance and "polarity" in instance:
            if POL[instance["emotion"]] != instance["polarity"]:
                errors.append(f"polarity mapping wrong at {where}")
        if "by_emotion" in instance:
            n = instance["analysed_count"]
            for grp in ("by_emotion", "by_polarity", "by_language"):
                c = sum(x["count"] for x in instance[grp].values())
                pc = sum(x["percent"] for x in instance[grp].values())
                if c != n: errors.append(f"{grp} counts {c} != analysed_count {n} at {where}")
                if abs(pc - 100) > 0.1: errors.append(f"{grp} percents {pc} != 100 at {where}")
            for lang, counts in instance["emotion_by_language"].items():
                if sum(counts.values()) != instance["by_language"][lang]["count"]:
                    errors.append(f"emotion_by_language[{lang}] sum mismatch at {where}")
            for emo in POL:
                col = sum(instance["emotion_by_language"][l][emo] for l in ("kk", "ru", "mixed"))
                if col != instance["by_emotion"][emo]["count"]:
                    errors.append(f"emotion_by_language column {emo}={col} != by_emotion at {where}")
        for k, v in instance.items():
            semantic(v, f"{where}.{k}")
    elif isinstance(instance, list):
        for i, v in enumerate(instance):
            semantic(v, f"{where}[{i}]")

def check_media(media, where):
    if "schema" not in media:
        return
    schema = media["schema"]
    if "example" in media:
        validate(media["example"], schema, where + ".example")
        semantic(media["example"], where + ".example")
    for name, ex in (media.get("examples") or {}).items():
        ex = deref(ex)
        validate(ex["value"], schema, f"{where}.examples.{name}")
        semantic(ex["value"], f"{where}.examples.{name}")

op_ids = {}
n_ops = 0
for p, item in spec["paths"].items():
    path_params = set(re.findall(r"{(\w+)}", p))
    shared = [deref(x) for x in item.get("parameters", [])]
    for method in ("get", "post", "put", "patch", "delete"):
        if method not in item:
            continue
        n_ops += 1
        op = item[method]
        oid = op.get("operationId")
        if not oid: errors.append(f"{method.upper()} {p}: no operationId")
        elif oid in op_ids: errors.append(f"duplicate operationId {oid}")
        op_ids[oid] = p
        if not op.get("responses"): errors.append(f"{method.upper()} {p}: no responses")
        params = shared + [deref(x) for x in op.get("parameters", [])]
        declared = {x["name"] for x in params if x.get("in") == "path"}
        if declared != path_params:
            errors.append(f"{method.upper()} {p}: path params {path_params} declared {declared}")
        rb = op.get("requestBody")
        if rb:
            for mt, media in deref(rb)["content"].items():
                check_media(media, f"{method.upper()} {p} request {mt}")
        for code, resp in op["responses"].items():
            resp = deref(resp)
            for mt, media in (resp.get("content") or {}).items():
                if mt.startswith("application/json"):
                    check_media(media, f"{method.upper()} {p} {code} {mt}")

# component responses examples too
for name, resp in spec["components"].get("responses", {}).items():
    for mt, media in resp.get("content", {}).items():
        check_media(media, f"components.responses.{name}")

# schemas themselves must be valid JSON Schema 2020-12
for name, s in spec["components"]["schemas"].items():
    try:
        Draft202012Validator.check_schema(s)
    except Exception as e:
        errors.append(f"schema {name} invalid: {e}")

print(f"operations: {n_ops}, schemas: {len(spec['components']['schemas'])}, "
      f"error codes: {len(spec['components']['schemas']['Error']['properties']['error']['properties']['code']['enum'])}")
if errors:
    print(f"{len(errors)} problem(s):")
    for e in errors: print(" -", e)
    sys.exit(1)
print("OK: refs resolve, operationIds unique, path params declared, all examples valid & consistent")
