import { useState } from "react";

function AddCustomer() {
  const [form, setForm] = useState({
    name: "",
    phone: "",
    address: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState({ type: "", text: "" });

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setMessage({ type: "", text: "" });

    try {
      const response = await fetch("http://localhost:8000/api/customers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(form)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to add customer");
      }

      setMessage({
        type: "success",
        text: `Customer added successfully: ${data.name}`
      });
      setForm({ name: "", phone: "", address: "" });
    } catch (error) {
      setMessage({
        type: "error",
        text: error.message || "Something went wrong while adding customer"
      });
    } finally {
      setIsSubmitting(false);
    }
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
            required
          />
        </label>

        <label>
          <span>Phone Number</span>
          <input
            name="phone"
            placeholder="Phone Number"
            value={form.phone}
            onChange={handleChange}
            required
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

        {message.text && (
          <div className={`full-width ${message.type === "success" ? "success-message" : "error-message"}`}>
            {message.text}
          </div>
        )}

        <button type="submit" className="primary-btn full-width-btn" disabled={isSubmitting}>
          {isSubmitting ? "Adding..." : "Add Customer"}
        </button>
      </form>
    </div>
  );
}

export default AddCustomer;
