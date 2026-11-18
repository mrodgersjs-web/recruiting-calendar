export interface DivisionRuleRow {
  level: string;
  rosterCapOrLimit: string;
  aidModel: string;
  firstDirectContact: string;
  officialVisitsStart: string;
  realityNote: string;
}

export interface SopStep {
  id: string;
  title: string;
  detail: string;
  timing: string;
  category: string;
}

export interface GradeChecklist {
  grade: string;
  windowLabel: string;
  goal: string;
  steps: SopStep[];
}

export interface AthleteSop {
  sportSlug: string;
  sportLabel: string;
  athleteName: string;
  subtitle: string;
  verifiedDate: string;
  governingBodies: string[];
  headlineReality: string;
  divisionMatrix: DivisionRuleRow[];
  gradeChecklists: GradeChecklist[];
  videoStandard: {
    idealLength: string;
    mustShowFirst30Sec: string[];
    cameraAndFormatRules: string[];
    cutImmediately: string[];
  };
  campAndCircuitFilter: {
    worthPayingFor: string[];
    skipOrTrap: string[];
    redFlagTest: string[];
  };
  costVsWaste: {
    item: string;
    typicalSpend: string;
    verdict: string;
    why: string;
  }[];
  paperworkAndDeadlines: {
    milestone: string;
    when: string;
    cost: string;
    rule: string;
  }[];
  tenMistakes: {
    number: number;
    mistake: string;
    fix: string;
  }[];
}
