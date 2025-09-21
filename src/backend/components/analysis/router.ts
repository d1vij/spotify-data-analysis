import express from "express";
import {getAnalysis} from "./get-analysis.js"

const router = express.Router();

// GET @/analysis
router.get("/", getAnalysis);

/**Mount path @/analysis */
export const AnalysisRouter = router;
