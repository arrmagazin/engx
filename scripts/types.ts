export type Path = string | string[];

export type FileOp<T = any> = (arg0: string, dir: string) => T | null;
