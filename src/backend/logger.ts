import chalk from "chalk";
import { Request, Response, NextFunction } from "express";

export async function logger(request: Request, response: Response, next: NextFunction) {
  switch (request.method) {
    case "GET": {
      console.log(`[*] ${chalk.green("GET")} on ${request.url}`);
      break;
    }
    case "POST": {
      console.log(`[*] ${chalk.blue("POST")} on ${request.url}`);
      break;
    }
    case "DELETE": {
      console.log(`[*] ${chalk.red("DELETE")} on ${request.url}`);
      break;
    }
    default: {
      console.log(`[*] ${chalk.grey(request.method)} on ${request.url}`);
      break;
    }
  }
  next();
}