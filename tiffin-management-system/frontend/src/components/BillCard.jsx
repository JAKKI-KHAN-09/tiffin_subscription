function BillCard({ bill }) {
  return (
    <div className="bill-card">
      <div className="bill-header">
        <div>
          <p className="mini-label">Monthly Summary</p>
          <h3>Invoice</h3>
        </div>
        <span className="bill-total">₹{bill.total_amount}</span>
      </div>

      <div className="bill-grid">
        <div>
          <span>Scheduled Days</span>
          <strong>{bill.scheduled_days}</strong>
        </div>
        <div>
          <span>Paused Days</span>
          <strong>{bill.paused_days}</strong>
        </div>
        <div>
          <span>Served Days</span>
          <strong>{bill.served_days}</strong>
        </div>
        <div>
          <span>Daily Rate</span>
          <strong>₹{bill.daily_rate}</strong>
        </div>
      </div>
    </div>
  );
}

export default BillCard;