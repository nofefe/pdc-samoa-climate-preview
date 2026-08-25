#!/usr/bin/env node
/**
 * Build reproducible, client-safe analysis assets for the MERRA-2/POWER
 * grid-point series and the NOAA PSL Niño 3.4 context series.
 *
 * No data are silently merged with the SPC Samoa-wide annual series.  The
 * The script prepares descriptive seasonal views only; it does not produce an
 * operational forecast or a taro-yield model.
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
const normalByMonth = new Map(Array.from({ length: 12 }, (_, index) => {
  const month = index + 1;
  return [month, mean(rainfall.filter((row) => row.month === month).map((row) => row.total_mm))];
}));
const distribution = Array.from({ length: 12 }, (_, index) => {
  const month = index + 1; const values = rainfall.filter((row) => row.month === month).map((row) => row.total_mm);
  return { month, mean_mm: mean(values), p10_mm: quantile(values, 0.10), q1_mm: quantile(values, 0.25), median_mm: quantile(values, 0.5), q3_mm: quantile(values, 0.75), p90_mm: quantile(values, 0.90), n: values.length };
});
const enso = parseNino34(await fs.readFile(ensoRawPath, 'utf8'));
const ensoByDate = new Map(enso.map((row) => [`${row.year}-${row.month}`, row.anomaly]));
const enriched = rainfall.map((row) => ({ ...row, anomaly_mm: row.total_mm - normalByMonth.get(row.month), nino34_anomaly_c: ensoByDate.get(`${row.year}-${row.month}`) ?? null }));

const output = {
  provenance: {
    rainfall: 'NASA/POWER PRECTOTCORR, source response identified as MERRA-2; grid coordinate -13.83, -171.75; retrieved 2026-08-18.',
    enso: `NOAA Physical Sciences Laboratory Niño 3.4 monthly SST source: ${NOAA_URL}; values converted to 1981–2010 calendar-month anomalies locally.`,
    warning: 'Rainfall is a gridded point product near central Upolu, not a local gauge, catchment or Samoa-national estimate. Niño 3.4 is Pacific climate context, not proof of Samoa or taro impacts.',
  },
  rainfall: enriched,
  distribution,
};
await fs.writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`);
console.log(`PASS seasonal analysis: ${rainfall.length} rainfall months; ${distribution.length} monthly distributions; ${enso.length} Niño 3.4 months`);
