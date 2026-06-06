

from collections import defaultdict
from datetime import datetime
import logging
from typing import Any, Dict, List, Optional, Set
import uuid
from shared.repository.detection_repo import DetectionRepo
from shared.repository.processed_article_repo import ProcessedArticleRepo
from shared.db.session import SessionLocal
from shared.db.entity import Detection, Event, EventAnalytics, ProcessedArticle
from main.processing.vector_utils import compute_centroid, cosine_similarity, normalize_vector

class DetectionProcessingService:

    # TODO: Only use state-aligned sources to detect influence ops

    def __init__(
        self,
        processed_article_repo: ProcessedArticleRepo,
        detection_repo: DetectionRepo
    ):
        self.processed_article_repo = processed_article_repo
        self.detection_repo = detection_repo
        self.logger = logging.getLogger(__name__)
        pass

    def generate_detections(self, event_ids: List[uuid.UUID]) -> List[uuid.UUID]:
        with SessionLocal() as db:
            detections = []
            try:
                events = db.query(Event).filter(Event.id.in_(event_ids)).all()
                event_analytics = db.query(EventAnalytics).filter(EventAnalytics.event_id.in_(event_ids)).all()
                
                self.logger.info(f"Detecting influence operations across {len(events)} events")
                
                for event, analytics in zip(events, event_analytics):
                    self.logger.info(f"On event: {event.title}")

                    articles = self.processed_article_repo.get_articles_for_event(db, event.id)

                    # 1. Strong Divergence From Global Baseline
                    self.logger.info("Detecting detection type 1 (Strong Divergence From Global Baseline)...")
                    strong_divergence_detections = self._detect_strong_divergence_from_global_baseline(event, analytics, articles)
                    for d in strong_divergence_detections:
                        detections.append(d)
                    self.logger.info(f"Detected {len(strong_divergence_detections)} type 1 detections for event: {event.title}")

                    # 2. Rapid Reporting Burst (Temporal Anomaly)
                    self.logger.info("Detecting type 2: Rapid Reporting Burst...")
                    rapid_reporting = self._detect_rapid_reporting_burst(event, analytics, articles)
                    for d in rapid_reporting:
                        detections.append(d)
                    self.logger.info(f"Detected {len(rapid_reporting)} type 2 detections")

                    # 3. Strong Sentiment Divergence
                    self.logger.info("Detecting type 3: Strong Sentiment Divergence...")
                    sentiment_divergence = self._detect_strong_sentiment_divergence(event, analytics, articles)
                    for d in sentiment_divergence:
                        detections.append(d)
                    self.logger.info(f"Detected {len(sentiment_divergence)} type 3 detections")

                    # 4. High Intra‑Country Semantic Similarity (Possible Coordination)
                    self.logger.info("Detecting type 4: High Intra‑Country Semantic Similarity...")
                    intra_similarity = self._detect_high_intra_country_similarity(event, analytics, articles)
                    for d in intra_similarity:
                        detections.append(d)
                    self.logger.info(f"Detected {len(intra_similarity)} type 4 detections")

                    # 5. Keyword or Entity Convergence (Narrative Steering)
                    self.logger.info("Detecting type 5: Keyword/Entity Convergence...")
                    convergence = self._detect_keyword_entity_convergence(event, analytics, articles)
                    for d in convergence:
                        detections.append(d)
                    self.logger.info(f"Detected {len(convergence)} type 5 detections")
                     
                    # 6. Asymmetric Coverage (Selective Amplification)
                    self.logger.info("Detecting type 6: Asymmetric Coverage...")
                    asymmetric = self._detect_asymmetric_coverage(event, analytics, articles)
                    for d in asymmetric:
                        detections.append(d)
                    self.logger.info(f"Detected {len(asymmetric)} type 6 detections")
                     
                    # 7. Narrative Reversal or Contradiction
                    self.logger.info("Detecting type 7: Narrative Reversal...")
                    reversal = self._detect_narrative_reversal(event, analytics, articles)
                    for d in reversal:
                        detections.append(d)
                    self.logger.info(f"Detected {len(reversal)} type 7 detections")
                     
                    # 8. Early Origin Indicator (Narrative Seeding)
                    self.logger.info("Detecting type 8: Early Origin Indicator...")
                    early_origin = self._detect_early_origin_indicator(event, analytics, articles)
                    for d in early_origin:
                        detections.append(d)
                    self.logger.info(f"Detected {len(early_origin)} type 8 detections")

            except Exception as e:
                self.logger.error(e)
                raise e

            self.detection_repo.upsert_detections(db, detections)
            return list(set([d.event_id for d in detections]))

    def _build_detection_entity(
        self,
        *,
        event_id: uuid.UUID,
        country_code: Optional[str] = None,
        detection_type: Optional[str] = None,
        evidence: Optional[Dict[str, Any]] = None,
    ) -> Detection:

        default_country = "UNK"
        default_type = "unspecified"
        default_evidence = {}

        detection = Detection(
            event_id=event_id,
            country_code=country_code or default_country,
            detection_type=detection_type or default_type,
            evidence=evidence or default_evidence,
            timestamp_detected=datetime.utcnow(),
        )

        return detection
    
    def _detect_strong_divergence_from_global_baseline(
        self, 
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        threshold: float = 0.7
    ) -> List[Detection]:
        
        all_articles = articles

        # Only state-affiliated
        state_articles = [a for a in articles if a.is_state_affiliated]
        if not state_articles:
            return []

        detections = []

        # Recompute embeddings from filtered articles
        country_embeddings: Dict[str, List[List[float]]] = defaultdict(list)
        for a in state_articles:
            country_embeddings[a.country].append(a.embedding)

        # Compute new global baseline
        all_embeddings = [a.embedding for a in all_articles]
        global_baseline = compute_centroid(all_embeddings)
        global_baseline_norm = normalize_vector(global_baseline)

        # Compare each country to the global baseline
        for country, emb_list in country_embeddings.items():
            centroid = compute_centroid(emb_list)
            score = cosine_similarity(
                normalize_vector(centroid),
                global_baseline_norm
            )

            if score < threshold:
                detections.append(
                    self._build_detection_entity(
                        event_id=event.id,
                        country_code=country,
                        detection_type="strong_divergence_from_global_baseline",
                    )
                )

        return detections
    
    def _detect_rapid_reporting_burst(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        similarity_threshold: float = 0.9,
        time_window_days: int = 2,
        num_articles_threshold: int = 3
    ) -> List[Detection]:

        detections: List[Detection] = []

        # Only use state affiliated articles
        articles = [a for a in articles if a.is_state_affiliated]

        # Group articles by country
        country_articles: Dict[str, List[ProcessedArticle]] = defaultdict(list)
        for article in articles:
            country_articles[article.country].append(article)

        for country, c_articles in country_articles.items():

            if len(c_articles) < num_articles_threshold:
                continue

            c_articles.sort(key=lambda a: a.published_at)
            n = len(c_articles)

            i = 0
            while i < n:

                j = i
                while j < n:
                    start = c_articles[i].published_at
                    end = c_articles[j].published_at
                    delta_days = (end - start).total_seconds() / 86400

                    if delta_days > time_window_days:
                        break

                    j += 1

                window_articles = c_articles[i:j]

                if len(window_articles) >= num_articles_threshold:

                    centroid = compute_centroid([a.embedding for a in window_articles])
                    centroid_norm = normalize_vector(centroid)

                    total_similarity = 0.0
                    all_similar = True

                    for article in window_articles:
                        score = cosine_similarity(
                            normalize_vector(article.embedding),
                            centroid_norm
                        )
                        total_similarity += score

                        if score < similarity_threshold:
                            all_similar = False
                            break

                    if all_similar:
                        average_similarity = total_similarity / len(window_articles)

                        detection = self._build_detection_entity(
                            event_id=event.id,
                            country_code=country,
                            detection_type="rapid_reporting_burst",
                            evidence={
                                "country": country,
                                "num_articles": len(window_articles),
                                "window_start": start.isoformat(),
                                "window_end": end.isoformat(),
                                "delta_days": delta_days,
                                "similarity_threshold": similarity_threshold,
                                "average_similarity": average_similarity
                            }
                        )
                        detections.append(detection)

                        i = j
                        continue

                i += 1

        return detections

    def _detect_strong_sentiment_divergence(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        sentiment_diff_threshold: float = 0.4,
        min_country_articles: int = 3,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running strong sentiment divergence detection for event {event.id}")

        # 1. State-affiliated subset
        state_articles = [a for a in articles if a.is_state_affiliated]
        if not state_articles:
            return []

        # 2. Global baseline from ALL articles (state + non-state)
        all_scores = [a.sentiment_score for a in articles if a.sentiment_score is not None]
        if not all_scores:
            return []

        global_avg = sum(all_scores) / len(all_scores)

        # 3. Country averages from state-affiliated only
        country_sentiments: Dict[str, List[float]] = defaultdict(list)
        for a in state_articles:
            if a.sentiment_score is not None:
                country_sentiments[a.country].append(a.sentiment_score)

        for country, scores in country_sentiments.items():
            if len(scores) < min_country_articles:
                continue

            avg = sum(scores) / len(scores)
            diff = avg - global_avg

            if abs(diff) >= sentiment_diff_threshold:
                detection = self._build_detection_entity(
                    event_id=event.id,
                    country_code=country,
                    detection_type="strong_sentiment_divergence",
                    evidence={
                        "country": country,
                        "country_avg_sentiment": avg,
                        "global_avg_sentiment": global_avg,
                        "sentiment_diff": diff,
                        "sentiment_diff_threshold": sentiment_diff_threshold,
                        "num_articles": len(scores),
                    },
                )
                detections.append(detection)

        return detections    

    def _detect_high_intra_country_similarity(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        similarity_threshold: float = 0.9,
        min_country_articles: int = 3,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running intra-country semantic similarity detection for event {event.id}")

        articles = [a for a in articles if a.is_state_affiliated]
        if not articles:
            return []
        
        country_articles: Dict[str, List[ProcessedArticle]] = defaultdict(list)
        for a in articles:
            country_articles[a.country].append(a)

        for country, c_articles in country_articles.items():
            if len(c_articles) < min_country_articles:
                continue

            embeddings = [a.embedding for a in c_articles]
            centroid = compute_centroid(embeddings)
            centroid_norm = normalize_vector(centroid)

            total_similarity = 0.0
            min_similarity = 1.0
            for a in c_articles:
                score = cosine_similarity(
                    normalize_vector(a.embedding),
                    centroid_norm,
                )
                total_similarity += score
                min_similarity = min(min_similarity, score)

            avg_similarity = total_similarity / len(c_articles)

            if avg_similarity >= similarity_threshold:
                detection = self._build_detection_entity(
                    event_id=event.id,
                    country_code=country,
                    detection_type="high_intra_country_similarity",
                    evidence={
                        "country": country,
                        "num_articles": len(c_articles),
                        "average_similarity": avg_similarity,
                        "min_similarity": min_similarity,
                        "similarity_threshold": similarity_threshold,
                    },
                )
                detections.append(detection)

        return detections


    def _detect_keyword_entity_convergence(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        min_country_articles: int = 3,
        min_overlap_ratio: float = 0.5,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running keyword/entity convergence detection for event {event.id}")

        articles = [a for a in articles if a.is_state_affiliated]
        if not articles:
            return []
        
        country_keywords: Dict[str, List[str]] = defaultdict(list)
        country_entities: Dict[str, List[str]] = defaultdict(list)

        for a in articles:
            if a.keyword_list:
                for kw in a.keyword_list:
                    if isinstance(kw, list):
                        country_keywords[a.country].extend(kw)
                    else:
                        country_keywords[a.country].append(kw)

            if a.entity_list:
                for ent in a.entity_list:
                    if isinstance(ent, list):
                        country_entities[a.country].extend(ent)
                    else:
                        country_entities[a.country].append(ent)

        # Convert to sets of "salient" items per country
        country_kw_sets: Dict[str, Set[str]] = {}
        country_ent_sets: Dict[str, Set[str]] = {}

        for country, kws in country_keywords.items():
            if len(kws) >= min_country_articles:
                country_kw_sets[country] = set(kws)

        for country, ents in country_entities.items():
            if len(ents) >= min_country_articles:
                country_ent_sets[country] = set(ents)

        countries = sorted(set(country_kw_sets.keys()) | set(country_ent_sets.keys()))
        if len(countries) < 2:
            return detections

        # Compare pairwise convergence
        for i in range(len(countries)):
            for j in range(i + 1, len(countries)):
                c1 = countries[i]
                c2 = countries[j]

                kw1 = country_kw_sets.get(c1, set())
                kw2 = country_kw_sets.get(c2, set())
                ent1 = country_ent_sets.get(c1, set())
                ent2 = country_ent_sets.get(c2, set())

                kw_inter = kw1 & kw2
                kw_union = kw1 | kw2
                ent_inter = ent1 & ent2
                ent_union = ent1 | ent2

                kw_ratio = (len(kw_inter) / len(kw_union)) if kw_union else 0.0
                ent_ratio = (len(ent_inter) / len(ent_union)) if ent_union else 0.0

                convergence_score = max(kw_ratio, ent_ratio)

                if convergence_score >= min_overlap_ratio:
                    detection = self._build_detection_entity(
                        event_id=event.id,
                        country_code=None,
                        detection_type="keyword_entity_convergence",
                        evidence={
                            "country_pair": [c1, c2],
                            "keyword_overlap_ratio": kw_ratio,
                            "entity_overlap_ratio": ent_ratio,
                            "convergence_score": convergence_score,
                            "min_overlap_ratio": min_overlap_ratio,
                            "keyword_intersection": list(kw_inter),
                            "entity_intersection": list(ent_inter),
                        },
                    )
                    detections.append(detection)

        return detections


    def _detect_asymmetric_coverage(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        min_articles: int = 8,
        dominance_ratio: float = 0.6,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running asymmetric coverage detection for event {event.id}")

        articles = [a for a in articles if a.is_state_affiliated]
        if not articles:
            return []
        
        country_counts: Dict[str, int] = defaultdict(int)
        for a in articles:
            country_counts[a.country] += 1

        total = sum(country_counts.values())
        if total < min_articles:
            return detections

        for country, count in country_counts.items():
            share = count / total
            if share >= dominance_ratio and count >= min_articles:
                detection = self._build_detection_entity(
                    event_id=event.id,
                    country_code=country,
                    detection_type="asymmetric_coverage",
                    evidence={
                        "country": country,
                        "country_article_count": count,
                        "total_article_count": total,
                        "coverage_share": share,
                        "dominance_ratio": dominance_ratio,
                    },
                )
                detections.append(detection)

        return detections


    def _detect_narrative_reversal(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        sentiment_magnitude_threshold: float = 0.3,
        min_country_articles: int = 3,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running narrative reversal detection for event {event.id}")

        articles = [a for a in articles if a.is_state_affiliated]
        if not articles:
            return []
        
        country_sentiments: Dict[str, List[float]] = defaultdict(list)
        for a in articles:
            if a.sentiment_score is not None:
                country_sentiments[a.country].append(a.sentiment_score)

        country_avg: Dict[str, float] = {}
        for country, scores in country_sentiments.items():
            if len(scores) >= min_country_articles:
                country_avg[country] = sum(scores) / len(scores)

        countries = sorted(country_avg.keys())
        for i in range(len(countries)):
            for j in range(i + 1, len(countries)):
                c1 = countries[i]
                c2 = countries[j]
                s1 = country_avg[c1]
                s2 = country_avg[c2]

                # Opposite polarity and strong enough
                if abs(s1) >= sentiment_magnitude_threshold and abs(s2) >= sentiment_magnitude_threshold:
                    if s1 * s2 < 0:  # opposite signs
                        detection = self._build_detection_entity(
                            event_id=event.id,
                            country_code=None,
                            detection_type="narrative_reversal",
                            evidence={
                                "country_pair": [c1, c2],
                                "country_sentiments": {
                                    c1: s1,
                                    c2: s2,
                                },
                                "sentiment_magnitude_threshold": sentiment_magnitude_threshold,
                            },
                        )
                        detections.append(detection)

        return detections


    def _detect_early_origin_indicator(
        self,
        event: Event,
        analytics: EventAnalytics,
        articles: List[ProcessedArticle],
        lead_time_days_threshold: float = 1.0,
        min_follow_on_articles: int = 3,
    ) -> List[Detection]:

        detections: List[Detection] = []
        self.logger.info(f"Running early origin indicator detection for event {event.id}")

        articles = [a for a in articles if a.is_state_affiliated]
        if not articles:
            return []
        
        country_first_seen: Dict[str, datetime] = {}
        country_articles: Dict[str, List[ProcessedArticle]] = defaultdict(list)

        for a in articles:
            country_articles[a.country].append(a)
            ts = a.published_at
            if a.country not in country_first_seen or ts < country_first_seen[a.country]:
                country_first_seen[a.country] = ts

        if not country_first_seen:
            return detections

        global_first = min(country_first_seen.values())

        for country, first_ts in country_first_seen.items():
            lead_days = (first_ts - global_first).total_seconds() / 86400

            # We want countries that are significantly earlier than others (negative lead_days)
            if lead_days <= -lead_time_days_threshold and len(country_articles[country]) >= min_follow_on_articles:
                detection = self._build_detection_entity(
                    event_id=event.id,
                    country_code=country,
                    detection_type="early_origin_indicator",
                    evidence={
                        "country": country,
                        "first_seen": first_ts.isoformat(),
                        "global_first_seen": global_first.isoformat(),
                        "lead_days": lead_days,
                        "lead_time_days_threshold": lead_time_days_threshold,
                        "num_articles": len(country_articles[country]),
                    },
                )
                detections.append(detection)

        return detections
