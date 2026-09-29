# Shaarli Newsletter

Générez et envoyez chaque matin une newsletter à partir des liens partagés la veille sur votre instance Shaarli. Configurez la source, les envois, la météo et l’apparence depuis une interface web protégée, avec six palettes et trois mises en page.

## Fonctionnalités

- Interface d’administration avec page de connexion et session sécurisée
- Six palettes (couleurs et polices) associées à trois compositions : éditoriale, liste numérotée ou lien à la une
- Météo du jour via Open-Meteo, sans clé API
- Aperçu de la newsletter et envoi manuel
- Envoi automatique avec planificateur intégré

## Installation

```bash
git clone https://github.com/ludovicmorisset/newsletter.git
cd newsletter
cp env.example .env
```

Dans `.env`, définissez `ADMIN_USER`, un `ADMIN_PASSWORD` robuste et une clé aléatoire pour `SESSION_SECRET` (par exemple `openssl rand -hex 32`). Pour une connexion via HTTPS, définissez également `SESSION_COOKIE_SECURE=true`.

```bash
docker compose up -d --build
```

Ouvrez `http://votre-vps:8080/login` ou configurez un reverse proxy HTTPS avant d’exposer l’application à Internet.

## Configuration Shaarli

Dans Shaarli, ouvrez **Réglages > Configuration > API REST**, copiez le secret généré et renseignez-le dans l’interface d’administration.

L’URL de Shaarli doit inclure `http://` ou `https://` et désigner la racine de l’instance, sans ajouter `/api/v1/links`. Si Shaarli tourne aussi dans Docker, `localhost` depuis Newsletter désigne le conteneur Newsletter : utilisez le nom du service Shaarli et partagez un réseau Docker entre les deux services.