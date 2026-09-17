import { useState } from "react";
import CustomerCard from "../components/CustomerCard";

function Customers() {
  const [phone, setPhone] = useState("");
  const [customer, setCustomer] = useState({
    name: "Rahul Sharma",
    phone: "9876543210",
    status: "ACTIVE",
    plan_price: 3000,
    address: "Jaipur, Rajasthan"
  });

  const searchCustomer = async () => {
    if (!phone) return;

    const response = await fetch(`http://localhost:8000/api/customers/phone/${phone}`);
    const data = await response.json();
    if (data?.phone) setCustomer(data);
  };

  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Customer Records</p>
          <h1>Search Customer</h1>
        </div>
      </section>

      <div className="form-panel">
        <div className="search-row">
          <input
            type="text"
            placeholder="Enter phone number"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
          />
          <button className="primary-btn" onClick={searchCustomer}>Search</button>
        </div>
      </div>

      {customer && <CustomerCard customer={customer} />}
    </div>
  );
}

export default Customers;