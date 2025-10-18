import multer from "multer";
import { nanoid } from "nanoid";

export function createUploadMiddleware(dataFolder:string){
    const diskStorage = multer.diskStorage({
        destination: dataFolder,
        filename: (request, file, cb) => {
            const name = nanoid() + ".zip";
            cb(null, name);
        }
    })
    const allowedMimes = [
        "application/zip",
        "application/x-zip-compressed",
        "multipart/x-zip",
        "application/octet-stream"
    ]

    return multer({
        dest: dataFolder,
        storage: diskStorage,
        
        fileFilter: (request, file, cb) => {
            if (!allowedMimes.includes(file.mimetype)) {
                cb(new TypeError("File is not a zip"));
            }
            else cb(null, true);
        }
    })
}