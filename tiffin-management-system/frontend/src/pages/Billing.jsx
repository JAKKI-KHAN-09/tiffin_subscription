import { useState } from "react";
import BillCard from "../components/BillCard";

function Billing() {
  const [customerId, setCustomerId] = useState("");
  const [month, setMonth] = useState("2026-09");
  const [bill, setBill] = useState({
    scheduled_days: 22,
    paused_days: 3,
    served_days: 19,
    daily_rate: 136.36,
    total_amount: 2590.91
  });

  const calculateBill = async () => {
    const response = await fetch(`http://localhost:8000/api/billing/${customerId}?month=${month}`);
    const data = await response.json();
    setBill(data);
  };

  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Finance</p>
          <h1>Monthly Billing</h1>
        </div>
      </section>

      <div className="form-panel form-grid billing-filter">
        <label>
          <span>Customer ID</span>
          <input
            placeholder="Customer ID"
            value={customerId}
            onChange={(e) => setCustomerId(e.target.value)}
          />
        </label>

        <label>
          <span>Billing Month</span>
          <input
            type="month"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
          />
        </label>

        <button className="primary-btn full-width-btn" onClick={calculateBill}>Calculate Bill</button>
      </div>

      {bill && <BillCard bill={bill} />}
    </div>
  );
}

export default Billing;