import React from "react";

const ScanResults = ({ results }) => {
  return (
    <table border="1" cellPadding="5" style={{ marginTop: "10px" }}>
      <thead>
        <tr>
          <th>Filename</th>
          <th>Line</th>
          <th>Issue</th>
          <th>Severity</th>
          <th>Created At</th>
        </tr>
      </thead>
      <tbody>
        {results.map((res, idx) => (
          <tr key={idx}>
            <td>{res.filename}</td>
            <td>{res.line_number}</td>
            <td>{res.issue_text}</td>
            <td>{res.issue_severity}</td>
            <td>{res.created_at || "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default ScanResults;
