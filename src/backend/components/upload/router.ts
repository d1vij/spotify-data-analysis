import express from "express";
import { processUploadedZip } from "./process-uploaded-zip.js";

const router = express.Router();

// POST @/upload;
router.post("/", processUploadedZip);

/**Mount path @/upload */
export const UploadRouter = router;