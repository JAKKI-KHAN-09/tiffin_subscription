const stats = [
  { label: "Total Customers", value: "100", tone: "blue" },
  { label: "Active", value: "85", tone: "green" },
  { label: "Paused", value: "15", tone: "amber" },
  { label: "Monthly Revenue", value: "₹2,45,000", tone: "purple" }
];

function Dashboard() {
  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Overview</p>
          <h1>Dashboard</h1>
        </div>
        <button className="primary-btn">+ New Customer</button>
      </section>

      <div className="stats-grid">
        {stats.map((stat) => (
          <div key={stat.label} className={`stat-card ${stat.tone}`}>
            <p>{stat.label}</p>
            <h2>{stat.value}</h2>
          </div>
        ))}
      </div>

      <div className="panel-grid">
        <div className="panel-card">
          <h3>Recent Activity</h3>
          <ul className="activity-list">
            <li><span>Rahul Sharma</span><small>Paid ₹3,000</small></li>
            <li><span>Priya Nair</span><small>Paused for travel</small></li>
            <li><span>Rohit Verma</span><small>New subscription added</small></li>
          </ul>
        </div>

        <div className="panel-card">
          <h3>Quick Notes</h3>
          <ul className="activity-list compact">
            <li><span>Service status</span><small>Healthy</small></li>
            <li><span>Pending bills</span><small>7 customers</small></li>
            <li><span>Next delivery</span><small>Tomorrow</small></li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;