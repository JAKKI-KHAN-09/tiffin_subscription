import StatusBadge from "./StatusBadge";

function CustomerCard({ customer }) {
  return (
    <div className="customer-card">
      <div className="card-head">
        <div>
          <p className="mini-label">Customer</p>
          <h3>{customer.name}</h3>
        </div>
        <StatusBadge status={customer.status || "ACTIVE"} />
      </div>

      <div className="detail-grid">
        <div>
          <span>Phone</span>
          <strong>{customer.phone}</strong>
        </div>
        <div>
          <span>Plan</span>
          <strong>₹{customer.plan_price || 3000}/month</strong>
        </div>
      </div>
    </div>
  );
}

export default CustomerCard;