import { Parser, Generator } from "sparqljs";

export const parser = new Parser({ skipValidation: true });
export const generator = new Generator();
