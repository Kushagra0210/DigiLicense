import { config as loadEnvironment } from "dotenv";
import { resolve } from "node:path";
import { defineConfig } from "prisma/config";

loadEnvironment({
  path: resolve(import.meta.dirname, "../../.env"),
  quiet: true,
});

export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: {
    path: "prisma/migrations",
  },
  // An empty fallback lets schema-only validate/generate commands run without
  // credentials. Commands that connect to PostgreSQL still fail closed.
  datasource: {
    url: process.env.DATABASE_URL ?? "",
  },
});
