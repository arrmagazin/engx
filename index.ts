import { launchBook } from "../arrmatura-books";
import pkg from "./package.json";

const { author, copyright, description, displayName, logo, keywords, name, store, version } = pkg;
const release = `arrmagazin/engx@${version}`;

const app = { id: name, name: displayName, logo, version, description, author, keywords, copyright };
const book = {
  indexUrl: `https://data.jsdelivr.com/v1/packages/gh/${release}?structure=tree`,
  docUrl: `https://cdn.jsdelivr.net/gh/${release}/docs/*`,
  scope: "docs",
  store,
};
launchBook({
  app,
  book,
});
