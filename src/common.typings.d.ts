export interface Content {
    name: str,
    data:str,
    "type":str
}
export interface TextContent extends Content{
    "type": "text"
}
export interface ImageContent extends Content {
    "type": "image"
}
export type AnalyzedData = Array<TextContent | ImageContent | Content>;
