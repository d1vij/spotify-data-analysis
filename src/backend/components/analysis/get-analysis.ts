import { Request, Response } from "express";
import { ResponseStatus } from "../../enums.js";
import fs from "fs";
import { execute } from "@d1vij/py-bridge";
import path from "path";
import { piePath } from "../../server.js";

import {AnalyzedData} from "../../../common.typings.js";


export async function getAnalysis(request:Request, response:Response){

    const {jsonpath} = request.cookies;
    if(jsonpath === undefined){
        response.status(400);
        response.json({
            status: ResponseStatus.failure,
            err: "No stored jsonpath found in cookies. Make sure that the zip file has been uploaded successfully."
        })
        return;
    }
    if(fs.existsSync(jsonpath) === false){
        response.status(400);
        response.json({
            status: ResponseStatus.failure,
            err: "The found jsonpath is not a valid path."
        })
        return;
    }
    const results = await execute<AnalyzedData>(path.join(piePath, "analysis_generator.py"), "generate", {
        filepath: jsonpath
    })
    if(results.success === false){
        response.status(500)
        response.json({
            status: ResponseStatus.failure,
            err: "Error in generating analysis : " +  results.errorMsg
        })
        return;
    }
    
    response.json({
        status: ResponseStatus.success,
        analysis: results.payload as AnalyzedData
    });
    return;
}