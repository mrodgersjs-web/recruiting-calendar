export interface SampleSource {
  platform: string;
  url: string;
  signal: string;
}

export interface RecruitingOffer {
  id: string;
  rank: number;
  title: string;
  category: string;
  status: string;
  priceDisplay: string;
  whoItsFor: string;
  problemSolved: string;
  deliverable: string[];
  whyExistingFails: string;
  demandEvidence?: {
    summary?: string;
    postCount?: number;
    sampleSources?: SampleSource[];
  };
  chatStarterPrompt?: string;
}

export interface OffersCatalog {
  generatedAt: string;
  socialSignalsCount?: number;
  platformsQueried?: string[];
  offers: RecruitingOffer[];
}
