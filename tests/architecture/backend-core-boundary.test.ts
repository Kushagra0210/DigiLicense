import { readFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

import { describe, expect, it } from "vitest";

const repositoryRoot = resolve(dirname(fileURLToPath(import.meta.url)), "../..");
const backendCoreRoot = join(repositoryRoot, "packages/backend-core");
const forbiddenImports = [
  "next",
  "react",
  "@prisma/",
  "@digilicense/db",
  "drizzle",
  "express",
  "openai",
  "@anthropic-ai/",
];

async function listTypeScriptFiles(directory: string): Promise<string[]> {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(
    entries.map(async (entry) => {
      const path = join(directory, entry.name);
      if (entry.isDirectory()) return listTypeScriptFiles(path);
      return entry.name.endsWith(".ts") ? [path] : [];
    }),
  );
  return nested.flat();
}

describe("backend-core dependency boundary", () => {
  it("has no runtime dependencies", async () => {
    const manifest = JSON.parse(
      await readFile(join(backendCoreRoot, "package.json"), "utf8"),
    ) as { dependencies?: Record<string, string> };
    expect(manifest.dependencies ?? {}).toEqual({});
  });

  it("does not import frameworks, persistence, or provider SDKs", async () => {
    const files = await listTypeScriptFiles(join(backendCoreRoot, "src"));

    for (const file of files) {
      const source = await readFile(file, "utf8");
      for (const forbiddenImport of forbiddenImports) {
        expect(source, `${file} imports ${forbiddenImport}`).not.toContain(
          `from "${forbiddenImport}`,
        );
        expect(source, `${file} imports ${forbiddenImport}`).not.toContain(
          `from '${forbiddenImport}`,
        );
      }
    }
  });
});
