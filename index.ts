import { launchBook } from "../arrmatura-books";
import pkg from "./package.json";

const { author, copyright, description, displayName, logo, keywords, name, storeUrl, version, repository } = pkg;
const repoUrl = repository.url;
const release = `${repoUrl.replace("https://github.com/", "")}@${version}`;

const app = { id: name, name: displayName, logo, version, description, author, keywords, copyright, storeUrl, repoUrl };
const book = {
  indexUrl: `https://data.jsdelivr.com/v1/packages/gh/${release}?structure=tree`,
  docUrl: `https://cdn.jsdelivr.net/gh/${release}/docs/*`,
  scope: "docs",
};
launchBook({
  app,
  book,
});
