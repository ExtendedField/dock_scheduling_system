import { useState } from "react";

const ReservationForm = () => {
  const [selectedDock, setSelectedDock] = useState();
  // datepickers
  return (
    <label>
      Select a Dock:
      <select
        value={selectedDock}
        onChange={(e) => setSelectedDock(e.target.value)}
      ></select>
    </label>
  );
};

export default ReservationForm;
