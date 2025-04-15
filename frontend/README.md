# Interface DHFC

## Config

`src/config.ts` :
- `API_URL`: l'URL de l'API (backend)
- `FAKE_DATA`: si `true`, des données factices sont utilisées au lieu de l'API

## Run

```bash
pnpm install
pnpm dev
```

## Build

```bash
pnpm build
```

Puis déployer le contenu du dossier `dist` sur un serveur web (ex: nginx).
