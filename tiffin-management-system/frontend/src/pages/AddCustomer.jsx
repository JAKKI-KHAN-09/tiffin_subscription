import { useState } from "react";

function AddCustomer() {
  const [form, setForm] = useState({
    name: "",
    phone: "",
    address: ""
  });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch("http://localhost:8000/api/customers", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="page-shell">
      <section className="page-header">
        <div>
          <p className="section-kicker">Customer Setup</p>
          <h1>Add Customer</h1>
        </div>
      </section>

      <form className="form-panel form-grid" onSubmit={handleSubmit}>
        <label>
          <span>Customer Name</span>
          <input
            name="name"
            placeholder="Customer Name"
            value={form.name}
            onChange={handleChange}
          />
        </label>

        <label>
          <span>Phone Number</span>
          <input
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
          />
        </label>

        <label className="full-width">
          <span>Address</span>
          <textarea
            name="address"
            placeholder="Address"
            value={form.address}
            onChange={handleChange}
          />
        </label>

        <button type="submit" className="primary-btn full-width-btn">Add Customer</button>
      </form>
    </div>
  );
}

export default AddCustomer;
