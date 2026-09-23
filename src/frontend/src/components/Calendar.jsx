import { useMemo, useState } from "react";

const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

const getDateKey = (date) => {
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, "0");
	const day = String(date.getDate()).padStart(2, "0");
	return `${year}-${month}-${day}`;
};

const getMonthDays = (month) => {
	const firstDay = new Date(month.getFullYear(), month.getMonth(), 1);
	const firstGridDay = new Date(firstDay);
	firstGridDay.setDate(firstDay.getDate() - firstDay.getDay());

	return Array.from({ length: 42 }, (_, index) => {
		const day = new Date(firstGridDay);
		day.setDate(firstGridDay.getDate() + index);
		return day;
	});
};

const Calendar = ({ reservations, error }) => {
	const [month, setMonth] = useState(new Date());

	const reservationsByDate = useMemo(() => {
		return reservations.reduce((grouped, reservation) => {
			const entries = grouped[reservation.date] ?? [];
			grouped[reservation.date] = [...entries, reservation];
			return grouped;
		}, {});
	}, [reservations]);

	const monthDays = getMonthDays(month);
	const monthLabel = month.toLocaleDateString(undefined, {
		month: "long",
		year: "numeric",
	});

	const changeMonth = (offset) => {
		setMonth((currentMonth) =>
			new Date(currentMonth.getFullYear(), currentMonth.getMonth() + offset, 1),
		);
	};

	return (
		<section className="calendar" aria-label="Existing reservations calendar">
			<header className="calendar__header">
				<h2>{monthLabel}</h2>
				<div className="calendar__controls">
					<button type="button" onClick={() => changeMonth(-1)}>
						Prev
					</button>
					<button type="button" onClick={() => changeMonth(1)}>
						Next
					</button>
				</div>
			</header>
			{error ? (
				<p className="form-message form-message--error">{error}</p>
			) : (
				<div className="calendar__grid">
					{weekdays.map((weekday) => (
						<div className="calendar__weekday" key={weekday}>
							{weekday}
						</div>
					))}
					{monthDays.map((day) => {
						const dateKey = getDateKey(day);
						const dayReservations = reservationsByDate[dateKey] ?? [];
						const belongsToMonth = day.getMonth() === month.getMonth();

						return (
							<div
								className={`calendar__day${belongsToMonth ? "" : " calendar__day--outside"}${dayReservations.length ? " calendar__day--reserved" : ""}`}
								key={dateKey}
								title={dayReservations
									.map(
										(reservation) =>
											`${reservation.dock_id} - ${reservation.reserved_by ?? "Reserved"}`,
									)
									.join("\n")}
							>
								<span>{day.getDate()}</span>
								{dayReservations.length > 0 && (
									<small>{dayReservations.length} reserved</small>
								)}
							</div>
						);
					})}
				</div>
			)}
		</section>
	);
};

export default Calendar;
