import type { ArticleSource } from "./articleSource";
import type { EventSource } from "./eventSource";
import type { EventAnalyticsSource } from "./eventAnalyticsSource";
import type { DetectionSource } from "./detectionSource";

export type SourceItem =
  | EventSource
  | EventAnalyticsSource
  | ArticleSource
  | DetectionSource;
