export default function Home() {
  return (
    <div style={{ background: "#1e1e1e", color: "#fff", padding: "2rem", fontFamily: "monospace" }}>
      <h1>Empire OS – Today</h1>
      <div style={{marginTop:"1rem"}}>
        <pre>{JSON.stringify({
          seed_fund: { amount: 100, next_goal: 500 },
          treasury: { ops: 12, cloud_ai: 4, upgrade: 60, emergency: 25 },
          security: { grade: "B+", score: 86 },
          proposal: "Try FlipSim beta with a TikTok short to attract users."
        }, null, 2)}</pre>
      </div>
    </div>
  );
}
