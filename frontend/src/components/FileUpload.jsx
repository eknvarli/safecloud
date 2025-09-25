import React, { useState } from "react";
import { runScan } from "../services/api";

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    const data = await runScan(file);
    setResults(data.results);
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Scan File</button>

      {results && (
        <div>
          <h3>Scan Results</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
