import requests
from datetime import datetime
import os

# CONFIGURAÇÃO
GITHUB_USER = "Dc0st4"           
TOKEN = os.getenv("GITHUB_TOKEN")  # opcional para evitar rate limit
OUTPUT_FILE = "torres.svg"

# Função para pegar commits de um repositório no mês atual
def commits_this_month(repo):
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    today = datetime.utcnow()
    since = today.replace(day=1).isoformat() + "Z"
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo}/commits?since={since}&author={GITHUB_USER}&per_page=100"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Erro ao acessar {repo}: {r.status_code}")
        return 0
    return len(r.json())

# Lista de repositórios para mostrar torres
repos = ["Dc0st4", "outro-repo"]  # EDITAR: seus repos

# Obter commits
commit_counts = [commits_this_month(r) for r in repos]
max_commits = max(commit_counts) if commit_counts else 1

# SVG - cada torre proporcional ao número de commits
svg_parts = [
    f'<svg viewBox="0 0 {len(repos)*60+40} 200" xmlns="http://www.w3.org/2000/svg">',
    '<rect width="100%" height="100%" fill="#050010"/>',
    '<defs>',
    '<linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">',
    '<stop offset="0%" stop-color="#0ff"/>',
    '<stop offset="100%" stop-color="#f0f"/>',
    '</linearGradient>',
    '</defs>'
]

# criar torres
for i, count in enumerate(commit_counts):
    height = min(count, max_commits)
    x = 20 + i*60
    svg_parts.append(f'''
    <rect x="{x}" y="180" width="30" height="0" fill="url(#grad)">
        <animate attributeName="height" values="0;{height};0" dur="6s" repeatCount="indefinite"/>
        <animate attributeName="y" values="180;{180-height};180" dur="6s" repeatCount="indefinite"/>
    </rect>
    <text x="{x+15}" y="195" text-anchor="middle" fill="#0ff" font-family="monospace" font-size="12">{count}</text>
    ''')

svg_parts.append('</svg>')

# salvar arquivo
with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(svg_parts))

print(f"SVG gerado: {OUTPUT_FILE}")
