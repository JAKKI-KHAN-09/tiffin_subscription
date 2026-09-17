import { useState } from "react";

function PauseResume() {
  const [customerId, setCustomerId] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [reason, setReason] = useState("");

  const pauseSubscription = async () => {
    const response = await fetch(`http://localhost:8000/api/subscriptions/${customerId}/pause`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        start_date: startDate,
        end_date: endDate,
        reason: reason
      })
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Service Control</p>
          <h1>Pause / Resume</h1>
        </div>
      </section>

      <div className="form-panel form-grid">
        <label>
          <span>Customer</span>
          <input
            placeholder="Customer ID"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
          />
        </label>

        <label>
          <span>Pause Start</span>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </label>

        <label>
          <span>Pause End</span>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>

        <label className="full-width">
          <span>Reason</span>
          <input
            placeholder="Reason"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
          />
        </label>

        <button className="primary-btn full-width-btn" onClick={pauseSubscription}>Pause Subscription</button>
      </div>
    </div>
  );
}

export default PauseResume;
