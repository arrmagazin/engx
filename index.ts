import { launchBook } from "../arrmatura-books";
import pkg from "./package.json";

const { author, copyright, description, displayName, keywords, name } = pkg;
const logo = "/favicon.svg";
const {
  storeUrl,
  version,
  repository: { url: repoUrl },
} = pkg;

const app = { id: name, name: displayName, logo, version, description, author, keywords, copyright, storeUrl, repoUrl };

const book = {
  indexUrl: "/index.json",
  docUrl: "/docs/*",
  scope: "docs",
};

launchBook({ app, book });
