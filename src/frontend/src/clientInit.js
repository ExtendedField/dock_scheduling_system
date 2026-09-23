import { client } from "./client/client.gen";

client.setConfig({
  baseUrl:
    import.meta.env.VITE_BACKEND_URL || "http://localhost:8000",
});
