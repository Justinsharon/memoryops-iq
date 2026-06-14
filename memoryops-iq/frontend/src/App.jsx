import { useState } from "react";
import "./App.css";

function App() {

  const [incidentId, setIncidentId] = useState("");
  const [incidentText, setIncidentText] = useState("");
  const [activeTab, setActiveTab] = useState("overview");
  const [result, setResult] = useState(null);

  const analyzeIncident = async () => {

    if (!incidentId || !incidentText) {
      alert("Enter Incident ID and Description");
      return;
    }

    const response = await fetch(
      "http://127.0.0.1:8000/incident",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          incident_id: incidentId,
          incident_text: incidentText
        })
      }
    );

    const data = await response.json();

    setResult(data);
  };

  const tabs = [
    ["overview", "OVERVIEW"],
    ["changes", "SIMILAR CHANGES"],
    ["incidents", "SIMILAR INCIDENTS"],
    ["rca", "RCA ANALYSIS"],
    ["recommendations", "RECOMMENDATIONS"],
    ["investigation", "INVESTIGATION"],
    ["executive", "EXECUTIVE SUMMARY"]
  ];

  return (

    <div className="dashboard">

      <div className="dashboard-title">
        INTELLIGENT INCIDENT REASONING PLATFORM
      </div>

      <div className="search-bar">

        <input
          className="incident-input"
          placeholder="INC90001"
          value={incidentId}
          onChange={(e) => setIncidentId(e.target.value)}
        />

        <input
          className="description-input"
          placeholder="VPN outage in APAC after firewall update..."
          value={incidentText}
          onChange={(e) => setIncidentText(e.target.value)}
        />

        <button
          className="analyze-btn"
          onClick={analyzeIncident}
        >
          Analyze
        </button>

      </div>

      <div className="tabs">

        {tabs.map((tab) => (

          <button
            key={tab[0]}
            className={
              activeTab === tab[0]
                ? "tab-button tab-active"
                : "tab-button"
            }
            onClick={() => setActiveTab(tab[0])}
          >
            {tab[1]}
          </button>

        ))}

      </div>

      {!result && (
        <div className="content-card">
          Enter an Incident ID and Description then click Analyze.
        </div>
      )}

      {result && activeTab === "overview" && (

        <div className="overview-grid">

          <div className="card">

            <div className="card-title">
              INCIDENT SUMMARY
            </div>

            <div className="incident-id">
              {result.overview.incident_summary.incident_id}
            </div>

            <div className="info-row">
              <span>Service</span>
              <span>{result.overview.incident_summary.service}</span>
            </div>

            <div className="info-row">
              <span>Region</span>
              <span>{result.overview.incident_summary.region}</span>
            </div>

            <div className="info-row">
              <span>Category</span>
              <span>{result.overview.incident_summary.category}</span>
            </div>

            <div className="metric-label">
              Confidence Score
            </div>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width:
                  `${result.overview.incident_summary.confidence_score}%`
                }}
              />
            </div>

          </div>

          <div className="card">

            <div className="card-title">
              LIKELY ROOT CAUSE
            </div>

            <div className="card-body">

              Based on historical patterns,
              change correlation and RCA
              reasoning, the most probable
              root cause is:

              <div className="root-cause">
                {result.overview.likely_root_cause.root_cause}
              </div>

              <div className="metric-label">
                Pattern Frequency
              </div>

              <div>

                <div className="pattern-text">
                  {result.overview.likely_root_cause.pattern_frequency.occurrences}
                  {" "}Historical Matches
                </div>

                incidents

              </div>

              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width:
                    `${result.overview.likely_root_cause.pattern_frequency.percentage}%`
                  }}
                />
              </div>

              <div className="metric-label">
                RCA Confidence
              </div>

              <div>
                {result.overview.likely_root_cause.rca_confidence}%
              </div>

              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width:
                    `${result.overview.likely_root_cause.rca_confidence}%`
                  }}
                />
              </div>

            </div>

          </div>

          <div className="card">

            <div className="card-title">
              RECOMMENDED ACTIONS
            </div>

            {
              result.remediation
                .recommended_actions
                .slice(0, 5)
                .map((action, index) => (
                  <div
                    key={index}
                    className="action-item"
                  >
                    <span className="action-check">✓</span>
                    <span>{action}</span>
                  </div>
                ))
            }

            <button
              className="view-runbook-btn"
              onClick={() => setActiveTab("recommendations")}
            >
              <span className="runbook-btn-icon">📋</span>
              View Runbook
            </button>

          </div>

          <div className="card">

            <div className="card-title">
              IMPACT ANALYSIS
            </div>

            <div className="impact-metric">
              <div className="impact-icon">👤</div>
              <div>
                <div className="impact-label">Users Affected</div>
                <div className="impact-value">
                  {result.impact_analysis.users_affected}
                </div>
              </div>
            </div>

            <div className="impact-metric">
              <div className="impact-icon">📈</div>
              <div>
                <div className="impact-label">Business Impact</div>
                <div className="impact-high">HIGH</div>
              </div>
            </div>

            <div className="impact-metric">
              <div className="impact-icon">🕒</div>
              <div>
                <div className="impact-label">MTTR Improvement</div>
                <div className="impact-value-small">
                  {result.impact_analysis.mttr_improvement}
                </div>
              </div>
            </div>

            <div className="impact-metric">
              <div className="impact-icon">⏱</div>
              <div>
                <div className="impact-label">Potential Downtime</div>
                <div className="impact-value">
                  {result.impact_analysis.potential_downtime}
                </div>
              </div>
            </div>

          </div>

        </div>

      )}

      {/* FIX 1: Use foundry_iq.related_change_records instead of similar_changes.related_changes */}
      {result && activeTab === "changes" && (

        <div className="content-card">

          <h2 className="section-title">
            Similar Changes
          </h2>

          {
            result.foundry_iq.related_change_records.map(
              (change, index) => (
                <div
                  className="list-card"
                  key={index}
                >
                  <div className="list-title">
                    {change.change_id}
                  </div>

                  <div className="list-description">
                    {change.description}
                  </div>
                </div>
              )
            )
          }

        </div>

      )}

      {result && activeTab === "incidents" && (() => {

        // Merge the RCA reference incident (similar_incident.incident) with
        // foundry_iq.similar_incidents, deduplicate by incident_id, and
        // tag which one the RCA agent actually used so the user is never confused.
        const rcaIncident = result.similar_incident?.incident
          ? { ...result.similar_incident.incident, _isRcaSource: true }
          : null;

        const foundryIncidents = (result.foundry_iq.similar_incidents || []).map(inc => ({
          ...inc,
          _isRcaSource: false
        }));

        const seen = new Set();
        const allIncidents = [
          ...(rcaIncident ? [rcaIncident] : []),
          ...foundryIncidents
        ].filter(inc => {
          if (seen.has(inc.incident_id)) return false;
          seen.add(inc.incident_id);
          return true;
        });

        return (
          <div className="content-card">

            <h2 className="section-title">Similar Incidents</h2>

            {allIncidents.map((incident, index) => (
              <div className="list-card" key={index}>

                <div className="similar-inc-header">
                  <div className="list-title">{incident.incident_id}</div>
                  {incident._isRcaSource && (
                    <span className="rca-source-badge">⭐ Used for RCA</span>
                  )}
                </div>

                <div className="list-description">
                  <span className="inc-field-label">Root Cause: </span>
                  {incident.root_cause}
                </div>

                <div className="list-description">
                  <span className="inc-field-label">Resolution: </span>
                  {incident.resolution}
                </div>

                {incident.mttr_minutes && (
                  <div className="list-description">
                    <span className="inc-field-label">MTTR: </span>
                    {incident.mttr_minutes} minutes
                  </div>
                )}

              </div>
            ))}

          </div>
        );
      })()}


      {result && activeTab === "rca" && (() => {

        const raw = result.root_cause_analysis.rca || "";
        const lines = raw.split("\n").map(l => l.trim()).filter(Boolean);

        const sections = [];
        let current = null;

        lines.forEach(line => {
          const colonIdx = line.indexOf(":");
          const potentialLabel = colonIdx > 0 ? line.slice(0, colonIdx).trim() : null;
          const potentialValue = colonIdx > 0 ? line.slice(colonIdx + 1).trim() : null;
          const isLabel =
            potentialLabel &&
            potentialLabel.length < 40 &&
            /^[a-zA-Z\s]+$/.test(potentialLabel);

          if (isLabel) {
            current = { label: potentialLabel, value: potentialValue || "", items: [] };
            sections.push(current);
          } else if (current) {
            if (/^\d+\./.test(line) || line.startsWith("-")) {
              current.items.push(line.replace(/^\d+\.\s*|-\s*/, ""));
            } else {
              current.value = current.value ? current.value + " " + line : line;
            }
          } else {
            sections.push({ label: null, value: line, items: [] });
          }
        });

        const icons = {
          "Incident ID": "🎯", "Service": "⚙️", "Region": "🌏",
          "Severity": "⚠️", "Root Cause": "🔍", "Impact": "📊",
          "Resolution": "✅", "MTTR": "⏱", "Lessons Learned": "📘",
          "Preventive Actions": "🛡️",
        };

        const severityColor = {
          "Critical": "#ef4444", "High": "#f97316",
          "Medium": "#eab308", "Low": "#22c55e",
        };

        return (
          <div className="content-card">
            <h2 className="section-title">RCA Analysis</h2>
            <div className="rca-grid">
              {sections.map((sec, i) => {
                if (!sec.label) {
                  return <div key={i} className="rca-header-banner">{sec.value}</div>;
                }
                const icon = icons[sec.label] || "📋";
                const isSeverity = sec.label === "Severity";
                const severityStyle = isSeverity
                  ? { color: severityColor[sec.value] || "white", fontWeight: 700, fontSize: "18px" }
                  : {};
                return (
                  <div key={i} className="rca-field-card">
                    <div className="rca-field-header">
                      <span className="rca-field-icon">{icon}</span>
                      <span className="rca-field-label">{sec.label}</span>
                    </div>
                    {sec.value && (
                      <div className="rca-field-value" style={severityStyle}>
                        {sec.value}
                      </div>
                    )}
                    {sec.items.length > 0 && (
                      <ul className="rca-field-list">
                        {sec.items.map((item, j) => (
                          <li key={j} className="rca-field-list-item">
                            <span className="rca-list-bullet">→</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        );
      })()}

      {result && activeTab === "recommendations" && (

        <div className="content-card">

          <h2 className="section-title">
            Recommendations
          </h2>

          {
            result.remediation
              .recommended_actions
              .map((action, index) => (
                <div
                  className="action-item"
                  key={index}
                >
                  <span className="action-check">✓</span>
                  <span>{action}</span>
                </div>
              ))
          }

        </div>

      )}

      {result && activeTab === "investigation" && (

        <div className="content-card">

          <h2 className="section-title">
            Investigation
          </h2>

          {/* 1. Escalation Level */}
          <div className="list-card">
            <div className="list-title">Escalation Level</div>
            {result.investigation.escalation_level}
          </div>

          {/* 2. Escalation Recommendation */}
          <div className="list-card">
            <div className="list-title">Escalation Recommendation</div>
            {result.investigation.escalation_recommendation}
          </div>

          {/* 3. New Hypotheses */}
          <div className="sub-section-heading">
            New Hypotheses
          </div>

          {result.investigation.new_hypotheses.map(
            (item, index) => (
              <div
                className="list-card"
                key={index}
              >
                {item}
              </div>
            )
          )}

          {/* 4. Reasoning */}
          <div className="list-card" style={{ marginTop: "8px" }}>
            <div className="list-title">Reasoning</div>
            {result.investigation.reasoning}
          </div>

          {/* 5. Additional Checks */}
          {result.investigation.additional_checks && (
            <div className="list-card">
              <div className="list-title">Additional Checks</div>
              {result.investigation.additional_checks.map((item, index) => (
                <div className="action-item" key={index}>
                  <span className="investigation-arrow">→</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          )}

          {/* 6. Deep Dive Steps */}
          {result.investigation.deep_dive_steps && (
            <div className="list-card">
              <div className="list-title">Deep Dive Steps</div>
              {result.investigation.deep_dive_steps.map((item, index) => (
                <div className="action-item" key={index}>
                  <span className="investigation-arrow">→</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          )}

        </div>

      )}
      {result && activeTab === "executive" && (() => {

        // Parse **bold** markdown and plain paragraphs
        const raw = result.executive_summary || "";

        // Split into paragraphs on blank lines
        const paragraphs = raw.split(/\n\n+/).map(p => p.trim()).filter(Boolean);

        // Render inline **text** as <strong>
        const renderInline = (text, key) => {
          const parts = text.split(/\*\*(.+?)\*\*/g);
          return (
            <span key={key}>
              {parts.map((part, i) =>
                i % 2 === 1
                  ? <strong key={i} className="exec-bold">{part}</strong>
                  : part
              )}
            </span>
          );
        };

        // Detect paragraph "type" for styling
        const getType = (text) => {
          if (/^\*\*.*\*\*$/.test(text.trim())) return "heading";
          if (/^\*\*Business Impact/.test(text)) return "impact";
          if (/^\*\*Next Steps/.test(text)) return "nextsteps";
          if (/^\(\d+ words\)/.test(text)) return "wordcount";
          return "body";
        };

        return (
          <div className="content-card">
            <h2 className="section-title">Executive Summary</h2>
            <div className="exec-body">
              {paragraphs.map((para, i) => {
                const type = getType(para);
                if (type === "heading") {
                  return (
                    <div key={i} className="exec-title-banner">
                      {para.replace(/\*\*/g, "")}
                    </div>
                  );
                }
                if (type === "wordcount") {
                  return <div key={i} className="exec-wordcount">{para}</div>;
                }
                if (type === "impact") {
                  return (
                    <div key={i} className="exec-highlight-card exec-impact">
                      <div className="exec-highlight-icon">📊</div>
                      <div>{renderInline(para, i)}</div>
                    </div>
                  );
                }
                if (type === "nextsteps") {
                  return (
                    <div key={i} className="exec-highlight-card exec-nextsteps">
                      <div className="exec-highlight-icon">🚀</div>
                      <div>{renderInline(para, i)}</div>
                    </div>
                  );
                }
                return (
                  <p key={i} className="exec-paragraph">
                    {renderInline(para, i)}
                  </p>
                );
              })}
            </div>
          </div>
        );
      })()}

    </div>
  );
}

export default App;
