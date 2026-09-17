import { useState } from "react";

function Subscription() {
  const [customerId, setCustomerId] = useState("");
  const [planId, setPlanId] = useState("");

  const subscribe = async () => {
    const response = await fetch("http://localhost:8000/api/subscriptions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        customer_id: customerId,
        plan_id: planId,
        start_date: "2026-09-17"
      })
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Plan Management</p>
          <h1>Create Subscription</h1>
        </div>
      </section>

      <div className="form-panel form-grid">
        <label>
          <span>Customer ID</span>
          <input
            placeholder="Customer ID"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
          />
        </label>

        <label>
          <span>Plan ID</span>
          <input
            placeholder="Plan ID"
            value={planId}
            onChange={(e) => setPlanId(e.target.value)}
          />
        </label>

        <button className="primary-btn full-width-btn" onClick={subscribe}>Subscribe</button>
      </div>
    </div>
  );
}

export default Subscription;
