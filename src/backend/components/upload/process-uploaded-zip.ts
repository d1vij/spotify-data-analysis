import path from "path";
import { Request, Response } from "express";

import {execute} from "@d1vij/py-bridge";

import { DIRPATH, piePath, upload } from "../../server.js";
import { ResponseStatus } from "../../enums.js";

export async function processUploadedZip(request:Request, response:Response){
    
    console.log("uploaded");
    try{
        await new Promise<void>((resolve, reject) => {
            upload.single("zipfile")(request, response, (err: any) => {
                if(err) return reject(err);
                resolve();
            });
        })
        console.log(request.file)
        console.log("got file");
        
        if(request.file == undefined){
            console.log("File undefined");
            throw new Error("Error in saving file! ");
        }

        console.log(`> File saved at : ${request.file.path}`);
        const results = await execute<string>(path.join(piePath, "process_zip.py"), "process", {
            filepath: request.file.path
        });
        if(results.success === false) throw new Error("Error in executing process_zip.py -> " + results.errorMsg);

        const jsonpath = results.payload;
        response.cookie("jsonpath", jsonpath, {
            maxAge: 8.64e+7 //expire after 1 day
        })
        response.json(results);
    } catch (e){
        console.log("error occured" + e)
        response.json({
            status: ResponseStatus.failure,
            err: e
        })
    }
}