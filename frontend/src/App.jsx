import React from "react";
import FileUpload from "./components/FileUpload";
import ScanHistory from "./components/ScanHistory";

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>SafeCloud</h1>
      <FileUpload />
      <hr />
      <ScanHistory />
    </div>
  );
}

export default App;
