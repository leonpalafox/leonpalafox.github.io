// Content and prompt assembly for /teaching/vibe-coding/.
// Imported by the Astro pages (server render) and by src/scripts/vibe-coding.ts
// (the interactive parts), so the page works before the script loads and both
// sides always produce the same text.

export type EngineId = 'colab' | 'jupyter' | 'script';
export type TaskId = 'binary' | 'multiclass' | 'regression' | 'forecast';

/* ---------- Rule 1: environments ---------- */

export interface Engine {
  id: EngineId;
  label: string;
  what: string;
  facts: { output: string; installs: string; files: string; watch: string };
  /** The short block shown on the rules page. */
  block: string;
}

export const ENGINES: Engine[] = [
  {
    id: 'colab',
    label: 'Google Colab',
    what: 'Browser notebook with an assistant built in',
    facts: {
      output: 'Notebook cells, each with a markdown cell above it',
      installs: '!pip, and only if the package is missing',
      files: 'A folder under /content',
      watch: 'A runtime reset loses every variable and file',
    },
    block: `ENVIRONMENT
- Google Colab notebook, Python 3. pandas, scikit-learn and matplotlib are already installed.
- Give the code as separate cells, with a short markdown cell before each one.
- Install extra packages only if essential, with !pip install in the first cell.
- Read the data from its URL. No Google Drive, no local paths.
- Show plots inline.`,
  },
  {
    id: 'jupyter',
    label: 'Laptop · Jupyter',
    what: 'An .ipynb file in VS Code or JupyterLab',
    facts: {
      output: 'A notebook that imports functions from src/',
      installs: '.venv and a pinned requirements.txt',
      files: 'A project file tree you define',
      watch: 'The kernel has to be the one from your .venv',
    },
    block: `ENVIRONMENT
- My own computer: a Jupyter notebook in VS Code or JupyterLab, Python 3.10+ in a virtual environment (.venv).
- Give the code as notebook cells, each preceded by a markdown cell.
- Dependencies go in requirements.txt with pinned versions.
- I run Jupyter from the project root. Reusable functions live in src/ and the notebook imports them.
- Show plots inline and also save them to outputs/figures.`,
  },
  {
    id: 'script',
    label: 'Laptop · script',
    what: '.py files run from the terminal',
    facts: {
      output: 'An entry point such as scripts/run_pipeline.py',
      installs: '.venv and a pinned requirements.txt',
      files: 'A project file tree you define',
      watch: 'No !pip, no %magic, no display()',
    },
    block: `ENVIRONMENT
- My own computer, terminal, Python 3.10+ in a virtual environment (.venv). I will run: python scripts/run_pipeline.py
- One entry point with an if __name__ == "__main__": guard. When a file changes, show the full updated file.
- Dependencies go in requirements.txt with pinned versions.
- No notebook syntax: no !pip, no %magic, no display(). Use print() for results.
- Save plots as PNG files instead of calling plt.show().`,
  },
];

/* ---------- Rule 2: data contract ---------- */

export const CONTRACT_BASE = `DATA
- Source: <URL or path>. <rows> rows, <columns> columns.
- Target: "<column>" (<its values, and which one is the positive class>).`;

export interface ColumnPitfall {
  id: string;
  label: string;
  guess: string;
  line: string;
}

export const COLUMN_PITFALLS: ColumnPitfall[] = [
  {
    id: 'codes',
    label: 'Codes that look like numbers',
    guess: 'Zip codes, area codes and store numbers get read as quantities, so 90210 counts as more than 10001.',
    line: '- "<column>" is a code, not a quantity: treat it as categorical.',
  },
  {
    id: 'dates',
    label: 'Dates stored as text',
    guess: 'Left as strings, or one-hot encoded into one column per day.',
    line: '- "<column>" is a date (YYYY-MM-DD): parse it as a date, do not encode it as text.',
  },
  {
    id: 'after',
    label: 'Columns filled in after the outcome',
    guess: 'Used as a feature like any other. The score looks excellent and the model is useless on new rows.',
    line: '- "<column>" is only known after the outcome: drop it before any modeling.',
  },
  {
    id: 'ids',
    label: 'Row identifiers',
    guess: 'Kept as a feature the model can memorize.',
    line: '- "<column>" is a row identifier: drop it.',
  },
  {
    id: 'missing',
    label: 'Missing values written as codes',
    guess: 'A -1 or a 999 is read as a real measurement.',
    line: '- In "<column>", -1 means missing: convert it to NaN before anything else.',
  },
  {
    id: 'duplicates',
    label: 'The same information twice',
    guess: 'Both columns stay in. Feature importance gets split between them and neither looks important.',
    line: '- "<column A>" and "<column B>" carry the same information: say so in the audit and when you report feature importance.',
  },
];

export function buildContract(selected: string[]): string {
  const lines = COLUMN_PITFALLS.filter((p) => selected.includes(p.id)).map((p) => p.line);
  return [CONTRACT_BASE, ...lines].join('\n');
}

/* ---------- Rule 3: model and search space ---------- */

export interface GridParam {
  name: string;
  values: string[];
}

export const GRID_PARAMS: GridParam[] = [
  { name: 'max_depth', values: ['2', '3', '4', '5', '6', '8', '10', '12'] },
  { name: 'min_samples_leaf', values: ['1', '5', '10', '20'] },
  { name: 'criterion', values: ['"gini"', '"entropy"'] },
  { name: 'class_weight', values: ['None', '"balanced"'] },
];

export const FOLD_OPTIONS = [3, 5, 10];

/** `chosen` maps a parameter name to the values that are switched on. */
export function buildModelSetup(chosen: Record<string, string[]>): string {
  const grid = GRID_PARAMS.map((p) => `  - ${p.name}: [${(chosen[p.name] ?? p.values).join(', ')}]`);
  return [
    'MODEL SETUP (hard constraints)',
    '- Use ONLY scikit-learn DecisionTreeClassifier.',
    '- Search exactly this grid with GridSearchCV:',
    ...grid,
    '- No other models, no feature scaling, no resampling, no PCA.',
    '- random_state=42 everywhere.',
  ].join('\n');
}

export function countCombinations(chosen: Record<string, string[]>): number {
  return GRID_PARAMS.reduce((total, p) => total * (chosen[p.name] ?? p.values).length, 1);
}

/* ---------- Rule 4: where each step learns from ---------- */

export interface PipelineStep {
  step: string;
  vague: { rows: 'all' | 'test'; note: string };
  rule: { rows: 'train' | 'test-once'; note: string };
}

export const PIPELINE_STEPS: PipelineStep[] = [
  {
    step: 'Fit imputers, encoders, scalers',
    vague: { rows: 'all', note: 'Fitted on every row, then split' },
    rule: { rows: 'train', note: 'Fitted on train, applied to test' },
  },
  {
    step: 'Explore and select features',
    vague: { rows: 'all', note: 'Correlations computed on the full table' },
    rule: { rows: 'train', note: 'Looked at on train only' },
  },
  {
    step: 'Tune hyperparameters',
    vague: { rows: 'all', note: 'Fitted on train, compared by test score' },
    rule: { rows: 'train', note: 'Cross-validation inside train' },
  },
  {
    step: 'Pick the decision threshold',
    vague: { rows: 'test', note: 'A few cutoffs tried on test' },
    rule: { rows: 'train', note: 'Out-of-fold predictions on train' },
  },
  {
    step: 'Report the final number',
    vague: { rows: 'test', note: 'The same rows, for the fifth time' },
    rule: { rows: 'test-once', note: 'Test opened once, here' },
  },
];

/* ---------- The eight rules ---------- */

export interface Rule {
  n: number;
  id: string;
  title: string;
  short: string;
  why: string;
  vague: string;
  spec: string;
  /** Heading of the prompt section this rule lives in; used by correction prompts. */
  section: string;
  /** A typical way this rule gets broken, phrased to follow "you ..." or stand alone. */
  breach: string;
  takeaway?: string;
}

export const RULES: Rule[] = [
  {
    n: 1,
    id: 'environment',
    title: 'Name the environment',
    short: 'Environment',
    why: 'The same request comes back as notebook cells in Colab and as a script on a laptop. Say where the code will run and what the answer has to look like: cells or files, how packages get installed, where plots go.',
    vague: 'Write the code to train a model on this data.',
    spec: ENGINES[0].block,
    section: 'ENVIRONMENT',
    breach: 'you gave notebook cells but I need a .py script',
    takeaway: 'Notebook code pasted into a script, or the reverse, is the usual reason a first answer does not run.',
  },
  {
    n: 2,
    id: 'data-contract',
    title: 'Give a data contract',
    short: 'Data contract',
    why: 'Say what the data is: where it lives, how many rows and columns, which column is the target and the type each column really has. Anything you leave out gets guessed, and the guesses are worst on columns that look like numbers and are not.',
    vague: 'Here is a CSV with customer data.',
    spec: CONTRACT_BASE,
    section: 'DATA',
    breach: 'you treated a code column as a number',
  },
  {
    n: 3,
    id: 'model-setup',
    title: 'Fix the model and the search space',
    short: 'Model setup',
    why: 'Without limits the assistant reaches for its favorite model, adds preprocessing nobody asked for and tunes whatever it likes. Name the model family, write the grid yourself and list what is off the table. Strict limits also keep results comparable when you run the same prompt in two tools.',
    vague: 'Use the best model.',
    spec: buildModelSetup({}),
    section: 'MODEL SETUP',
    breach: 'you added StandardScaler',
    takeaway: 'You decide the search space. The assistant writes the code that searches it.',
  },
  {
    n: 4,
    id: 'split-first',
    title: 'Split first, fit on train',
    short: 'Split first',
    why: 'Leakage starts as soon as anything learns from test rows. The split comes before encoding, scaling, exploring or tuning, and every transformation is fitted on train only.',
    vague: 'Preprocess the data and train a model.',
    spec: `VALIDATION RULES
- Split first: stratified 80/20 train/test with random_state=42, before any preprocessing.
- Fit every transformation (imputers, encoders, scalers) on train only.`,
    section: 'VALIDATION RULES',
    breach: 'you fitted the encoder before the split',
  },
  {
    n: 5,
    id: 'tuning',
    title: 'Fix how to tune',
    short: 'Tuning',
    why: '“Tune it” is an invitation to peek at the test set. Say which grid, which cross-validation and which score, and say where the decision threshold comes from. The test set gets opened once.',
    vague: 'Optimize the hyperparameters.',
    spec: `VALIDATION RULES
- Tune with GridSearchCV, 5-fold StratifiedKFold on train, scoring="roc_auc".
- Choose the decision threshold on out-of-fold predictions, never on test.
- Use the test set exactly once, at the end.`,
    section: 'VALIDATION RULES',
    breach: 'you chose max_depth using the test set',
    takeaway: 'If a number helped you choose, it cannot also be the number you report.',
  },
  {
    n: 6,
    id: 'success',
    title: 'Define success',
    short: 'Success',
    why: 'On data where one row in twenty is positive, a model that always answers “no” is 95% accurate. State the goal in business terms, the metrics that reflect it and the baseline any model has to beat.',
    vague: 'Make it accurate.',
    spec: `SUCCESS
- Goal: catch the positive cases, even at the cost of some false alarms.
- Report recall and precision for the positive class, ROC AUC and the confusion matrix.
- Always show the majority-class baseline next to accuracy.`,
    section: 'SUCCESS',
    breach: 'you reported accuracy without the baseline',
  },
  {
    n: 7,
    id: 'output',
    title: 'Shape the output',
    short: 'Output',
    why: 'Output you can read and rerun is part of the spec. Ask for a short explanation before each block of code, results that were actually printed, and no new libraries without asking.',
    vague: '(nothing said)',
    spec: `WORKING STYLE
- Before each code block, 2–3 lines on what you will do and why.
- Print every key number. Never invent results.
- Ask before adding a library.
- In every answer, list the files you created or changed.`,
    section: 'WORKING STYLE',
    breach: 'the summary quotes numbers that no cell printed',
    takeaway: 'A number in the prose that no cell printed is a claim. Ask for the cell.',
  },
  {
    n: 8,
    id: 'one-step',
    title: 'One step at a time',
    short: 'One step',
    why: 'Small steps can be reviewed. Ask for one step per answer and check it before you type “next”. When a rule is broken, name it and ask for the smallest fix. Do not start over.',
    vague: 'Do everything end to end.',
    spec: `WORKING STYLE
- Do ONE step per answer and wait for me to say "next".
- If I say a rule is broken, redo only the affected code and keep everything else.`,
    section: 'WORKING STYLE',
    breach: 'you did three steps in one answer',
  },
];

/* ---------- Correction prompt (rule 8 and the review page) ---------- */

export interface Breach {
  rule: number;
  what: string;
}

const tidy = (text: string) => text.trim().replace(/[.\s]+$/, '');

export function buildCorrection(breaches: Breach[]): string {
  const items = breaches
    .map((b) => ({ section: RULES[b.rule - 1]?.section ?? 'WORKING STYLE', what: tidy(b.what) || '<what happened>' }))
    .filter((b, i, all) => all.findIndex((o) => o.section === b.section && o.what === b.what) === i);
  if (items.length === 0) return '';
  if (items.length === 1) {
    return [
      `That answer breaks my rules under ${items[0].section}: ${items[0].what}.`,
      'Keep everything else exactly as it is.',
      'Redo only the affected code, explain the change in 2 lines, and show the new output.',
    ].join('\n');
  }
  return [
    `That answer breaks my rules in ${items.length} places:`,
    ...items.map((b) => `- ${b.section}: ${b.what}.`),
    'Keep everything else exactly as it is.',
    'Redo only the affected code, explain each change in 2 lines, and show the new output.',
  ].join('\n');
}

/* ---------- Review checklist ---------- */

export interface CheckItem {
  id: string;
  rule: number;
  label: string;
  /** Default evidence when the item is marked broken. */
  what: string;
  /** Your own housekeeping: nothing to send back to the assistant. */
  own?: boolean;
}

export const CHECKLIST: CheckItem[] = [
  { id: 'format', rule: 1, label: 'The output format matches my environment', what: 'the code is in the wrong format for my environment' },
  { id: 'files', rule: 1, label: 'Files go only where the prompt said, with paths from config', what: 'files were written outside the folders I named' },
  { id: 'types', rule: 2, label: 'Column types match the data contract', what: 'a column did not get the type I declared' },
  { id: 'models', rule: 3, label: 'Only the models I allowed appear in the code', what: 'the code uses a model I did not allow' },
  { id: 'extras', rule: 3, label: 'No scaler, resampling or PCA slipped in', what: 'you added a preprocessing step I ruled out' },
  { id: 'split', rule: 4, label: 'The split happens before any preprocessing', what: 'preprocessing runs before the train/test split' },
  { id: 'fit', rule: 4, label: 'Every transformer is fitted on train only', what: 'a transformer was fitted on rows from the test set' },
  { id: 'cv', rule: 5, label: 'Every choice was made with cross-validation, not the test set', what: 'a setting was chosen by looking at the test score' },
  { id: 'threshold', rule: 5, label: 'The threshold, if there is one, comes from out-of-fold predictions', what: 'the decision threshold was picked on the test set' },
  { id: 'baseline', rule: 6, label: 'The baseline sits next to the headline metric', what: 'the baseline is missing from the results' },
  { id: 'metrics', rule: 6, label: 'The metrics I asked for are all reported', what: 'some of the metrics I asked for are missing' },
  { id: 'printed', rule: 7, label: 'Numbers are printed outputs, not claims', what: 'the text quotes numbers that the code never printed' },
  { id: 'logged', rule: 8, label: 'The prompt is saved in prompts/ and this run is logged', what: '', own: true },
];

/* ---------- Prompt builder ---------- */

export interface TaskPreset {
  id: TaskId;
  label: string;
  score: string;
  metrics: string;
  baseline: string;
}

export const TASKS: TaskPreset[] = [
  {
    id: 'binary',
    label: 'Binary classification',
    score: 'roc_auc',
    metrics: 'recall and precision for the positive class, ROC AUC and the confusion matrix',
    baseline: 'the majority-class baseline (predict the most common class for every row)',
  },
  {
    id: 'multiclass',
    label: 'Multiclass classification',
    score: 'f1_macro',
    metrics: 'precision and recall per class, macro F1 and the confusion matrix',
    baseline: 'the majority-class baseline (predict the most common class for every row)',
  },
  {
    id: 'regression',
    label: 'Regression',
    score: 'neg_root_mean_squared_error',
    metrics: 'RMSE and MAE in the units of the target, and a residual plot',
    baseline: 'a model that always predicts the training mean',
  },
  {
    id: 'forecast',
    label: 'Forecasting (time-ordered data)',
    score: 'neg_mean_absolute_error',
    metrics: 'MAE and RMSE in the units of the target, and a plot of forecast against actual values',
    baseline: 'a naive forecast that repeats the last observed value',
  },
];

export const BANS = [
  { id: 'models', label: 'Any other model, AutoML included', text: 'other models (AutoML included)' },
  { id: 'scaling', label: 'Feature scaling', text: 'feature scaling' },
  { id: 'resampling', label: 'Resampling (SMOTE, over- or undersampling)', text: 'resampling (SMOTE, over- or undersampling)' },
  { id: 'pca', label: 'Dimensionality reduction (PCA)', text: 'dimensionality reduction (PCA)' },
];

export const STYLE_LINES = [
  { id: 'step', label: 'One step per answer', text: 'One step per answer; wait for me to say "next".' },
  { id: 'explain', label: 'Explain before each code block', text: 'Before each code block, 2–3 lines on what you will do and why.' },
  { id: 'print', label: 'Print every number, invent none', text: 'Print every key number. Never invent results.' },
  { id: 'libs', label: 'Ask before adding a library', text: 'Ask before adding any library.' },
  { id: 'files', label: 'List the files touched', text: 'In every answer, list the files you created or changed.' },
  { id: 'fix', label: 'Smallest fix when a rule breaks', text: 'If I say a rule is broken, redo only the affected code and keep everything else.' },
];

export interface SpecState {
  goal: string;
  task: TaskId;
  engine: EngineId;
  project: string;
  structure: boolean;
  source: string;
  rows: string;
  cols: string;
  target: string;
  targetNote: string;
  columnNotes: string;
  models: string;
  grid: string;
  bans: string[];
  seed: string;
  testPct: string;
  folds: string;
  score: string;
  threshold: string;
  outcome: string;
  metrics: string;
  style: string[];
}

export const DEFAULT_SPEC: SpecState = {
  goal: '',
  task: 'binary',
  engine: 'colab',
  project: 'my-project',
  structure: true,
  source: '',
  rows: '',
  cols: '',
  target: '',
  targetNote: '',
  columnNotes: '',
  models: '',
  grid: '',
  bans: BANS.map((b) => b.id),
  seed: '42',
  testPct: '20',
  folds: '5',
  score: TASKS[0].score,
  threshold: '',
  outcome: '',
  metrics: TASKS[0].metrics,
  style: STYLE_LINES.map((s) => s.id),
};

const or = (value: string, placeholder: string) => value.trim() || `<${placeholder}>`;
const lines = (text: string) =>
  text
    .split('\n')
    .map((line) => line.trim().replace(/^[-•*]\s*/, ''))
    .filter(Boolean);
const clampInt = (value: string, min: number, max: number, fallback: number) => {
  const n = Math.round(Number(value));
  return Number.isFinite(n) && value.trim() !== '' ? Math.min(max, Math.max(min, n)) : fallback;
};

export const projectSlug = (name: string) =>
  name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '') || 'my-project';

function projectStructure(engine: EngineId, slug: string): string {
  const pkg = slug.replace(/-/g, '_');
  const entry: [string, string] =
    engine === 'jupyter'
      ? ['├── notebooks/analysis.ipynb', 'imports from src, shows results']
      : ['├── scripts/run_pipeline.py', 'the entry point'];
  const tree: [string, string][] = [
    [`${slug}/`, ''],
    ['├── README.md', 'setup and run, 3 commands at most'],
    ['├── requirements.txt', 'pinned versions'],
    ['├── .gitignore', '.venv/, data/, outputs/'],
    ['├── prompts/', 'my prompts and run logs (do not modify)'],
    ['├── data/', ''],
    ['│   ├── raw/', 'original data, never edited'],
    ['│   └── processed/', 'the train and test sets, saved once'],
    [`├── src/${pkg}/`, ''],
    ['│   ├── __init__.py', ''],
    ['│   ├── config.py', 'paths, seed, search grids'],
    ['│   ├── data.py', 'download, load, fix types, split'],
    ['│   ├── features.py', 'fit on train, apply to any dataframe'],
    ['│   ├── models.py', 'the searches over the allowed models'],
    ['│   └── evaluate.py', 'metrics, thresholds, plots'],
    entry,
    ['└── outputs/', ''],
    ['    ├── figures/', 'plots as PNG'],
    ['    ├── models/', 'fitted models (.joblib)'],
    ['    └── reports/', 'metrics.json, summary.md'],
  ];
  const width = Math.max(...tree.map(([left]) => left.length)) + 3;
  return [
    'PROJECT STRUCTURE (create exactly this; never write outside it)',
    ...tree.map(([left, note]) => (note ? left.padEnd(width) + note : left)),
    '',
    'FILE RULES',
    `- All paths come from src/${pkg}/config.py with pathlib, relative to the project root. No absolute paths.`,
    '- data/raw is read-only. Generated files go only to data/processed/ or outputs/.',
    `- Functions live in src/${pkg}/. The notebook or script only calls them.`,
    '- In every answer, list the files you created or changed, with their full path.',
  ].join('\n');
}

function environmentBlock(state: SpecState): string {
  const slug = projectSlug(state.project);
  if (state.engine === 'colab') {
    return [
      'ENVIRONMENT',
      '- Google Colab notebook, Python 3. pandas, scikit-learn and matplotlib are already installed.',
      '- Give the code as separate notebook cells. Put a short markdown cell (a title and 1–2 lines) before each code cell.',
      '- Install extra packages only if essential, with !pip install in the first cell.',
      '- Read the data directly from the source under DATA. No Google Drive, no local paths.',
      `- Work inside /content/${slug} with folders data/raw, data/processed, outputs/figures, outputs/models and outputs/reports (create them with pathlib).`,
      '- Show plots inline.',
    ].join('\n');
  }
  const head =
    state.engine === 'jupyter'
      ? [
          'ENVIRONMENT',
          '- My own computer: a Jupyter notebook in VS Code or JupyterLab, Python 3.10+ in a virtual environment (.venv).',
          '- Give the code as notebook cells, each preceded by a markdown cell.',
          '- Dependencies go in requirements.txt with pinned versions.',
          '- I run Jupyter from the project root. In the first cell, add the project root to sys.path so the notebook can import from src.',
          '- Show plots inline and also save them as PNG.',
        ]
      : [
          'ENVIRONMENT',
          '- My own computer, terminal, Python 3.10+ in a virtual environment (.venv). From the project root I will run: python scripts/run_pipeline.py',
          '- The entry point has an if __name__ == "__main__": guard and only calls functions from src. When a file changes, show the full updated file.',
          '- Dependencies go in requirements.txt with pinned versions.',
          '- No notebook syntax: no !pip, no %magic, no display(). Use print() for results.',
          '- Save plots as PNG instead of calling plt.show().',
        ];
  return state.structure ? `${head.join('\n')}\n\n${projectStructure(state.engine, slug)}` : head.join('\n');
}

export function buildSetupPrompt(state: SpecState): string {
  const task = TASKS.find((t) => t.id === state.task) ?? TASKS[0];
  const seed = clampInt(state.seed, 0, 999999, 42);
  const test = clampInt(state.testPct, 5, 50, 20);
  const folds = clampInt(state.folds, 2, 20, 5);
  const score = state.score.trim() || task.score;

  const data = [
    'DATA',
    `- Source: ${or(state.source, 'URL or path')}. ${or(state.rows, 'rows')} rows, ${or(state.cols, 'columns')} columns.`,
    `- Target: "${or(state.target, 'column')}"${state.targetNote.trim() ? ` (${tidy(state.targetNote)})` : ''}.`,
    ...lines(state.columnNotes).map((line) => `- ${line}`),
  ];

  const banned = BANS.filter((b) => state.bans.includes(b.id)).map((b) => b.text);
  const grid = lines(state.grid);
  const model = [
    'MODEL SETUP (hard constraints)',
    `- Use ONLY ${or(state.models, 'the model classes you allow')}.`,
    ...(grid.length ? ['- Search exactly this space, nothing wider:', ...grid.map((line) => `  - ${line}`)] : []),
    ...(banned.length ? [`- No ${banned.join(', no ')}.`] : []),
    `- random_state=${seed} everywhere.`,
  ];

  const validation = ['VALIDATION RULES'];
  if (state.task === 'forecast') {
    validation.push(
      `- Split first, by time: the most recent ${test}% of the dates are the test set. No shuffling.`,
      '- Build every feature for a date only from information available before that date.',
      '- Fit every transformation (imputers, encoders, scalers) on train only.',
      `- Tune hyperparameters only with TimeSeriesSplit (${folds} splits) on train, scoring="${score}".`,
    );
  } else {
    const stratified = state.task !== 'regression';
    validation.push(
      `- Split first: ${stratified ? 'stratified ' : ''}${100 - test}/${test} train/test with random_state=${seed}, before any preprocessing.`,
      '- Fit every transformation (imputers, encoders, scalers) on train only.',
      `- Tune hyperparameters only with ${folds}-fold ${stratified ? 'StratifiedKFold' : 'KFold'} cross-validation (shuffle=True, random_state=${seed}) on train, scoring="${score}".`,
    );
    if (state.task === 'binary') {
      const rule = tidy(state.threshold);
      validation.push(
        `- Choose the decision threshold on out-of-fold predictions, never on test${rule ? `: ${rule}` : ''}.`,
      );
    }
  }
  validation.push('- Use the test set exactly once, at the end.');

  const success = [
    'SUCCESS',
    `- Goal: ${or(tidy(state.outcome), 'what a good result lets someone do')}.`,
    `- Report ${tidy(state.metrics) || task.metrics}.`,
    `- Always compare with ${task.baseline}.`,
  ];

  const style = STYLE_LINES.filter((s) => state.style.includes(s.id)).map((s) => `- ${s.text}`);

  return [
    'ROLE AND GOAL',
    `You will help me build ${or(tidy(state.goal), 'what you are building, in one sentence')}, step by step. Do not write any code in this answer.`,
    '',
    environmentBlock(state),
    '',
    data.join('\n'),
    '',
    model.join('\n'),
    '',
    validation.join('\n'),
    '',
    success.join('\n'),
    ...(style.length ? ['', ['WORKING STYLE', ...style].join('\n')] : []),
    '',
    'Reply only with: (1) the task in 5 bullets, (2) your step plan, (3) any question.',
  ].join('\n');
}

/* ---------- Prompt rendering ---------- */

const HEADINGS =
  /^(ROLE AND GOAL|ENVIRONMENT|DATA|MODEL SETUP(?: \(hard constraints\))?|VALIDATION RULES|SUCCESS|WORKING STYLE|PROJECT STRUCTURE \(create exactly this; never write outside it\)|FILE RULES)$/gm;

/** Escape a prompt for HTML and mark its section headings and <placeholders>. */
export function highlightPrompt(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(HEADINGS, '<span class="vc-h">$1</span>')
    .replace(/&lt;[^&\n]+&gt;/g, '<span class="vc-ph">$&</span>');
}

/* ---------- Where prompts live ---------- */

export interface TreeNode {
  name: string;
  key?: string;
  note?: string;
  what?: string;
  rule?: string;
  pre?: string;
  kids?: TreeNode[];
}

export const PROMPT_TREE_START = 'steps/00_setup.md';

export const PROMPT_TREE: TreeNode = {
  name: 'prompts/',
  what: 'Lives inside the project, or in its own repository. Every prompt you send comes from here.',
  rule: 'If a prompt is not in this folder, it does not exist. A chat history is not storage.',
  kids: [
    {
      name: 'README.md',
      what: 'How the folder works: the assembly order (rules, then environment, then step), the eight rules in short, and who may change what.',
    },
    {
      name: 'CHANGELOG.md',
      what: 'One line per change, newest first. Every edit to a prompt bumps its version, so a result can be traced to the exact text that produced it.',
      pre: `2026-11-11  03_tune           v1.1  add min_samples_leaf 20 (one tool kept picking 1)
2026-11-11  env/local_script  v1.1  require a scripts/run_pipeline.py entry point
2026-11-04  00_setup          v1.0  first version`,
    },
    {
      name: 'rules/',
      what: 'The reusable rule blocks. Written once, inserted into every prompt that needs them.',
      kids: [
        { name: 'model_setup.md', note: 'rule 3', what: 'The allowed models, the grids and what is off the table.' },
        {
          name: 'validation.md',
          note: 'rules 4–5',
          what: 'Split first, fit on train, tune with cross-validation, threshold from out-of-fold predictions, test once.',
        },
        { name: 'success.md', note: 'rule 6', what: 'The goal, the metrics and the baseline.' },
        {
          name: 'working_style.md',
          note: 'rules 7–8',
          what: 'One step per answer, printed outputs only, list the files touched.',
        },
      ],
    },
    {
      name: 'env/',
      what: 'One block per place the code can run. Swap the block to move the same prompt from one tool to another; the modeling rules stay identical.',
      kids: [
        { name: 'colab.md', what: 'Notebook cells, a workspace under /content, plots inline.' },
        { name: 'local_jupyter.md', what: 'A notebook plus src/ modules, with the project structure and file rules.' },
        { name: 'local_script.md', what: 'An entry-point script plus src/ modules, with the project structure and file rules.' },
      ],
    },
    {
      name: 'steps/',
      what: 'One file per step, named so they sort in the order you send them.',
      kids: [
        {
          name: '00_setup.md',
          what: 'Each step file opens with a small header and then the text. Placeholders pull in the environment and the rule blocks.',
          pre: `---
id: 00_setup
version: 1.2
updated: 2026-11-11
uses: env/{engine}.md, rules/*.md
goal: context and rules, no code yet
expect: constraints restated, step plan, questions
---
ROLE AND GOAL
You will help me build ...

{{env}}

{{rules/model_setup}}
{{rules/validation}}
{{rules/success}}
{{rules/working_style}}`,
        },
        { name: '01_load_audit.md', what: 'Load the data, check it against the contract, flag anything odd. No split, no model.' },
        { name: '02_split.md', what: 'The split, the transformations fitted on train, and the baseline.' },
        { name: '03_tune.md', what: 'The search over the allowed space, scored by cross-validation on train.' },
        { name: '04_final_test.md', what: 'Threshold from out-of-fold predictions, then the test set, once.' },
        { name: '05_explain.md', what: 'What drives the predictions, written for the people who will use them.' },
        { name: '90_correction.md', what: 'The template you send when a rule is broken.' },
      ],
    },
    {
      name: 'runs/',
      what: 'One log per run. This is how you compare two tools, or the same tool a month later.',
      kids: [
        {
          name: '2026-11-11_colab.md',
          what: 'What was sent, what broke and what came out.',
          pre: `# Run · 2026-11-11 · Colab
engine:      Colab with its built-in assistant
llm:         <name and version shown by the tool>
prompts:     00_setup v1.2 · 01–05 v1.0
corrections: 1 → model setup (added StandardScaler), fixed with 90_correction
results:     <the cross-validation and test numbers, as printed>
notes:       had to ask twice for the plot`,
        },
      ],
    },
    {
      name: 'assemble.py',
      note: 'optional',
      what: 'Ten lines that glue a step, the environment and the rules into the final prompt, so nobody edits prompts by hand.',
      pre: `from pathlib import Path
import sys

root = Path(__file__).parent
step, engine = sys.argv[1], sys.argv[2]    # e.g. 00_setup local_script
text = (root / "steps" / f"{step}.md").read_text(encoding="utf-8")
text = text.split("---", 2)[-1]            # drop the header
text = text.replace("{{env}}", (root / "env" / f"{engine}.md").read_text(encoding="utf-8"))
for rule in (root / "rules").glob("*.md"):
    text = text.replace("{{rules/" + rule.stem + "}}", rule.read_text(encoding="utf-8"))
print(text.strip())

# python prompts/assemble.py 00_setup local_script > prompt.txt`,
    },
  ],
};

export interface FlatNode extends TreeNode {
  key: string;
  depth: number;
  isDir: boolean;
}

/** The tree as a flat, ordered list with stable keys (`steps/00_setup.md`). */
export function flattenTree(root: TreeNode = PROMPT_TREE): FlatNode[] {
  const out: FlatNode[] = [];
  const walk = (node: TreeNode, depth: number, prefix: string) => {
    const key = depth === 0 ? node.name : `${prefix}${node.name}`;
    out.push({ ...node, key, depth, isDir: Boolean(node.kids) });
    for (const kid of node.kids ?? []) walk(kid, depth + 1, depth === 0 ? '' : key);
  };
  walk(root, 0, '');
  return out;
}
