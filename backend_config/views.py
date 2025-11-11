from django.http import HttpResponse
from django.db import connection
from django.conf import settings
import psutil
import platform


def home(request):
    # --- DB status ---
    try:
        with connection.cursor() as c:
            c.execute("SELECT 1")
        db_status, db_color = "Online", "#2ecc71"
    except Exception:
        db_status, db_color = "Offline", "#e74c3c"

    # --- Debug status ---
    debug_status = "Active" if settings.DEBUG else "Inactive"
    debug_color = "#f39c12" if settings.DEBUG else "#2ecc71"

    # --- System metrics ---
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    mem_used = round(mem.used / (1024 ** 3), 1)
    mem_total = round(mem.total / (1024 ** 3), 1)
    disk_used = round(disk.used / (1024 ** 3), 1)
    disk_total = round(disk.total / (1024 ** 3), 1)

    def color(v):
        return "#2ecc71" if v < 75 else "#f39c12" if v < 90 else "#e74c3c"

    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Deverse Backend</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        :root {{
          --fg:#2c3e50; --muted:#6b7785; --link:#2d7fd3; --border:#e6e8eb;
        }}
        * {{ box-sizing: border-box; }}
        body {{
          margin: 0;
          background:#fff;
          color:var(--fg);
          font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
          min-height: 100vh;
          display:flex;
          flex-direction:column;
          align-items:center;
          justify-content:center;
          gap:18px;
          text-align:center;
          padding: 24px;
        }}
        h1 {{ margin:0; font-size: 2.2rem; font-weight:700; }}
        h2 {{ margin:0; font-size:1rem; font-weight:400; color:var(--muted); }}
        .tags {{
          display:flex; flex-wrap:wrap; justify-content:center; gap:8px; margin-top:10px;
        }}
        .tag {{
          display:inline-flex; align-items:center; gap:6px;
          border:1px solid var(--border);
          border-radius:9999px;
          padding:4px 10px;
          font-size:.95rem;
          line-height:1.1;
          background:#fff;
        }}
        .dot {{ width:10px; height:10px; border-radius:50%; display:inline-block; }}
        a {{
          color:var(--link);
          text-decoration:none;
          font-weight:600;
          margin-top:6px;
        }}
        a:hover {{ text-decoration:underline; }}
        footer {{
          position:fixed;
          bottom:14px;
          left:0; right:0;
          color:var(--muted);
          font-size:.9rem;
        }}
      </style>
    </head>
    <body>
      <h1>I'm ready to flirt with your frontend!! 😏</h1>
      <h2>Backend is up, alive, and feeling smooth.</h2>

      <div class="tags">
        <span class="tag"><span class="dot" style="background:{db_color}"></span>Database: <strong>{db_status}</strong></span>
        <span class="tag"><span class="dot" style="background:{debug_color}"></span>Debug Mode: <strong>{debug_status}</strong></span>
        <span class="tag"><span class="dot" style="background:{color(cpu)}"></span>CPU: <strong>{cpu:.1f}%</strong></span>
        <span class="tag"><span class="dot" style="background:{color(mem.percent)}"></span>Memory: <strong>{mem.percent:.1f}%</strong> ({mem_used} GB / {mem_total} GB)</span>
        <span class="tag"><span class="dot" style="background:{color(disk.percent)}"></span>Disk: <strong>{disk.percent:.1f}%</strong> ({disk_used} GB / {disk_total} GB)</span>
      </div>

      <a href="/api/hello/">👉 Go to /api/hello/</a>

      <footer>Host: {platform.node()} • OS: {platform.system()} {platform.release()}</footer>
    </body>
    </html>
    """
    return HttpResponse(html)
