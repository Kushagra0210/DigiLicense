import { PrismaPg } from "@prisma/adapter-pg";

import { PrismaClient } from "./generated/prisma/client";

export interface PrismaClientOptions {
  databaseUrl: string;
  poolMax: number;
  connectionTimeoutMs: number;
}

interface CachedClient {
  client: PrismaClient;
  databaseUrl: string;
}

let productionClient: CachedClient | undefined;

function createPrismaClient(options: PrismaClientOptions): PrismaClient {
  const adapter = new PrismaPg({
    connectionString: options.databaseUrl,
    max: options.poolMax,
    connectionTimeoutMillis: options.connectionTimeoutMs,
  });

  return new PrismaClient({ adapter });
}

function assertSameDatabase(cached: CachedClient, databaseUrl: string): void {
  if (cached.databaseUrl !== databaseUrl) {
    throw new Error(
      "The cached Prisma client was initialized with different database configuration.",
    );
  }
}

function getDevelopmentClient(options: PrismaClientOptions): PrismaClient {
  const cache = globalThis as typeof globalThis & {
    __digilicensePrismaClient?: CachedClient;
  };
  const existing = cache.__digilicensePrismaClient;

  if (existing) {
    assertSameDatabase(existing, options.databaseUrl);
    return existing.client;
  }

  const client = createPrismaClient(options);
  cache.__digilicensePrismaClient = {
    client,
    databaseUrl: options.databaseUrl,
  };
  return client;
}

function getProductionClient(options: PrismaClientOptions): PrismaClient {
  if (productionClient) {
    assertSameDatabase(productionClient, options.databaseUrl);
    return productionClient.client;
  }

  const client = createPrismaClient(options);
  productionClient = { client, databaseUrl: options.databaseUrl };
  return client;
}

export function getPrismaClient(
  options: PrismaClientOptions & {
    environment: "development" | "production" | "test";
    cache?: boolean;
  },
): PrismaClient {
  if (options.cache === false || options.environment === "test") {
    return createPrismaClient(options);
  }

  return options.environment === "development"
    ? getDevelopmentClient(options)
    : getProductionClient(options);
}
