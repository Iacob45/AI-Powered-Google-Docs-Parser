import React, { useState } from "react";
import PaginaProfilUtilizator from "./PaginaProfilUtilizator";

function PaginaProcesare({ numeUtilizator }) {
  const [url, setUrl] = useState("");
  const [procesare, setProcesare] = useState("Regex");
  const [raspuns, setRaspuns] = useState(null);
  const [eroare, setEroare] = useState("");

  const trimiteCerereProcesare = async () => {
    const CerereProcesare = {
      url,
      procesare,
      nume_utilizator: numeUtilizator,
    };

    try {
      const response = await fetch("http://25.29.81.125:5050/proceseaza-orar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(CerereProcesare),
      });

      if (!response.ok) {
        alert("Eroare la cererea de procesare");
      }

      const data = await response.json();
      setRaspuns(data);
    } catch (e) {
      alert("Eroare la cererea de procesare: " + e);
    }
  };

  const salveazaOrar = async () => {
    if (!raspuns || !raspuns.activitati) {
      alert("Nu există un orar de salvat.");
      return;
    }

    try {
      const response = await fetch("http://25.29.81.125:5050/incarca-orar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(raspuns),
      });

      const data = await response.json();
      alert(data.mesaj || "Orarul a fost salvat cu succes.");
    } catch (e) {
      alert("Eroare la salvarea orarului:", e);
    }
  };

  const thStyle = {
    padding: "10px",
    border: "1px solid #ddd",
    textAlign: "left",
  };

  const tdStyle = {
    padding: "8px",
    border: "1px solid #ddd",
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginTop: "40px",
        fontFamily: "Arial, sans-serif",
        padding: "0 20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "400px",
          display: "flex",
          flexDirection: "column",
          gap: "10px",
        }}
      >
        <h1 style={{ textAlign: "center" }}>Procesare Orar</h1>

        <label>
          URL orar:
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            style={{ width: "100%", padding: "6px" }}
          />
        </label>

        <label>
          Tip procesare:
          <select
            value={procesare}
            onChange={(e) => setProcesare(e.target.value)}
            style={{ width: "100%", padding: "6px" }}
          >
            <option value="Regex">Regex</option>
            <option value="AI">AI</option>
          </select>
        </label>

        <button
          onClick={trimiteCerereProcesare}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#63C5DA",
            border: "none",
            color: "white",
            cursor: "pointer",
          }}
        >
          Trimite
        </button>
        <button
          onClick={salveazaOrar}
          style={{
            width: "100%",
            padding: "10px",
            backgroundColor: "#63C5DA",
            border: "none",
            color: "white",
            cursor: "pointer",
          }}
        >
          Salvează tabel
        </button>
        {eroare && <p style={{ color: "red", marginTop: "10px" }}>{eroare}</p>}
      </div>

      {raspuns && raspuns.activitati && (
        <div
          style={{
            marginTop: "40px",
            overflowX: "auto",
            width: "100%",
            maxWidth: "1000px",
          }}
        >
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              boxShadow: "0 0 10px rgba(0,0,0,0.1)",
              fontSize: "14px",
            }}
          >
            <thead style={{ backgroundColor: "#63C5DA", color: "white" }}>
              <tr>
                <th style={thStyle}>Nume</th>
                <th style={thStyle}>Profesor</th>
                <th style={thStyle}>Sala</th>
                <th style={thStyle}>Zi</th>
                <th style={thStyle}>Interval</th>
                <th style={thStyle}>Durata</th>
                <th style={thStyle}>Grupe</th>
                <th style={thStyle}>Anul</th>
                <th style={thStyle}>Categorie</th>
                <th style={thStyle}>Paritate</th>
              </tr>
            </thead>
            <tbody>
              {raspuns.activitati.map((act, index) => (
                <tr
                  key={index}
                  style={{
                    backgroundColor: index % 2 === 0 ? "#f9f9f9" : "#ffffff",
                  }}
                >
                  <td style={tdStyle}>{act.nume}</td>
                  <td style={tdStyle}>{act.profesor}</td>
                  <td style={tdStyle}>{act.sala}</td>
                  <td style={tdStyle}>{act.zi}</td>
                  <td style={tdStyle}>{act.interval}</td>
                  <td style={tdStyle}>{act.durata}</td>
                  <td style={tdStyle}>{act.grupe.join(", ")}</td>
                  <td style={tdStyle}>{act.anul}</td>
                  <td style={tdStyle}>{act.categorie}</td>
                  <td style={tdStyle}>{act.paritate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default PaginaProcesare;
