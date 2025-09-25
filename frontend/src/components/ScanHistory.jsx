import React, { useEffect, useState } from "react";
import { getScanHistory } from "../services/api";
import ScanResults from "./ScanResults";

const ScanHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const data = await getScanHistory();
      setHistory(data.results || []);
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>Scan History</h2>
      {history.length === 0 ? (
        <p>No scans found.</p>
      ) : (
        <ScanResults results={history} />
      )}
    </div>
  );
};

export default ScanHistory;
