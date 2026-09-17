function StatusBadge({ status }) {
  const isActive = status === "ACTIVE" || status === "Active";

  return (
    <span className={`status-badge ${isActive ? "active" : "paused"}`}>
      {isActive ? "Active" : "Paused"}
    </span>
  );
}

export default StatusBadge;