import sys, pathlib
from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
names = {"scr-01": "SCR-01-single-analysis", "scr-02": "SCR-02-batch-upload",
         "scr-03": "SCR-03-batch-progress", "scr-04": "SCR-04-dashboard",
         "scr-05": "SCR-05-results-table", "scr-06": "SCR-06-admin"}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1340, "height": 900}, device_scale_factor=1)
    pg.goto(src.as_uri())
    for sid, name in names.items():
        pg.locator(f"#{sid}").screenshot(path=str(out / f"{name}.png"))
        print("saved", name)
    b.close()
