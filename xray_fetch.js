const https = require('https');

const EMAIL = 'nuno.gouveia@parceiros.nos.pt';
const TOKEN = 'ATATT3xFfGF0O0XGHzz9IIScV1yuAfwR2fWDTEwwPCxx2uASCFlMTOXY5yLtr6Ygwo-YrQyigmmGfy6PDwVkiHpbMSJVh4jj0uM8wRSK0nXlgvOPOrzpVPnc12P4RhjxS7_7ss-bP7ajs8KnHjAP12Uriak4IgEVHu2nmBiZZ9o4ZDFttW7azmg=A7F019ED';
const AUTH = Buffer.from(`${EMAIL}:${TOKEN}`).toString('base64');
const BASE = 'nos-corporativo.atlassian.net';

function get(path) {
  return new Promise((resolve, reject) => {
    const opts = { hostname: BASE, path, headers: { Authorization: `Basic ${AUTH}`, 'Content-Type': 'application/json' } };
    https.get(opts, r => {
      let d = '';
      r.on('data', c => d += c);
      r.on('end', () => {
        try { resolve({ status: r.statusCode, body: JSON.parse(d) }); }
        catch { resolve({ status: r.statusCode, body: d }); }
      });
    }).on('error', reject);
  });
}

async function main() {
  // Check versionedRepresentations for Xray data
  const r = await get('/rest/api/2/issue/HT-5238?expand=versionedRepresentations,names');
  if (r.status === 200) {
    const vr = r.body.versionedRepresentations || {};
    // Print customfields that have versionedRepresentations
    Object.keys(vr).filter(k => k.startsWith('customfield')).forEach(k => {
      const name = r.body.names[k] || k;
      const versions = vr[k];
      const vkeys = Object.keys(versions || {});
      if (vkeys.length > 0) {
        console.log(`\n${k} = ${name}`);
        vkeys.forEach(v => {
          const val = JSON.stringify(versions[v]).substring(0, 200);
          if (val && val !== 'null' && val !== '""' && val !== '[]' && val !== '{}') {
            console.log(`  v${v}:`, val);
          }
        });
      }
    });
  }
}

main().catch(console.error);
