import type http from "node:http";
import * as esbuild from "esbuild";
import { readFileJsonContent } from "./utils/files";
import { getEsbuildOptions } from "./utils/getEsbuildOptions";

export async function main(options: any = {}) {
  try {
    const { name, esbuild: esBuildPackageOpions } = readFileJsonContent([`${process.cwd()}/package.json`]) ?? {};

    const {
      entryPoints = esBuildPackageOpions?.entryPoints,
      servedir = esBuildPackageOpions?.servedir ?? process.env.WWW ?? "./www",
      fallback = `${servedir}/index.html`,
      port = parseInt(process.env.PORT ?? "8080", 10),
      host = process.env.HOST ?? "localhost",
      noWatch = false,
      ...buildOptions
    } = options;

    const clients = new Set<http.ServerResponse>();

    const ctx = await esbuild.context(
      getEsbuildOptions({
        entryPoints,
        plugins: [],
        outdir: `${servedir}/dist`,
        // Dev only: link the map so devtools pick it up. Production builds (build.ts) keep
        // the "external" default, which emits no sourceMappingURL reference.
        sourcemap: "linked",
        ...buildOptions,
      }),
    );

    if (!noWatch) {
      await ctx.watch();
    }

    const serveOptions = {
      servedir,
      fallback,
      port,
      host,
      onRequest: ({ method, path, status }) => {
        console.log(`>> ${method}${path} - ${status}`);
      },
    };

    const { hosts: serveHosts, port: servePort } = await ctx.serve(serveOptions);

    const addresses = (port) =>
      String(serveHosts)
        .split(",")
        .map((h) => `http://${h}:${port}`)
        .join(" ");

    console.log(`✅ Serving "${name}" app at ${addresses(servePort)} from ${servedir}`);
  } catch (err: any) {
    console.error("❌ Error:", err.message || err);
    if (err.details) {
      console.error(err.details);
    }
    process.exit(1);
  }
}

main();
