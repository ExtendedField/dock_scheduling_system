import Header from "./components/Header";
import ReservationForm from "./components/ReservationForm/ReservationForm";

const App = () => {
  return (
    <div>
      <Header name="Dock Scheduling System" />
      <ReservationForm />
    </div>
  );
};

export default App;
