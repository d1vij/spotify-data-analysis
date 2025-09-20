import express from "express";
import { processUploadedZip } from "./process-uploaded-zip.js";

const router = express.Router();

// POST @/upload;
router.post("/", processUploadedZip);
export const UploadRouter = router;