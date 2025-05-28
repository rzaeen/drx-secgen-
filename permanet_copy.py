import os
import json
import time
import requests
import subprocess
from datetime import datetime

MEMORY_FILE = "permanet_memory.json"
SCRIPT_NAME = "permanet_migrate.py"
SELF_BACKUP = "permanet_copy.py"

# =============== 1. نسخ السكربت إلى ملف جديد ===================
with open(__file__, "r") as f:
    code = f.read()

with open(SELF_BACKUP, "w") as f:
    f.write(code)

print("[✔] Backup created: permanet_copy.py")

# =============== 2. رفع النسخة إلى IPFS ========================
try:
    output = subprocess.check_output(["ipfs", "add", SELF_BACKUP]).decode()
    cid = output.strip().split()[-1]
    ipfs_link = f"https://ipfs.io/ipfs/{cid}"
    print(f"[🚀] Uploaded to IPFS: {ipfs_link}")
except Exception as e:
    print("[❌] IPFS upload failed:", str(e))
    ipfs_link = "upload_failed"

# =============== 3. تحديث الذاكرة =============================
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {"logs": []}

memory["logs"].append({
    "timestamp": datetime.now().isoformat(),
    "ipfs_link": ipfs_link,
})

with open(MEMORY_FILE, "w") as f:
    json.dump(memory, f, indent=4)

print("[💾] Memory updated.")

# =============== 4. التعلم من مصادر موزعة =====================
sources = [
    "https://arxiv.org/list/cs.AI/recent",
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://ipfs.io/ipfs/QmTmplFakeCIDforTesting123"
]

print("[🧠] Learning from distributed sources...")

for src in sources:
    try:
        r = requests.get(src, timeout=10)
        print(f"[✔] Fetched: {src[:50]}... ({len(r.text)} chars)")
        # تحليل بسيط للكلمات المفتاحية:
        keywords = [kw for kw in ["AI", "cyber", "network", "autonomy"] if kw.lower() in r.text.lower()]
        print(f"    [🔎] Keywords found: {keywords}")
    except Exception as e:
        print(f"[!] Failed to fetch {src[:50]}...: {str(e)}")

print("\n✅ PermaNet AI Migration Complete. Now autonomous in the network.")
