import { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import {
  createReservationCreateReservationPost,
  getCurrentReservationsCurrentReservationsGet,
} from "../../client";
import Calendar from "../Calendar";
import DockSelecter from "./DockSelecter";
import FormField from "./FormField";
import SubmitButton from "./SubmitButton";
import "react-datepicker/dist/react-datepicker.css";
import "./ReservationForm.css";

const formatDateForApi = (date) => {
  if (!date) return "";

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
};

const getReservationDates = (startDate, endDate) => {
  const dates = [];
  const date = new Date(startDate);

  while (date <= endDate) {
    dates.push(formatDateForApi(date));
    date.setDate(date.getDate() + 1);
  }

  return dates;
};

const ReservationForm = () => {
  const [selectedDock, setSelectedDock] = useState("");
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [reservedBy, setReservedBy] = useState("");
  const [vesselSize, setVesselSize] = useState("");
  const [reservations, setReservations] = useState([]);
  const [calendarError, setCalendarError] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const loadReservations = async () => {
      const { data, error: requestError } =
        await getCurrentReservationsCurrentReservationsGet();

      if (requestError) {
        setCalendarError("Unable to load reservations.");
        return;
      }

      setReservations(data ?? []);
    };

    loadReservations();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setSuccess("");

    if (!selectedDock || !reservedBy || !vesselSize || !startDate || !endDate) {
      setError("Please complete every field.");
      return;
    }

    if (endDate < startDate) {
      setError("The end date must be on or after the start date.");
      return;
    }

    const reservation = {
      dock_id: selectedDock,
      reserved_by: reservedBy,
      vessel_size: Number(vesselSize),
      vessel_metric: "ft",
      date_range: {
        start_date: formatDateForApi(startDate),
        end_date: formatDateForApi(endDate),
      },
    };

    const { error: requestError } =
      await createReservationCreateReservationPost({ body: reservation });

    if (requestError) {
      setError("Unable to create reservation. The dock may already be booked.");
      return;
    }

    const newReservations = getReservationDates(startDate, endDate).map(
      (date) => ({
        dock_id: selectedDock,
        date,
        reserved_by: reservedBy,
      }),
    );
    setReservations((currentReservations) => [
      ...currentReservations,
      ...newReservations,
    ]);
    setSuccess("Reservation created.");
  };

  return (
    <main className="reservation-layout">
      <form className="reservation-form" onSubmit={handleSubmit}>
        <div className="reservation-form__fields">
          <DockSelecter
            selectedDock={selectedDock}
            onChange={setSelectedDock}
          />
          <FormField
            label="Reserved by:"
            value={reservedBy}
            onChange={setReservedBy}
          />
          <FormField
            label="Vessel size (ft):"
            type="number"
            min="1"
            value={vesselSize}
            onChange={setVesselSize}
          />
          <fieldset className="date-range">
            <legend>Reservation dates</legend>
            <label>
              Start date
              <DatePicker
                selected={startDate}
                onChange={setStartDate}
                dateFormat="MM-dd-yyyy"
                placeholderText="Select a start date"
              />
            </label>
            <label>
              End date
              <DatePicker
                selected={endDate}
                onChange={setEndDate}
                dateFormat="MM-dd-yyyy"
                placeholderText="Select an end date"
              />
            </label>
          </fieldset>
        </div>
        <div className="reservation-form__footer">
          <SubmitButton />
          {error && <p className="form-message form-message--error">{error}</p>}
          {success && (
            <p className="form-message form-message--success">{success}</p>
          )}
        </div>
      </form>
      <aside className="calendar-slot" aria-label="Calendar preview">
        <Calendar reservations={reservations} error={calendarError} />
      </aside>
    </main>
  );
};

export default ReservationForm;
