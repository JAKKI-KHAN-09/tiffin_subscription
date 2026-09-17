const API_URL = "http://localhost:8000/api";

export async function getCustomerByPhone(phone) {
  const response = await fetch(`${API_URL}/customers/phone/${phone}`);
  return response.json();
}

export async function createCustomer(customer) {
  const response = await fetch(`${API_URL}/customers`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(customer)
  });

  return response.json();
}

export async function createSubscription(data) {
  const response = await fetch(`${API_URL}/subscriptions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return response.json();
}

export async function pauseSubscription(subscriptionId, data) {
  const response = await fetch(`${API_URL}/subscriptions/${subscriptionId}/pause`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  return response.json();
}

export async function resumeSubscription(subscriptionId) {
  const response = await fetch(`${API_URL}/subscriptions/${subscriptionId}/resume`, {
    method: "POST"
  });

  return response.json();
}

export async function getBill(customerId, month) {
  const response = await fetch(`${API_URL}/billing/${customerId}?month=${month}`);
  return response.json();
}
