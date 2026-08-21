import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";

export default defineConfig([
  ...nextVitals,
  {
    files: ["src/**/*.{js,jsx,ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@prisma/**", "@digilicense/db", "@digilicense/db/**"],
              message:
                "Transport and UI files must call the server composition layer, not persistence.",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/server/composition/**/*.{js,jsx,ts,tsx}"],
    rules: {
      "no-restricted-imports": "off",
    },
  },
  globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);
