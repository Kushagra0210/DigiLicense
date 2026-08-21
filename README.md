# DigiLicense

## Prerequisites

- Node.js >= 20.19.0
- pnpm 11.22.0

## Getting Started

```bash
# Install dependencies
pnpm install

# Set up the database
pnpm db:generate
pnpm db:migrate

# Start development servers
pnpm dev
```

## Available Commands

| Command | Description |
| --- | --- |
| `pnpm dev` | Start all apps in development mode |
| `pnpm build` | Build all packages and apps |
| `pnpm lint` | Lint all packages |
| `pnpm typecheck` | Type-check all packages |
| `pnpm db:generate` | Generate Prisma client |
| `pnpm db:migrate` | Run database migrations |
| `pnpm db:studio` | Open Prisma Studio |
