import { useState } from "react";
import DatePicker from "react-datepicker";
import DockSelecter from "./DockSelecter";
import "react-datepicker/dist/react-datepicker.css";

const ReservationForm = () => {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  // datepickers
  // this needs a new query in the backend that gets all the unique docks
  return (
    <div>
      <div>
        <DockSelecter />
      </div>
      <DatePicker
        selected={startDate}
        onChange={setStartDate}
        dateFormat="MM-dd-yyyy"
        placeholderText="Select a start date"
      />
      <DatePicker
        selected={endDate}
        onChange={setEndDate}
        dateFormat="MM-dd-yyyy"
        placeholderText="Select an end date"
      />
    </div>
  );
};

export default ReservationForm;
