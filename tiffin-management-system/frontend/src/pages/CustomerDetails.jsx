function CustomerDetails({ customer }) {
  return (
    <div>
      <h1>{customer.name}</h1>

      <p>Phone: {customer.phone}</p>
      <p>Address: {customer.address}</p>
      <p>Status: {customer.status}</p>
      <p>Plan: ₹{customer.plan_price}/month</p>
    </div>
  );
}

export default CustomerDetails;
