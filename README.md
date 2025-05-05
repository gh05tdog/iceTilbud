# Smirnoff Ice Tilbud App

Denne guide viser, hvordan du sætter hele applikationen op på en Ubuntu-server kørende i Proxmox.

## Anbefalet Operativsystem
- **Ubuntu 24.04 LTS Server (ISO image)**

## 1. Opret VM i Proxmox
1. Download den **Ubuntu 24.04 LTS Server ISO**.
2. I Proxmox, vælg **Create VM**.
3. Navngiv VM, vælg ISO, tildel 2 CPU, 4 GB RAM, 20 GB disk.
4. Installér Ubuntu med standardindstillinger.

## 2. Installer Node.js, npm og Git
```bash
sudo apt update
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs git nginx
```

## 3. Klon Repo
```bash
git clone https://github.com/username/iceweb.git
cd iceweb
```

## 4. Opsæt Backend
```bash
cd backend
npm install
npm start
```
- Kører på http://localhost:5000

## 5. Opsæt Frontend
Åbn en ny terminal:
```bash
cd iceweb/frontend
npm install
npm start
```
- Åbner http://localhost:3000

## 6. Produktion (valgfrit)
Byg frontend:
```bash
cd frontend
npm run build
```

Server buildet med **nginx**:
```bash
sudo rm /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/iceweb > /dev/null <<EOF
server {
  listen 80;
  server_name your.domain.com;
  root /home/iceweb/frontend/build;
  index index.html;
  location /api/ {
    proxy_pass http://localhost:5000/;
  }
  location / {
    try_files $uri /index.html;
  }
}
EOF
sudo ln -s /etc/nginx/sites-available/iceweb /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## Troubleshooting
- **CORS**: Tjek at backend er tilgængelig.
- **Scraping**: Hvis data ændrer sig, opdater selektorer i `backend/server.js`.
