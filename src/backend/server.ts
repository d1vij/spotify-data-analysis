import express from "express";
import path from "path";
import chalk from "chalk";
import { fileURLToPath } from "url";

// dotenv setup
import dotenv from "dotenv";
dotenv.configDotenv({ path: "config.env" });

// py-bridge setup
import { pythonPath } from "@d1vij/py-bridge";
if(process.env.PYTHON_PATH === undefined) throw new Error("No python path found, check wheter config.env is setup correctly.");
pythonPath.set(process.env.PYTHON_PATH)

// ROUTERS
import {UploadRouter} from "./components/upload/router.js";

import { logger } from "./logger.js";


// Filepaths
export const FILEPATH = fileURLToPath(import.meta.url);
console.log(`Filename ${FILEPATH}`)
export const DIRPATH = path.dirname(FILEPATH);
console.log(`Dirname ${DIRPATH}`)

export const dataFolder = path.resolve(DIRPATH, "..","..","data");
console.log(`Datafolder ${dataFolder}`)

export const frontendFolder = path.resolve(DIRPATH, "..", "frontend");
console.log(`FrontendFolder ${frontendFolder}`)

export const piePath = path.resolve(DIRPATH, "..", "..","pie");
console.log(`Piepath ${piePath}`);

// Upload middleware singleton
import { createUploadMiddleware } from "./components/upload/multer-middleware.js";
export const upload = createUploadMiddleware(dataFolder);


// express
const app = express();
app.use(logger);
app.use(express.json());

// Static folder hookups
app.use("/",express.static(frontendFolder));

app.get("/", (_, response) => {
    response.sendFile(path.join(frontendFolder, "index.html"));
})

// Router mounting
app.use("/upload", UploadRouter);



app.listen(process.env.port, () => console.log(chalk.green("Server running on port " + process.env.port)));