#!/usr/bin/env node
/**
 * Build reproducible, client-safe analysis assets for the MERRA-2/POWER
 * grid-point series and the NOAA PSL Niño 3.4 context series.
 *
 * No data are silently merged with the SPC Samoa-wide annual series.  The
 * resulting model comparison is back-testing only, never an operational
 * forecast or a taro-yield model.
 */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const rainfallPath = path.join(root, 'data/processed/nasa-power-upolu-monthly-precipitation-1981-2025.csv');
const ensoRawPath = path.join(root, 'data/raw/noaa-psl-nino34-monthly.data');
const outputPath = path.join(root, 'public/data/seasonal-analysis.json');
const NOAA_URL = 'https://psl.noaa.gov/data/correlation/nina34.data';

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const keys = header.split(',');
  return lines.map((line) => Object.fromEntries(line.split(',').map((value, i) => [keys[i], value])));
}
function mean(values) { return values.reduce((a, b) => a + b, 0) / values.length; }
function quantile(values, q) {
  const sorted = [...values].sort((a, b) => a - b);
  const p = (sorted.length - 1) * q;
  const lo = Math.floor(p); const hi = Math.ceil(p);
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (p - lo);
}
function rmse(errors) { return Math.sqrt(mean(errors.map((value) => value ** 2))); }
function mae(errors) { return mean(errors.map((value) => Math.abs(value))); }

// Additive Holt-Winters for a clearly bounded historical-method comparison.
function initialise(values, m = 12) {
  const first = values.slice(0, m); const second = values.slice(m, m * 2);
  const level = mean(first);
  const trend = (mean(second) - mean(first)) / m;
  const season = first.map((value) => value - level);
  return { level, trend, season };
}
function holtWintersForecast(train, horizon, alpha, beta, gamma, m = 12) {
  if (train.length < m * 2) throw new Error('Need at least two full seasons');
  let { level, trend, season } = initialise(train, m);
  for (let i = m; i < train.length; i += 1) {
    const oldLevel = level;
    const priorSeason = season[i % m];
    level = alpha * (train[i] - priorSeason) + (1 - alpha) * (level + trend);
    trend = beta * (level - oldLevel) + (1 - beta) * trend;
    season[i % m] = gamma * (train[i] - level) + (1 - gamma) * priorSeason;
  }
  return Array.from({ length: horizon }, (_, h) => level + (h + 1) * trend + season[(train.length + h) % m]);
}
function evaluate(values, params, startTestIndex, horizon = 12) {
  const errors = [];
  for (let origin = startTestIndex; origin + horizon <= values.length; origin += horizon) {
    const forecast = holtWintersForecast(values.slice(0, origin), horizon, ...params);
    for (let h = 0; h < horizon; h += 1) errors.push(values[origin + h] - forecast[h]);
  }
  return { mae: mae(errors), rmse: rmse(errors), n: errors.length };
}
function seasonalNaive(values, startTestIndex) {
  const errors = [];
  for (let i = startTestIndex; i < values.length; i += 1) errors.push(values[i] - values[i - 12]);
  return { mae: mae(errors), rmse: rmse(errors), n: errors.length };
}
function parseNino34(raw) {
  const rows = [];
  for (const line of raw.split(/\r?\n/)) {
    if (!/^\s*\d{4}\s/.test(line)) continue;
    const fields = line.trim().split(/\s+/).map(Number);
    const year = fields[0];
    for (let month = 1; month <= 12; month += 1) {
      if (Number.isFinite(fields[month]) && fields[month] > -90) rows.push({ year, month, value: fields[month] });
    }
  }
  const baseline = new Map();
  for (let month = 1; month <= 12; month += 1) baseline.set(month, mean(rows.filter((r) => r.year >= 1981 && r.year <= 2010 && r.month === month).map((r) => r.value)));
  return rows.map((row) => ({ ...row, anomaly: row.value - baseline.get(row.month) }));
}

const rainfall = parseCsv(await fs.readFile(rainfallPath, 'utf8')).map((row) => ({
  year: Number(row.year), month: Number(row.month), total_mm: Number(row.derived_monthly_total_mm),
}));
const totals = rainfall.map((row) => row.total_mm);
const normalByMonth = new Map(Array.from({ length: 12 }, (_, index) => {
  const month = index + 1;
  return [month, mean(rainfall.filter((row) => row.month === month).map((row) => row.total_mm))];
}));
const distribution = Array.from({ length: 12 }, (_, index) => {
  const month = index + 1; const values = rainfall.filter((row) => row.month === month).map((row) => row.total_mm);
  return { month, mean_mm: mean(values), p10_mm: quantile(values, 0.10), q1_mm: quantile(values, 0.25), median_mm: quantile(values, 0.5), q3_mm: quantile(values, 0.75), p90_mm: quantile(values, 0.90), n: values.length };
});
const startTestIndex = rainfall.findIndex((row) => row.year === 2016 && row.month === 1);
const candidates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9];
let best = null;
for (const alpha of candidates) for (const beta of candidates) for (const gamma of candidates) {
  const result = evaluate(totals, [alpha, beta, gamma], startTestIndex);
  if (!best || result.rmse < best.result.rmse) best = { params: { alpha, beta, gamma }, result };
}
const naive = seasonalNaive(totals, startTestIndex);
const enso = parseNino34(await fs.readFile(ensoRawPath, 'utf8'));
const ensoByDate = new Map(enso.map((row) => [`${row.year}-${row.month}`, row.anomaly]));
const enriched = rainfall.map((row) => ({ ...row, anomaly_mm: row.total_mm - normalByMonth.get(row.month), nino34_anomaly_c: ensoByDate.get(`${row.year}-${row.month}`) ?? null }));

const output = {
  provenance: {
    rainfall: 'NASA/POWER PRECTOTCORR, source response identified as MERRA-2; grid coordinate -13.83, -171.75; retrieved 2026-08-18.',
    enso: `NOAA Physical Sciences Laboratory Niño 3.4 monthly SST source: ${NOAA_URL}; values converted to 1981–2010 calendar-month anomalies locally.`,
    warning: 'Rainfall is a gridded point product near central Upolu, not a local gauge, catchment or Samoa-national estimate. Niño 3.4 is Pacific climate context, not proof of Samoa or taro impacts. Forecast scores are a retrospective method comparison, not an operational forecast.',
  },
  rainfall: enriched,
  distribution,
  backtest: {
    test_period: '2016-01 to 2025-12; annual rolling origins; 120 held-out monthly observations.',
    seasonal_naive: naive,
    additive_holt_winters: { ...best.result, parameters: best.params },
    winner: best.result.rmse < naive.rmse ? 'additive_holt_winters' : 'seasonal_naive',
  },
};
await fs.writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(`PASS seasonal analysis: ${rainfall.length} rainfall months; ${distribution.length} monthly distributions; ${enso.length} Niño 3.4 months`);
console.log(`PASS back-test: seasonal-naïve RMSE ${naive.rmse.toFixed(2)}, ETS RMSE ${best.result.rmse.toFixed(2)}; winner ${output.backtest.winner}`);
