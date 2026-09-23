import { useEffect, useState } from "react";
import { getDocksDocksGet } from "../../client";

const DockSelecter = () => {
  const [docks, setDocks] = useState([]);
  const [selectedDock, setSelectedDock] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDocks = async () => {
      const { data, error: requestError } = await getDocksDocksGet();

      if (requestError) {
        setError("Unable to load docks.");
        return;
      }

      setDocks(data ?? []);
    };

    loadDocks();
  }, []);

  return (
    <label>
      Select a Dock:
      <select
        value={selectedDock}
        onChange={(event) => setSelectedDock(event.target.value)}
        disabled={Boolean(error)}
      >
        <option value="">Select a dock</option>
        {docks.map((dock) => (
          <option key={dock.dock_id} value={dock.dock_id}>
            {dock.dock_name}
          </option>
        ))}
      </select>
      {error && <span>{error}</span>}
    </label>
  );
};

export default DockSelecter;
