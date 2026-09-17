import { Link } from "react-router-dom";

const navItems = [
  { to: "/", label: "Dashboard" },
  { to: "/customers", label: "Customers" },
  { to: "/customers/add", label: "Add Customer" },
  { to: "/subscriptions", label: "Subscriptions" },
  { to: "/pause-resume", label: "Pause / Resume" },
  { to: "/billing", label: "Billing" }
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand-box">
        <div className="brand-icon">T</div>
        <div>
          <p className="brand-kicker">Management</p>
          <h2>Tiffin</h2>
        </div>
      </div>

      <nav className="side-nav">
        {navItems.map((item) => (
          <Link key={item.to} to={item.to} className="nav-link">
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;