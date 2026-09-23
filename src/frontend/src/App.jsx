import Header from "./components/Header";
import ReservationForm from "./components/ReservationForm/ReservationForm";

// Plan:
// super simple dropdown with all docks
// two date pickers with start and end date
// submit button calls write to DB endpoiint which then can raise errors
// if there are erros put them in a nice box

const App = () => {
  return (
    <div>
      <Header name="Dock Scheduling System" />
      <ReservationForm />
    </div>
  );
};

export default App;
