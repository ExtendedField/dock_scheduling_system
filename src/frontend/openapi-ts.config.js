import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  client: "@hey-api/client-axios",
  input: "../../openapi.json",
  output: "./src/client", // This is where all your hooks/functions will live
});
