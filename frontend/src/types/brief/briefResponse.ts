import type { SourceItem } from "../source/sourceItem";

export interface BriefResponse {
    brief: string | null;
    sources: Record<string, SourceItem>;
}